#!/usr/bin/env python3
"""Planeja os cortes de uma gravacao falada: encurta pausas e remove os trechos de erro indicados.

Os instantes de corte vem do VOLUME do audio (nao dos tempos da transcricao, que escorregam 0,2 a 0,5 s).
Cada corte usa a emenda com sobreposicao: o proximo trecho entra colado no comeco da fala e comeca ainda
durante o finalzinho do anterior. Gera cortes.json (para montar.py) e plano_cortes.md (para conferir).

Uso:
  python planejar_cortes.py bruto.mp4 --saida pasta [--estilo curto|aula|suave] [--remover "62.0-71.5,120-131"]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ff  # noqa: E402

JANELA = 0.01   # s por amostra do envelope
FOLGA = 0.025   # s antes do primeiro som do trecho novo (para nao comer a consoante)

# pausa_min: pausas maiores que isso sao encurtadas | pausa_final: pausa que sobra | sobrep_pausa: sobreposicao ao encurtar
# emenda_gap (pode ser negativo = as vozes se sobrepoem) | sobrep_emenda: sobreposicao ao remover um erro
ESTILOS = {
    'aula':  dict(pausa_min=0.55, pausa_final=0.30, sobrep_pausa=0.12, emenda_gap=-0.10, sobrep_emenda=0.22),
    'curto': dict(pausa_min=0.22, pausa_final=0.08, sobrep_pausa=0.12, emenda_gap=-0.10, sobrep_emenda=0.22),
    'suave': dict(pausa_min=0.90, pausa_final=0.55, sobrep_pausa=0.15, emenda_gap=-0.05, sobrep_emenda=0.20),
}


def niveis(env: list[float]) -> tuple[float, float]:
    """(piso de ruido, nivel da fala) em dB: percentis 10 e 90 do volume medido a cada 10 ms."""
    return _ff.percentil(env, 10), _ff.percentil(env, 90)


def limiar_auto(env: list[float]) -> float:
    """Limiar de silencio em dB, entre o piso de ruido e o nivel da fala.

    Parte do piso + 12 dB (ou +40% da distancia ate a fala, se o audio for ruidoso), nunca abaixo de -46 dB (audio muito
    limpo) e nunca acima de (fala - 10 dB). O limite de cima NAO e fixo: numa sala com ruido de fundo alto, um limiar
    fixo baixo demais enxerga o ruido como fala e nenhuma pausa e cortada."""
    piso, fala = niveis(env)
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


def alinhar_remocao(faixas, r0: float, r1: float, tol: float = 1.5):
    """Alinha um trecho a remover aos limites reais da fala: comeca no FIM da fala mais proxima de r0 e
    termina no COMECO da fala mais proxima de r1. Devolve (indice_ultima_mantida, indice_primeira_retomada) ou None."""
    cand_a = [(abs(e - r0), k) for k, (s, e) in enumerate(faixas) if abs(e - r0) <= tol]
    if not cand_a:
        return None
    k = min(cand_a)[1]
    cand_b = [(abs(s - r1), m) for m, (s, e) in enumerate(faixas) if m > k and abs(s - r1) <= tol]
    if not cand_b:
        return None
    m = min(cand_b)[1]
    return k, m


def planejar(duracao: float, faixas, params: dict, remocoes=None, alinhar: bool = True) -> dict:
    """Devolve segmentos (em tempo bruto), removidos, avisos e duracao final."""
    avisos: list[str] = []
    remocoes = remocoes or []
    n = len(faixas)
    if n == 0:
        raise ValueError('Nao encontrei fala no audio (volume abaixo do limiar). Tente --limiar -50.')
    removido = [False] * n          # fala removida por pedido
    emenda_apos = set()             # indices de faixa mantida seguida de uma emenda (erro removido)
    notas_remocao = []
    for r0, r1 in remocoes:
        if r1 <= r0:
            avisos.append(f'Remocao ignorada (fim antes do inicio): {r0}-{r1}')
            continue
        if alinhar:
            ali = alinhar_remocao(faixas, r0, r1)
            if not ali:
                avisos.append(f'Nao consegui alinhar a remocao {r0:.2f}-{r1:.2f} a uma pausa (o erro esta no meio de uma fala '
                              'continua?). Ajuste os tempos ou use --sem-alinhar.')
                continue
            k, m = ali
            for q in range(k + 1, m):
                removido[q] = True
            emenda_apos.add(k)
            notas_remocao.append((r0, r1, faixas[k][1], faixas[m][0]))
        else:
            for q, (s, e) in enumerate(faixas):
                if s >= r0 - 0.05 and e <= r1 + 0.05:
                    removido[q] = True
            ant = [q for q, (s, e) in enumerate(faixas) if e <= r0 + 0.05 and not removido[q]]
            if ant:
                emenda_apos.add(ant[-1])
            notas_remocao.append((r0, r1, r0, r1))

    mantidas = [q for q in range(n) if not removido[q]]
    if not mantidas:
        raise ValueError('As remocoes apagariam toda a fala.')

    # descobrir os cortes entre faixas mantidas consecutivas
    cortes = []   # (idx_faixa_a, idx_faixa_b, tipo)
    for a, b in zip(mantidas, mantidas[1:]):
        gap = faixas[b][0] - faixas[a][1]
        if a in emenda_apos or b - a > 1:
            tipo = 'emenda'
        elif gap > params['pausa_min']:
            tipo = 'pausa'
        else:
            continue
        G = params['emenda_gap'] if tipo == 'emenda' else params['pausa_final']
        d = params['sobrep_emenda'] if tipo == 'emenda' else params['sobrep_pausa']
        cauda = max(0.0, G + d - FOLGA)      # quanto do silencio/decaimento do trecho anterior fica
        if tipo == 'pausa' and cauda + FOLGA >= gap:
            continue                         # nada a remover
        cortes.append(dict(a=a, b=b, tipo=tipo, cauda=cauda, d=d, G=G, gap=gap))

    def montar_segmentos(cortes_):
        cut_after = {c['a']: c for c in cortes_}
        segs, ini_faixa = [], mantidas[0]
        for pos, q in enumerate(mantidas):
            c = cut_after.get(q)
            if c is None and pos != len(mantidas) - 1:
                continue
            ini = faixas[ini_faixa][0] - (0.25 if not segs else FOLGA)
            fim = faixas[q][1] + (0.35 if c is None else c['cauda'])
            segs.append(dict(ini=max(0.0, ini), fim=min(duracao, fim), d=c['d'] if c else 0.0,
                             tipo=c['tipo'] if c else None, _cut=c))
            if pos + 1 < len(mantidas):
                ini_faixa = mantidas[pos + 1]
        return segs

    segs = montar_segmentos(cortes)
    # Trecho curto (uma palavra solta entre duas pausas) nao comporta a sobreposicao dos dois lados. Antes de desfazer
    # o corte (o que deixa a pausa original inteira, perceptivel), REDUZ a sobreposicao ate o minimo (D_MIN). So junta
    # com o vizinho se nem assim couber.
    D_MIN, reduzidos, unidos = 0.04, set(), []
    for _ in range(400):
        ajustou = False
        for i, s in enumerate(segs):
            c_dep, c_ant = s['_cut'], (segs[i - 1]['_cut'] if i else None)
            d_max = max(c_dep['d'] if c_dep else 0.0, c_ant['d'] if c_ant else 0.0)
            permitido = (s['fim'] - s['ini'] - 0.06) / 2
            if permitido >= d_max or (c_dep is None and c_ant is None):
                continue
            if permitido >= D_MIN:
                for c in (c_dep, c_ant):
                    if c and c['d'] > permitido:
                        c['d'] = permitido
                        c['cauda'] = max(0.0, c['G'] + permitido - FOLGA)
                        reduzidos.add(id(c))
            else:
                alvo = c_dep or c_ant
                cortes = [c for c in cortes if c is not alvo]
                unidos.append((faixas[alvo['a']][1], alvo['gap']))
            segs = montar_segmentos(cortes)
            ajustou = True
            break
        if not ajustou:
            break
    if reduzidos:
        avisos.append(f'{len(reduzidos)} corte(s) com sobreposicao reduzida em trecho curto (palavra solta entre pausas): a pausa foi cortada '
                      'mesmo assim, com emenda mais curta.')
    for t, g in unidos:
        avisos.append(f'Trecho curtissimo em {_ff.mmss(t)}: nao coube corte ali e a pausa de {g:.2f} s ficou como no original. '
                      'Confira de ouvido; se incomodar, remova esse trecho com --remover.')

    for s in segs:
        s.pop('_cut', None)
        s['ini'], s['fim'], s['d'] = round(s['ini'], 4), round(s['fim'], 4), round(s['d'], 4)
    final = sum(s['fim'] - s['ini'] for s in segs) - sum(s['d'] for s in segs[:-1])

    removidos = []
    for s1, s2 in zip(segs, segs[1:]):
        if s2['ini'] > s1['fim']:
            removidos.append(dict(ini=s1['fim'], fim=s2['ini'], motivo=s1['tipo'] or 'pausa'))
    if segs[0]['ini'] > 0.01:
        removidos.insert(0, dict(ini=0.0, fim=segs[0]['ini'], motivo='inicio'))
    if segs[-1]['fim'] < duracao - 0.01:
        removidos.append(dict(ini=segs[-1]['fim'], fim=duracao, motivo='fim'))
    return dict(segmentos=segs, removidos=removidos, avisos=avisos, duracao_final=round(final, 3),
                remocoes_alinhadas=[dict(pedido=[a, b], alinhado=[round(c, 3), round(d_, 3)]) for a, b, c, d_ in notas_remocao])


def parse_tempo(txt: str) -> float:
    t = txt.strip().replace(',', '.')
    partes = t.split(':')
    total = 0.0
    for p in partes:
        total = total * 60 + float(p)
    return total


def parse_remocoes(txt: str):
    saida = []
    for par in [p for p in txt.split(',') if p.strip()]:
        ini, fim = par.strip().split('-', 1)
        saida.append((parse_tempo(ini), parse_tempo(fim)))
    return saida


def relatorio_md(video: str, duracao: float, thr: float, estilo: str, params: dict, plano: dict) -> str:
    L = [f'# Plano de cortes: {Path(video).name}', '',
         f'- Duracao bruta: {_ff.mmss(duracao)} | duracao final prevista: {_ff.mmss(plano["duracao_final"])} '
         f'(economia de {duracao - plano["duracao_final"]:.0f} s, {100 * (1 - plano["duracao_final"] / duracao):.0f}%)',
         f'- Estilo: {estilo} | limiar de silencio: {thr:.0f} dB | trechos mantidos: {len(plano["segmentos"])}',
         f'- Pausas maiores que {params["pausa_min"]:.2f} s ficam com {params["pausa_final"]:.2f} s; '
         f'emendas com {params["sobrep_emenda"]:.2f} s de sobreposicao.', '']
    if plano['avisos']:
        L += ['## Avisos', ''] + [f'- {a}' for a in plano['avisos']] + ['']
    if plano['remocoes_alinhadas']:
        L += ['## Remocoes pedidas e como foram alinhadas', '',
              '| Pedido (bruto) | Alinhado ao som (bruto) |', '|---|---|']
        for r in plano['remocoes_alinhadas']:
            L.append(f'| {_ff.mmss(r["pedido"][0])} a {_ff.mmss(r["pedido"][1])} | {_ff.mmss(r["alinhado"][0])} a {_ff.mmss(r["alinhado"][1])} |')
        L.append('')
    rem = sorted(plano['removidos'], key=lambda r: r['ini'] - r['fim'])[:15]
    L += ['## Maiores trechos removidos', '', '| Onde (bruto) | Duracao | Motivo |', '|---|---|---|']
    for r in rem:
        L.append(f'| {_ff.mmss(r["ini"])} a {_ff.mmss(r["fim"])} | {r["fim"] - r["ini"]:.2f} s | {r["motivo"]} |')
    return '\n'.join(L) + '\n'


def main() -> int:
    _ff.configurar_saida()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video', type=Path)
    ap.add_argument('--saida', type=Path, required=True, help='pasta onde gravar cortes.json e plano_cortes.md')
    ap.add_argument('--estilo', choices=list(ESTILOS), default='curto')
    ap.add_argument('--remover', default='', help='trechos de erro a remover (tempo bruto), ex.: "62.0-71.5,2:00-2:11"')
    ap.add_argument('--limiar', type=float, help='limiar de silencio em dB (padrao: automatico)')
    ap.add_argument('--sem-alinhar', action='store_true', help='nao alinha --remover as pausas (usa os tempos como estao)')
    ap.add_argument('--pausa-minima', type=float)
    ap.add_argument('--pausa-final', type=float)
    ap.add_argument('--sobreposicao-emenda', type=float)
    ap.add_argument('--emenda-gap', type=float, help='negativo = as vozes se sobrepoem (padrao -0.10)')
    a = ap.parse_args()

    info = _ff.info_basica(a.video)
    if not info['tem_audio']:
        raise SystemExit('Erro: o arquivo nao tem faixa de audio.')
    env = _ff.envelope_db(a.video)
    thr = a.limiar if a.limiar is not None else limiar_auto(env)
    params = dict(ESTILOS[a.estilo])
    for chave, val in (('pausa_min', a.pausa_minima), ('pausa_final', a.pausa_final),
                       ('sobrep_emenda', a.sobreposicao_emenda), ('emenda_gap', a.emenda_gap)):
        if val is not None:
            params[chave] = val
    faixas = faixas_de_fala(env, thr)
    piso, fala = niveis(env)
    plano = planejar(info['duracao'], faixas, params, parse_remocoes(a.remover), alinhar=not a.sem_alinhar)

    cobertura = sum(f1 - f0 for f0, f1 in faixas) / max(1e-9, info['duracao'])
    if info['duracao'] > 15 and cobertura > 0.97:
        plano['avisos'].insert(0, 'O arquivo inteiro foi tratado como fala continua (nenhuma pausa achada): quase sempre e ruido de '
                                  'fundo alto. Tente --limiar com um valor mais alto (ex.: -30) ou confira o audio.')
    if fala - piso < 12.0:
        plano['avisos'].insert(0, f'Audio com muito ruido de fundo (piso {piso:.0f} dB, fala {fala:.0f} dB): a deteccao de pausas fica menos '
                                  'precisa. Confira o resultado de ouvido e, se preciso, ajuste com --limiar.')
    a.saida.mkdir(parents=True, exist_ok=True)
    out = dict(video=str(a.video.resolve()), duracao_bruta=info['duracao'], estilo=a.estilo, limiar_db=round(thr, 1),
               piso_db=round(piso, 1), fala_db=round(fala, 1),
               parametros=params, **plano)
    (a.saida / 'cortes.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    (a.saida / 'plano_cortes.md').write_text(relatorio_md(str(a.video), info['duracao'], thr, a.estilo, params, plano), encoding='utf-8')
    print(f'{len(plano["segmentos"])} trechos | {_ff.mmss(info["duracao"])} -> {_ff.mmss(plano["duracao_final"])} '
          f'| limiar {thr:.0f} dB | cortes.json e plano_cortes.md em {a.saida}')
    for av in plano['avisos']:
        print('AVISO:', av)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
