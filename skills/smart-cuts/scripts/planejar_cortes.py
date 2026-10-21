#!/usr/bin/env python3
"""Planeja os cortes: transforma os trechos escolhidos (cortes.json) em segmentos do video bruto com emendas.

Os instantes de emenda vem do VOLUME do audio (nao dos tempos da transcricao, que escorregam 0,2 a 0,5 s).
Cada emenda usa a sobreposicao: o trecho seguinte entra colado no comeco da voz, sem respiro, e comeca ainda
durante o finalzinho do anterior, com IMAGEM e AUDIO juntos. A frase anterior termina inteira.

Gera plano_cortes.json (para montar.py) e plano_cortes.md (para conferir o texto de cada corte).

Uso:
  python planejar_cortes.py cortes.json --saida pasta [--estilo curto|aula|suave] [--limiar -42]
"""
from __future__ import annotations

import argparse
import bisect
import json
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ff  # noqa: E402
import _fala  # noqa: E402

FOLGA = 0.025        # s antes do primeiro som do trecho novo (para nao comer a consoante)
FOLGA_INICIO = 0.04  # idem, no comeco do corte

# pausa_min: pausas maiores que isso sao encurtadas | pausa_final: pausa que sobra | sobrep_pausa: sobreposicao ao encurtar
# emenda_gap (negativo = as vozes se sobrepoem) | sobrep_emenda: sobreposicao ao remover trecho | cauda_final: o corte acaba junto da fala
ESTILOS = {
    'curto': dict(pausa_min=0.22, pausa_final=0.08, sobrep_pausa=0.12, emenda_gap=-0.10, sobrep_emenda=0.22, cauda_final=0.12),
    'aula':  dict(pausa_min=0.55, pausa_final=0.30, sobrep_pausa=0.12, emenda_gap=-0.10, sobrep_emenda=0.22, cauda_final=0.15),
    'suave': dict(pausa_min=0.90, pausa_final=0.55, sobrep_pausa=0.15, emenda_gap=-0.05, sobrep_emenda=0.20, cauda_final=0.20),
}


def calcular_tempos(segs: list[dict]) -> tuple[list[float], float]:
    """Inicio de cada segmento no tempo final e duracao total (cada emenda 'come' a sobreposicao d)."""
    T, t = [], 0.0
    for i, s in enumerate(segs):
        T.append(t)
        t += (s['fim'] - s['ini']) - (s['d'] if i < len(segs) - 1 else 0.0)
    return T, t


def contexto_fonte(palavras: list[dict], faixas: list[tuple[float, float]], duracao: float) -> SimpleNamespace:
    c = SimpleNamespace(ws=palavras, faixas=faixas, duracao=duracao, starts=[w['start'] for w in palavras],
                        f_starts=[f[0] for f in faixas], f_ends=[f[1] for f in faixas])
    c.run_of = [run_da_palavra(c, t) for t in c.starts]   # faixa com voz de cada palavra (ou None)
    return c


def palavra_em(c: SimpleNamespace, t: float) -> tuple[int, float]:
    """Indice da palavra cujo INICIO esta mais perto de t, e a distancia (empate: a que termina antes)."""
    i = bisect.bisect_left(c.starts, t)
    cand = [k for k in (i - 1, i) if 0 <= k < len(c.starts)]
    k = min(cand, key=lambda k: (round(abs(c.starts[k] - t), 3), c.ws[k]['end']))
    return k, abs(c.starts[k] - t)


def run_da_palavra(c: SimpleNamespace, t: float, alcance: float = 1.0) -> int | None:
    """Faixa com voz a que uma palavra pertence, a partir do INICIO dela na transcricao (t). O Whisper costuma pôr o
    inicio de uma palavra no fim da anterior (a pausa fica "dentro" dela): se t cai num silencio, a voz da palavra
    e a PROXIMA faixa, nao a mais proxima."""
    if not c.faixas:
        return None
    i = bisect.bisect_right(c.f_starts, t + 0.02) - 1      # ultima faixa que comeca ate t
    if i >= 0 and t <= c.f_ends[i]:
        return i
    j = i + 1
    if j < len(c.faixas) and c.f_starts[j] - t <= alcance:
        return j
    return i if i >= 0 and t - c.f_ends[i] <= alcance else None


