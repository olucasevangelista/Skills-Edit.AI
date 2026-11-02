#!/usr/bin/env python3
"""Instala o kit Remotion da Fábrica de Criativos num projeto Remotion (so biblioteca padrao).

Uso:
  python instalar_kit.py <pasta do projeto Remotion>

Copia o codigo do kit para <projeto>/src/fabrica/ e as fontes e marcas (logos) para <projeto>/public/fabrica/.
Nao sobrescreve nada que voce ja tenha editado sem avisar: se src/fabrica ou public/fabrica ja existirem, use --atualizar.
Depois e so renderizar, por exemplo:
  npx remotion still src/fabrica/index.ts Noticia out/teste.png --frame=60 --props=props.json
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1] / 'kit'
PRECISA = ['remotion', '@remotion/cli', '@remotion/media', 'react']


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('projeto', type=Path)
    ap.add_argument('--atualizar', action='store_true', help='substitui src/fabrica e public/fabrica se ja existirem')
    a = ap.parse_args()
    proj = a.projeto.resolve()
    pkg = proj / 'package.json'
    if not pkg.exists():
        print(f'Nao achei {pkg}: aponte para a pasta de um projeto Remotion.', file=sys.stderr)
        return 1
    deps = {**json.loads(pkg.read_text(encoding='utf-8')).get('dependencies', {}), **json.loads(pkg.read_text(encoding='utf-8')).get('devDependencies', {})}
    faltam = [d for d in PRECISA if d not in deps]
    codigo, assets = proj / 'src' / 'fabrica', proj / 'public' / 'fabrica'
    if (codigo.exists() or assets.exists()) and not a.atualizar:
        print('src/fabrica ou public/fabrica ja existem. Rode de novo com --atualizar para substituir.', file=sys.stderr)
        return 1
    for destino in (codigo, assets):
        shutil.rmtree(destino, ignore_errors=True)
    shutil.copytree(KIT, codigo, ignore=shutil.ignore_patterns('README.md', 'assets'))
    shutil.copytree(KIT / 'assets', assets)
    print(f'Kit copiado para {codigo}')
    print(f'Fontes e marcas copiadas para {assets}')
    if faltam:
        print(f'\nFalta instalar no projeto: npm install {" ".join(faltam)}')
    print('\nProximo passo: veja kit/README.md (props de cada formato) e kit/exemplo/props.ts.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
