"""Faixas de voz pelo volume do audio (somente biblioteca padrao)."""
from __future__ import annotations

JANELA = 0.01   # s por amostra do envelope (_ff.envelope_db)


def limiar_auto(env: list[float]) -> float:
    """Piso de ruido + 12 dB, limitado entre -46 e -38 dB."""
    s = sorted(env)
    piso = s[min(len(s) - 1, max(0, int(round(0.10 * (len(s) - 1)))))]
    return max(-46.0, min(-38.0, piso + 12.0))


def faixas_de_fala(env: list[float], limiar: float, fecha: float = 0.12, ilha: float = 0.05) -> list[tuple[float, float]]:
    """Trechos com voz [(inicio, fim)] em segundos. Fecha buracos menores que `fecha` e ignora estalos menores que `ilha`."""
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