def fim_anterior(c: SimpleNamespace, t: float) -> float | None:
    """Fim da ultima faixa com voz que termina antes de t."""
    i = bisect.bisect_left(c.f_ends, t - 1e-6)
    return c.f_ends[i - 1] if i else None


def inicio_seguinte(c: SimpleNamespace, t: float) -> float | None:
    """Inicio da primeira faixa com voz que comeca depois de t."""
    i = bisect.bisect_right(c.f_starts, t + 1e-6)
    return c.f_starts[i] if i < len(c.f_starts) else None


def planejar_corte(corte: dict, ctx: dict[str, SimpleNamespace], params: dict, fonte_padrao: str) -> dict:
    """Um corte: trechos -> pecas com voz -> segmentos do bruto com sobreposicao -> tempos finais e texto."""
    avisos: list[str] = []
    cid = corte['id']
    if not corte.get('trechos'):
        raise ValueError(f'[{cid}] sem "trechos".')

    # 1) pecas: cada trecho vira uma ou mais pecas de voz; pausa longa dentro do trecho divide a peca
    pecas: list[dict] = []
    intencao: dict[str, set[int]] = {}
    for n, t in enumerate(corte['trechos']):
        a, b = float(t[0]), float(t[1])
        fid = str(t[2]) if len(t) > 2 else fonte_padrao
        if fid not in ctx:
            raise ValueError(f'[{cid}] trecho {n}: fonte "{fid}" nao existe em "fontes".')
        c = ctx[fid]
        ia, da = palavra_em(c, a)
        ib, db = palavra_em(c, b)
        if da > 0.15 or db > 0.15:
            avisos.append(f'trecho {n} ({a:.2f}-{b:.2f}): a palavra mais proxima esta a {max(da, db):.2f} s '
                          f'("{c.ws[ia]["word"]}" {c.ws[ia]["start"]:.2f} / "{c.ws[ib]["word"]}" {c.ws[ib]["start"]:.2f}); confira os tempos')
        if ib < ia:
            raise ValueError(f'[{cid}] trecho {n}: o fim ({b}) vem antes do inicio ({a}).')
        intencao.setdefault(fid, set()).update(range(ia, ib + 1))
        k0, k1 = c.run_of[ia], c.run_of[ib]      # o fim se acha pelo INICIO da ultima palavra (o fim dela costuma vir errado)
        if k0 is None or k1 is None or k1 < k0:
            raise ValueError(f'[{cid}] trecho {n}: nao achei voz no audio perto de "{c.ws[ia]["word"]}" ({c.ws[ia]["start"]:.2f}) '
                             f'ou de "{c.ws[ib]["word"]}" ({c.ws[ib]["start"]:.2f}). Confira os tempos ou o limiar (--limiar).')
        proxima = c.starts[ib + 1] if ib + 1 < len(c.starts) else float('inf')
        limite = min(c.ws[ib]['end'], proxima)    # palavra com buraco no meio: segue ate onde ela vai, sem entrar na proxima
        while k1 + 1 < len(c.faixas) and c.f_starts[k1 + 1] < limite - 0.02:
            k1 += 1
        runs = c.faixas[k0:k1 + 1]
        cur = [runs[0][0], runs[0][1]]
        for s, e in runs[1:]:
            if s - cur[1] > params['pausa_min']:
                pecas.append(dict(fonte=fid, ini=cur[0], fim=cur[1], depois='pausa', trecho=n))
                cur = [s, e]
            else:
                cur[1] = e
        pecas.append(dict(fonte=fid, ini=cur[0], fim=cur[1], depois='emenda', trecho=n))
    pecas[-1]['depois'] = None

    # 2) ajustes feitos a mao (instantes do bruto, em silencio que o agente mediu com ler.py --silencio)
    bordas = corte.get('bordas', {})
    if 'inicio' in bordas:
        pecas[0]['ini'] = float(bordas['inicio'])
    if 'fim' in bordas:
        pecas[-1]['fim'] = float(bordas['fim'])
    for k, par in (corte.get('emendas') or {}).items():
        k = int(k)
        if not 0 <= k < len(corte['trechos']) - 1:
            raise ValueError(f'[{cid}] "emendas": a emenda {k} nao existe (um corte com {len(corte["trechos"])} trecho(s) tem '
                             f'{max(0, len(corte["trechos"]) - 1)} emenda(s), de 0 a {max(0, len(corte["trechos"]) - 2)}).')
        ult = max(i for i, p in enumerate(pecas) if p['trecho'] == k)
        pri = min(i for i, p in enumerate(pecas) if p['trecho'] == k + 1)
        pecas[ult]['fim'], pecas[pri]['ini'] = float(par[0]), float(par[1])

    # 3) pausa que nao comporta a sobreposicao: nao corta ali (une as duas pecas)
    i = 0
    while i < len(pecas) - 1:
        p, q = pecas[i], pecas[i + 1]
        if p['depois'] == 'pausa' and q['ini'] - p['fim'] <= params['pausa_final'] + params['sobrep_pausa']:
            p['fim'], p['depois'] = q['fim'], q['depois']
            del pecas[i + 1]
        else:
            i += 1

    # 4) segmentos do bruto: cada peca ganha um respiro minimo antes e uma cauda curta depois
    segs: list[dict] = []
    for i, p in enumerate(pecas):
        c = ctx[p['fonte']]
        ultimo = i == len(pecas) - 1
        folga = FOLGA_INICIO if i == 0 else FOLGA
        pe = fim_anterior(c, p['ini'] - 1e-3)
        if pe is not None:
            folga = min(folga, max(0.0, p['ini'] - pe - 0.01))
        if ultimo:
            d, cauda = 0.0, params['cauda_final']
        elif p['depois'] == 'emenda':
            d = params['sobrep_emenda']
            cauda = max(0.0, params['emenda_gap'] + d - FOLGA)
        else:
            d = params['sobrep_pausa']
            cauda = max(0.0, params['pausa_final'] + d - FOLGA)
        ns = inicio_seguinte(c, p['fim'] + 1e-3)
        if ns is not None:
            cauda = min(cauda, max(0.0, ns - p['fim'] - 0.015))   # a cauda nunca pega o som seguinte
        segs.append(dict(fonte=p['fonte'], ini=max(0.0, p['ini'] - folga), fim=min(c.duracao, p['fim'] + cauda),
                         d=d, tipo=p['depois']))
    for i in range(len(segs) - 1):
        # a sobreposicao nao pode passar da metade do menor dos dois segmentos
        dmax = min(segs[i]['fim'] - segs[i]['ini'], segs[i + 1]['fim'] - segs[i + 1]['ini']) / 2 - 0.03
        if segs[i]['d'] > dmax:
            segs[i]['d'] = max(0.02, dmax)
            avisos.append(f'emenda {i}: trecho muito curto, sobreposicao reduzida para {segs[i]["d"]:.2f} s')
    for s in segs:
        s['ini'], s['fim'], s['d'] = round(s['ini'], 4), round(s['fim'], 4), round(s['d'], 4)
    T, total = calcular_tempos(segs)
    for s, t0 in zip(segs, T):
        s['final_ini'] = round(t0, 4)

    # 5) o que ficou: faixas com voz dentro de cada peca. Cada palavra pertence a uma faixa (run_da_palavra);
    #    palavra na faixa que fica e fora do pedido ENTROU (colada na fala); palavra pedida fora das faixas SAIU
    mantidas: dict[str, dict[int, int]] = {}   # fonte -> {faixa: indice da peca}
    for i, p in enumerate(pecas):
        c = ctx[p['fonte']]
        for r in range(bisect.bisect_right(c.f_ends, p['ini'] + 0.005), len(c.faixas)):
            if c.f_starts[r] >= p['fim'] - 0.005:
                break
            mantidas.setdefault(p['fonte'], {})[r] = i
    ficou: list[tuple[int, str, int]] = []      # (peca, fonte, palavra)
    for fid, c in ctx.items():
        quer, kd = intencao.get(fid, set()), mantidas.get(fid, {})
        if not quer:
            continue
        tem = {k for k, r in enumerate(c.run_of) if r in kd}
        ficou += [(kd[c.run_of[k]], fid, k) for k in tem]
        for k in sorted(tem - quer):
            avisos.append(f'ENTROU "{c.ws[k]["word"]}" @{c.ws[k]["start"]:.2f}: nao estava nos trechos pedidos, mas esta colada na fala que fica '
                          '(sem silencio entre as duas). Mude o trecho para incluir ou excluir de proposito, ou ajuste com "emendas".')
        for k in sorted(quer - tem):
            avisos.append(f'SAIU "{c.ws[k]["word"]}" @{c.ws[k]["start"]:.2f}: estava nos trechos pedidos, mas a voz dela nao esta nas faixas que ficam '
                          '(tempo da transcricao deslocado?). Confira com ler.py --silencio.')

    # 6) texto final e palavras com tempo no corte (estimadas: o inicio da palavra e levado para dentro da sua faixa com voz)
    palavras = []
    for i, fid, k in sorted(ficou):
        c, w, r = ctx[fid], ctx[fid].ws[k], ctx[fid].run_of[k]
        a_ini = min(max(w['start'], c.f_starts[r]), c.f_ends[r])
        a_fim = min(max(w['end'], a_ini + 0.03), max(c.f_ends[r], a_ini + 0.03))
        palavras.append(dict(palavra=w['word'], ini=round(T[i] + a_ini - segs[i]['ini'], 3), fim=round(T[i] + a_fim - segs[i]['ini'], 3)))
    extras = {k: v for k, v in corte.items() if k not in ('id', 'estilo', 'gancho', 'porque', 'trechos', 'bordas', 'emendas')}
    return dict(id=cid, estilo=corte.get('estilo', 'serio'), gancho=corte.get('gancho', ''), porque=corte.get('porque', ''),
                estilo_pausa=params.get('nome', 'curto'), parametros={k: v for k, v in params.items() if k != 'nome'},
                trechos=corte['trechos'], segmentos=segs, duracao_final=round(total, 3),
                texto=' '.join(w['palavra'] for w in palavras), palavras=palavras, avisos=avisos, extras=extras)


