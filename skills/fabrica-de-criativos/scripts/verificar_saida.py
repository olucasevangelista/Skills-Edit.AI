#!/usr/bin/env python3
"""Mede o arquivo final de um criativo (so FFmpeg e biblioteca padrao): tamanho, taxa de quadros, duracao, audio,
volume, quadros pretos e imagem congelada. Sai com codigo 0 (tudo certo) ou 1 (algo fora do esperado).

Uso:
  python verificar_saida.py criativo.mp4 [--tamanho 1080x1920] [--fps 30] [--duracao 30] [--lufs -14]
O script MEDE; o gosto (musica, ritmo) e a reproducao com som sao de quem assiste.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ff  # noqa: E402


def medir_volume(video: Path) -> tuple[float | None, float | None]:
    r = _ff.rodar([_ff.exe('ffmpeg'), '-hide_banner', '-i', str(video), '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'], check=False)
    resumo = r.stderr[r.stderr.rfind('Summary:'):]
    i = re.search(r'I:\s+(-?[\d.]+) LUFS', resumo)
    p = re.search(r'Peak:\s+(-?[\d.]+) dBFS', resumo)
    return (float(i.group(1)) if i else None, float(p.group(1)) if p else None)


def detectar_preto_e_congelado(video: Path, congelado_min: float) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    """Trechos de quadro preto (inicio, duracao) e de imagem congelada (inicio, duracao), em segundos."""
    filtro = f'blackdetect=d=0.1:pic_th=0.98:pix_th=0.10,freezedetect=n=0.003:d={congelado_min}'
    r = _ff.rodar([_ff.exe('ffmpeg'), '-hide_banner', '-i', str(video), '-an', '-vf', filtro, '-f', 'null', '-'], check=False)
    pretos = [(float(a), float(d)) for a, d in re.findall(r'black_start:([\d.]+).*?black_duration:([\d.]+)', r.stderr)]
    ini = [float(x) for x in re.findall(r'freeze_start:\s*([\d.]+)', r.stderr)]
    dur = [float(x) for x in re.findall(r'freeze_duration:\s*([\d.]+)', r.stderr)]
    congelados = list(zip(ini, dur))
    # um trecho congelado ainda em andamento no fim do arquivo nao tem "freeze_duration": conta ate o fim
    if len(ini) > len(dur):
        total = float(_ff.sonda(video)['format']['duration'])
        congelados.append((ini[-1], total - ini[-1]))
    return pretos, congelados


def main() -> int:
    _ff.configurar_saida()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video', type=Path)
    ap.add_argument('--tamanho', default='1080x1920', help='largura x altura esperadas (padrao 1080x1920)')
    ap.add_argument('--fps', type=float, default=30.0, help='taxa de quadros esperada (padrao 30)')
    ap.add_argument('--duracao', type=float, help='duracao esperada em segundos')
    ap.add_argument('--tolerancia-duracao', type=float, default=0.3)
    ap.add_argument('--lufs', type=float, default=-14.0, help='volume alvo (padrao -14 LUFS)')
    ap.add_argument('--tolerancia-lufs', type=float, default=2.0)
    ap.add_argument('--pico-max', type=float, default=-0.5, help='pico maximo em dBFS (padrao -0.5)')
    ap.add_argument('--preto-max', type=float, default=0.5, help='trecho preto mais longo aceito, em s (padrao 0.5)')
    ap.add_argument('--congelado-max', type=float, default=3.0, help='imagem parada mais longa aceita, em s (padrao 3)')
    ap.add_argument('--json', action='store_true', help='imprime o resultado em JSON')
    a = ap.parse_args()

    info = _ff.info_basica(a.video)
    problemas: list[str] = []
    linhas: list[str] = []
    w, h = (int(x) for x in a.tamanho.lower().split('x'))
    linhas.append(f'tamanho: {info["largura"]}x{info["altura"]} (esperado {w}x{h})')
    if (info['largura'], info['altura']) != (w, h):
        problemas.append(f'tamanho {info["largura"]}x{info["altura"]} diferente de {w}x{h}')
    linhas.append(f'quadros por segundo: {info["fps"]:.2f} (esperado {a.fps:g})' + ('; taxa variavel' if info['vfr'] else ''))
    if abs(info['fps'] - a.fps) > 0.1:
        problemas.append(f'taxa de quadros {info["fps"]:.2f} diferente de {a.fps:g}')
    if info['vfr']:
        problemas.append('taxa de quadros variavel (pode dessincronizar em alguns players)')
    linhas.append(f'duracao: {info["duracao"]:.2f} s' + (f' (esperado {a.duracao:g})' if a.duracao else ''))
    if a.duracao is not None and abs(info['duracao'] - a.duracao) > a.tolerancia_duracao:
        problemas.append(f'duracao {info["duracao"]:.2f} s diferente de {a.duracao:g} s')

    lufs = pico = None
    if info['tem_audio']:
        lufs, pico = medir_volume(a.video)
        linhas.append(f'volume: {lufs} LUFS (alvo {a.lufs:g}), pico {pico} dBFS')
        if lufs is None:
            problemas.append('nao consegui medir o volume')
        elif abs(lufs - a.lufs) > a.tolerancia_lufs:
            problemas.append(f'volume {lufs:.1f} LUFS fora do alvo {a.lufs:g} (tolerancia {a.tolerancia_lufs:g})')
        if pico is not None and pico > a.pico_max:
            problemas.append(f'pico de {pico:.1f} dBFS acima de {a.pico_max:g} (risco de distorcer)')
    else:
        linhas.append('audio: nenhum')
        problemas.append('o arquivo nao tem faixa de audio')

    pretos, congelados = detectar_preto_e_congelado(a.video, min(a.congelado_max, 1.0))
    longos_pretos = [(i, d) for i, d in pretos if d > a.preto_max]
    longos_congelados = [(i, d) for i, d in congelados if d > a.congelado_max]
    linhas.append(f'quadros pretos: {len(pretos)} trecho(s), o maior com {max((d for _, d in pretos), default=0):.2f} s')
    linhas.append(f'imagem congelada: {len(congelados)} trecho(s) de pelo menos 1 s, o maior com {max((d for _, d in congelados), default=0):.2f} s')
    for i, d in longos_pretos:
        problemas.append(f'quadro preto por {d:.2f} s a partir de {i:.2f} s')
    for i, d in longos_congelados:
        problemas.append(f'imagem congelada por {d:.2f} s a partir de {i:.2f} s (a menos que seja o quadro final estavel de proposito)')

    if a.json:
        print(json.dumps(dict(arquivo=str(a.video), problemas=problemas, medidas=linhas, lufs=lufs, pico_dbfs=pico), ensure_ascii=False, indent=1))
    else:
        print(f'## {a.video.name}')
        for l in linhas:
            print(f'- {l}')
        print('\nTudo certo.' if not problemas else '\nProblemas:')
        for p in problemas:
            print(f'- {p}')
    return 1 if problemas else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
