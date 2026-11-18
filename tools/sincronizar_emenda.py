#!/usr/bin/env python3
"""Mantem uma unica fonte para a regra da emenda por sobreposicao.

Cada skill e instalada sozinha (`npx skills add ... --skill NOME`), entao nao pode depender de um arquivo de outra
skill: cada uma carrega a sua copia. A fonte e `tools/emenda.md`; este script copia para as skills e confere se
alguma copia ficou diferente.

Uso:
  python tools/sincronizar_emenda.py           copia a fonte para todas as skills
  python tools/sincronizar_emenda.py --check   so confere (codigo de saida 1 se alguma copia divergir)
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / 'tools' / 'emenda.md'
DESTINOS = [
    'skills/editar-reels/references/emenda.md',
    'skills/editar-youtube/references/emenda.md',
    'skills/editar-aula/references/emenda.md',
    'skills/creative-lab/references/emenda.md',
    'skills/fabrica-de-criativos/references/base/emenda.md',
    'skills/smart-cuts/references/emenda.md',
]


def main() -> int:
    conferir = '--check' in sys.argv[1:]
    texto = FONTE.read_text(encoding='utf-8')
    divergentes = 0
    for rel in DESTINOS:
        destino = RAIZ / rel
        atual = destino.read_text(encoding='utf-8') if destino.exists() else None
        if atual == texto:
            print(f'igual      {rel}')
            continue
        divergentes += 1
        if conferir:
            print(f'DIVERGE    {rel}' if atual is not None else f'FALTA      {rel}')
        else:
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(texto, encoding='utf-8', newline='\n')
            print(f'atualizado {rel}')
    if conferir and divergentes:
        print(f'{divergentes} copia(s) diferente(s) da fonte: rode sem --check para sincronizar.')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
