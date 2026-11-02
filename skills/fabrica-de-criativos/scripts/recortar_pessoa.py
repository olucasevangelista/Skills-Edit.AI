#!/usr/bin/env python3
"""Recorta a pessoa de um video em QUALQUER fundo e salva um WebM com transparencia (VP9 + alfa, audio original em Opus).
Usa o modelo de segmentacao do rembg (instale uma vez: pip install rembg onnxruntime pillow; o modelo, ~176 MB, baixa na primeira execucao).

Uso:
  python recortar_pessoa.py entrada.mp4 pessoa.webm [--de 0] [--ate 8] [--altura-max 960] [--suavizar 0.4]

Mede cerca de 0,6 s por quadro em CPU (um trecho de 8 s a 30 fps leva uns 2 a 3 minutos). Teste num trecho curto e olhe a borda
ampliada, sobre fundo claro e escuro, antes de recortar o video inteiro. No Remotion, use o .webm com <Video> normalmente.
Se a pessoa foi gravada em fundo verde, o `chromakey` do FFmpeg e mais rapido e mais limpo (veja references/formatos/02-fundo-verde.md).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ff  # noqa: E402


def main() -> int:
    _ff.configurar_saida()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('entrada', type=Path)
    ap.add_argument('saida', type=Path, help='arquivo .webm de saida')
    ap.add_argument('--de', type=float, default=0.0, help='inicio do trecho, em segundos')
    ap.add_argument('--ate', type=float, help='fim do trecho, em segundos (padrao: ate o final)')
    ap.add_argument('--altura-max', type=int, default=960, help='lado maior de trabalho (menor = mais rapido; padrao 960)')
    ap.add_argument('--suavizar', type=float, default=0.4, help='0 a 0,9: quanto da mascara anterior entra na atual (reduz tremida da borda; padrao 0,4)')
    ap.add_argument('--modelo', default='u2net_human_seg', help='modelo do rembg (padrao u2net_human_seg)')
    a = ap.parse_args()
    try:
        import numpy as np
        from PIL import Image
        from rembg import new_session, remove
    except ImportError:
        print('Faltam pacotes. Instale com: pip install rembg onnxruntime pillow', file=sys.stderr)
        return 2

    info = _ff.info_basica(a.entrada)
    escala = min(1.0, a.altura_max / max(info['largura'], info['altura']))
    w, h = int(info['largura'] * escala) // 2 * 2, int(info['altura'] * escala) // 2 * 2
    fps = min(info['fps'], 30.0)
    dur = (a.ate if a.ate is not None else info['duracao']) - a.de
    if dur <= 0:
        print('Trecho vazio: --ate precisa ser maior que --de', file=sys.stderr)
        return 1

    ffmpeg = _ff.exe('ffmpeg')
    leitor = subprocess.Popen([ffmpeg, '-v', 'error', '-ss', str(a.de), '-t', str(dur), '-i', str(a.entrada), '-vf', f'fps={fps},scale={w}:{h}',
                               '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    gravador = subprocess.Popen([ffmpeg, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{w}x{h}', '-r', f'{fps}', '-i', '-',
                                 '-ss', str(a.de), '-t', str(dur), '-i', str(a.entrada), '-map', '0:v', '-map', '1:a?',
                                 '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '3M', '-auto-alt-ref', '0', '-c:a', 'libopus', '-shortest',
                                 str(a.saida)], stdin=subprocess.PIPE)
    sessao = new_session(a.modelo)
    tam = w * h * 3
    anterior = None
    n = 0
    while True:
        bruto = leitor.stdout.read(tam)
        if len(bruto) < tam:
            break
        quadro = Image.frombytes('RGB', (w, h), bruto)
        mascara = np.asarray(remove(quadro, session=sessao, only_mask=True), dtype=np.float32)
        if anterior is not None and a.suavizar > 0:
            mascara = a.suavizar * anterior + (1 - a.suavizar) * mascara
        anterior = mascara
        rgba = np.dstack([np.asarray(quadro), mascara.astype(np.uint8)])
        gravador.stdin.write(rgba.tobytes())
        n += 1
        if n % 30 == 0:
            print(f'{n} quadros...', flush=True)
    gravador.stdin.close()
    leitor.stdout.close()
    gravador.wait()
    leitor.wait()
    if n == 0 or gravador.returncode != 0 or not a.saida.exists():
        print('Nao consegui gerar o recorte.', file=sys.stderr)
        return 1
    print(f'Pronto: {a.saida} ({n} quadros, {w}x{h}). Olhe a borda ampliada antes de usar.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
