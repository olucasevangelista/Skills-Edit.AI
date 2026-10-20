#!/usr/bin/env python3
"""Cola os clipes de motion (com transparencia) sobre o video limpo e exporta o video final.

O video limpo e codificado UMA vez, com os clipes por cima, so nas janelas deles. O audio e copiado sem recodificar.

Uso:
  python colar.py trabalho/aula_limpa.mp4 clips/manifest.json --saida aula_final.mp4 [--qualidade boa|maxima] [--folha]

manifest.json (gerado por clips.mjs): [{"arquivo": "clips/clip00.mov", "inicio": 1.0, "duracao": 3.0, "nomes": ["Titulo"]}]
--folha gera folha_motions.png: um quadro no meio de cada motion, para conferir de uma vez.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ff  # noqa: E402


def montar_filtro(manifesto: list[dict]) -> str:
    """Cada clipe entra no instante certo; fora da janela o video passa limpo (eof_action=pass)."""
    linhas, atual = [], '0:v'
    for i, c in enumerate(manifesto):
        ini, fim = c['inicio'], c['inicio'] + c['duracao']
        linhas.append(f'[{i + 1}:v]format=yuva444p[c{i}]')
        linhas.append(f"[{atual}][c{i}]overlay=eof_action=pass:format=auto:enable='between(t,{ini:.4f},{fim:.4f})'[o{i}]")
        atual = f'o{i}'
    linhas.append(f'[{atual}]format=yuv420p[v]')
    return ';\n'.join(linhas)


def normalizar(manifesto: list[dict], base: Path) -> list[dict]:
    """Caminhos relativos do manifesto contam a partir da pasta do proprio manifesto."""
    for c in manifesto:
        p = Path(c['arquivo'])
        c['arquivo'] = str(p if p.is_absolute() else (base / p).resolve())
    return manifesto


def validar(manifesto: list[dict], duracao_video: float) -> None:
    if not manifesto:
        raise ValueError('O manifest.json esta vazio.')
    for c in manifesto:
        arq = Path(c['arquivo'])
        if not arq.is_file():
            raise FileNotFoundError(f'Clipe nao encontrado: {arq}')
        if c['inicio'] < 0 or c['inicio'] + c['duracao'] > duracao_video + 0.5:
            raise ValueError(f'O clipe {arq.name} ({c["inicio"]:.2f} a {c["inicio"] + c["duracao"]:.2f} s) fica fora do video ({duracao_video:.2f} s).')


def folha(video: Path, manifesto: list[dict], destino: Path) -> None:
    """Um quadro no meio de cada motion, lado a lado (so FFmpeg)."""
    tmp = destino.parent / '_folha'
    tmp.mkdir(exist_ok=True)
    ff = _ff.exe('ffmpeg')
    for i, c in enumerate(manifesto):
        meio = c['inicio'] + c['duracao'] / 2
        _ff.rodar([ff, '-v', 'error', '-y', '-ss', f'{meio:.3f}', '-i', str(video), '-frames:v', '1',
                   '-vf', 'scale=360:-2', str(tmp / f'q{i:03d}.png')])
    colunas = min(5, len(manifesto))
    linhas = -(-len(manifesto) // colunas)
    _ff.rodar([ff, '-v', 'error', '-y', '-framerate', '1', '-i', str(tmp / 'q%03d.png'), '-vf', f'tile={colunas}x{linhas}',
               '-frames:v', '1', str(destino)])
    for f in tmp.glob('*.png'):
        f.unlink()
    tmp.rmdir()


def main() -> int:
    _ff.configurar_saida()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video', type=Path)
    ap.add_argument('manifesto', type=Path)
    ap.add_argument('--saida', type=Path, required=True)
    ap.add_argument('--qualidade', choices=['boa', 'maxima'], default='boa',
                    help='boa (padrao): libx264 medium CRF 14 | maxima: preset slow, mais lento')
    ap.add_argument('--folha', action='store_true', help='gera folha_motions.png com um quadro por motion')
    a = ap.parse_args()

    manifesto = normalizar(json.loads(a.manifesto.read_text(encoding='utf-8')), a.manifesto.resolve().parent)
    info = _ff.info_basica(a.video)
    validar(manifesto, info['duracao'])
    ff = _ff.exe('ffmpeg')
    # -itsoffset coloca cada clipe no instante certo da linha do tempo (e mantem a leitura sincronizada, com pouca memoria)
    entradas = [x for c in manifesto for x in ('-itsoffset', f'{c["inicio"]:.4f}', '-i', c['arquivo'])]
    a.saida.parent.mkdir(parents=True, exist_ok=True)
    filtro = a.saida.parent / '_filtro_colar.txt'
    filtro.write_text(montar_filtro(manifesto), encoding='utf-8')
    preset = 'slow' if a.qualidade == 'maxima' else 'medium'
    transf = next((s.get('color_transfer') for s in _ff.sonda(a.video)['streams'] if s['codec_type'] == 'video'), None)
    cor = [] if transf in ('arib-std-b67', 'smpte2084') else ['-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709']
    print(f'{len(manifesto)} clipes sobre {_ff.mmss(info["duracao"])} | libx264 {preset} CRF 14', flush=True)
    try:
        _ff.rodar([ff, '-v', 'error', '-y', '-i', str(a.video), *entradas, _ff.flag_filtro_arquivo(), str(filtro),
                   '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-preset', preset, '-crf', '14', '-pix_fmt', 'yuv420p', *cor,
                   '-c:a', 'copy', '-movflags', '+faststart', str(a.saida)])
    finally:
        if filtro.exists():
            os.remove(filtro)
    dur = _ff.info_basica(a.saida)['duracao']
    print(f'pronto: {a.saida} ({_ff.mmss(dur)}; o video limpo tem {_ff.mmss(info["duracao"])})')
    if abs(dur - info['duracao']) > 0.2:
        print('AVISO: a duracao final difere do video limpo.', file=sys.stderr)
    if a.folha:
        destino = a.saida.parent / 'folha_motions.png'
        folha(a.saida, manifesto, destino)
        print(f'folha de conferencia: {destino}')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError, KeyError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
