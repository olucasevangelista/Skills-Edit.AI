#!/usr/bin/env python3
"""Mede o ataque de efeitos sonoros, para alinhá-los à batida (opcional; precisa de numpy e FFmpeg).

Um arquivo de efeito quase nunca tem o som forte no primeiro instante: um "pop" pode ter 80 ms de silêncio antes,
um whoosh leva meio segundo para chegar ao máximo. Se o arquivo começa no instante do evento, o som cai atrasado.
Este script diz onde está cada ponto do som, para você começar o arquivo mais cedo e o ponto certo cair no evento:

  inicio  primeiro instante audível (8% do pico)         -> use em camas e sons longos (alinhar: início)
  pico    instante do máximo                              -> use em batidas, pops, cliques e whooshes (alinhar: pico)
  fim     último instante audível (5% do pico)            -> use em risers que devem terminar na revelação (alinhar: fim)

Uso:
  python ataque.py som1.wav som2.mp3 ... [--json]
Para um evento no instante E (em segundos) e o ponto escolhido em P (em segundos, contado do começo do arquivo),
o arquivo deve começar em E - P.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np

SR = 48000
JANELA = 0.01   # s: resolução do envelope de volume


def carregar(caminho: Path) -> np.ndarray:
    bruto = subprocess.run(["ffmpeg", "-v", "error", "-i", str(caminho), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                           capture_output=True, check=True).stdout
    return np.frombuffer(bruto, dtype=np.float32).astype(np.float64)


def envelope(x: np.ndarray) -> np.ndarray:
    n = int(JANELA * SR)
    cortes = len(x) // n
    return np.abs(x[:cortes * n]).reshape(cortes, n).max(axis=1) if cortes else np.zeros(0)


def medir(caminho: Path) -> dict:
    x = carregar(caminho)
    e = envelope(x)
    if e.size == 0 or e.max() < 1e-6:
        return {"arquivo": caminho.name, "duracao": round(len(x) / SR, 3), "inicio": None, "pico": None, "fim": None}
    pico = e.max()
    return {
        "arquivo": caminho.name,
        "duracao": round(len(x) / SR, 3),
        "inicio": round(float(np.argmax(e > 0.08 * pico)) * JANELA, 3),
        "pico": round(float(np.argmax(e)) * JANELA, 3),
        "fim": round(float(np.where(e > 0.05 * pico)[0][-1] + 1) * JANELA, 3),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arquivos", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true", help="saída em JSON (uma lista)")
    a = ap.parse_args()
    medidas = [medir(f) for f in a.arquivos]
    if a.json:
        print(json.dumps(medidas, ensure_ascii=False, indent=1))
        return 0
    print(f"{'arquivo':<40} {'duração':>8} {'início':>8} {'pico':>8} {'fim':>8}   (segundos desde o começo do arquivo)")
    for m in medidas:
        if m["pico"] is None:
            print(f"{m['arquivo'][:40]:<40} {m['duracao']:8.3f}   arquivo mudo")
        else:
            print(f"{m['arquivo'][:40]:<40} {m['duracao']:8.3f} {m['inicio']:8.2f} {m['pico']:8.2f} {m['fim']:8.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
