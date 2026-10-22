#!/usr/bin/env python3
"""Verifica o kit TypeScript contra um projeto Remotion real (somente biblioteca padrão; precisa de Node, ffmpeg e do projeto).

  python verificar_kit.py <pasta do projeto Remotion, com node_modules> [--sem-3d]

O projeto precisa ter instalado: remotion, @remotion/cli, react, typescript (e, para o teste 3D, three,
@react-three/fiber e @remotion/three). O script copia o kit para src/_kit_teste/, confere e apaga a cópia.
Confere: tipos (tsc), render dos quadros do exemplo, determinismo (mesmo quadro duas vezes dá o mesmo arquivo),
zona segura do texto e, no 3D, que a câmera segue as chaves e que shiftPx positivo SOBE o assunto.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
KIT = RAIZ / "kit"
FIXTURE_3D = Path(__file__).resolve().parent / "fixtures" / "cena3d"
L, A = 1080, 1920
resultados: list[tuple[bool, str]] = []


def ok(cond: bool, texto: str) -> None:
    resultados.append((bool(cond), texto))
    print(("OK    " if cond else "FALHOU"), texto, flush=True)


def rodar(args: list[str], cwd: Path, check=False) -> subprocess.CompletedProcess:
    r = subprocess.run(args, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode:
        raise RuntimeError(f"{' '.join(args)} falhou:\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}")
    return r


def still(npx: str, proj: Path, entrada: str, comp: str, quadro: int, saida: Path, gl: bool = False) -> bool:
    args = [npx, "remotion", "still", entrada, comp, str(saida), f"--frame={quadro}", "--log=error"]
    if gl:
        args.append("--gl=angle")
    rodar(args, proj)
    return saida.exists() and saida.stat().st_size > 1000


def pixels(png: Path) -> bytes:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(png), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    if len(r.stdout) != L * A * 3:
        raise RuntimeError(f"{png.name}: esperado {L}x{A}, veio {len(r.stdout) // 3} pixels")
    return r.stdout


def claros(px: bytes, y0: int, y1: int, x0: int = 0, x1: int = L, limiar: int = 170) -> int:
    n = 0
    for y in range(y0, y1, 2):
        base = y * L * 3
        for x in range(x0, x1, 2):
            i = base + x * 3
            if max(px[i], px[i + 1], px[i + 2]) > limiar:
                n += 1
    return n


def caixa_azul(px: bytes):
    ys = []
    for y in range(0, A, 4):
        for x in range(0, L, 4):
            i = (y * L + x) * 3
            r, g, b = px[i], px[i + 1], px[i + 2]
            if b > 150 and b > r + 20 and b > g + 10:
                ys.append(y)
    return (min(ys), max(ys), len(ys)) if ys else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projeto", type=Path)
    ap.add_argument("--sem-3d", action="store_true")
    a = ap.parse_args()
    proj = a.projeto.resolve()
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not (proj / "node_modules").is_dir() or not npx or not shutil.which("ffmpeg"):
        print("Precisa de: node_modules no projeto, npx e ffmpeg no PATH.", file=sys.stderr)
        return 2
    dest = proj / "src" / "_kit_teste"
    tmp = Path(tempfile.mkdtemp(prefix="kit_teste_"))
    shutil.rmtree(dest, ignore_errors=True)
    try:
        dest.mkdir(parents=True)
        shutil.copy(KIT / "movimento.ts", dest / "movimento.ts")
        shutil.copytree(KIT / "exemplo", dest / "exemplo")
        tem3d = not a.sem_3d and (proj / "node_modules" / "three").is_dir() and (proj / "node_modules" / "@remotion" / "three").is_dir()
        if tem3d:
            shutil.copy(KIT / "camera3d.tsx", dest / "camera3d.tsx")
            shutil.copytree(FIXTURE_3D, dest / "cena3d")
        elif not a.sem_3d:
            print("three ou @remotion/three não instalados: pulando o teste 3D.")

        r = rodar([npx, "tsc", "--noEmit", "-p", "."], proj)
        erros = [l for l in (r.stdout + r.stderr).splitlines() if "_kit_teste" in l and "error" in l]
        ok(not erros, f"tsc: o kit compila sem erros{'' if not erros else ' (' + erros[0] + ')'}")

        entrada = "src/_kit_teste/exemplo/index.ts"
        quadros = {20: "gancho", 120: "processo etapa 1", 200: "processo etapa 3", 260: "pacote saindo", 330: "fecho"}
        px = {}
        for q, nome in quadros.items():
            f = tmp / f"ex_{q}.png"
            if not ok_still(npx, proj, entrada, "Exemplo", q, f):
                continue
            px[q] = pixels(f)
        ok(len(px) == len(quadros), f"render: {len(px)} de {len(quadros)} quadros do exemplo foram gerados")
        for q in (20, 200):
            if q in px:
                again = tmp / f"ex_{q}_b.png"
                still(npx, proj, entrada, "Exemplo", q, again)
                same = again.exists() and hashlib.sha256(pixels(again)).digest() == hashlib.sha256(px[q]).digest()
                ok(same, f"determinismo: o quadro {q} renderizado duas vezes é idêntico")
        for q, nome in quadros.items():
            if q not in px:
                continue
            topo, laterais = claros(px[q], 0, 270), claros(px[q], 0, A, 0, 90) + claros(px[q], 0, A, 990, L)
            base = claros(px[q], 1560, A)
            if q == 260:   # o pacote sai de cena pela base de propósito
                ok(topo == 0 and laterais == 0, f"zona segura (quadro {q}, {nome}): topo e laterais livres (a base pode ser cruzada por um objeto que sai)")
            else:
                ok(topo == 0 and base == 0 and laterais == 0, f"zona segura (quadro {q}, {nome}): nada claro no topo, na base e nas laterais")

        if tem3d:
            p0, p45 = tmp / "c3d_0.png", tmp / "c3d_45.png"
            e3 = "src/_kit_teste/cena3d/index.ts"
            if still(npx, proj, e3, "Cena3D", 0, p0, gl=True) and still(npx, proj, e3, "Cena3D", 45, p45, gl=True):
                c0, c45 = caixa_azul(pixels(p0)), caixa_azul(pixels(p45))
                ok(bool(c0 and c45 and c0[2] > 200 and c45[2] > c0[2] * 5), "3D: o objeto aparece e fica bem maior quando a câmera se aproxima (chaves seguidas)")
                if c0:
                    centro = (c0[0] + c0[1]) / 2
                    ok(centro < A / 2 - 60, f"3D: shiftPx=110 sobe o assunto (centro em y={centro:.0f}, o centro da tela é {A // 2})")
            else:
                ok(False, "3D: não consegui renderizar os quadros (GL indisponível nesta máquina?)")
    finally:
        shutil.rmtree(dest, ignore_errors=True)
        shutil.rmtree(tmp, ignore_errors=True)
    falhas = [t for c, t in resultados if not c]
    print(f"\n{len(resultados) - len(falhas)} de {len(resultados)} verificações passaram.")
    return 1 if falhas else 0


def ok_still(npx, proj, entrada, comp, q, f) -> bool:
    good = still(npx, proj, entrada, comp, q, f)
    if not good:
        ok(False, f"render: o quadro {q} do exemplo não foi gerado")
    return good


if __name__ == "__main__":
    raise SystemExit(main())
