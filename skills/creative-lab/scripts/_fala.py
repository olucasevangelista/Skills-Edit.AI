"""Faixas de voz pelo volume do audio (somente biblioteca padrao)."""
from __future__ import annotations

JANELA = 0.01   # s por amostra do envelope (_ff.envelope_db)


def _percentil(valores: list[float], p: float) -> float:
    s = sorted(valores)
    return s[min(len(s) - 1, max(0, int(round(p / 100 * (len(s) - 1)))))]


def limiar_auto(env: list[float]) -> float:
    """Limiar de silencio em dB, entre o piso de ruido (percentil 10) e o nivel da fala (percentil 90).

    Piso + 12 dB (ou +40% da distancia ate a fala, em audio ruidoso), nunca abaixo de -46 dB e nunca acima de (fala - 10 dB).
    O teto NAO e fixo: numa sala com ruido de fundo alto, um teto fixo baixo trata o ruido como fala."""
    piso, fala = _percentil(env, 10), _percentil(env, 90)
    margem = min(12.0, 0.4 * max(0.0, fala - piso))
    return min(max(-46.0, piso + margem), fala - 10.0)


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
