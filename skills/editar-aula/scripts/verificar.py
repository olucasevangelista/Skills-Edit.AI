#!/usr/bin/env python3
"""Verifica o video limpo medindo (nao confiando): duracao, volume, pausas que sobraram, estalos nas emendas e quadros.

Uso:
  python verificar.py pasta/aula_limpa.mp4 --timeline pasta/timeline.json [--pausa-max 0.8]
Gera relatorio_verificacao.md ao lado do video e sai com codigo 0 (tudo certo) ou 1 (ha problemas).
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ff  # noqa: E402
import planejar_cortes as pc  # noqa: E402


def volume(video: Path) -> tuple[float, float]:
    r = _ff.rodar([_ff.exe('ffmpeg'), '-hide_banner', '-i', str(video), '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'], check=False)
    txt = r.stderr
    resumo = txt[txt.rfind('Summary:'):]
    i = re.search(r'I:\s+(-?[\d.]+) LUFS', resumo)
    p = re.search(r'Peak:\s+(-?[\d.]+) dBFS', resumo)
    return (float(i.group(1)) if i else float('nan'), float(p.group(1)) if p else float('nan'))


def estalo_na_emenda(video: Path, t: float) -> float:
    """Maior salto entre amostras vizinhas (0 a 1, fundo de escala) em 120 ms ao redor de t. Estalo = salto grande."""
    p = subprocess.run([_ff.exe('ffmpeg'), '-v', 'error', '-ss', f'{max(0.0, t - 0.06):.3f}', '-t', '0.12', '-i', str(video),
                        '-vn', '-ac', '1', '-ar', '48000', '-f', 's16le', '-'], capture_output=True)
    dados = p.stdout
    n = len(dados) // 2
    if n < 3:
        return 0.0
    x = struct.unpack(f'<{n}h', dados[:n * 2])
    return max(abs(x[i] - x[i - 1]) for i in range(1, n)) / 32768.0


def main() -> int:
    _ff.configurar_saida()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video', type=Path)
    ap.add_argument('--timeline', type=Path, required=True)
    ap.add_argument('--pausa-max', type=float, default=0.8, help='pausas acima disso sao consideradas sobras (padrao 0.8 s)')
    ap.add_argument('--lufs', type=float, default=-16.0)
    ap.add_argument('--limite-estalo', type=float, default=0.35, help='salto de amostra (fundo de escala) a partir do qual conta como estalo')
    a = ap.parse_args()

    tl = json.loads(a.timeline.read_text(encoding='utf-8'))
    problemas: list[str] = []
    linhas = [f'# Verificacao: {a.video.name}', '']

    d = _ff.sonda(a.video)
    fmt = float(d['format']['duration'])
    vs = next((s for s in d['streams'] if s['codec_type'] == 'video'), None)
    as_ = next(s for s in d['streams'] if s['codec_type'] == 'audio')
    dv, da = (float(vs.get('duration', fmt)) if vs else fmt), float(as_.get('duration', fmt))
    esperado = tl['duracao_final']
    nq = int(vs.get('nb_frames', 0) or 0) if vs else 0
    linhas += ['## Duracao e sincronia', '',
               f'- Esperado pelo plano: {esperado:.2f} s | arquivo: {fmt:.2f} s | video: {dv:.2f} s | audio: {da:.2f} s',
               (f'- Quadros: {nq} (a {tl["fps"]:g} fps = {nq / tl["fps"]:.2f} s)' if vs else '- Arquivo so de audio')]
    if abs(fmt - esperado) > 0.25:
        problemas.append(f'Duracao {fmt:.2f} s difere do plano ({esperado:.2f} s).')
    if abs(dv - da) > 0.12:
        problemas.append(f'Video ({dv:.2f} s) e audio ({da:.2f} s) com duracoes diferentes: possivel dessincronia.')

    lufs, pico = volume(a.video)
    linhas += ['', '## Volume', '', f'- Integrado: {lufs:.1f} LUFS (alvo {a.lufs:g}) | pico: {pico:.1f} dBFS']
    if lufs == lufs and abs(lufs - a.lufs) > 1.5:
        problemas.append(f'Volume {lufs:.1f} LUFS fora do alvo {a.lufs:g}.')
    if pico == pico and pico > -0.5:
        problemas.append(f'Pico de {pico:.1f} dBFS: risco de distorcer.')

    env = _ff.envelope_db(a.video)
    faixas = pc.faixas_de_fala(env, pc.limiar_auto(env))
    pausas = [faixas[i + 1][0] - faixas[i][1] for i in range(len(faixas) - 1)]
    longas = [(round(faixas[i][1], 2), round(p, 2)) for i, p in enumerate(pausas) if p > a.pausa_max]
    linhas += ['', '## Pausas que sobraram', '',
               f'- Maior pausa: {max(pausas) if pausas else 0:.2f} s | acima de {a.pausa_max:g} s: {len(longas)}']
    for t, p in longas[:10]:
        linhas.append(f'  - em {_ff.mmss(t)}: {p:.2f} s')
    if longas:
        problemas.append(f'{len(longas)} pausa(s) acima de {a.pausa_max:g} s sobraram.')

    juncoes = [t['final_ini'] for t in tl['trechos'][1:]]
    amostra = juncoes if len(juncoes) <= 40 else [juncoes[int(i * len(juncoes) / 40)] for i in range(40)]
    ruins = []
    for t in amostra:
        s = estalo_na_emenda(a.video, t)
        if s > a.limite_estalo:
            ruins.append((t, s))
    linhas += ['', '## Emendas', '', f'- {len(juncoes)} emendas; {len(amostra)} conferidas; com estalo provavel: {len(ruins)}']
    for t, s in ruins[:10]:
        linhas.append(f'  - em {_ff.mmss(t)} (salto {s:.2f})')
    if ruins:
        problemas.append(f'{len(ruins)} emenda(s) com estalo provavel.')

    linhas += ['', '## Resultado', '', 'Tudo certo.' if not problemas else 'Problemas:'] + [f'- {p}' for p in problemas]
    (a.video.parent / 'relatorio_verificacao.md').write_text('\n'.join(linhas) + '\n', encoding='utf-8')
    print('\n'.join(linhas[-(len(problemas) + 3):]))
    print(f'volume {lufs:.1f} LUFS | duracao {fmt:.1f} s (plano {esperado:.1f}) | maior pausa {max(pausas) if pausas else 0:.2f} s | '
          f'emendas com estalo: {len(ruins)}/{len(amostra)}')
    return 1 if problemas else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError, StopIteration) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