def relatorio_md(plano: dict) -> str:
    L = ['# Plano de cortes', '']
    for c in plano['cortes']:
        pr = c['parametros']
        L += [f'## {c["id"]} [{c["estilo"]}] {c["duracao_final"]:.1f} s', '',
              f'Gancho: {c["gancho"] or "(a definir)"}', '',
              f'Pausa: estilo {c["estilo_pausa"]} (pausas maiores que {pr["pausa_min"]:.2f} s ficam com {pr["pausa_final"]:.2f} s) | '
              f'emendas com {pr["sobrep_emenda"]:.2f} s de sobreposicao (imagem e audio do trecho novo entram juntos)', '']
        if c['porque']:
            L += [f'Por que: {c["porque"]}', '']
        L += ['Texto final (confira se faz sentido lendo em voz alta):', '', f'> {c["texto"]}', '']
        cortes_ = [s for s in c['segmentos'][1:]]
        if cortes_:
            L += ['| Tempo final | Tipo | Sobreposicao |', '|---|---|---|']
            for s, ant in zip(cortes_, c['segmentos']):
                L.append(f'| {_ff.mmss(s["final_ini"])} | {ant["tipo"]} | {ant["d"]:.2f} s |')
            L.append('')
        if c['avisos']:
            L += ['Avisos:', ''] + [f'- {a}' for a in c['avisos']] + ['']
    return '\n'.join(L) + '\n'


