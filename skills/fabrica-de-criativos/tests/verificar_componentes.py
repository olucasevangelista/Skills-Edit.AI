#!/usr/bin/env python3
"""Verifica os componentes de apoio em assets/componentes contra um projeto Remotion real (so biblioteca padrao;
precisa de Node, ffmpeg e do projeto com node_modules).

  python verificar_componentes.py <pasta do projeto Remotion> [--manter]

O projeto precisa ter: remotion, @remotion/cli, @remotion/media, react e typescript.
Copia os componentes para src/_comp_teste/, cria entradas sinteticas em public/_comp_teste/, confere e APAGA as duas pastas.

Confere: compilacao (tsc); CaixaPergunta (no alto, centralizada, texto centralizado, digitada x fixa); MancheteNoticia (a caixa
entra antes do texto, que termina ~0,5 s depois; dentro das margens; o modo deslize); TakesSobrepostos (imagem e audio do take
novo entram juntos, antes de a voz anterior acabar, com sobreposicao curta e a duracao esperada).
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

COMP = Path(__file__).resolve().parents[1] / "assets" / "componentes"
PREFIXO = "_comp_teste"
L, A, E = 1080, 1920, 4
resultados: list[tuple[bool, str]] = []

INDEX = '''import React from "react";
import { AbsoluteFill, Composition, registerRoot } from "remotion";
import { CaixaPergunta } from "./CaixaPergunta";
import { MancheteNoticia } from "./MancheteNoticia";
import { TakesSobrepostos } from "./TakesSobrepostos";
import { EstudioTelejornal, TituloBancada } from "./EstudioTelejornal";

const FUNDO = ({ children }: { children: React.ReactNode }) => <AbsoluteFill style={{ background: "#2B6CB0" }}>{children}</AbsoluteFill>;
const PERGUNTA = "É verdade que dá pra editar criativos com inteligência artificial?";
const PALAVRAS = PERGUNTA.split(" ").map((p, i) => ({ p, s: 0.6 + i * 0.28 }));
const Digitada: React.FC = () => <FUNDO><CaixaPergunta texto={PERGUNTA} modo="digitado" palavras={PALAVRAS} deS={0.2} ateS={5} /></FUNDO>;
const Fixa: React.FC = () => <FUNDO><CaixaPergunta texto={PERGUNTA} modo="fixo" deS={0.2} ateS={5} /></FUNDO>;
const M = [{ texto: "Escreva aqui a manchete verdadeira do seu anúncio", deS: 0.5, ateS: 4 }];
const Revelacao: React.FC = () => <FUNDO><MancheteNoticia manchetes={M} modo="revelacao" fonte="Arial Narrow, Arial, sans-serif" etiqueta="URGENTE" /></FUNDO>;
const Deslize: React.FC = () => <FUNDO><MancheteNoticia manchetes={M} modo="deslize" fonte="Arial Narrow, Arial, sans-serif" /></FUNDO>;
const Estudio: React.FC = () => <AbsoluteFill style={{ background: "#000" }}><EstudioTelejornal /><TituloBancada /></AbsoluteFill>;
const Takes: React.FC = () => (
  <AbsoluteFill style={{ background: "#000" }}>
    <TakesSobrepostos fps={30} sobreposicaoS={0.22} takes={[{ src: "_comp_teste/takeA.mp4", deS: 0, ateS: 2.1 }, { src: "_comp_teste/takeB.mp4", deS: 0.17, ateS: 2.3 }]} />
  </AbsoluteFill>
);

const Raiz: React.FC = () => (
  <>
    <Composition id="Digitada" component={Digitada} width={1080} height={1920} fps={30} durationInFrames={150} />
    <Composition id="Fixa" component={Fixa} width={1080} height={1920} fps={30} durationInFrames={150} />
    <Composition id="Revelacao" component={Revelacao} width={1080} height={1920} fps={30} durationInFrames={150} />
    <Composition id="Deslize" component={Deslize} width={1080} height={1920} fps={30} durationInFrames={150} />
    <Composition id="Estudio" component={Estudio} width={1080} height={1920} fps={30} durationInFrames={150} />
    <Composition id="Takes" component={Takes} width={540} height={960} fps={30} durationInFrames={121} />
  </>
);
registerRoot(Raiz);
'''


def ok(cond, texto: str) -> bool:
    resultados.append((bool(cond), texto))
    print(("OK    " if cond else "FALHOU"), texto, flush=True)
    return bool(cond)


def ff(*args) -> bytes:
    return subprocess.run(["ffmpeg", "-v", "error", *map(str, args)], capture_output=True).stdout


def rodar(args, cwd: Path):
    return subprocess.run([str(x) for x in args], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace")


def reduzido(png: Path) -> bytes:
    return ff("-i", png, "-vf", f"scale={L // E}:{A // E}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-")


def caixa(rgb: bytes, y0: int, y1: int, teste):
    xs, ys = [], []
    for y in range(y0 // E, y1 // E):
        for x in range(L // E):
            i = (y * (L // E) + x) * 3
            if teste(rgb[i], rgb[i + 1], rgb[i + 2]):
                xs.append(x)
                ys.append(y)
    return (min(xs) * E, min(ys) * E, (max(xs) + 1) * E, (max(ys) + 1) * E) if xs else None


def contar(rgb: bytes, bb, teste) -> int:
    x0, y0, x1, y1 = bb
    n = 0
    for y in range(y0 // E, y1 // E):
        for x in range(x0 // E, x1 // E):
            i = (y * (L // E) + x) * 3
            if teste(rgb[i], rgb[i + 1], rgb[i + 2]):
                n += 1
    return n


def goertzel(x, f, sr):
    k = 2 * math.cos(2 * math.pi * f / sr)
    s1 = s2 = 0.0
    for v in x:
        s0 = v + k * s1 - s2
        s1, s2 = s0, s1
    return (s1 * s1 + s2 * s2 - k * s1 * s2) / (len(x) ** 2)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projeto", type=Path)
    ap.add_argument("--manter", action="store_true", help="nao apaga os quadros renderizados")
    a = ap.parse_args()
    proj = a.projeto.resolve()
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not (proj / "node_modules").is_dir() or not npx or not shutil.which("ffmpeg"):
        print("Precisa de: node_modules no projeto, npx e ffmpeg no PATH.", file=sys.stderr)
        return 2
    src, pub = proj / "src" / PREFIXO, proj / "public" / PREFIXO
    tmp = Path(tempfile.mkdtemp(prefix="comp_teste_"))
    try:
        shutil.rmtree(src, ignore_errors=True)
        shutil.rmtree(pub, ignore_errors=True)
        src.mkdir(parents=True)
        pub.mkdir(parents=True)
        for f in COMP.glob("*.tsx"):
            shutil.copy(f, src / f.name)
        (src / "index.tsx").write_text(INDEX, encoding="utf-8")
        for nome, cor, f in (("takeA", "0xC53030", 440), ("takeB", "0x2B50C5", 880)):
            ff("-y", "-f", "lavfi", "-i", f"color=c={cor}:s=540x960:r=30:d=2.6,format=yuv420p",
               "-f", "lavfi", "-i", f"sine=f={f}:d=2.6,volume='if(between(t,0.2,2.0),1,0)':eval=frame", "-c:v", "libx264", "-c:a", "aac", "-shortest", pub / f"{nome}.mp4")
        entrada = f"src/{PREFIXO}/index.tsx"

        r = rodar([npx, "tsc", "--noEmit", "-p", "."], proj)
        erros = [l for l in (r.stdout + r.stderr).splitlines() if PREFIXO in l and "error" in l]
        ok(not erros, f"tsc: os componentes compilam sem erros{'' if not erros else ' (' + erros[0] + ')'}")

        def quadro(comp: str, n: int) -> Path:
            destino = tmp / f"{comp}_{n}.png"
            rodar([npx, "remotion", "still", entrada, comp, destino, f"--frame={n}", "--log=error"], proj)
            if not destino.exists():
                raise RuntimeError(f"nao consegui renderizar {comp} no quadro {n}")
            return destino

        # ---- CaixaPergunta
        escuro = lambda r, g, b: max(r, g, b) < 30  # noqa: E731  (o cabecalho do cartao)
        fixa, digitada_cedo, digitada_fim = (reduzido(quadro(c, n)) for c, n in (("Fixa", 60), ("Digitada", 30), ("Digitada", 100)))
        cab = caixa(fixa, 0, 400, escuro)
        ok(cab and cab[1] <= 260 and cab[1] >= 180, f"CaixaPergunta: o cartao fica no alto (topo do cabecalho em y = {cab and cab[1]}, entre 180 e 260)")
        ok(cab and abs((cab[0] + cab[2]) / 2 - L / 2) <= 12 and abs((cab[2] - cab[0]) - 780) <= 12, f"CaixaPergunta: o cartao esta centralizado na horizontal, com ~780 px (medi {cab and cab[2] - cab[0]})")
        corpo = (cab[0], cab[3], cab[2], cab[3] + 290) if cab else None
        texto = caixa(fixa, corpo[1], corpo[3], lambda r, g, b: max(r, g, b) < 90) if corpo else None
        ok(texto and abs((texto[0] + texto[2]) / 2 - L / 2) <= 60, f"CaixaPergunta: o texto fica centralizado no cartao (centro do texto em x = {texto and (texto[0] + texto[2]) // 2}, o do cartao em 540)")
        ok(cab and caixa(fixa, 0, 800, lambda r, g, b: min(r, g, b) > 240) and caixa(fixa, 0, 800, lambda r, g, b: min(r, g, b) > 240)[3] < 700, "CaixaPergunta: o cartao com o texto completo termina antes de y = 700 (acima de onde ficariam as sobrancelhas num rosto em tela cheia)")
        tinta = lambda rgb: contar(rgb, (0, 330, L, 700), lambda r, g, b: max(r, g, b) < 90)  # noqa: E731
        ok(0 < tinta(digitada_cedo) < tinta(digitada_fim), f"CaixaPergunta digitada: o texto vai aparecendo (tinta {tinta(digitada_cedo)} depois {tinta(digitada_fim)})")
        ok(tinta(fixa) >= 0.9 * tinta(digitada_fim), "CaixaPergunta fixa: o texto ja aparece inteiro")

        # ---- MancheteNoticia
        branco = lambda r, g, b: min(r, g, b) >= 240  # noqa: E731
        tint = lambda r, g, b: max(r, g, b) < 50  # noqa: E731
        r12, r19, r25, r45 = (reduzido(quadro("Revelacao", n)) for n in (12, 19, 25, 45))
        final = caixa(r45, 880, 1250, branco)
        ok(caixa(r12, 880, 1250, branco) is None, "MancheteNoticia: antes da hora nao aparece caixa")
        ok(caixa(r19, 880, 1250, branco) is not None, "MancheteNoticia: a caixa ja esta entrando aos 0,63 s")
        ok(final and final[0] >= 88 and final[2] <= 962 and final[3] <= 1250, f"MancheteNoticia: a caixa fica dentro das margens de seguranca e acima da zona de interface (medi {final})")
        c25 = caixa(r25, 880, 1250, branco)
        ok(final and c25 and abs(c25[2] - final[2]) <= 12, "MancheteNoticia: aos 0,83 s a caixa ja terminou de entrar")
        t19, t25, t45 = (contar(r, final, tint) if final else 0 for r in (r19, r25, r45))
        ok(t45 > 100 and t19 < 0.1 * t45 and t25 < 0.75 * t45, f"MancheteNoticia: o texto entra DEPOIS da caixa (tinta {t19} / {t25} / {t45} aos 0,63 / 0,83 / 1,5 s)")
        d10, d30 = (reduzido(quadro("Deslize", n)) for n in (16, 45))
        ok(caixa(d10, 880, 1250, branco) is None or caixa(d10, 880, 1250, branco)[2] < 500, "MancheteNoticia deslize: no comeco a faixa ainda esta chegando da esquerda")
        f30 = caixa(d30, 880, 1250, branco)
        ok(f30 and f30[0] >= 88 and f30[2] <= 962, "MancheteNoticia deslize: depois do deslize a faixa esta dentro das margens de seguranca")

        # ---- EstudioTelejornal e TituloBancada
        e0, e1 = quadro("Estudio", 30), quadro("Estudio", 100)
        r0, r1 = reduzido(e0), reduzido(e1)
        centro = contar(r0, (440, 200, 640, 260), lambda r, g, b: b > 60 and b > r + 20)
        ok(centro > 100, "EstudioTelejornal: o degrade azul do cenario aparece no alto")
        ok(contar(r0, (0, 1300, L, 1900), lambda r, g, b: max(r, g, b) < 60) > 0.4 * ((L // E) * (600 // E)), "EstudioTelejornal: o degrade escurece para as bordas e a base")
        regiao_globo = (560, 40, 1080, 800)
        dif = sum(abs(a - b) for a, b in zip(ff("-i", e0, "-vf", "crop=520:760:560:40,scale=65:95", "-f", "rawvideo", "-pix_fmt", "gray", "-"), ff("-i", e1, "-vf", "crop=520:760:560:40,scale=65:95", "-f", "rawvideo", "-pix_fmt", "gray", "-"))) / (65 * 95)
        ok(dif > 0.15, f"EstudioTelejornal: os globos e os feixes se mexem com o tempo (diferenca media {dif:.2f} entre 1 s e 3,3 s)")
        placa = contar(r1, (300, 340, 780, 520), lambda r, g, b: r > 150 and g < 60 and b < 70)
        ok(placa > 200, f"TituloBancada: a placa vermelha aparece abaixo da linha cromada (pixels {placa})")
        claro = contar(r1, (300, 270, 780, 350), lambda r, g, b: min(r, g, b) > 170)
        ok(claro > 60, f"TituloBancada: a linha cromada clara aparece no alto (pixels {claro})")

        # ---- TakesSobrepostos
        mp4 = tmp / "takes.mp4"
        rodar([npx, "remotion", "render", entrada, "Takes", mp4, "--codec=h264", "--crf=28", "--pixel-format=yuv420p", "--concurrency=1", "--log=error"], proj)
        v = ff("-i", mp4, "-vf", "scale=8:6", "-f", "rawvideo", "-pix_fmt", "rgb24", "-")
        centros = [v[i + 84:i + 87] for i in range(0, len(v) - 143, 144)]
        azuis = [i for i, c in enumerate(centros) if c[2] > 150 and c[0] < 110]
        t_video = azuis[0] / 30.0 if azuis else None
        au = ff("-i", mp4, "-vn", "-ac", "1", "-ar", "48000", "-f", "s16le", "-")
        x = struct.unpack(f"<{len(au) // 2}h", au)
        j = 480
        pa = [goertzel(x[i:i + j], 440, 48000) for i in range(0, len(x) - j, j)]
        pb = [goertzel(x[i:i + j], 880, 48000) for i in range(0, len(x) - j, j)]
        t_b = next(i for i, e in enumerate(pb) if e > 0.15 * max(pb)) * 0.01
        t_a_fim = (max(i for i, e in enumerate(pa) if e > 0.15 * max(pa)) + 1) * 0.01
        ok(t_video is not None and abs(t_video - t_b) < 0.08, f"TakesSobrepostos: a imagem do take novo ({t_video}) e o audio dele ({t_b:.2f}) entram juntos")
        ok(t_b < t_a_fim - 0.03 and t_a_fim - t_b < 0.3, f"TakesSobrepostos: o take novo entra ANTES de a voz anterior acabar (entra em {t_b:.2f} s; a anterior acaba em {t_a_fim:.2f} s), com sobreposicao curta")
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)], capture_output=True, text=True).stdout.strip())
        ok(abs(dur - 4.0) < 0.2, f"TakesSobrepostos: a duracao ({dur:.2f} s) bate com a soma dos takes menos a sobreposicao (~4,0 s)")
    except RuntimeError as e:
        ok(False, str(e))
    finally:
        shutil.rmtree(src, ignore_errors=True)
        shutil.rmtree(pub, ignore_errors=True)
        if a.manter:
            print(f"Quadros mantidos em {tmp}")
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    falhas = [t for c, t in resultados if not c]
    print(f"\n{len(resultados) - len(falhas)} de {len(resultados)} verificacoes passaram.")
    return 1 if falhas else 0


if __name__ == "__main__":
    raise SystemExit(main())
