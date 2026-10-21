"""Fala e transcricao (somente biblioteca padrao): palavras com tempo, trechos com voz e silencios reais."""
from __future__ import annotations

import json
import re
from pathlib import Path

JANELA = 0.01   # s por amostra do envelope (_ff.envelope_db)

# palavras que o Whisper escreve de um jeito ou de outro, ou que ele engole: nao contam como "faltando"
IGNORAR = {'é', 'e', 'o', 'a', 'né', 'tá', 'pô', 'aí', 'hein', 'ó', 'ah', 'eh', 'hum', 'hã', 'beleza', 'the', 'uh'}
EQUIV = {'pra': 'para', 'pro': 'para', 'tá': 'está', 'tô': 'estou', 'cê': 'você', 'tava': 'estava', 'tão': 'estão',
         'num': 'não'}


def carregar_palavras(caminho: Path) -> list[dict]:
    """Le o transcricao.json da skill de transcricao (ou uma lista de palavras) e devolve
    [{word, start, end}] em segundos do ARQUIVO ORIGINAL (usa source_start/source_end quando existem)."""
    d = json.loads(Path(caminho).read_text(encoding='utf-8'))
    bruto = d.get('words') if isinstance(d, dict) else d
    if not bruto:
        raise ValueError(f'Sem palavras com tempo em {caminho}. A transcricao precisa ter "words" (com start/end).')
    out = []
    for w in bruto:
        txt = str(w.get('word', w.get('text', ''))).strip()
        a, b = w.get('source_start', w.get('start')), w.get('source_end', w.get('end'))
        if txt and a is not None and b is not None:
            out.append(dict(word=txt, start=float(a), end=float(b)))
    out.sort(key=lambda w: w['start'])
    return out


def tokens(texto: str) -> list[str]:
    return [EQUIV.get(t, t) for t in re.findall(r'[a-zà-ú0-9]+', texto.lower())]


def limiar_auto(env: list[float]) -> float:
    """Piso de ruido + 12 dB, limitado entre -46 e -38 dB."""
    s = sorted(env)
    piso = s[min(len(s) - 1, max(0, int(round(0.10 * (len(s) - 1)))))]
    return max(-46.0, min(-38.0, piso + 12.0))


def faixas_de_fala(env: list[float], limiar: float, fecha: float = 0.06, ilha: float = 0.04) -> list[tuple[float, float]]:
    """Trechos com voz [(inicio, fim)] em segundos. Buracos menores que `fecha` sao fechados (por isso uma pausa
    de 60 ms ja separa duas faixas) e estalos menores que `ilha` sao ignorados."""
    runs: list[list[int]] = []
    i, n = 0, len(env)
    while i < n:
        if env[i] > limiar:
            j = i
            while j < n and env[j] > limiar:
                j += 1
            runs.append([i, j])
            i = j
        else:
            i += 1
    fundidos: list[list[int]] = []
    for r in runs:
        if fundidos and (r[0] - fundidos[-1][1]) * JANELA < fecha:
            fundidos[-1][1] = r[1]
        else:
            fundidos.append(r)
    return [(a * JANELA, b * JANELA) for a, b in fundidos if (b - a) * JANELA >= ilha]


def silencios(env: list[float], limiar: float, a: float, b: float, minimo: float = 0.06) -> list[tuple[float, float]]:
    """Silencios reais (abaixo do limiar por pelo menos `minimo` s) entre a e b."""
    i0, i1 = max(0, int(a / JANELA)), min(len(env), int(b / JANELA) + 1)
    out, i = [], i0
    while i < i1:
        if env[i] <= limiar:
            j = i
            while j < i1 and env[j] <= limiar:
                j += 1
            if (j - i) * JANELA >= minimo:
                out.append((i * JANELA, j * JANELA))
            i = j
        else:
            i += 1
    return out