def resolver(base: Path, p: str) -> Path:
    q = Path(p)
    return q if q.is_absolute() else (base / q).resolve()


def carregar_fontes(spec: dict, base: Path) -> dict[str, dict]:
    if 'fontes' in spec:
        return {str(k): dict(video=resolver(base, v['video']), transcricao=resolver(base, v['transcricao'])) for k, v in spec['fontes'].items()}
    if 'video' in spec and 'transcricao' in spec:
        return {'f1': dict(video=resolver(base, spec['video']), transcricao=resolver(base, spec['transcricao']))}
    raise ValueError('cortes.json precisa de "video" e "transcricao" (ou de "fontes" para mais de um video).')


def main() -> int:
    _ff.configurar_saida()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cortes', type=Path, help='cortes.json (formato em references/plano.md)')
    ap.add_argument('--saida', type=Path, required=True, help='pasta onde gravar plano_cortes.json e plano_cortes.md')
    ap.add_argument('--estilo', choices=list(ESTILOS), default='curto', help='ritmo das pausas (padrao curto)')
    ap.add_argument('--limiar', type=float, help='limiar de silencio em dB (padrao: automatico)')
    ap.add_argument('--pausa-minima', type=float)
    ap.add_argument('--pausa-final', type=float)
    ap.add_argument('--sobreposicao-emenda', type=float)
    ap.add_argument('--emenda-gap', type=float, help='negativo = as vozes se sobrepoem (padrao -0.10)')
    ap.add_argument('--cauda-final', type=float, help='s depois da ultima palavra no fim do corte')
    ap.add_argument('--so', default='', help='planejar so estes ids (separados por virgula)')
    a = ap.parse_args()

    base = a.cortes.resolve().parent
    spec = json.loads(a.cortes.read_text(encoding='utf-8'))
    fontes = carregar_fontes(spec, base)
    params = dict(ESTILOS[a.estilo], nome=a.estilo)
    for chave, val in (('pausa_min', a.pausa_minima), ('pausa_final', a.pausa_final), ('sobrep_emenda', a.sobreposicao_emenda),
                       ('emenda_gap', a.emenda_gap), ('cauda_final', a.cauda_final)):
        if val is not None:
            params[chave] = val

    ctx, limiares = {}, {}
    for fid, f in fontes.items():
        info = _ff.info_basica(f['video'])
        if not info['tem_audio']:
            raise ValueError(f'{f["video"].name} nao tem faixa de audio.')
        print(f'lendo o volume de {f["video"].name}...', flush=True)
        env = _ff.envelope_db(f['video'])
        thr = a.limiar if a.limiar is not None else _fala.limiar_auto(env)
        faixas = _fala.faixas_de_fala(env, thr)
        if not faixas:
            raise ValueError(f'Nao encontrei fala em {f["video"].name} (volume abaixo do limiar). Tente --limiar -50.')
        ctx[fid] = contexto_fonte(_fala.carregar_palavras(f['transcricao']), faixas, info['duracao'])
        limiares[fid] = round(thr, 1)
    fonte_padrao = next(iter(fontes))

    so = {x for x in a.so.split(',') if x}
    cortes = [planejar_corte(c, ctx, params, fonte_padrao) for c in spec['cortes'] if not so or c['id'] in so]
    a.saida.mkdir(parents=True, exist_ok=True)
    arq = a.saida / 'plano_cortes.json'
    todos = {c['id']: c for c in json.loads(arq.read_text(encoding='utf-8'))['cortes']} if so and arq.exists() else {}
    todos.update({c['id']: c for c in cortes})
    ordem = [c['id'] for c in spec['cortes']]
    plano = dict(fontes={k: dict(video=str(v['video']), transcricao=str(v['transcricao'])) for k, v in fontes.items()},
                 limiar_db=limiares, cortes=sorted(todos.values(), key=lambda c: ordem.index(c['id']) if c['id'] in ordem else 999))
    arq.write_text(json.dumps(plano, ensure_ascii=False, indent=1), encoding='utf-8')
    (a.saida / 'plano_cortes.md').write_text(relatorio_md(plano), encoding='utf-8')
    for c in cortes:
        print(f'\n### {c["id"]} [{c["estilo"]}] {c["duracao_final"]:.1f} s | gancho: {c["gancho"]}\n{c["texto"]}')
        for av in c['avisos']:
            print(f'  AVISO [{c["id"]}]: {av}')
    n_av = sum(len(c['avisos']) for c in cortes)
    print(f'\n{len(cortes)} cortes planejados | {n_av} aviso(s) | plano_cortes.json e plano_cortes.md em {a.saida}')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError, KeyError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
