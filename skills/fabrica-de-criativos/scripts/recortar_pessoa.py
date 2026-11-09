#!/usr/bin/env python3
"""Recorta a pessoa de um video em QUALQUER fundo com Robust Video Matting (RVM) e salva um WebM com transparencia
(VP9 + alfa, com o audio original em Opus). Tambem grava a posicao da cabeca ao longo do tempo, para ancorar elementos.

E MATERIAL DE APOIO: o recorte vai para o Remotion (<Video> com o .webm), onde voce compoe o que quiser atras da pessoa.

Uso:
  python recortar_pessoa.py entrada.mp4 pessoa.webm [--de 0] [--ate 8] [--altura-max 1920]

Saidas: pessoa.webm e pessoa_cabeca.json ({"passo_s", "topo", "cx"}: topo do cabelo em y e centro da cabeca em x, em pixels
do quadro de saida, uma amostra a cada `passo_s` segundos, suavizadas; -1 onde nao houve deteccao).

Precisa de: pip install torch numpy (o modelo, ~100 MB, baixa na primeira execucao pelo torch.hub, que usa o GitHub).
Com GPU (CUDA) e rapido; em CPU leva alguns segundos por quadro. Teste num trecho curto e olhe a borda ampliada, sobre
fundo claro e escuro, antes de recortar o video inteiro.
Se a pessoa foi gravada em fundo verde, o `chromakey` do FFmpeg e mais rapido e mais limpo (references/formatos/02-fundo-verde.md).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ff  # noqa: E402


def suaviza(x, mediana=15, media=45):
    """Mediana (tira os saltos) e media movel (tira o tremor), como nos exemplos do autor."""
    import numpy as np

    pad = mediana // 2
    xp = np.pad(x, pad, mode='edge')
    med = np.array([np.median(xp[i:i + mediana]) for i in range(len(x))])
    mp = np.pad(med, media // 2, mode='edge')
    return np.convolve(mp, np.ones(media) / media, mode='valid')[:len(x)]


def main() -> int:
    _ff.configurar_saida()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('entrada', type=Path)
    ap.add_argument('saida', type=Path, help='arquivo .webm de saida')
    ap.add_argument('--de', type=float, default=0.0, help='inicio do trecho, em segundos')
    ap.add_argument('--ate', type=float, help='fim do trecho, em segundos (padrao: ate o final)')
    ap.add_argument('--altura-max', type=int, default=1920, help='lado maior de trabalho (menor = mais rapido; padrao 1920)')
    ap.add_argument('--fps', type=float, default=30.0)
    a = ap.parse_args()
    try:
        import numpy as np
        import torch
    except ImportError:
        print('Faltam pacotes. Instale com: pip install torch numpy', file=sys.stderr)
        return 2

    info = _ff.info_basica(a.entrada)
    escala = min(1.0, a.altura_max / max(info['largura'], info['altura']))
    w, h = int(info['largura'] * escala) // 2 * 2, int(info['altura'] * escala) // 2 * 2
    dur = (a.ate if a.ate is not None else info['duracao']) - a.de
    if dur <= 0:
        print('Trecho vazio: --ate precisa ser maior que --de', file=sys.stderr)
        return 1
    ratio = min(1.0, 512 / max(w, h))  # o RVM trabalha melhor com o lado maior reduzido para ~512

    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Dispositivo: {dev}. Carregando o modelo...', flush=True)
    modelo = torch.hub.load('PeterL1n/RobustVideoMatting', 'resnet50', trust_repo=True).eval().to(dev)

    ffmpeg = _ff.exe('ffmpeg')
    leitor = subprocess.Popen([ffmpeg, '-v', 'error', '-ss', str(a.de), '-t', str(dur), '-i', str(a.entrada), '-vf', f'fps={a.fps},scale={w}:{h}',
                               '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    gravador = subprocess.Popen([ffmpeg, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{w}x{h}', '-r', f'{a.fps}', '-i', '-',
                                 '-ss', str(a.de), '-t', str(dur), '-i', str(a.entrada), '-map', '0:v', '-map', '1:a?',
                                 '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '0', '-crf', '24', '-auto-alt-ref', '0',
                                 '-deadline', 'good', '-cpu-used', '4', '-row-mt', '1', '-c:a', 'libopus', '-shortest', str(a.saida)],
                                stdin=subprocess.PIPE)
    tam = w * h * 3
    rec = [None] * 4
    cabeca: list[list[int]] = []
    n = 0
    t0 = time.time()
    with torch.no_grad():
        while True:
            bruto = leitor.stdout.read(tam)
            if len(bruto) < tam:
                break
            quadro = np.frombuffer(bruto, dtype=np.uint8).reshape(h, w, 3)
            src = torch.from_numpy(quadro.copy()).to(dev).permute(2, 0, 1).float().div(255).unsqueeze(0)
            fgr, pha, *rec = modelo(src, *rec, ratio)  # o estado recorrente (`rec`) da estabilidade no tempo
            rgb = (fgr[0].clamp(0, 1) * 255).byte().permute(1, 2, 0)
            alfa8 = (pha[0].clamp(0, 1) * 255).byte().permute(1, 2, 0)
            al = pha[0, 0]
            linhas = (al > 0.5).sum(dim=1)
            idx = torch.nonzero(linhas > max(10, w // 18))
            topo = int(idx[0]) if len(idx) else -1
            cx = -1
            if topo >= 0:
                cols = torch.nonzero((al[topo:topo + h // 12] > 0.5).any(dim=0))
                cx = int((cols[0] + cols[-1]) // 2) if len(cols) else -1
            cabeca.append([topo, cx])
            gravador.stdin.write(torch.cat([rgb, alfa8], dim=2).cpu().numpy().tobytes())
            n += 1
            if n % 60 == 0:
                print(f'{n} quadros, {n / (time.time() - t0):.1f} q/s', flush=True)
    gravador.stdin.close()
    leitor.stdout.close()
    gravador.wait()
    leitor.wait()
    if n == 0 or gravador.returncode != 0 or not a.saida.exists():
        print('Nao consegui gerar o recorte.', file=sys.stderr)
        return 1

    dados = np.array(cabeca, dtype=float)
    series = []
    for k in (0, 1):
        s = dados[:, k].copy()
        ruim = s < 0
        if ruim.all():
            series.append([-1] * n)
            continue
        idx = np.arange(n)
        s[ruim] = np.interp(idx[ruim], idx[~ruim], s[~ruim])
        series.append(suaviza(s))
    passo = max(1, round(a.fps * 0.2))
    saida_json = a.saida.with_name(a.saida.stem + '_cabeca.json')
    saida_json.write_text(json.dumps({'passo_s': passo / a.fps, 'largura': w, 'altura': h,
                                      'topo': [int(round(v)) for v in series[0][::passo]], 'cx': [int(round(v)) for v in series[1][::passo]]}), encoding='utf-8')
    print(f'Pronto: {a.saida} e {saida_json.name} ({n} quadros, {w}x{h}, {n / (time.time() - t0):.1f} q/s). Olhe a borda ampliada antes de usar.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
