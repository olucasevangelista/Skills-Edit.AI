#!/usr/bin/env python3
"""Monta uma folha numerada de quadros: o storyboard de uma peça, ou uma folha de contato para revisar (opcional; precisa de Pillow).

Cada imagem da pasta vira um quadro numerado, na ordem do nome do arquivo (01.png, 02.png...). Com --legendas, cada quadro
leva embaixo o que você descreveu dele; sem, leva o nome do arquivo.

Uso:
  python folha_de_quadros.py quadros/ --saida storyboard.png [--legendas legendas.json] [--colunas 3] [--largura 640]

legendas.json: uma lista, na mesma ordem das imagens. Todos os campos são opcionais:
  [{"tempo": "0 a 3 s", "titulo": "Gancho", "texto": "o objeto herói assenta", "move": "câmera recua devagar",
    "vira": "o disco cresce e vira o fundo da cena 2"}, ...]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

EXT = {".png", ".jpg", ".jpeg", ".webp"}
FUNDO, TINTA, SUAVE, MOVE, VIRA = (14, 16, 24), (242, 244, 255), (152, 162, 195), (245, 208, 78), (61, 220, 151)
FONTES = ["/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf", "C:/Windows/Fonts/arial.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans.ttf"]


def fonte(tam: int):
    for f in FONTES:
        try:
            return ImageFont.truetype(f, tam)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=tam)   # Pillow 10.1 ou mais novo
    except TypeError:
        return ImageFont.load_default()


def quebrar(draw: ImageDraw.ImageDraw, texto: str, f, largura: int) -> list[str]:
    linhas, atual = [], ""
    for palavra in texto.split():
        teste = f"{atual} {palavra}".strip()
        if draw.textlength(teste, font=f) <= largura or not atual:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    return linhas + ([atual] if atual else [])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pasta", type=Path)
    ap.add_argument("--saida", type=Path, required=True)
    ap.add_argument("--legendas", type=Path)
    ap.add_argument("--colunas", type=int, default=3)
    ap.add_argument("--largura", type=int, default=640, help="largura de cada quadro na folha (px)")
    a = ap.parse_args()

    arquivos = sorted(p for p in a.pasta.iterdir() if p.suffix.lower() in EXT)
    if not arquivos:
        raise SystemExit(f"Nenhuma imagem em {a.pasta}")
    legendas = json.loads(a.legendas.read_text(encoding="utf-8")) if a.legendas else []
    f_peq, f_med, f_num = fonte(20), fonte(26), fonte(30)
    margem, gap, largura = 30, 28, a.largura
    cols = max(1, min(a.colunas, len(arquivos)))

    # tamanho de cada quadro: proporção da primeira imagem; a altura do texto cabe no maior bloco
    primeira = Image.open(arquivos[0])
    altura = int(largura * primeira.height / primeira.width)
    medidor = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    blocos = []
    for i, arq in enumerate(arquivos):
        lg = legendas[i] if i < len(legendas) else {}
        linhas = []   # (texto, fonte, cor)
        if lg.get("tempo"):
            linhas += [(lg["tempo"], f_peq, SUAVE)]
        linhas += [(lg.get("titulo") or (arq.stem if not lg else ""), f_med, TINTA)]
        for chave, cor, prefixo in (("texto", SUAVE, ""), ("move", MOVE, "move: "), ("vira", VIRA, "vira: ")):
            if lg.get(chave):
                linhas += [(prefixo + lg[chave], f_peq, cor)]
        quebradas = []
        for texto, f, cor in linhas:
            if texto:
                quebradas += [(l, f, cor) for l in quebrar(medidor, texto, f, largura)]
        blocos.append(quebradas)
    h_texto = max(sum(int(f.size * 1.35) for _, f, _ in b) for b in blocos) + 14
    linhas_folha = (len(arquivos) + cols - 1) // cols
    folha = Image.new("RGB", (margem * 2 + cols * largura + (cols - 1) * gap,
                              margem * 2 + linhas_folha * (altura + h_texto) + (linhas_folha - 1) * gap), FUNDO)
    d = ImageDraw.Draw(folha)
    for i, arq in enumerate(arquivos):
        x = margem + (i % cols) * (largura + gap)
        y = margem + (i // cols) * (altura + h_texto + gap)
        folha.paste(Image.open(arq).convert("RGB").resize((largura, altura), Image.LANCZOS), (x, y))
        d.ellipse((x + 10, y + 10, x + 54, y + 54), fill=(255, 255, 255))
        rotulo = str(i + 1)
        d.text((x + 32, y + 32), rotulo, font=f_num, fill=(0, 0, 0), anchor="mm")
        ty = y + altura + 12
        for texto, f, cor in blocos[i]:
            d.text((x, ty), texto, font=f, fill=cor)
            ty += int(f.size * 1.35)
    a.saida.parent.mkdir(parents=True, exist_ok=True)
    folha.save(a.saida)
    print(f"{len(arquivos)} quadros -> {a.saida} ({folha.width}x{folha.height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
