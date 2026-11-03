#!/usr/bin/env python3
"""Verifica o kit Remotion contra um projeto real (somente biblioteca padrao; precisa de Node, ffmpeg e do projeto).

  python verificar_kit.py <pasta do projeto Remotion, com node_modules> [--rapido]

O projeto precisa ter instalado: remotion, @remotion/cli, @remotion/media, react, typescript e eslint (opcional).
O script copia o kit para src/_fabrica_teste/, gera entradas sinteticas em public/_fabrica_teste/, confere e APAGA as duas pastas.

Confere: tipos e lint; render de quadros de cada formato; determinismo; zona segura do texto; layout de cada formato
(areas, cores, janela do cinema); pausa e retomada do React; deslize do Antes e Depois; balões do
Chat; zoom do Depoimento; formatos distintos entre si; e a emenda com sobreposicao (imagem e audio entram juntos).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

KIT = Path(__file__).resolve().parents[1] / "kit"
L, A, E = 1080, 1920, 4          # tamanho do quadro e a escala da leitura reduzida (270 x 480)
PREFIXO = "_fabrica_teste"
resultados: list[tuple[bool, str]] = []


def ok(cond, texto: str) -> bool:
    resultados.append((bool(cond), texto))
    print(("OK    " if cond else "FALHOU"), texto, flush=True)
    return bool(cond)


def rodar(args, cwd: Path, **kw) -> subprocess.CompletedProcess:
    return subprocess.run([str(x) for x in args], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def ff(*args, entrada=None) -> bytes:
    return subprocess.run(["ffmpeg", "-v", "error", *map(str, args)], capture_output=True, input=entrada).stdout


# ------------------------------------------------------------------------------------------- entradas sinteticas

def gerar_entradas(pub: Path) -> None:
    pub.mkdir(parents=True, exist_ok=True)
    ff("-y", "-f", "lavfi", "-i", "color=c=0x2B6CB0:s=720x1280:r=30:d=12,drawbox=x=250:y=330:w=220:h=260:color=0xE0AC82:t=fill,drawbox=x=170:y=600:w=380:h=680:color=0x1A365D:t=fill,format=yuv420p",
       "-f", "lavfi", "-i", "sine=f=440:d=12", "-c:v", "libx264", "-c:a", "aac", "-shortest", pub / "pessoa.mp4")
    ff("-y", "-f", "lavfi", "-i", "color=c=0x6B46C1:s=720x1280:r=30:d=12,drawbox=x=250:y=330:w=220:h=260:color=0xD69E80:t=fill,drawbox=x=170:y=600:w=380:h=680:color=0x322659:t=fill,format=yuv420p",
       "-f", "lavfi", "-i", "sine=f=330:d=12", "-c:v", "libx264", "-c:a", "aac", "-shortest", pub / "reacao.mp4")
    ff("-y", "-f", "lavfi", "-i", "color=c=0xDD6B20:s=640x360:r=30:d=12[bg];color=c=0x7B341E:s=140x120:d=12[bx];[bg][bx]overlay=x='mod(t*60,500)':y=120,format=yuv420p",
       "-f", "lavfi", "-i", "sine=f=660:d=12", "-c:v", "libx264", "-c:a", "aac", "-shortest", pub / "conteudo3.mp4")
    for nome, cor, tam in (("conteudo1", "ED8936", "1280x720"), ("conteudo2", "319795", "1280x720"), ("antes", "9B2C2C", "1080x1260"), ("depois", "2F855A", "1080x1260"), ("prova", "D69E2E", "984x520")):
        ff("-y", "-f", "lavfi", "-i", f"color=c=0x{cor}:s={tam}:d=1,drawbox=x=40:y=40:w=iw/3:h=ih/4:color=black@0.35:t=fill", "-frames:v", "1", pub / f"{nome}.png")
    ff("-y", "-f", "lavfi", "-i", "sine=f=262:d=12", "-af", "volume=0.5", "-c:a", "pcm_s16le", pub / "musica.wav")
    # dois takes para o teste da emenda: A (vermelho, 440 Hz, voz de 0,2 a 2,0 s) e B (azul, 880 Hz, voz de 0,2 a 2,0 s)
    for nome, cor, f in (("takeA", "0xC53030", 440), ("takeB", "0x2B50C5", 880)):
        ff("-y", "-f", "lavfi", "-i", f"color=c={cor}:s=720x1280:r=30:d=2.6,format=yuv420p",
           "-f", "lavfi", "-i", f"sine=f={f}:d=2.6,volume='if(between(t,0.2,2.0),1,0)':eval=frame", "-c:v", "libx264", "-c:a", "aac", "-shortest", pub / f"{nome}.mp4")


def preparar(proj: Path) -> Path:
    dest = proj / "src" / PREFIXO
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(KIT, dest, ignore=shutil.ignore_patterns("README.md", "assets"))
    shutil.copytree(KIT / "assets", proj / "public" / "fabrica", dirs_exist_ok=True)  # fontes e marcas, como o instalador faz
    props = dest / "exemplo" / "props.ts"
    texto = props.read_text(encoding="utf-8")
    texto = re.sub(r'"((?:pessoa|reacao|conteudo[123]|antes|depois|prova|musica)\.(?:mp4|png|wav))"', rf'"{PREFIXO}/\1"', texto)
    props.write_text(texto, encoding="utf-8")
    return dest


# ------------------------------------------------------------------------------------------------ renders e medidas

class Projeto:
    def __init__(self, proj: Path, tmp: Path):
        self.proj, self.tmp = proj, tmp
        self.npx = shutil.which("npx") or shutil.which("npx.cmd")
        self.entrada = f"src/{PREFIXO}/index.ts"

    def quadro(self, comp: str, n: int, nome: str | None = None, props: Path | None = None) -> Path:
        destino = self.tmp / (nome or f"{comp}_{n}.png")
        if destino.exists():
            return destino
        args = [self.npx, "remotion", "still", self.entrada, comp, destino, f"--frame={n}", "--log=error"]
        if props:
            args.append(f"--props={props}")
        rodar(args, self.proj)
        if not destino.exists() or destino.stat().st_size < 1000:
            raise RuntimeError(f"nao consegui renderizar {comp} no quadro {n}")
        return destino

    def video(self, comp: str, props: Path, nome: str) -> Path:
        destino = self.tmp / nome
        rodar([self.npx, "remotion", "render", self.entrada, comp, destino, f"--props={props}", "--codec=h264", "--crf=18", "--pixel-format=yuv420p",
               "--image-format=png", "--concurrency=2", "--log=error"], self.proj)
        if not destino.exists():
            raise RuntimeError(f"nao consegui renderizar o video de {comp}")
        return destino


def reduzido(png: Path) -> bytes:
    return ff("-i", png, "-vf", f"scale={L // E}:{A // E}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-")


def cor_media(png: Path, x: int, y: int, w: int, h: int) -> tuple[int, int, int]:
    d = ff("-i", png, "-vf", f"crop={w}:{h}:{x}:{y},scale=1:1:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-")
    return d[0], d[1], d[2]


def proximo(cor, alvo, tol=28) -> bool:
    return all(abs(a - b) <= tol for a, b in zip(cor, alvo))


def hex_rgb(h: str) -> tuple[int, int, int]:
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def pixel(rgb: bytes, x: int, y: int) -> tuple[int, int, int]:
    i = ((y // E) * (L // E) + (x // E)) * 3
    return rgb[i], rgb[i + 1], rgb[i + 2]


def brancos(rgb: bytes, y0: int, y1: int, x0: int = 0, x1: int = L, minimo: int = 215) -> int:
    """Pixels quase brancos (texto claro) na faixa, em coordenadas do quadro cheio."""
    n = 0
    for y in range(y0 // E, min(y1, A) // E):
        base = y * (L // E) * 3
        for x in range(x0 // E, x1 // E):
            i = base + x * 3
            if min(rgb[i], rgb[i + 1], rgb[i + 2]) >= minimo:
                n += 1
    return n


def contagem_cor(rgb: bytes, alvo, y0: int, y1: int, tol=18) -> int:
    n = 0
    for y in range(y0 // E, y1 // E):
        for x in range(L // E):
            i = (y * (L // E) + x) * 3
            if all(abs(rgb[i + k] - alvo[k]) <= tol for k in range(3)):
                n += 1
    return n


def caixa(rgb: bytes, y0: int, y1: int, teste) -> tuple[int, int, int, int] | None:
    xs, ys = [], []
    for y in range(y0 // E, y1 // E):
        for x in range(L // E):
            i = (y * (L // E) + x) * 3
            if teste(rgb[i], rgb[i + 1], rgb[i + 2]):
                xs.append(x)
                ys.append(y)
    return (min(xs) * E, min(ys) * E, (max(xs) + 1) * E, (max(ys) + 1) * E) if xs else None


def contar(rgb: bytes, x0: int, y0: int, x1: int, y1: int, teste) -> int:
    """Pixels que passam no teste dentro do retangulo (coordenadas do quadro cheio)."""
    n = 0
    for y in range(y0 // E, y1 // E):
        for x in range(x0 // E, x1 // E):
            i = (y * (L // E) + x) * 3
            if teste(rgb[i], rgb[i + 1], rgb[i + 2]):
                n += 1
    return n


def cinza_pequeno(png: Path) -> bytes:
    return ff("-i", png, "-vf", "scale=54:96:flags=area", "-f", "rawvideo", "-pix_fmt", "gray", "-")


def dif(a: bytes, b: bytes) -> float:
    return sum(abs(x - y) for x, y in zip(a, b)) / max(1, len(a))


def regiao_cinza(png: Path, x: int, y: int, w: int, h: int, lado=64) -> bytes:
    return ff("-i", png, "-vf", f"crop={w}:{h}:{x}:{y},scale={lado}:{lado}:flags=area", "-f", "rawvideo", "-pix_fmt", "gray", "-")


def goertzel(x, f, sr):
    k = 2 * math.cos(2 * math.pi * f / sr)
    s1 = s2 = 0.0
    for v in x:
        s0 = v + k * s1 - s2
        s1, s2 = s0, s1
    return (s1 * s1 + s2 * s2 - k * s1 * s2) / (len(x) ** 2)


# ----------------------------------------------------------------------------------------------------- verificacoes

def verificar_formatos(p: Projeto) -> dict[str, Path]:
    destaque, apoio = hex_rgb("3DDC97"), hex_rgb("7C8CFF")
    ficha: dict[str, Path] = {}

    # 01 Tela Dividida
    t1, t2 = p.quadro("TelaDividida", 40), p.quadro("TelaDividida", 130)
    ficha["TelaDividida"] = t2
    ok(proximo(cor_media(t1, 100, 120, 880, 600), hex_rgb("ED8936")) and proximo(cor_media(t2, 100, 120, 880, 600), hex_rgb("319795")),
       "Tela Dividida: a area de cima troca de conteudo (laranja em 1,3 s, azul-petroleo em 4,3 s)")
    ok(proximo(cor_media(t2, 40, 1500, 160, 300), hex_rgb("2B6CB0"), 40), "Tela Dividida: a pessoa fica na area de baixo")
    ok(proximo(cor_media(t2, 0, 954, 60, 12), destaque, 40), "Tela Dividida: a divisoria (cor de destaque) esta em y = 960")

    # 15 Cinema
    c = p.quadro("Cinema", 60)
    ficha["Cinema"] = c
    rgb = reduzido(c)
    jan = caixa(rgb, 470, 1800, lambda r, g, b: max(r, g, b) > 24 and max(r, g, b) - min(r, g, b) > 30)  # so a janela (colorida); o titulo e branco
    ok(jan and abs((jan[2] - jan[0]) - 984) <= 12 and abs((jan[3] - jan[1]) - 984) <= 12, f"Cinema: a janela e quadrada, ~984 x 984 (medi {jan and (jan[2] - jan[0], jan[3] - jan[1])})")
    ok(jan and abs(jan[0] - 48) <= 12 and jan[1] >= 480, "Cinema: a janela esta centrada, com ~48 px de margem, e comeca abaixo do titulo")
    ok(proximo(cor_media(c, 0, 520, 36, 400), (0, 0, 0), 10) and proximo(cor_media(c, 0, 1560, 1080, 340), (0, 0, 0), 10), "Cinema: o fundo e preto (laterais e base)")
    ok(brancos(rgb, 270, 520) > 150, "Cinema: o titulo esta no topo, em branco")

    # 08 React: pausa, retomada e ampliacao
    r62, r100, r105, r40, r55 = (p.quadro("React", n) for n in (62, 100, 105, 40, 55))
    ficha["React"] = p.quadro("React", 75)
    topo = lambda png: regiao_cinza(png, 0, 580, 760, 260)  # noqa: E731  (abaixo da tarja e do titulo)
    ok(dif(topo(r62), topo(r100)) < 1.0, "React: o conteudo fica PARADO durante a pausa (quadros 62 e 100 iguais)")
    ok(dif(topo(r40), topo(r55)) > 2.0, "React: o conteudo se mexe antes da pausa")
    ok(dif(topo(r105), topo(r62)) < 1.5, "React: depois da pausa o conteudo RETOMA do mesmo ponto (quadro 105 igual ao quadro parado)")
    ok(dif(topo(p.quadro("React", 125)), topo(r105)) > 2.0, "React: depois de retomar, o conteudo volta a se mexer")
    r160, r40d = p.quadro("React", 160), r40
    ok(proximo(cor_media(r160, 300, 1276, 480, 8), destaque, 45) and proximo(cor_media(r40d, 300, 956, 480, 8), destaque, 45),
       "React: a ampliacao cresce a area do conteudo (divisoria em y ~ 1280 e, fora dela, em y ~ 960)")

    # 14 Antes e Depois
    a40, a90, a200 = p.quadro("AntesDepois", 40), p.quadro("AntesDepois", 90), p.quadro("AntesDepois", 200)
    ficha["AntesDepois"] = a90
    vermelho, verde = hex_rgb("9B2C2C"), hex_rgb("2F855A")
    ok(proximo(cor_media(a40, 800, 700, 160, 60), vermelho) and proximo(cor_media(a40, 100, 700, 160, 60), vermelho), "Antes e Depois: antes da revelacao so aparece o ANTES")
    ok(proximo(cor_media(a90, 140, 700, 160, 60), verde) and proximo(cor_media(a90, 800, 700, 160, 60), vermelho), "Antes e Depois: no meio do deslize, o DEPOIS fica a esquerda e o ANTES a direita")
    ok(proximo(cor_media(a200, 800, 700, 160, 60), verde) and proximo(cor_media(a200, 100, 700, 160, 60), verde), "Antes e Depois: depois da revelacao so aparece o DEPOIS")
    ok(min(cor_media(a90, 524, 944, 32, 32)) > 200, "Antes e Depois: o puxador da divisoria esta no meio (50% do deslize)")

    # 13 Chat
    h0, h90, h210 = p.quadro("Chat", 9), p.quadro("Chat", 90), p.quadro("Chat", 210)
    ficha["Chat"] = p.quadro("Chat", 200)
    n = lambda png: contagem_cor(reduzido(png), apoio, 430, 1240, 14)  # noqa: E731
    ok(n(h0) == 0 and n(h90) > 100 and n(h210) > n(h90), f"Chat: os baloes surgem em sequencia (balao enviado: 0 -> {n(h90)} -> {n(h210)} pixels)")
    ok(contagem_cor(reduzido(h0), hex_rgb("222B37"), 470, 1240, 6) == 0, "Chat: antes da primeira mensagem a conversa esta vazia")

    # 13 Chat: a faixa do contato tem a largura da conversa (x de 90 a 960) e cantos arredondados
    cab = hex_rgb("161D27")
    ok(proximo(cor_media(h90, 600, 300, 100, 20), cab, 3) and proximo(cor_media(h90, 880, 300, 60, 20), cab, 3), "Chat: a faixa do contato aparece no topo da conversa")
    ok(not proximo(cor_media(h90, 20, 300, 50, 20), cab, 3) and not proximo(cor_media(h90, 975, 300, 50, 20), cab, 3), "Chat: a faixa do contato tem a mesma largura da conversa, sem encostar nas bordas da tela")
    ok(not proximo(cor_media(h90, 90, 270, 6, 6), cab, 3), "Chat: os cantos da faixa do contato sao arredondados")

    # 07 Depoimento: zoom e insert de prova
    d40, d60, d120 = p.quadro("Depoimento", 40), p.quadro("Depoimento", 60), p.quadro("Depoimento", 120)
    ficha["Depoimento"] = d40
    pele = lambda r, g, b: abs(r - 224) < 34 and abs(g - 172) < 34 and abs(b - 130) < 34  # noqa: E731
    c40, c60 = caixa(reduzido(d40), 520, 1050, pele), caixa(reduzido(d60), 520, 1050, pele)
    razao = (c60[2] - c60[0]) / max(1, c40[2] - c40[0]) if c40 and c60 else 0
    ok(1.06 <= razao <= 1.17, f"Depoimento: o zoom pontual aumenta a cabeca em ~1,11 vezes (medi {razao:.2f})")
    ok(proximo(cor_media(d120, 120, 460, 840, 440), hex_rgb("D69E2E"), 30), "Depoimento: o insert de prova aparece em 3 a 5 s, abaixo da tarja de identificacao")


    # 03 Post de Rede Social
    ps = p.quadro("PostSocial", 40)
    ficha["PostSocial"] = ps
    rgb_ps = reduzido(ps)
    branco = lambda r, g, b: min(r, g, b) >= 245  # noqa: E731
    cartao = caixa(rgb_ps, 0, 900, branco)  # o cartao fica acima de y = 900
    ok(cartao and cartao[0] == 0 and cartao[1] == 0 and 540 <= cartao[3] <= 760, f"Post de Rede Social: o cartao branco comeca no topo e termina em y ~ 560 a 760 (medi {cartao and cartao[3]})")
    ok(proximo(cor_media(ps, 20, 800, 60, 100), hex_rgb("2B6CB0"), 40) and proximo(cor_media(ps, 1000, 800, 60, 100), hex_rgb("6B46C1"), 40) and max(cor_media(ps, 537, 800, 6, 100)) < 40,
       "Post de Rede Social: as duas midias ficam lado a lado, separadas por uma linha preta")
    ok(contar(rgb_ps, 90, 400, 960, 700, lambda r, g, b: max(r, g, b) < 80) > 30, "Post de Rede Social: o texto do post esta escrito no cartao")
    ok(contagem_cor(rgb_ps, (255, 212, 0), 270, 420, 40) > 25, "Post de Rede Social: o exemplo usa a marca pronta da Choquei no avatar")
    escuro_props = p.tmp / "props_post_escuro.json"
    escuro_props.write_text(json.dumps({"fundoCartao": "escuro"}), encoding="utf-8")
    ps_escuro = p.quadro("PostSocial", 40, nome="PostSocial_escuro.png", props=escuro_props)

    # 04 Noticia: a caixa branca entra primeiro e o texto termina meio segundo depois
    n12, n19, n25, n45, n70 = (p.quadro("Noticia", n) for n in (12, 19, 25, 45, 70))
    ficha["Noticia"] = n70
    r12, r19, r25, r45, r70 = (reduzido(x) for x in (n12, n19, n25, n45, n70))
    branco_n = lambda r, g, b: min(r, g, b) >= 240  # noqa: E731
    tinta = lambda r, g, b: max(r, g, b) < 50  # noqa: E731
    final = caixa(r45, 880, 1250, branco_n)
    ok(caixa(r12, 880, 1250, branco_n) is None, "Noticia: antes da hora da manchete nao aparece nenhuma caixa")
    ok(caixa(r19, 880, 1250, branco_n) is not None, "Noticia: a caixa branca ja esta entrando aos 0,63 s")
    ok(final and 88 <= final[0] and final[2] <= 962 and final[3] <= 1250, f"Noticia: a caixa fica dentro das margens e acima da zona de interface (medi {final})")
    caixa25 = caixa(r25, 880, 1250, branco_n)
    ok(final and caixa25 and abs(caixa25[2] - final[2]) <= 12, "Noticia: aos 0,83 s a caixa ja terminou de entrar (mesmo tamanho do final)")
    t19, t25, t45, t70 = (contar(r, *final, tinta) if final else 0 for r in (r19, r25, r45, r70))
    ok(t45 > 200 and t19 < 0.1 * t45, f"Noticia: o texto ainda nao apareceu quando a caixa entra (tinta {t19} contra {t45} no final)")
    ok(t25 < 0.75 * t45, f"Noticia: quando a caixa termina, o texto ainda esta entrando (tinta {t25} contra {t45})")
    ok(t45 >= 0.99 * t70, "Noticia: o texto termina de entrar cerca de 0,5 s depois da caixa (aos 1,5 s ja esta completo)")
    ok(contagem_cor(r12, hex_rgb("D7263D"), 270, 420, 20) > 20, "Noticia: o logotipo da marca aparece no topo, dentro da zona segura")
    logo_props = p.tmp / "props_logo.json"
    logo_props.write_text(json.dumps({"marca": {"nome": "Logo proprio", "cor": "#000000", "logo": f"{PREFIXO}/prova.png"}}), encoding="utf-8")
    com_logo = reduzido(p.quadro("Noticia", 12, nome="Noticia_logo.png", props=logo_props))
    ok(contagem_cor(com_logo, hex_rgb("D69E2E"), 270, 420, 20) > 40 and contagem_cor(com_logo, hex_rgb("D7263D"), 270, 420, 20) == 0, "Noticia: o logo da pessoa (arquivo em public/) substitui o logotipo desenhado")
    logo_post = reduzido(p.quadro("PostSocial", 40, nome="PostSocial_logo.png", props=logo_props))
    ok(contagem_cor(logo_post, hex_rgb("D69E2E"), 270, 420, 20) > 20, "Post de Rede Social: o logo da pessoa (arquivo em public/) vira o avatar")

    # marca pronta: o logo da Choquei (arquivo do kit) vira o avatar, e a fonte condensada carrega de verdade
    choquei_props = p.tmp / "props_choquei.json"
    choquei_props.write_text(json.dumps({"marca": {"nome": "Choquei", "cor": "#FFD400", "logo": "fabrica/marcas/choquei.png"}, "texto": "Texto de teste do post"}), encoding="utf-8")
    ps_choquei = p.quadro("PostSocial", 40, nome="PostSocial_choquei.png", props=choquei_props)
    ok(contagem_cor(reduzido(ps_choquei), (255, 212, 0), 270, 420, 40) > 25, "Post de Rede Social: o logo pronto da Choquei (assets/marcas) aparece como avatar")
    fonte_props = p.tmp / "props_fonte.json"
    fonte_props.write_text(json.dumps({"manchetes": [{"texto": "MMMMMMMMMMMM", "deS": 0.0, "ateS": 4}]}), encoding="utf-8")
    com_barlow = caixa(reduzido(p.quadro("Noticia", 60, nome="Noticia_fonte.png", props=fonte_props)), 880, 1250, branco_n)
    ok(com_barlow and (com_barlow[2] - com_barlow[0]) < 760, f"Fonte: a manchete usa a fonte condensada carregada (12 letras M ocupam {com_barlow and com_barlow[2] - com_barlow[0]} px; uma fonte comum passaria de 760)")

    # zona segura: nenhum texto claro no topo (0 a 270) nem na base (a partir de 1250), nos quadros sem objetos brancos de proposito
    seguros = {"PostSocial": ps_escuro, "Noticia": n70, "TelaDividida": t2, "Cinema": c, "React": p.quadro("React", 75), "AntesDepois": a40, "Chat": h210, "Depoimento": d40}
    for nome, png in seguros.items():
        rgb = reduzido(png)
        ok(brancos(rgb, 0, 270) == 0 and brancos(rgb, 1260, A) == 0 and brancos(rgb, 0, A, 0, 90) == 0 and brancos(rgb, 0, A, 960, L) == 0,
           f"Zona segura ({nome}): nenhum texto claro no topo, na base nem nas laterais")
    return ficha


def verificar_distintos(ficha: dict[str, Path]) -> None:
    ims = {k: cinza_pequeno(v) for k, v in ficha.items()}
    nomes = list(ims)
    difs = [(a, b, dif(ims[a], ims[b])) for i, a in enumerate(nomes) for b in nomes[i + 1:]]
    menor = min(difs, key=lambda t: t[2])
    ok(menor[2] > 12, f"Formatos distintos: a menor diferenca entre dois formatos e {menor[2]:.1f} (entre {menor[0]} e {menor[1]}; exige mais de 12)")


def verificar_determinismo(p: Projeto) -> None:
    for comp, n in (("React", 100), ("Chat", 100)):
        a = p.quadro(comp, n)
        b = p.quadro(comp, n, nome=f"{comp}_{n}_b.png")
        ok(hashlib.sha256(a.read_bytes()).digest() == hashlib.sha256(b.read_bytes()).digest(), f"Determinismo: o quadro {n} de {comp} renderizado duas vezes e identico")


def verificar_emenda(p: Projeto) -> None:
    props = p.tmp / "props_takes.json"
    props.write_text(json.dumps({
        "video": None, "duracaoS": 4, "titulo": None, "identificacao": None, "inserts": [], "zooms": [], "zoomBase": 1,
        "sobreposicaoS": 0.22,
        "takes": [{"src": f"{PREFIXO}/takeA.mp4", "deS": 0, "ateS": 2.1}, {"src": f"{PREFIXO}/takeB.mp4", "deS": 0.17, "ateS": 2.3}],
    }), encoding="utf-8")
    mp4 = p.video("Depoimento", props, "takes.mp4")
    v = ff("-i", mp4, "-vf", "scale=8:6", "-f", "rawvideo", "-pix_fmt", "rgb24", "-")
    centros = [v[i + 84:i + 87] for i in range(0, len(v) - 143, 144)]  # pixel central de cada quadro
    azuis = [i for i, c in enumerate(centros) if c[2] > 150 and c[0] < 110]
    t_video = azuis[0] / 30.0 if azuis else None
    a = ff("-i", mp4, "-vn", "-ac", "1", "-ar", "48000", "-f", "s16le", "-")
    x = struct.unpack(f"<{len(a) // 2}h", a)
    j = 480
    pa = [goertzel(x[i:i + j], 440, 48000) for i in range(0, len(x) - j, j)]
    pb = [goertzel(x[i:i + j], 880, 48000) for i in range(0, len(x) - j, j)]
    t_b = next(i for i, e in enumerate(pb) if e > 0.15 * max(pb)) * 0.01
    t_a_fim = (max(i for i, e in enumerate(pa) if e > 0.15 * max(pa)) + 1) * 0.01
    ok(t_video is not None and abs(t_video - t_b) < 0.08, f"Emenda: a imagem do take novo ({t_video}) e o audio dele ({t_b:.2f}) entram juntos")
    ok(t_b < t_a_fim - 0.03, f"Emenda: o take novo entra ANTES de a voz do anterior acabar (entra em {t_b:.2f} s; a voz anterior acaba em {t_a_fim:.2f} s)")
    ok(t_a_fim - t_b < 0.3, "Emenda: a sobreposicao das vozes e curta (menos de 0,3 s)")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)], capture_output=True, text=True).stdout.strip())
    ok(abs(dur - 4.0) < 0.2, f"Emenda: a duracao ({dur:.2f} s) bate com a soma dos takes menos a sobreposicao (~4,01 s)")


def verificar_musica(p: Projeto) -> None:
    props = p.tmp / "props_cinema.json"
    props.write_text(json.dumps({"duracaoS": 6}), encoding="utf-8")
    mp4 = p.video("Cinema", props, "cinema.mp4")

    def musica(a, b):
        """Energia da trilha (262 Hz); a voz sintetica e de 440 Hz e fica de fora."""
        d = ff("-ss", a, "-t", b - a, "-i", mp4, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-")
        s = struct.unpack(f"<{len(d) // 2}h", d)
        return math.sqrt(goertzel(s, 262, 16000))
    meio, fim = musica(2.0, 3.0), musica(5.75, 6.0)
    ok(meio > 0 and fim < 0.5 * meio, f"Cinema: a trilha toca e desce em fade no fim (energia da trilha no meio {meio:.1f}, nos ultimos 0,25 s {fim:.1f})")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projeto", type=Path)
    ap.add_argument("--rapido", action="store_true", help="nao renderiza os dois videos (emenda e musica)")
    ap.add_argument("--manter", action="store_true", help="nao apaga os quadros renderizados (para olhar quando algo falha)")
    a = ap.parse_args()
    proj = a.projeto.resolve()
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not (proj / "node_modules").is_dir() or not npx or not shutil.which("ffmpeg"):
        print("Precisa de: node_modules no projeto, npx e ffmpeg no PATH.", file=sys.stderr)
        return 2
    tmp = Path(tempfile.mkdtemp(prefix="fabrica_kit_"))
    pub = proj / "public" / PREFIXO
    dest = proj / "src" / PREFIXO
    try:
        shutil.rmtree(pub, ignore_errors=True)
        preparar(proj)
        gerar_entradas(pub)
        r = rodar([npx, "tsc", "--noEmit", "-p", "."], proj)
        erros = [l for l in (r.stdout + r.stderr).splitlines() if PREFIXO in l and "error" in l]
        ok(not erros, f"tsc: o kit compila sem erros{'' if not erros else ' (' + erros[0] + ')'}")
        r = rodar([npx, "eslint", f"src/{PREFIXO}"], proj)
        if "not found" not in (r.stderr or "").lower() and "no eslint" not in (r.stderr or "").lower() and "Cannot find" not in (r.stderr or ""):
            ok(r.returncode == 0, "eslint: o kit passa no lint" + ("" if r.returncode == 0 else f" ({(r.stdout or r.stderr).strip().splitlines()[-3:]})"))
        p = Projeto(proj, tmp)
        try:
            ficha = verificar_formatos(p)
            verificar_distintos(ficha)
            verificar_determinismo(p)
            if not a.rapido:
                verificar_emenda(p)
                verificar_musica(p)
        except RuntimeError as e:
            ok(False, str(e))
    finally:
        shutil.rmtree(dest, ignore_errors=True)
        shutil.rmtree(pub, ignore_errors=True)
        shutil.rmtree(proj / "public" / "fabrica", ignore_errors=True)
        if a.manter:
            print(f"Quadros mantidos em {tmp}")
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    falhas = [t for c, t in resultados if not c]
    print(f"\n{len(resultados) - len(falhas)} de {len(resultados)} verificacoes passaram.")
    return 1 if falhas else 0


if __name__ == "__main__":
    raise SystemExit(main())
