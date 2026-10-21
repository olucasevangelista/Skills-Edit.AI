#!/usr/bin/env python3
"""Ferramentas de leitura para escolher cortes e marcar emendas, a partir do transcricao.json.

  python ler.py transcricao.json                        texto corrido, uma linha por frase, com o tempo de inicio
  python ler.py transcricao.json 120 180                palavra@inicio-fim e as pausas (||x||) entre 120 s e 180 s
  python ler.py transcricao.json 120 180 --video a.mp4 --silencio   idem, com os silencios REAIS do audio marcados
  python ler.py transcricao.json 120 125 --video a.mp4 --energia    volume a cada 20 ms (para escolher uma emenda a mao)

Tempos em segundos do arquivo original. Pausa de 60 ms ou mais ja serve de ponto de emenda.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ff  # noqa: E402
import _fala  # noqa: E402


def hms(t: float) -> str:
    t = max(0.0, t)
    return f'{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:04.1f}'


def corrido(ws: list[dict], a: float | None, b: float | None, frase_s: float = 12.0) -> None:
    """Uma linha por frase (quebra em pontuacao final ou a cada ~frase_s), com o tempo de inicio."""
    ws = [w for w in ws if (a is None or w['start'] >= a) and (b is None or w['start'] <= b)]
    linha, t0 = [], None
    for i, w in enumerate(ws):
        if not linha:
            t0 = w['start']
        gap = w['start'] - ws[i - 1]['end'] if i else 0
        if linha and gap > 1.0:
            linha.append(f'||{gap:.1f}||')
        linha.append(w['word'])
        if (w['word'].endswith(('.', '?', '!')) and w['end'] - t0 > 4) or w['end'] - t0 > frase_s:
            print(f'[{t0:8.2f} {hms(t0)}] {" ".join(linha)}')
            linha = []
    if linha:
        print(f'[{t0:8.2f} {hms(t0)}] {" ".join(linha)}')


def palavras(ws: list[dict], a: float, b: float, sil: list[tuple[float, float]] | None) -> None:
    ev, prev = [], None
    for w in ws:
        if not a <= w['start'] <= b:
            continue
        if prev is not None and w['start'] - prev > 0.6 and sil is None:
            ev.append((w['start'] - 0.001, f'||{w["start"] - prev:.1f}||'))
        ev.append((w['start'], f'{w["word"]}@{w["start"]:.2f}-{w["end"]:.2f}'))
        prev = w['end']
    if sil is not None:
        ev += [(s, f'||SIL {s:.2f}-{e:.2f}||') for s, e in sil]
    print(' '.join(x for _, x in sorted(ev)))


def energia(ws: list[dict], env: list[float], a: float, b: float) -> None:
    out, t = [], a
    while t <= b:
        db = env[min(len(env) - 1, int(t / _fala.JANELA))]
        marca = '▁▂▃▄▅▆▇█'[min(7, max(0, int((db + 60) / 6)))]
        nomes = [w['word'] for w in ws if abs(w['start'] - t) < 0.01]
        out.append(f'{t:.2f}{marca}{int(db)}' + (f'[{nomes[0]}]' if nomes else ''))
        t = round(t + 0.02, 3)
    print(' '.join(out))


def main() -> int:
    _ff.configurar_saida()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('transcricao', type=Path)
    ap.add_argument('ini', nargs='?', type=float)
    ap.add_argument('fim', nargs='?', type=float)
    ap.add_argument('--video', type=Path, help='arquivo original (necessario com --silencio e --energia)')
    ap.add_argument('--silencio', action='store_true')
    ap.add_argument('--energia', action='store_true')
    ap.add_argument('--corrido', action='store_true', help='texto corrido mesmo com ini/fim')
    a = ap.parse_args()
    ws = _fala.carregar_palavras(a.transcricao)
    if a.ini is None or a.corrido:
        corrido(ws, a.ini, a.fim)
        return 0
    b = a.fim if a.fim is not None else a.ini + 30
    if a.silencio or a.energia:
        if not a.video:
            raise ValueError('--silencio e --energia precisam de --video com o arquivo original.')
        env = _ff.envelope_db(a.video)
        thr = _fala.limiar_auto(env)
        if a.energia:
            energia(ws, env, a.ini, b)
        else:
            print(f'(silencio = abaixo de {thr:.0f} dB por pelo menos 60 ms)')
            palavras(ws, a.ini, b, _fala.silencios(env, thr, a.ini, b))
    else:
        palavras(ws, a.ini, b, None)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
