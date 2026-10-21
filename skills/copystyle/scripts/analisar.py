#!/usr/bin/env python3
"""Mede um video de referencia de edicao so com FFmpeg (somente biblioteca padrao).

  python analisar.py analisar ref1.mp4 ref2.mp4 --saida pasta/analise
      por video, em saida/<nome>/: meta.json (duracao, tamanho, fps, cortes por minuto), scenes.json (instantes de
      corte de cena), sons.json (volume e prováveis efeitos sonoros) e sheets/ (folhas de contato 6x3 com o tempo
      em cada quadro)
  python analisar.py quadro ref1.mp4 12.5 [--saida quadro.png]
      um quadro em resolucao cheia (para medir fonte, tamanho e posicao da legenda)
  python analisar.py quadro ref1.mp4 12.5 --rajada 1.5 --fps 10 [--saida pasta]
      uma rajada de quadros em resolucao cheia a partir de 12.5 s (para ver a animacao de uma legenda ou de um insert)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ff  # noqa: E402

COLUNAS, LINHAS = 6, 3
FONTES = ['C:/Windows/Fonts/arial.ttf', '/System/Library/Fonts/Helvetica.ttc', '/Library/Fonts/Arial.ttf',
          '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/dejavu/DejaVuSans.ttf']


def nome_seguro(p: Path) -> str:
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', p.stem).strip('_') or 'video'


def cortes_de_cena(video: Path, limiar: float) -> list[float]:
    r = _ff.rodar([_ff.exe('ffmpeg'), '-hide_banner', '-i', str(video), '-an', '-vf', f"select='gt(scene,{limiar})',showinfo",
                   '-f', 'null', '-'], check=False)
    return [round(float(m), 3) for m in re.findall(r'pts_time:([0-9.]+)', r.stderr)]


def sons(video: Path, duracao: float) -> dict:
    """Volume geral e transientes (picos de volume sem fala parecida). Sao PISTAS: o que e voz, musica ou efeito
    quem decide e quem olha o video junto com a transcricao."""
    r = _ff.rodar([_ff.exe('ffmpeg'), '-hide_banner', '-i', str(video), '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'], check=False)
    resumo = r.stderr[r.stderr.rfind('Summary:'):]
    i = re.search(r'I:\s+(-?[\d.]+) LUFS', resumo)
    pico = re.search(r'Peak:\s+(-?[\d.]+) dBFS', resumo)
    env = _ff.envelope_db(video)
    trans, ult = [], -1.0
    for k in range(5, len(env)):
        subida = env[k] - min(env[k - 5:k])
        t = k * 0.01
        if subida >= 15 and env[k] >= -30 and t - ult > 0.25:
            trans.append(dict(t=round(t, 2), nivel_db=round(env[k], 1), subida_db=round(subida, 1)))
            ult = t
    ativos = sum(1 for v in env if v > -50)
    return dict(lufs=float(i.group(1)) if i else None, pico_dbfs=float(pico.group(1)) if pico else None,
                tempo_com_som_pct=round(100 * ativos / max(1, len(env)), 1), transientes=trans,
                aviso='transiente = subida brusca de volume: pode ser efeito sonoro, batida de musica ou inicio de fala. '
                      'So vale como efeito se coincidir com um evento visual no mesmo instante.')


def fonte_para_texto() -> str | None:
    for f in FONTES:
        if Path(f).exists():
            return f
    return None


def folhas(video: Path, duracao: float, saida: Path) -> list[str]:
    """Folhas de contato 6x3. Video curto (<= 60 s): 2 quadros por segundo; longo: 1 por segundo."""
    fps = 2 if duracao <= 60 else 1
    info = _ff.info_basica(video)
    retrato = info['altura'] > info['largura']
    escala = 'scale=-2:400' if retrato else 'scale=400:-2'
    f = fonte_para_texto()
    texto = ''
    if f:
        ff = f.replace(':', r'\:')
        texto = (f",drawtext=fontfile='{ff}':text='%{{pts\\:flt}}':x=6:y=6:fontsize=22:fontcolor=yellow:borderw=2:bordercolor=black")
    (saida / 'sheets').mkdir(parents=True, exist_ok=True)
    for velha in (saida / 'sheets').glob('*.jpg'):
        velha.unlink()
    _ff.rodar([_ff.exe('ffmpeg'), '-v', 'error', '-y', '-i', str(video), '-an',
               '-vf', f'fps={fps},{escala}{texto},tile={COLUNAS}x{LINHAS}', '-q:v', '3', str(saida / 'sheets' / 'tmp_%03d.jpg')])
    por_folha = COLUNAS * LINHAS / fps
    nomes = []
    for k, arq in enumerate(sorted((saida / 'sheets').glob('tmp_*.jpg'))):
        t0, t1 = k * por_folha, min(duracao, (k + 1) * por_folha)
        novo = arq.with_name(f'sheet_{k + 1:02d}_{round(t0, 1):g}-{round(t1, 1):g}.jpg')
        arq.replace(novo)
        nomes.append(novo.name)
    if not f:
        print('  aviso: nenhuma fonte de sistema achada; as folhas saem sem o tempo escrito em cada quadro '
              f'(cada folha cobre {por_folha:g} s, {fps} quadro(s) por segundo, da esquerda para a direita e de cima para baixo)')
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
                plano_medio_s=round(dur / (len(cortes) + 1), 2) if dur else 0, limiar_cena=limiar,
                aviso='cortes de cena nao pegam zoom nem jump cut leve: confira nas folhas')
    (pasta / 'meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding='utf-8')
    (pasta / 'scenes.json').write_text(json.dumps(cortes), encoding='utf-8')
    if info['tem_audio']:
        (pasta / 'sons.json').write_text(json.dumps(sons(video, dur), ensure_ascii=False, indent=1), encoding='utf-8')
    nomes = folhas(video, dur, pasta) if com_folhas and info['tem_video'] else []
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
    a = ap.parse_args()
    if a.cmd == 'analisar':
        for v in a.videos:
            analisar(v, a.saida, a.limiar_cena, not a.sem_folhas)
    else:
        quadro(a.video, a.t, a.saida, a.rajada, a.fps)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
