#!/usr/bin/env python3
"""Sintetiza trilha e efeitos sonoros a partir de um mapa de eventos (opcional; precisa de numpy).

Sem samples nem música de terceiros: cada som é gerado por matemática (ondas e ruído com envelope de volume).
Semente fixa: o mesmo mapa gera sempre o mesmo áudio. O resultado é eletrônico e simples (trilha conceitual),
feito para ser substituível por uma música de verdade.

Uso:
  python sintetizar.py mapa.json --saida pasta [--eventos config.ts] [--fps 30]
Gera em --saida: sfx.wav (efeitos), musica.wav (se o mapa tiver "trilha") e mix.wav (os dois, com limite de pico).

Som por evento: em vez de um instante digitado à mão ("t"), um evento do mapa pode apontar para um NOME ("evento"),
e os instantes vêm de --eventos: um .json ({"etapa.separa": 3.9}) ou o `config.ts` do projeto, que exporta
`EVENTOS` com um nome e um número de segundos por linha. Mudou um tempo na animação? O som acompanha.
--fps encaixa cada evento no quadro do vídeo (o mesmo arredondamento de `sec()` do kit de movimento).

Formato do mapa (veja mapa-exemplo.json):
  {"duracao": 12, "semente": 7, "fade_final": 0.7,
   "trilha": {"bpm": 120, "de": 0, "ate": 12, "acordes": [[50,57,60,64], [46,53,57,62]], "ganho": 1.0},
   "eventos": [{"t": 3.9, "tipo": "clique", "ganho": 0.8, "pan": 0.0}, {"t": 9.7, "tipo": "acorde", "nota": [57,60,64]},
               {"evento": "etapa.separa", "deslocamento": -0.05, "tipo": "toque"}]}
Tipos de evento: bumbo, clique, chiado, whoosh, toque (nota MIDI), acorde (lista de notas MIDI).
"""
from __future__ import annotations

import argparse
import json
import re
import wave
from pathlib import Path

import numpy as np

SR = 48000
PICO_MAX = 10 ** (-1.5 / 20)   # pico da mistura: -1,5 dBFS


def tt(d: float) -> np.ndarray:
    return np.arange(int(d * SR)) / SR


def mtof(m: float) -> float:
    return 440.0 * 2 ** ((m - 69) / 12)


def passa_alta(x: np.ndarray, n: int = 8) -> np.ndarray:
    return x - np.convolve(x, np.ones(n) / n, "same")


def bumbo(rng) -> np.ndarray:
    t = tt(0.36)
    fase = 2 * np.pi * (44 * t + (120 - 44) * 0.032 * (1 - np.exp(-t / 0.032)))
    return np.sin(fase) * np.exp(-t * 15) * np.minimum(t / 0.001, 1)


def clique(rng) -> np.ndarray:
    t = tt(0.09)
    return (np.sin(2 * np.pi * 1800 * t) * 0.8 + rng.normal(0, 0.2, len(t))) * np.exp(-t * 55)


def chiado(rng) -> np.ndarray:
    t = tt(0.08)
    return passa_alta(rng.normal(0, 1, len(t)), 5) * np.exp(-t * 70)


def whoosh(rng) -> np.ndarray:
    t = tt(0.5)
    ruido = np.convolve(rng.normal(0, 1, len(t)), np.ones(14) / 14, "same")
    return ruido * np.sin(np.pi * t / 0.5) ** 2 * 1.6


def toque(rng, nota: float = 81) -> np.ndarray:
    t = tt(0.9)
    f = mtof(nota)
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t)) * np.exp(-t * 5) * np.minimum(t / 0.004, 1)


def acorde(rng, notas=(57, 60, 64)) -> np.ndarray:
    t = tt(1.4)
    s = sum(np.sin(2 * np.pi * mtof(n) * t) + 0.2 * np.sin(4 * np.pi * mtof(n) * t) for n in notas)
    return s / max(1, len(notas)) * np.exp(-t * 2.6) * np.minimum(t / 0.01, 1)


