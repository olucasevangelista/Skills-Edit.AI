#!/usr/bin/env python3
"""Mede um criativo de anuncio em video so com FFmpeg (somente biblioteca padrao). O script MEDE; quem interpreta e o agente.

  python analisar.py analisar criativo.mp4 --saida pasta
      por video, em saida/<nome>/: meta.json (duracao, tamanho, fps, cortes de cena por minuto), scenes.json (instantes
      dos cortes de cena), sons.json (volume e picos de som) e sheets/ (folhas de contato 6x3 com o tempo em cada quadro)
  python analisar.py quadro criativo.mp4 12.5 [--saida quadro.png]
      um quadro em resolucao cheia (para ler texto na tela)
  python analisar.py quadro criativo.mp4 12.5 --rajada 1.5 --fps 10 [--saida pasta]
      uma rajada de quadros em resolucao cheia a partir de 12.5 s
  python analisar.py janela criativo.mp4 --de 0 --ate 3 --fps 8 [--saida pasta]
      folha de contato de uma JANELA de tempo, com o tempo escrito em cada quadro (o gancho: 0 a 3 s a 8 quadros por segundo;
      o final com o CTA: os ultimos segundos)
  python analisar.py mapa criativo.mp4 --transcricao transcricao.json --saida pasta [--janela 1]
      mapa de ritmo (mapa_ritmo.json e mapa_ritmo.md): cortes, palavras, volume e som por janela de tempo, mais um resumo
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ff  # noqa: E402

COLUNAS = 6
FONTES = ['C:/Windows/Fonts/arial.ttf', '/System/Library/Fonts/Helvetica.ttc', '/Library/Fonts/Arial.ttf',
          '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/dejavu/DejaVuSans.ttf']
PAUSA_FALA = 0.4        # s entre duas palavras para contar como pausa
MAX_QUADROS_JANELA = 96
AVISO_CORTES = ('o detector de cortes de cena nao pega zoom nem jump cut leve, e dois planos de brilho parecido podem passar batido: '
                'confira nas folhas')


def nome_seguro(p: Path) -> str:
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', p.stem).strip('_') or 'video'


def cortes_de_cena(video: Path, limiar: float) -> list[float]:
    r = _ff.rodar([_ff.exe('ffmpeg'), '-hide_banner', '-i', str(video), '-an', '-vf', f"select='gt(scene,{limiar})',showinfo",
                   '-f', 'null', '-'], check=False)
    return [round(float(m), 3) for m in re.findall(r'pts_time:([0-9.]+)', r.stderr)]


def lufs_integrado(video: Path) -> tuple[float | None, float | None]:
    r = _ff.rodar([_ff.exe('ffmpeg'), '-hide_banner', '-i', str(video), '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'], check=False)
    resumo = r.stderr[r.stderr.rfind('Summary:'):]
    i = re.search(r'I:\s+(-?[\d.]+) LUFS', resumo)
    pico = re.search(r'Peak:\s+(-?[\d.]+) dBFS', resumo)
    return (float(i.group(1)) if i else None, float(pico.group(1)) if pico else None)


def sons(video: Path, duracao: float) -> dict:
    """Volume geral e transientes (subidas bruscas de volume). Sao PISTAS: o que e voz, musica ou efeito
    quem decide e quem olha o video junto com a transcricao."""
    lufs, pico = lufs_integrado(video)
    env = _ff.envelope_db(video)
    trans, ult = [], -1.0
    for k in range(5, len(env)):
        subida = env[k] - min(env[k - 5:k])
        t = k * 0.01
        if subida >= 15 and env[k] >= -30 and t - ult > 0.25:
            trans.append(dict(t=round(t, 2), nivel_db=round(env[k], 1), subida_db=round(subida, 1)))
            ult = t
    ativos = sum(1 for v in env if v > -50)
    return dict(lufs=lufs, pico_dbfs=pico, tempo_com_som_pct=round(100 * ativos / max(1, len(env)), 1), transientes=trans,
                aviso='transiente = subida brusca de volume: pode ser efeito sonoro, batida de musica ou inicio de fala. '
                      'So vale como efeito se coincidir com um evento visual no mesmo instante.')


def fonte_para_texto() -> str | None:
    for f in FONTES:
        if Path(f).exists():
            return f
    return None


def _folhas(video: Path, de: float, ate: float, fps: float, pasta: Path, linhas: int, nome: str) -> list[str]:
    """Folhas de contato (6 colunas) de uma janela [de, ate] com o tempo ABSOLUTO escrito em cada quadro.
    Cada folha tem `linhas` linhas; os arquivos se chamam <nome>_NN_<inicio>-<fim>.jpg."""
    info = _ff.info_basica(video)
    escala = 'scale=-2:400' if info['altura'] > info['largura'] else 'scale=400:-2'
    f = fonte_para_texto()
    texto = ''
    if f:
        ff = f.replace(':', r'\:')
        texto = (f",drawtext=fontfile='{ff}':text='%{{pts\\:flt\\:{de:g}}}':x=6:y=6:fontsize=22:fontcolor=yellow:borderw=2:bordercolor=black")
    pasta.mkdir(parents=True, exist_ok=True)
    for velha in list(pasta.glob('tmp_*.jpg')) + list(pasta.glob(f'{nome}_*.jpg')):
        velha.unlink()
    _ff.rodar([_ff.exe('ffmpeg'), '-v', 'error', '-y', '-ss', f'{de:.3f}', '-t', f'{ate - de:.3f}', '-i', str(video), '-an',
               '-vf', f'fps={fps:g},{escala}{texto},tile={COLUNAS}x{linhas}', '-q:v', '3', str(pasta / 'tmp_%03d.jpg')])
    por_folha = COLUNAS * linhas / fps
    nomes = []
    for k, arq in enumerate(sorted(pasta.glob('tmp_*.jpg'))):
        t0, t1 = de + k * por_folha, min(ate, de + (k + 1) * por_folha)
        novo = arq.with_name(f'{nome}_{k + 1:02d}_{round(t0, 1):g}-{round(t1, 1):g}.jpg')
        arq.replace(novo)
        nomes.append(novo.name)
    if not f:
        print('  aviso: nenhuma fonte de sistema achada; as folhas saem sem o tempo escrito em cada quadro '
              f'(cada folha cobre {por_folha:g} s, {fps:g} quadro(s) por segundo, da esquerda para a direita e de cima para baixo)')
    return nomes


def analisar(video: Path, saida: Path, limiar: float, com_folhas: bool) -> dict:
    info = _ff.info_basica(video)
    pasta = saida / nome_seguro(video)
    pasta.mkdir(parents=True, exist_ok=True)
    cortes = cortes_de_cena(video, limiar)
    dur = info['duracao']
    meta = dict(arquivo=str(video.resolve()), duracao=round(dur, 2), largura=info['largura'], altura=info['altura'],
                fps=round(info['fps'], 3), formato='vertical' if info['altura'] > info['largura'] else 'horizontal/quadrado',
                cortes_de_cena=len(cortes), cortes_por_minuto=round(len(cortes) / dur * 60, 1) if dur else 0,
                plano_medio_s=round(dur / (len(cortes) + 1), 2) if dur else 0, limiar_cena=limiar, aviso=AVISO_CORTES)
    (pasta / 'meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding='utf-8')
    (pasta / 'scenes.json').write_text(json.dumps(cortes), encoding='utf-8')
    if info['tem_audio']:
        (pasta / 'sons.json').write_text(json.dumps(sons(video, dur), ensure_ascii=False, indent=1), encoding='utf-8')
    nomes = []
    if com_folhas and info['tem_video']:
        fps = 2 if dur <= 60 else 1   # criativo curto: 2 quadros por segundo; longo: 1
        nomes = _folhas(video, 0.0, dur, fps, pasta / 'sheets', 3, 'sheet')
    print(f'{pasta.name}: {dur:.1f} s, {info["largura"]}x{info["altura"]} a {info["fps"]:.0f} fps, '
          f'{len(cortes)} cortes de cena ({meta["cortes_por_minuto"]}/min), {len(nomes)} folha(s) em {pasta}')
    return meta


def quadro(video: Path, t: float, saida: Path | None, rajada: float | None, fps: float) -> None:
    ff = _ff.exe('ffmpeg')
    if rajada:
        pasta = saida or video.with_name(f'{nome_seguro(video)}_rajada_{t:g}')
        pasta.mkdir(parents=True, exist_ok=True)
        _ff.rodar([ff, '-v', 'error', '-y', '-ss', f'{t:.3f}', '-t', f'{rajada:.3f}', '-i', str(video), '-an', '-vf', f'fps={fps:g}',
                   str(pasta / 'f_%03d.png')])
        n = len(list(pasta.glob('f_*.png')))
        print(f'{n} quadros em {pasta} (a cada {1 / fps:.3f} s a partir de {t:g} s)')
        return
    arq = saida or video.with_name(f'{nome_seguro(video)}_{t:g}s.png')
    _ff.rodar([ff, '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', str(video), '-frames:v', '1', str(arq)])
    print(f'quadro de {t:g} s em {arq}')


def janela(video: Path, de: float, ate: float, fps: float, saida: Path | None) -> None:
    info = _ff.info_basica(video)
    if not info['tem_video']:
        raise ValueError('O arquivo nao tem imagem.')
    ate = min(ate, info['duracao'])
    if de < 0 or ate <= de:
        raise ValueError(f'Janela invalida: de {de:g} s ate {ate:g} s (o video tem {info["duracao"]:.2f} s).')
    n = math.ceil((ate - de) * fps)
    if n > MAX_QUADROS_JANELA:
        raise ValueError(f'{n} quadros e demais ({MAX_QUADROS_JANELA} no maximo): reduza a janela ou o --fps.')
    pasta = saida or video.with_name(f'{nome_seguro(video)}_janela_{de:g}-{ate:g}')
    linhas = min(4, math.ceil(n / COLUNAS))
    nomes = _folhas(video, de, ate, fps, pasta, linhas, 'janela')
    print(f'janela de {de:g} a {ate:g} s a {fps:g} quadro(s) por segundo: {n} quadros em {len(nomes)} folha(s) em {pasta}')


# ----------------------------------------------------------------------------------------------- mapa de ritmo

def carregar_palavras(caminho: Path) -> list[dict]:
    """Palavras {word, start, end} do transcricao.json da skill de transcricao (ou de uma lista de palavras).
    Usa start e end, em segundos do trecho transcrito: para o arquivo inteiro, o mesmo que o tempo do video."""
    d = json.loads(Path(caminho).read_text(encoding='utf-8'))
    bruto = d.get('words') if isinstance(d, dict) else d
    if not bruto:
        raise ValueError(f'Sem palavras com tempo em {caminho}: a transcricao precisa ter "words" com start e end.')
    out = []
    for w in bruto:
        txt = str(w.get('word', w.get('text', ''))).strip()
        a, b = w.get('start'), w.get('end')
        if txt and a is not None and b is not None:
            out.append(dict(word=txt, start=float(a), end=float(b)))
    out.sort(key=lambda w: w['start'])
    return out


def limiar_auto(env: list[float]) -> float:
    """Piso de ruido + 12 dB, limitado entre -46 e -38 dB."""
    s = sorted(env)
    piso = s[min(len(s) - 1, max(0, int(round(0.10 * (len(s) - 1)))))]
    return max(-46.0, min(-38.0, piso + 12.0))


def potencia_db(valores: list[float]) -> float | None:
    """Media em potencia (nao em dB) de uma lista de niveis em dB."""
    if not valores:
        return None
    return round(10 * math.log10(sum(10 ** (v / 10) for v in valores) / len(valores)), 1)


def pct_com_som(env: list[float], limiar: float, a: float, b: float) -> float:
    seg = env[int(a * 100):int(b * 100)]
    return round(100 * sum(1 for v in seg if v > limiar) / len(seg), 1) if seg else 0.0


def calcular_mapa(dur: float, cortes: list[float], palavras: list[dict] | None, env: list[float] | None, janela_s: float) -> dict:
    avisos = [AVISO_CORTES]
    thr = limiar_auto(env) if env else None
    if palavras:
        dentro = [w for w in palavras if w['start'] < dur]
        if len(dentro) < len(palavras):
            avisos.append(f'{len(palavras) - len(dentro)} palavra(s) da transcricao comecam depois do fim do video ({dur:.1f} s) e foram '
                          'ignoradas: a transcricao e do mesmo arquivo?')
        palavras = dentro
    if palavras is None:
        avisos.append('sem transcricao: o mapa saiu sem palavras, pausas de fala e trecho falado')
    if env is None:
        avisos.append('o arquivo nao tem audio: o mapa saiu sem volume nem som')
    elif palavras is not None:
        avisos.append('"som" e o quanto da janela tem som acima do limiar (voz, musica ou efeito): com musica continua, o silencio '
                      'nao aparece; as pausas de fala vem da transcricao')

    def n_cortes(a, b):
        return sum(1 for c in cortes if a <= c < b)

    def palavras_em(a, b):
        return [w for w in (palavras or []) if a <= w['start'] < b]

    linhas = []
    for k in range(math.ceil(dur / janela_s)):
        a, b = k * janela_s, min(dur, (k + 1) * janela_s)
        pw = palavras_em(a, b)
        texto = ' '.join(w['word'] for w in pw)
        linhas.append(dict(t0=round(a, 2), t1=round(b, 2), cortes=n_cortes(a, b),
                           palavras=len(pw) if palavras is not None else None,
                           volume_db=potencia_db(env[int(a * 100):int(b * 100)]) if env else None,
                           som_pct=pct_com_som(env, thr, a, b) if env else None,
                           texto=(texto[:80] + ('...' if len(texto) > 80 else '')) if palavras is not None else None))
    marcas = [0.0] + [c for c in cortes if 0 < c < dur] + [dur]
    trechos = [(marcas[i], marcas[i + 1]) for i in range(len(marcas) - 1)]
    de_, ate_ = max(trechos, key=lambda t: t[1] - t[0])
    fim5 = max(0.0, dur - 5.0)
    resumo = dict(duracao_s=round(dur, 2), cortes_de_cena=len(cortes), cortes_por_minuto=round(len(cortes) / dur * 60, 1) if dur else 0,
                  cortes_nos_3_primeiros_s=n_cortes(0, 3), cortes_nos_5_primeiros_s=n_cortes(0, 5),
                  cortes_nos_5_ultimos_s=n_cortes(fim5, dur + 1),
                  maior_trecho_sem_corte=dict(de=round(de_, 2), ate=round(ate_, 2), duracao_s=round(ate_ - de_, 2)))
    pausas = []
    if palavras:
        resumo.update(palavras_total=len(palavras), palavras_por_minuto=round(len(palavras) / dur * 60) if dur else 0,
                      primeira_palavra_s=round(palavras[0]['start'], 2), palavras_nos_3_primeiros_s=len(palavras_em(0, 3)),
                      palavras_nos_5_ultimos_s=len(palavras_em(fim5, dur + 1)))
        for w0, w1 in zip(palavras, palavras[1:]):
            if w1['start'] - w0['end'] > PAUSA_FALA:
                pausas.append(dict(de=round(w0['end'], 2), ate=round(w1['start'], 2), duracao_s=round(w1['start'] - w0['end'], 2)))
        resumo.update(pausas_de_fala=len(pausas), maior_pausa_de_fala_s=max((p['duracao_s'] for p in pausas), default=0.0))
    if env:
        resumo.update(som_pct_total=pct_com_som(env, thr, 0, dur), silencio_do_audio_pct=round(100 - pct_com_som(env, thr, 0, dur), 1),
                      volume_medio_db=dict(primeiros_3_s=potencia_db(env[0:int(min(3, dur) * 100)]),
                                           meio=potencia_db(env[int(min(3, dur) * 100):int(fim5 * 100)]),
                                           ultimos_5_s=potencia_db(env[int(fim5 * 100):])), limiar_som_db=round(thr, 1))
    return dict(janela_s=janela_s, resumo=resumo, pausas_de_fala=pausas, janelas=linhas, avisos=avisos)


def mapa_md(nome: str, m: dict, lufs: float | None, pico: float | None) -> str:
    r = m['resumo']
    L = [f'# Mapa de ritmo: {nome}', '', 'O script mede; a leitura (o que cada trecho faz e onde pode perder gente) e do agente.', '',
         '## Resumo', '', '| Medida | Valor |', '|---|---|',
         f'| Duracao | {r["duracao_s"]} s |',
         f'| Cortes de cena | {r["cortes_de_cena"]} ({r["cortes_por_minuto"]} por minuto) |',
         f'| Cortes nos 3 e nos 5 primeiros segundos | {r["cortes_nos_3_primeiros_s"]} e {r["cortes_nos_5_primeiros_s"]} |',
         f'| Maior trecho sem corte de cena | {r["maior_trecho_sem_corte"]["duracao_s"]} s (de {r["maior_trecho_sem_corte"]["de"]} a {r["maior_trecho_sem_corte"]["ate"]} s) |',
         f'| Cortes nos 5 ultimos segundos (janela do CTA) | {r["cortes_nos_5_ultimos_s"]} |']
    if 'palavras_total' in r:
        L += [f'| Primeira palavra | {r["primeira_palavra_s"]} s |',
              f'| Palavras: total, por minuto | {r["palavras_total"]}, {r["palavras_por_minuto"]} |',
              f'| Palavras nos 3 primeiros e nos 5 ultimos segundos | {r["palavras_nos_3_primeiros_s"]} e {r["palavras_nos_5_ultimos_s"]} |',
              f'| Pausas de fala acima de {PAUSA_FALA:g} s | {r["pausas_de_fala"]} (a maior: {r["maior_pausa_de_fala_s"]} s) |']
    if 'volume_medio_db' in r:
        v = r['volume_medio_db']
        L += [f'| Tempo com som / silencio do audio | {r["som_pct_total"]}% / {r["silencio_do_audio_pct"]}% |',
              f'| Volume integrado, pico | {lufs} LUFS, {pico} dBFS |',
              f'| Volume medio (dB): primeiros 3 s, meio, ultimos 5 s | {v["primeiros_3_s"]}, {v["meio"]}, {v["ultimos_5_s"]} |']
    L += ['', f'## Por janela de {m["janela_s"]:g} s', '', '| t (s) | cortes | palavras | volume (dB) | som (%) | trecho falado | funcao (a preencher) |',
          '|---|---|---|---|---|---|---|']
    for j in m['janelas']:
        L.append(f'| {j["t0"]:g} | {j["cortes"]} | {"" if j["palavras"] is None else j["palavras"]} | '
                 f'{"" if j["volume_db"] is None else j["volume_db"]} | {"" if j["som_pct"] is None else j["som_pct"]} | '
                 f'{(j["texto"] or "").replace("|", "/")} | |')
    if m['pausas_de_fala']:
        L += ['', f'## Pausas de fala acima de {PAUSA_FALA:g} s', '', '| de (s) | ate (s) | duracao (s) |', '|---|---|---|']
        L += [f'| {p["de"]} | {p["ate"]} | {p["duracao_s"]} |' for p in m['pausas_de_fala']]
    L += ['', '## Avisos', ''] + [f'- {a}' for a in m['avisos']]
    return '\n'.join(L) + '\n'


def mapa(video: Path, transcricao: Path | None, saida: Path, janela_s: float | None, limiar: float) -> None:
    info = _ff.info_basica(video)
    if not info['tem_video']:
        raise ValueError('O arquivo nao tem imagem.')
    dur = info['duracao']
    janela_s = janela_s or (1.0 if dur <= 90 else 2.0)
    palavras = carregar_palavras(transcricao) if transcricao else None
    env = _ff.envelope_db(video) if info['tem_audio'] else None
    lufs, pico = lufs_integrado(video) if info['tem_audio'] else (None, None)
    m = calcular_mapa(dur, cortes_de_cena(video, limiar), palavras, env, janela_s)
    pasta = saida / nome_seguro(video)
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / 'mapa_ritmo.json').write_text(json.dumps(dict(arquivo=str(video.resolve()), lufs=lufs, pico_dbfs=pico, **m), ensure_ascii=False, indent=1), encoding='utf-8')
    (pasta / 'mapa_ritmo.md').write_text(mapa_md(video.name, m, lufs, pico), encoding='utf-8')
    r = m['resumo']
    print(f'{video.name}: {dur:.1f} s | {r["cortes_de_cena"]} cortes (3 primeiros s: {r["cortes_nos_3_primeiros_s"]}) | '
          f'maior trecho sem corte {r["maior_trecho_sem_corte"]["duracao_s"]} s'
          + (f' | {r["palavras_total"]} palavras, primeira em {r["primeira_palavra_s"]} s' if 'palavras_total' in r else '')
          + f' | mapa_ritmo.json e mapa_ritmo.md em {pasta}')


def main() -> int:
    _ff.configurar_saida()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    a1 = sub.add_parser('analisar', help='meta, cortes de cena, sons e folhas de contato de cada video')
    a1.add_argument('videos', nargs='+', type=Path)
    a1.add_argument('--saida', type=Path, required=True)
    a1.add_argument('--limiar-cena', type=float, default=0.3, help='sensibilidade do corte de cena (0 a 1; padrao 0.3)')
    a1.add_argument('--sem-folhas', action='store_true')
    a2 = sub.add_parser('quadro', help='um quadro (ou uma rajada) em resolucao cheia')
    a2.add_argument('video', type=Path)
    a2.add_argument('t', type=float, help='segundo do video')
    a2.add_argument('--saida', type=Path, help='arquivo .png (quadro) ou pasta (rajada)')
    a2.add_argument('--rajada', type=float, help='duracao da rajada em segundos')
    a2.add_argument('--fps', type=float, default=10.0, help='quadros por segundo da rajada (padrao 10)')
    a3 = sub.add_parser('janela', help='folha de contato de uma janela de tempo')
    a3.add_argument('video', type=Path)
    a3.add_argument('--de', type=float, required=True, help='inicio da janela, em segundos')
    a3.add_argument('--ate', type=float, required=True, help='fim da janela, em segundos')
    a3.add_argument('--fps', type=float, default=8.0, help='quadros por segundo (padrao 8)')
    a3.add_argument('--saida', type=Path, help='pasta (padrao: ao lado do video)')
    a4 = sub.add_parser('mapa', help='mapa de ritmo: cortes, palavras, volume e som por janela de tempo')
    a4.add_argument('video', type=Path)
    a4.add_argument('--transcricao', type=Path, help='transcricao.json da skill de transcricao (sem ela, o mapa sai sem palavras)')
    a4.add_argument('--saida', type=Path, required=True)
    a4.add_argument('--janela', type=float, help='tamanho da janela em segundos (padrao 1; 2 em videos de mais de 90 s)')
    a4.add_argument('--limiar-cena', type=float, default=0.3)
    a = ap.parse_args()
    if a.cmd == 'analisar':
        for v in a.videos:
            analisar(v, a.saida, a.limiar_cena, not a.sem_folhas)
    elif a.cmd == 'quadro':
        quadro(a.video, a.t, a.saida, a.rajada, a.fps)
    elif a.cmd == 'janela':
        janela(a.video, a.de, a.ate, a.fps, a.saida)
    else:
        mapa(a.video, a.transcricao, a.saida, a.janela, a.limiar_cena)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
