#!/usr/bin/env python3
"""Aplica o plano de cortes (cortes.json) e gera o video limpo com emendas por sobreposicao.

Video: cada trecho e codificado em paralelo (busca rapida no original) e depois colado sem recodificar.
Audio: trechos extraidos, emendados com crossfade (o anterior desce, o novo entra seco), tratados e normalizados.
Saidas em --saida: aula_limpa.mp4 (ou aula_limpa.m4a se o arquivo so tiver audio) e timeline.json (mapa de tempo bruto -> final).

Uso:
  python montar.py pasta/cortes.json --saida pasta [--qualidade boa|maxima] [--fps 30]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ff  # noqa: E402

FADE_ENTRADA = 0.03     # s: fade de entrada do trecho novo (so para evitar estalo)
FADE_FINAL = 0.25       # s: fade de saida no fim do video
CADEIA_AUDIO = ('highpass=f=70,equalizer=f=300:t=q:w=1:g=-1.2,equalizer=f=3200:t=q:w=1:g=1.6,'
                'acompressor=threshold=-21dB:ratio=3:attack=8:release=140:makeup=2')


def calcular_tempos(segs: list[dict]) -> tuple[list[float], float]:
    """Inicio de cada trecho no tempo final e duracao total (cada emenda 'come' a sobreposicao d)."""
    T, t = [], 0.0
    for i, s in enumerate(segs):
        T.append(t)
        t += (s['fim'] - s['ini']) - (s['d'] if i < len(segs) - 1 else 0.0)
    return T, t


def quadros_por_trecho(segs: list[dict], T: list[float], total: float, fps: float) -> list[int]:
    """Quadros de cada trecho com arredondamento acumulado (sem deriva entre audio e video)."""
    limites = [round(t * fps) for t in T] + [round(total * fps)]
    return [max(1, limites[i + 1] - limites[i]) for i in range(len(segs))]


def dimensoes_saida(info: dict, max_lado: int) -> tuple[int, int]:
    w, h = (info['altura'], info['largura']) if info['rotacao'] in (90, 270, -90, -270) else (info['largura'], info['altura'])
    k = min(1.0, max_lado / max(w, h))
    return int(round(w * k / 2) * 2), int(round(h * k / 2) * 2)


def escolher_fps(info: dict, pedido: float | None) -> float:
    if pedido:
        return float(pedido)
    f = info['fps'] or 30.0
    if f > 31:
        return 30.0
    return {23.976: 24.0, 29.97: 30.0}.get(round(f, 3), round(f * 1000) / 1000 if abs(f - round(f)) > 0.02 else float(round(f)))


def _job(args: list[str]) -> None:
    _ff.rodar(args)


def main() -> int:
    _ff.configurar_saida()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cortes', type=Path, help='cortes.json gerado por planejar_cortes.py')
    ap.add_argument('--saida', type=Path, required=True)
    ap.add_argument('--qualidade', choices=['boa', 'maxima'], default='boa',
                    help='boa (padrao): CRF 18 | maxima: CRF 16, mais lento')
    ap.add_argument('--fps', type=float, help='padrao: o do original, no maximo 30')
    ap.add_argument('--max-lado', type=int, default=1920, help='reduz se o maior lado passar disso (padrao 1920)')
    ap.add_argument('--lufs', type=float, default=-16.0)
    ap.add_argument('--sem-tratamento-audio', action='store_true', help='so normaliza o volume (sem EQ e compressor)')
    ap.add_argument('--trabalhadores', type=int, help='trechos de video em paralelo (padrao automatico)')
    ap.add_argument('--manter-temporarios', action='store_true')
    a = ap.parse_args()

    plano = json.loads(a.cortes.read_text(encoding='utf-8'))
    video = Path(plano['video'])
    segs = plano['segmentos']
    info = _ff.info_basica(video)
    fps = escolher_fps(info, a.fps)
    w, h = dimensoes_saida(info, a.max_lado) if info['tem_video'] else (0, 0)
    T, total = calcular_tempos(segs)
    nq = quadros_por_trecho(segs, T, total, fps)
    args_enc = _ff.perfil_video(a.qualidade) if info['tem_video'] else []
    paralelo = a.trabalhadores or max(2, (os.cpu_count() or 4) // 2)
    a.saida.mkdir(parents=True, exist_ok=True)
    tmp = a.saida / '_tmp'
    tmp.mkdir(exist_ok=True)
    ff = _ff.exe('ffmpeg')
    t0 = time.time()
    print(f'{len(segs)} trechos | ' + (f'{w}x{h} a {fps:g} fps' if info['tem_video'] else 'somente audio') + f' | duracao final {_ff.mmss(total)}', flush=True)

    # 1) video: um arquivo por trecho, em paralelo
    rw, rh = ((info['altura'], info['largura']) if info['rotacao'] in (90, 270, -90, -270)
              else (info['largura'], info['altura']))      # tamanho apos a rotacao automatica
    filtro_v = (f'fps={fps:g}' + ''
                + (f',scale={w}:{h}:flags=lanczos' if (w, h) != (rw, rh) else '') + ',setsar=1,format=yuv420p')
    tem_video = info['tem_video']
    jobs = []
    for i, s in enumerate(segs if tem_video else []):
        jobs.append([ff, '-v', 'error', '-y', '-ss', f'{s["ini"]:.4f}', '-i', str(video), '-map', '0:v:0', '-an',
                     '-vf', filtro_v, '-frames:v', str(nq[i]), *args_enc, '-g', str(int(round(fps * 2))), str(tmp / f'v{i:04d}.mp4')])
    if tem_video:
        with ThreadPoolExecutor(max_workers=paralelo) as ex:
            list(ex.map(_job, jobs))
        lista = tmp / 'lista.txt'
        lista.write_text(''.join(f"file 'v{i:04d}.mp4'\n" for i in range(len(segs))), encoding='utf-8')
        _ff.rodar([ff, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lista), '-c', 'copy', str(tmp / 'video.mp4')])
        print(f'  video pronto ({time.time() - t0:.0f} s)', flush=True)
    else:
        print('  arquivo sem imagem: so o audio sera limpo (saida .m4a)', flush=True)

    # 2) audio: trechos -> emendas com crossfade -> tratamento -> loudnorm em duas passadas
    ajobs = [[ff, '-v', 'error', '-y', '-ss', f'{s["ini"]:.4f}', '-t', f'{s["fim"] - s["ini"]:.4f}', '-i', str(video),
              '-vn', '-map', '0:a:0', '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s16le', str(tmp / f'a{i:04d}.wav')]
             for i, s in enumerate(segs)]
    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(_job, ajobs))
    n = len(segs)
    linhas = [f'[{i}:a]afade=t=in:d={0.01 if i == 0 else FADE_ENTRADA}[f{i}]' for i in range(n)]
    atual = 'f0'
    for i in range(1, n):
        d = segs[i - 1]['d']
        linhas.append(f'[{atual}][f{i}]acrossfade=d={d:.4f}:c1=qsin:c2=nofade[x{i}]')
        atual = f'x{i}'
    linhas.append(f'[{atual}]afade=t=out:st={max(0.0, total - FADE_FINAL):.4f}:d={FADE_FINAL}[mix]')
    (tmp / 'audio.filtro').write_text(';\n'.join(linhas), encoding='utf-8')
    flag = _ff.flag_filtro_arquivo()
    entradas = [x for i in range(n) for x in ('-i', f'a{i:04d}.wav')]
    cwd = os.getcwd()
    os.chdir(tmp)   # nomes curtos nos -i: a linha de comando do Windows tem limite de tamanho
    try:
        _ff.rodar([ff, '-v', 'error', '-y', *entradas, flag, 'audio.filtro', '-map', '[mix]', '-c:a', 'pcm_s16le', 'emendado.wav'])
    finally:
        os.chdir(cwd)
    cadeia = 'anull' if a.sem_tratamento_audio else CADEIA_AUDIO
    _ff.rodar([ff, '-v', 'error', '-y', '-i', str(tmp / 'emendado.wav'), '-af', cadeia, '-c:a', 'pcm_s16le', str(tmp / 'tratado.wav')])
    m = _ff.rodar([ff, '-hide_banner', '-i', str(tmp / 'tratado.wav'), '-af',
                   f'loudnorm=I={a.lufs}:TP=-1.5:LRA=8:print_format=json', '-f', 'null', '-'], check=False).stderr
    med = json.loads(m[m.rindex('{'):m.rindex('}') + 1])
    ln = (f'loudnorm=I={a.lufs}:TP=-1.5:LRA=8:measured_I={med["input_i"]}:measured_TP={med["input_tp"]}:'
          f'measured_LRA={med["input_lra"]}:measured_thresh={med["input_thresh"]}:offset={med["target_offset"]}:linear=true,'
          'alimiter=limit=0.84:level=false')
    _ff.rodar([ff, '-v', 'error', '-y', '-i', str(tmp / 'tratado.wav'), '-af', ln, '-ar', '48000', str(tmp / 'final.wav')])

    # 3) junta imagem e som
    if tem_video:
        saida = a.saida / 'aula_limpa.mp4'
        dur_v = float(_ff.sonda(tmp / 'video.mp4')['format']['duration'])
        _ff.rodar([ff, '-v', 'error', '-y', '-i', str(tmp / 'video.mp4'), '-i', str(tmp / 'final.wav'), '-map', '0:v', '-map', '1:a',
                   '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', f'{min(dur_v, total):.4f}', '-movflags', '+faststart', str(saida)])
    else:
        saida = a.saida / 'aula_limpa.m4a'
        _ff.rodar([ff, '-v', 'error', '-y', '-i', str(tmp / 'final.wav'), '-c:a', 'aac', '-b:a', '192k', str(saida)])

    mapa = dict(video_bruto=str(video), arquivo=str(saida), fps=fps, largura=w if tem_video else 0, altura=h if tem_video else 0, duracao_final=round(total, 3),
                trechos=[dict(bruto_ini=s['ini'], bruto_fim=s['fim'], final_ini=round(T[i], 4), sobreposicao_depois=s['d'],
                              tipo_corte_depois=s['tipo']) for i, s in enumerate(segs)])
    (a.saida / 'timeline.json').write_text(json.dumps(mapa, ensure_ascii=False, indent=1), encoding='utf-8')
    if not a.manter_temporarios:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'pronto em {time.time() - t0:.0f} s: {saida} ({_ff.mmss(total)}) | volume medido antes do ajuste: {med["input_i"]} LUFS')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError, KeyError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