def nota_grave(rng, midi: float) -> np.ndarray:
    t = tt(0.48)
    f = mtof(midi)
    return (np.sin(2 * np.pi * f * t) + 0.18 * np.sin(4 * np.pi * f * t)) * np.minimum(t / 0.008, 1) * np.exp(-t * 7)


SONS = {"bumbo": bumbo, "clique": clique, "chiado": chiado, "whoosh": whoosh}


def somar(bus: np.ndarray, sinal: np.ndarray, em: float, ganho: float = 1.0, pan: float = 0.0) -> None:
    ini = int(round(em * SR))
    if ini < 0 or ini >= len(bus):
        return
    n = min(len(sinal), len(bus) - ini)
    bus[ini:ini + n, 0] += sinal[:n] * ganho * np.sqrt((1 - pan) / 2)
    bus[ini:ini + n, 1] += sinal[:n] * ganho * np.sqrt((1 + pan) / 2)


def gerar_trilha(bus: np.ndarray, cfg: dict, rng) -> None:
    """Bumbo em todas as batidas, palma nas batidas ímpares, chiado fora do tempo, baixo e acorde por compasso."""
    bpm = float(cfg.get("bpm", 120))
    de, ate = float(cfg.get("de", 0)), float(cfg.get("ate", len(bus) / SR))
    ganho = float(cfg.get("ganho", 1.0))
    batida = 60.0 / bpm
    acordes = cfg.get("acordes") or [[50, 57, 60, 64]]
    n = int((ate - de) / batida)
    for b in range(n):
        em = de + b * batida
        somar(bus, bumbo(rng), em, 0.39 * ganho)
        if b % 2 == 1:
            t = tt(0.15)
            palma = passa_alta(rng.normal(0, 1, len(t)), 9) * (np.exp(-t * 42) + 0.5 * np.exp(-(((t - 0.016) / 0.005) ** 2)))
            somar(bus, palma, em, 0.05 * ganho, -0.1)
        if b >= 4:
            somar(bus, chiado(rng), em + batida / 2, 0.045 * ganho, 0.35 if b % 2 else -0.35)
        acorde_b = acordes[(b // 4) % len(acordes)]
        somar(bus, nota_grave(rng, acorde_b[0] - 12), em, 0.19 * ganho)
        if b % 4 == 0:
            somar(bus, acorde(rng, acorde_b[1:]), em, 0.12 * ganho)


def fade_final(bus: np.ndarray, d: float) -> None:
    n = min(len(bus), int(d * SR))
    if n > 0:
        bus[-n:] *= np.linspace(1, 0, n)[:, None]


def escrever(caminho: Path, bus: np.ndarray) -> None:
    pcm = (np.clip(bus, -1, 1) * 32767).astype("<i2")
    with wave.open(str(caminho), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def carregar_eventos(caminho: Path) -> dict[str, float]:
    """Nome -> segundos. Aceita .json ({nome: t} ou [{nome, t}]) ou um .ts/.tsx/.js com `EVENTOS = { "nome": 3.9, ... }`
    (um evento por linha, números literais em segundos)."""
    texto = caminho.read_text(encoding="utf-8")
    if caminho.suffix.lower() == ".json":
        dados = json.loads(texto)
        if isinstance(dados, dict):
            return {str(k): float(v) for k, v in dados.items()}
        return {str(e.get("nome") or e["name"]): float(e["t"]) for e in dados}
    m = re.search(r"\bEVENTOS\b\s*(?::[^=]+)?=\s*\{(.*?)\n\s*\}", texto, re.S)
    if not m:
        raise SystemExit(f"Não achei `EVENTOS = {{ ... }}` em {caminho}.")
    corpo = re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S)
    eventos: dict[str, float] = {}
    for linha in corpo.split("\n"):
        linha = re.sub(r"//.*", "", linha).strip()
        if not linha:
            continue
        par = re.fullmatch(r"""["']?([\w.\-]+)["']?\s*:\s*(-?\d+(?:\.\d+)?)\s*,?""", linha)
        if not par:
            raise SystemExit(f"EVENTOS em {caminho}: use um nome e um número de segundos por linha (não entendi: {linha!r}).")
        eventos[par.group(1)] = float(par.group(2))
    return eventos


def instante(ev: dict, eventos: dict[str, float], fps: float | None) -> tuple[float, str]:
    """Segundos em que o evento do mapa soa (e o nome, se houver). Com `fps`, cai no quadro do vídeo."""
    if "evento" in ev:
        if "t" in ev:
            raise SystemExit(f"O evento {ev['evento']!r} tem 'evento' e 't' ao mesmo tempo: use só um (e 'deslocamento' para ajustar).")
        if ev["evento"] not in eventos:
            achados = ", ".join(sorted(eventos)) or "nenhum: passe --eventos"
            raise SystemExit(f"Evento desconhecido: {ev['evento']!r} (eventos conhecidos: {achados})")
        t, nome = eventos[ev["evento"]] + float(ev.get("deslocamento", 0.0)), ev["evento"]
    else:
        t, nome = float(ev["t"]), ""
    return (round(t * fps) / fps if fps else t), nome


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mapa", type=Path)
    ap.add_argument("--saida", type=Path, required=True)
    ap.add_argument("--eventos", type=Path, help="eventos nomeados: um .json ou o config.ts do projeto (veja acima)")
    ap.add_argument("--fps", type=float, help="encaixa cada evento no quadro do vídeo (ex.: 30)")
    a = ap.parse_args()
    eventos = carregar_eventos(a.eventos) if a.eventos else {}
    mapa = json.loads(a.mapa.read_text(encoding="utf-8"))
    dur = float(mapa["duracao"])
    n = int(round(dur * SR))
    rng = np.random.default_rng(int(mapa.get("semente", 1)))
    sfx, musica = np.zeros((n, 2)), np.zeros((n, 2))
    relatorio = []
    for ev in mapa.get("eventos", []):
        em, nome = instante(ev, eventos, a.fps)
        tipo, g, pan = ev["tipo"], float(ev.get("ganho", 1.0)), float(ev.get("pan", 0.0))
        relatorio.append((em, nome, tipo))
        if tipo == "toque":
            sinal = toque(rng, float(ev.get("nota", 81)))
        elif tipo == "acorde":
            sinal = acorde(rng, ev.get("nota", [57, 60, 64]))
        elif tipo in SONS:
            sinal = SONS[tipo](rng)
        else:
            raise SystemExit(f"Tipo de evento desconhecido: {tipo} (use {', '.join(list(SONS) + ['toque', 'acorde'])})")
        somar(sfx, sinal, em, 0.5 * g, pan)
    if mapa.get("trilha"):
        gerar_trilha(musica, mapa["trilha"], rng)
    fim = float(mapa.get("fade_final", 0.7))
    for bus in (sfx, musica):
        fade_final(bus, fim)
    mix = sfx + musica
    pico = float(np.max(np.abs(mix))) if mix.size else 0.0
    k = PICO_MAX / pico if pico > PICO_MAX else 1.0     # mesmo ganho nas três faixas: a proporção entre elas não muda
    a.saida.mkdir(parents=True, exist_ok=True)
    escrever(a.saida / "sfx.wav", sfx * k)
    if mapa.get("trilha"):
        escrever(a.saida / "musica.wav", musica * k)
    escrever(a.saida / "mix.wav", mix * k)
    por_nome = [r for r in relatorio if r[1]]
    if por_nome:
        print("evento por nome -> instante" + (f" (quadro a {a.fps:g} fps)" if a.fps else ""))
        for em, nome, tipo in sorted(por_nome):
            print(f"  {nome:<24} {em:7.3f} s" + (f"  quadro {round(em * a.fps)}" if a.fps else "") + f"  {tipo}")
    print(f"{dur:g} s | {len(mapa.get('eventos', []))} eventos | trilha: {'sim' if mapa.get('trilha') else 'não'} | "
          f"pico da mistura {20 * np.log10(max(1e-9, np.max(np.abs(mix * k)))):.1f} dBFS | arquivos em {a.saida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
