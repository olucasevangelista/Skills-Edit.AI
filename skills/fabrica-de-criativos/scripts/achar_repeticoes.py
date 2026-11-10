#!/usr/bin/env python3
"""Aponta tentativas repetidas (retakes) numa transcricao com tempo por palavra e sugere o que remover.

Quem grava erra e repete a mesma frase varias vezes. Este script le o transcricao.json (palavras com inicio e fim),
separa a fala em takes pelas pausas e marca:
  - takes que COMECAM igual (mesmas primeiras palavras): normalmente sao tentativas da mesma frase;
  - reinicios DENTRO de um take (a pessoa recomeca sem pausa: "a melhor parte e que voce, a melhor parte e que a skill...").
Para cada grupo sugere ficar com a ULTIMA tentativa e remover as anteriores, e imprime o `--remover` para o planejar_cortes.py.

Isto e uma AJUDA, nao uma decisao: ele nao ouve o audio (nao julga entonacao nem fluidez) e o Whisper as vezes junta ou
omite repeticoes. Leia as tentativas e confirme. Frases repetidas de proposito (um refrao) tambem aparecem.

Uso:
  python achar_repeticoes.py transcricao.json [--pausa 0.5] [--palavras 3] [--janela 120] [--json saida.json]
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path


def normalizar(w: str) -> str:
    w = unicodedata.normalize('NFKD', w.lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in w if not unicodedata.combining(c)))


def palavras_da_transcricao(dados: dict) -> list[dict]:
    """[{texto, n, ini, fim}] em segundos do arquivo original (usa source_start/end quando existem)."""
    out = []
    for w in dados.get('words', []):
        n = normalizar(str(w.get('word', '')))
        if not n:
            continue
        ini = float(w.get('source_start', w.get('start')))
        fim = float(w.get('source_end', w.get('end')))
        out.append(dict(texto=str(w['word']).strip(), n=n, ini=ini, fim=fim))
    return out


def separar_takes(palavras: list[dict], pausa: float) -> list[list[dict]]:
    takes: list[list[dict]] = []
    for w in palavras:
        if takes and w['ini'] - takes[-1][-1]['fim'] < pausa:
            takes[-1].append(w)
        else:
            takes.append([w])
    return takes


def igual(a: str, b: str) -> bool:
    # tolera o erro tipico do Whisper (Claude/Cloud): mesma letra inicial e parecidas
    return a == b or (len(a) > 3 and len(b) > 3 and a[0] == b[0] and difflib.SequenceMatcher(None, a, b).ratio() >= 0.72)


def prefixo_comum(a: list[dict], b: list[dict]) -> int:
    k = 0
    for x, y in zip(a, b):
        if igual(x['n'], y['n']):
            k += 1
        else:
            break
    return k


def texto(take: list[dict], limite: int = 110) -> str:
    t = ' '.join(w['texto'] for w in take)
    return t if len(t) <= limite else t[:limite - 1] + '…'


def achar_grupos(takes: list[list[dict]], minimo: int, janela: float) -> list[list[int]]:
    """Grupos de indices de takes que comecam igual. O take de referencia e sempre o mais recente do grupo."""
    grupos: list[list[int]] = []
    usados: set[int] = set()
    for j in range(len(takes) - 1, -1, -1):
        if j in usados:
            continue
        g = [j]
        for i in range(j - 1, -1, -1):
            if takes[j][0]['ini'] - takes[i][-1]['fim'] > janela:
                break
            if i in usados:
                continue
            need = min(minimo, len(takes[i]), len(takes[j]))
            if need >= 2 and prefixo_comum(takes[i], takes[j]) >= need:
                g.append(i)
        if len(g) > 1:
            g.sort()
            usados.update(g)
            grupos.append(g)
    return sorted(grupos)


def reinicios_internos(takes: list[list[dict]], minimo: int, maximo_tentativa: int = 25) -> list[dict]:
    """Recomeco SEM pausa dentro de um take: um trecho de `minimo` palavras reaparece logo adiante ("a melhor parte e que
    voce, a melhor parte e que a skill..."). Exige uma sequencia mais longa que a das tentativas separadas por pausa
    (minimo + 1, pelo menos 4 palavras), porque estruturas paralelas ("a gente vai gravar... a gente vai editar") sao comuns."""
    n_min = max(minimo + 1, 4)
    achados = []
    for k, t in enumerate(takes):
        p = 0
        while p < len(t) - n_min:
            q = next((q for q in range(p + 2, min(len(t) - n_min + 1, p + maximo_tentativa))
                      if prefixo_comum(t[p:p + n_min], t[q:q + n_min]) >= n_min), None)
            if q is None:
                p += 1
                continue
            r0 = t[p - 1]['fim'] if p > 0 else (takes[k - 1][-1]['fim'] if k > 0 else 0.0)
            achados.append(dict(take=k, ini=t[p]['ini'], recomeca_em=t[q]['ini'], remover=[round(r0, 2), round(t[q]['ini'], 2)],
                                antes=texto(t[p:q]), depois=texto(t[q:])))
            p = q
    return achados


def analisar(dados: dict, pausa: float = 0.5, minimo: int = 3, janela: float = 120.0) -> dict:
    palavras = palavras_da_transcricao(dados)
    takes = separar_takes(palavras, pausa)
    grupos = []
    for g in achar_grupos(takes, minimo, janela):
        tent = [dict(take=i, ini=round(takes[i][0]['ini'], 2), fim=round(takes[i][-1]['fim'], 2), palavras=len(takes[i]),
                     texto=texto(takes[i])) for i in g]
        ultimo = g[-1]
        maior = max(t['palavras'] for t in tent)
        avisos = []
        if len(takes[ultimo]) < 0.7 * maior:
            avisos.append(f'A ultima tentativa tem {len(takes[ultimo])} palavras e uma anterior tem {maior}: confira se a ultima nao foi '
                          'interrompida (talvez a melhor seja outra).')
        intermediarios = [i for i in range(g[0] + 1, ultimo) if i not in g]
        if intermediarios:
            avisos.append(f'Ha {len(intermediarios)} take(s) de outro assunto entre as tentativas; a remocao sugerida apaga tudo isso: '
                          'confira.')
        # remover: do fim da fala anterior a primeira tentativa ate o comeco da tentativa escolhida
        r0 = takes[g[0] - 1][-1]['fim'] if g[0] > 0 else 0.0
        r1 = takes[ultimo][0]['ini']
        grupos.append(dict(tentativas=tent, escolhida=ultimo, remover=[round(r0, 2), round(r1, 2)], avisos=avisos))
    internos = reinicios_internos(takes, minimo)
    return dict(takes=len(takes), grupos=grupos, reinicios_internos=internos)


def formatar(res: dict) -> str:
    L = [f'{res["takes"]} takes (separados por pausas).', '']
    if not res['grupos'] and not res['reinicios_internos']:
        L.append('Nenhuma repeticao evidente. Isso NAO garante que nao ha retakes: o Whisper junta e omite repeticoes. '
                 'Transcreva cada trecho mantido sozinho e leia.')
    for n, g in enumerate(res['grupos'], 1):
        L.append(f'## Grupo {n}: {len(g["tentativas"])} tentativas da mesma abertura')
        for k, t in enumerate(g['tentativas']):
            marca = ' <- ultima (sugerida para ficar)' if t['take'] == g['escolhida'] else ''
            L.append(f'- {t["ini"]:.2f}-{t["fim"]:.2f} s | {t["palavras"]} palavras | {t["texto"]}{marca}')
        L.append(f'- sugestao: --remover "{g["remover"][0]}-{g["remover"][1]}"')
        L += [f'- AVISO: {a}' for a in g['avisos']]
        L.append('')
    for r in res['reinicios_internos']:
        L.append(f'## Possivel reinicio sem pausa em {r["ini"]:.2f} s (ou uma repeticao de proposito)')
        L.append(f'- tentativa: {r["antes"]}')
        L.append(f'- recomecou em {r["recomeca_em"]:.2f} s: {r["depois"]}')
        L.append(f'- sugestao: --remover "{r["remover"][0]}-{r["remover"][1]}" (se o erro esta no meio de uma fala continua, use --sem-alinhar)')
        L.append('')
    pedidos = [g['remover'] for g in res['grupos']] + [r['remover'] for r in res['reinicios_internos']]
    if pedidos:
        pedidos.sort()
        L.append('Todos juntos (confirme cada um antes): --remover "' + ','.join(f'{a}-{b}' for a, b in pedidos) + '"')
    return '\n'.join(L) + '\n'


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('transcricao', type=Path, help='transcricao.json (palavras com inicio e fim)')
    ap.add_argument('--pausa', type=float, default=0.5, help='pausa que separa um take do outro, em s (padrao 0.5)')
    ap.add_argument('--palavras', type=int, default=3, help='quantas palavras iniciais iguais indicam repeticao (padrao 3)')
    ap.add_argument('--janela', type=float, default=120.0, help='distancia maxima entre tentativas, em s (padrao 120)')
    ap.add_argument('--json', type=Path, help='grava o resultado em JSON')
    a = ap.parse_args()
    dados = json.loads(a.transcricao.read_text(encoding='utf-8'))
    if not dados.get('words'):
        raise ValueError('A transcricao nao tem tempo por palavra (campo "words").')
    res = analisar(dados, a.pausa, a.palavras, a.janela)
    if a.json:
        a.json.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print(formatar(res))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
