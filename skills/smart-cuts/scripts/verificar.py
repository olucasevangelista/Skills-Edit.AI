#!/usr/bin/env python3
"""Verifica cada corte medindo (nao confiando): duracao, sincronia, volume, pausas que sobraram, estalos nas emendas
e, principalmente, se TODA a fala esperada esta no corte final.

A conferencia de fala compara o texto esperado (do plano) com a transcricao do MP4 FINAL. Essa transcricao e feita antes,
com a skill de transcricao, uma pasta por corte: <transcricoes>/<id>/transcricao.json.
ALERTA ou PENDENTE = nao entregue. Sai com codigo 0 (tudo certo) ou 1.

Uso:
  python verificar.py pasta/plano.json --transcricoes pasta/transcricoes [--so c1,c2] [--sem-fala]
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ff  # noqa: E402
import _fala  # noqa: E402


def volume(video: Path) -> tuple[float, float]:
    r = _ff.rodar([_ff.exe('ffmpeg'), '-hide_banner', '-i', str(video), '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'], check=False)
    resumo = r.stderr[r.stderr.rfind('Summary:'):]
    i = re.search(r'I:\s+(-?[\d.]+) LUFS', resumo)
    p = re.search(r'Peak:\s+(-?[\d.]+) dBFS', resumo)
    return (float(i.group(1)) if i else float('nan'), float(p.group(1)) if p else float('nan'))


def estalo_na_emenda(video: Path, t: float) -> float:
    """Maior salto entre amostras vizinhas (0 a 1, fundo de escala) em 120 ms ao redor de t. Estalo = salto grande."""
    p = subprocess.run([_ff.exe('ffmpeg'), '-v', 'error', '-ss', f'{max(0.0, t - 0.06):.3f}', '-t', '0.12', '-i', str(video),
                        '-vn', '-ac', '1', '-ar', '48000', '-f', 's16le', '-'], capture_output=True)
    n = len(p.stdout) // 2
    if n < 3:
        return 0.0
    x = struct.unpack(f'<{n}h', p.stdout[:n * 2])
    return max(abs(x[i] - x[i - 1]) for i in range(1, n)) / 32768.0


def comparar_fala(esperado: str, ouvido: str) -> tuple[list[str], list[str], str]:
    """Devolve (faltando, sobrando, fim_ruim). Faltando = palavra de conteudo esperada e nao ouvida (ALERTA).
    Sobrando = palavra ouvida e nao esperada (confira a emenda; o Whisper varia a escrita, entao so avisa)."""
    esp, ouv = _fala.tokens(esperado), _fala.tokens(ouvido)
    sm = difflib.SequenceMatcher(a=esp, b=ouv, autojunk=False)
    faltando, sobrando = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op in ('delete', 'replace'):
            miss = [t for t in esp[i1:i2] if t not in _fala.IGNORAR and len(t) > 2]
            if miss and (op == 'delete' or len(miss) > (j2 - j1)):
                faltando.append(f'[{" ".join(esp[i1:i2])}] em: ...{" ".join(esp[max(0, i1 - 4):i2 + 4])}...')
        if op in ('insert', 'replace'):
            extra = [t for t in ouv[j1:j2] if t not in _fala.IGNORAR and len(t) > 2]
            if extra and (op == 'insert' or len(extra) > (i2 - i1)):
                sobrando.append(f'[{" ".join(ouv[j1:j2])}] em: ...{" ".join(ouv[max(0, j1 - 4):j2 + 4])}...')
    ult_e = [t for t in esp if t not in _fala.IGNORAR][-2:]
    ult_o = [t for t in ouv if t not in _fala.IGNORAR][-2:]
    fim = f'esperado terminar em "{" ".join(ult_e)}", ouvido "{" ".join(ult_o)}"' if ult_e and ult_e != ult_o else ''
    return faltando, sobrando, fim


def verificar_corte(c: dict, pasta: Path, transcricoes: Path | None, a: argparse.Namespace) -> list[str]:
    video = pasta / c['arquivo']
    problemas: list[str] = []
    linhas = [f'## {c["id"]}']
    if not video.exists():
        return [f'{c["id"]}: arquivo {video.name} nao existe (rode montar.py).']
    d = _ff.sonda(video)
    fmt = float(d['format']['duration'])
    vs = next((s for s in d['streams'] if s['codec_type'] == 'video'), None)
    as_ = next((s for s in d['streams'] if s['codec_type'] == 'audio'), None)
    if vs is None or as_ is None:
        return [f'{c["id"]}: o arquivo precisa ter imagem e audio.']
    dv, da = float(vs.get('duration', fmt)), float(as_.get('duration', fmt))
    linhas.append(f'- Duracao: plano {c["duracao"]:.2f} s | arquivo {fmt:.2f} s | video {dv:.2f} s | audio {da:.2f} s')
    if abs(fmt - c['duracao']) > 0.25:
        problemas.append(f'{c["id"]}: duracao {fmt:.2f} s difere do plano ({c["duracao"]:.2f} s).')
    if abs(dv - da) > 0.12:
        problemas.append(f'{c["id"]}: video ({dv:.2f} s) e audio ({da:.2f} s) com duracoes diferentes (possivel dessincronia).')

    lufs, pico = volume(video)
    linhas.append(f'- Volume: {lufs:.1f} LUFS (alvo {a.lufs:g}) | pico {pico:.1f} dBFS')
    if lufs == lufs and abs(lufs - a.lufs) > 1.5:
        problemas.append(f'{c["id"]}: volume {lufs:.1f} LUFS fora do alvo {a.lufs:g}.')
    if pico == pico and pico > -0.5:
        problemas.append(f'{c["id"]}: pico de {pico:.1f} dBFS (risco de distorcer).')

    env = _ff.envelope_db(video)
    faixas = _fala.faixas_de_fala(env, _fala.limiar_auto(env), fecha=0.12, ilha=0.05)
    pausas = [faixas[i + 1][0] - faixas[i][1] for i in range(len(faixas) - 1)]
    longas = [(faixas[i][1], p) for i, p in enumerate(pausas) if p > a.pausa_max]
    linhas.append(f'- Maior pausa: {max(pausas) if pausas else 0:.2f} s | acima de {a.pausa_max:g} s: {len(longas)}')
    if longas:
        problemas.append(f'{c["id"]}: {len(longas)} pausa(s) acima de {a.pausa_max:g} s (primeira em {_ff.mmss(longas[0][0])}).')

    ruins = [(e['t'], s) for e in c['emendas'] if (s := estalo_na_emenda(video, e['t'])) > a.limite_estalo]
    linhas.append(f'- Emendas: {len(c["emendas"])} | com estalo provavel: {len(ruins)}')
    if ruins:
        problemas.append(f'{c["id"]}: {len(ruins)} emenda(s) com estalo provavel (primeira em {_ff.mmss(ruins[0][0])}).')

    if not a.sem_fala:
        tj = (transcricoes / c['id'] / 'transcricao.json') if transcricoes else None
        if tj is None or not tj.exists():
            problemas.append(f'{c["id"]}: PENDENTE a conferencia de fala. Transcreva {video.name} (nome "{c["id"]}") e rode de novo '
                             f'com --transcricoes (esperado: {tj or "<pasta>/" + c["id"] + "/transcricao.json"}).')
        else:
            ouvido = ' '.join(w['word'] for w in _fala.carregar_palavras(tj))
            faltando, sobrando, fim = comparar_fala(c['texto'], ouvido)
            linhas.append(f'- Fala: {len(faltando)} palavra(s) faltando | {len(sobrando)} sobrando | fim {"ok" if not fim else "DIFERENTE"}')
            for f in faltando:
                problemas.append(f'{c["id"]}: ALERTA esperado e nao ouvido: {f}')
            if fim:
                problemas.append(f'{c["id"]}: ALERTA fim: {fim}')
            for s in sobrando[:5]:
                linhas.append(f'  - aviso (ouca a emenda): ouvido e nao esperado {s}')
    print('\n'.join(linhas))
    return problemas


def main() -> int:
    _ff.configurar_saida()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('plano', type=Path, help='plano.json gerado por montar.py')
    ap.add_argument('--pasta', type=Path, help='onde estao os mp4 (padrao: a pasta do plano)')
    ap.add_argument('--transcricoes', type=Path, help='pasta com <id>/transcricao.json de cada corte final')
    ap.add_argument('--so', default='', help='verificar so estes ids (separados por virgula)')
    ap.add_argument('--sem-fala', action='store_true', help='nao confere a fala (so medidas); o corte NAO esta liberado')
    ap.add_argument('--pausa-max', type=float, default=0.8, help='pausas acima disso sao sobras (padrao 0.8 s)')
    ap.add_argument('--lufs', type=float, default=-16.0)
    ap.add_argument('--limite-estalo', type=float, default=0.35, help='salto de amostra (fundo de escala) que conta como estalo')
    a = ap.parse_args()

    plano = json.loads(a.plano.read_text(encoding='utf-8'))
    pasta = a.pasta or a.plano.resolve().parent
    so = {x for x in a.so.split(',') if x}
    problemas: list[str] = []
    for c in plano['cortes']:
        if so and c['id'] not in so:
            continue
        problemas += verificar_corte(c, pasta, a.transcricoes, a)
    print('\n' + ('Tudo certo.' if not problemas else 'Problemas:'))
    for p in problemas:
        print(f'- {p}')
    return 1 if problemas else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError, StopIteration, KeyError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
