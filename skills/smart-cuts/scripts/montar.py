#!/usr/bin/env python3
"""Monta um mp4 por corte a partir de plano_cortes.json, com emendas por sobreposicao de imagem e audio.

Video: cada segmento e codificado em paralelo (busca precisa no original) e colado sem recodificar. A imagem do
segmento seguinte entra no MESMO instante em que o audio dele comeca, antes de a fala anterior acabar.
Audio: segmentos extraidos, emendados com crossfade (o anterior desce, o novo entra seco), tratados e normalizados.
Saidas em --saida: <id>.mp4 de cada corte e plano.json (o plano para quem vai acrescentar legenda, gancho, inserts e musica).

Uso:
  python montar.py pasta/plano_cortes.json --saida pasta [--so c1,c2] [--qualidade boa|maxima] [--fps 30]
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
from planejar_cortes import calcular_tempos  # noqa: E402

FADE_ENTRADA = 0.03     # s: fade de entrada do trecho novo (so para evitar estalo)
FADE_FINAL = 0.12       # s: fade de saida no fim do corte
CADEIA_AUDIO = ('highpass=f=70,equalizer=f=300:t=q:w=1:g=-1.2,equalizer=f=3200:t=q:w=1:g=1.6,'
                'acompressor=threshold=-21dB:ratio=3:attack=8:release=140:makeup=2')


def quadros_por_trecho(T: list[float], total: float, fps: float) -> list[int]:
    """Quadros de cada segmento com arredondamento acumulado (sem deriva entre audio e video)."""
    limites = [round(t * fps) for t in T] + [round(total * fps)]
    return [max(1, limites[i + 1] - limites[i]) for i in range(len(T))]


def tamanho(info: dict) -> tuple[int, int]:
    """Largura e altura apos a rotacao automatica."""
    return (info['altura'], info['largura']) if info['rotacao'] in (90, 270, -90, -270) else (info['largura'], info['altura'])


def dimensoes_saida(info: dict, max_lado: int) -> tuple[int, int]:
    w, h = tamanho(info)
    k = min(1.0, max_lado / max(w, h))
    return int(round(w * k / 2) * 2), int(round(h * k / 2) * 2)


def escolher_fps(info: dict, pedido: float | None) -> float:
    if pedido:
        return float(pedido)
    f = info['fps'] or 30.0
    if f > 31:
        return 30.0
    return {23.976: 24.0, 29.97: 30.0}.get(round(f, 3), round(f * 1000) / 1000 if abs(f - round(f)) > 0.02 else float(round(f)))


def _rodar(args: list[str]) -> None:
    _ff.rodar(args)


def montar_corte(corte: dict, fontes: dict, infos: dict, a: argparse.Namespace, ff: str) -> dict:
    cid, segs = corte['id'], corte['segmentos']
    ref = infos[segs[0]['fonte']]
    fps = escolher_fps(ref, a.fps)
    w, h = dimensoes_saida(ref, a.max_lado)
    T, total = calcular_tempos(segs)
    nq = quadros_por_trecho(T, total, fps)
    paralelo = a.trabalhadores or max(2, (os.cpu_count() or 4) // 2)
    tmp = a.saida / f'_tmp_{cid}'
    tmp.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    print(f'[{cid}] {len(segs)} segmentos | {w}x{h} a {fps:g} fps | duracao final {_ff.mmss(total)}', flush=True)

    # 1) video: um arquivo por segmento, em paralelo
    jobs = []
    for i, s in enumerate(segs):
        info = infos[s['fonte']]
        filtro = f'fps={fps:g}'
        if tamanho(info) != (w, h):   # fonte de outro tamanho: cabe inteira, com barras
            filtro += f',scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2'
        filtro += ',setsar=1,format=yuv420p'
        jobs.append([ff, '-v', 'error', '-y', '-ss', f'{s["ini"]:.4f}', '-i', str(fontes[s['fonte']]['video']), '-map', '0:v:0', '-an',
                     '-vf', filtro, '-frames:v', str(nq[i]), *_ff.perfil_video(a.qualidade), '-g', str(int(round(fps * 2))),
                     str(tmp / f'v{i:04d}.mp4')])
    with ThreadPoolExecutor(max_workers=paralelo) as ex:
        list(ex.map(_rodar, jobs))
    (tmp / 'lista.txt').write_text(''.join(f"file 'v{i:04d}.mp4'\n" for i in range(len(segs))), encoding='utf-8')
    _ff.rodar([ff, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(tmp / 'lista.txt'), '-c', 'copy', str(tmp / 'video.mp4')])

    # 2) audio: segmentos -> emendas com crossfade -> tratamento -> loudnorm em duas passadas
    ajobs = [[ff, '-v', 'error', '-y', '-ss', f'{s["ini"]:.4f}', '-t', f'{s["fim"] - s["ini"]:.4f}', '-i', str(fontes[s['fonte']]['video']),
              '-vn', '-map', '0:a:0', '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s16le', str(tmp / f'a{i:04d}.wav')]
             for i, s in enumerate(segs)]
    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(_rodar, ajobs))
    n = len(segs)
    linhas = [f'[{i}:a]afade=t=in:d={0.01 if i == 0 else FADE_ENTRADA}[f{i}]' for i in range(n)]
    atual = 'f0'
    for i in range(1, n):
        linhas.append(f'[{atual}][f{i}]acrossfade=d={segs[i - 1]["d"]:.4f}:c1=qsin:c2=nofade[x{i}]')
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
    saida = a.saida / f'{cid}.mp4'
    dur_v = float(_ff.sonda(tmp / 'video.mp4')['format']['duration'])
    _ff.rodar([ff, '-v', 'error', '-y', '-i', str(tmp / 'video.mp4'), '-i', str(tmp / 'final.wav'), '-map', '0:v', '-map', '1:a',
               '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', f'{min(dur_v, total):.4f}', '-movflags', '+faststart', str(saida)])
    if not a.manter_temporarios:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'[{cid}] pronto em {time.time() - t0:.0f} s: {saida.name} ({_ff.mmss(total)})', flush=True)

    emendas = [dict(t=s['final_ini'], tipo=ant['tipo'], sobreposicao=ant['d'])
               for s, ant in zip(segs[1:], segs)]
    return dict(id=cid, estilo=corte['estilo'], gancho=corte['gancho'], porque=corte.get('porque', ''), arquivo=saida.name,
                duracao=round(total, 3), fps=fps, largura=w, altura=h, texto=corte['texto'],
                palavras=corte['palavras'], palavras_origem='estimadas a partir do tempo da transcricao do bruto: '
                'para a legenda, transcreva o corte final e use esses tempos', emendas=emendas, **corte.get('extras', {}))


def main() -> int:
    _ff.configurar_saida()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('plano', type=Path, help='plano_cortes.json gerado por planejar_cortes.py')
    ap.add_argument('--saida', type=Path, required=True)
    ap.add_argument('--so', default='', help='montar so estes ids (separados por virgula)')
    ap.add_argument('--qualidade', choices=['boa', 'maxima'], default='boa', help='boa (padrao): CRF 18 | maxima: CRF 16, mais lento')
    ap.add_argument('--fps', type=float, help='padrao: o do original, no maximo 30')
    ap.add_argument('--max-lado', type=int, default=1920, help='reduz se o maior lado passar disso (padrao 1920)')
    ap.add_argument('--lufs', type=float, default=-16.0)
    ap.add_argument('--sem-tratamento-audio', action='store_true', help='so normaliza o volume (sem EQ e compressor)')
    ap.add_argument('--trabalhadores', type=int, help='segmentos de video em paralelo (padrao automatico)')
    ap.add_argument('--manter-temporarios', action='store_true')
    a = ap.parse_args()

    plano = json.loads(a.plano.read_text(encoding='utf-8'))
    fontes = {k: dict(video=Path(v['video'])) for k, v in plano['fontes'].items()}
    infos = {k: _ff.info_basica(v['video']) for k, v in fontes.items()}
    for k, info in infos.items():
        if not info['tem_video']:
            raise ValueError(f'{fontes[k]["video"].name} nao tem imagem: a Smart Cuts monta cortes de video.')
    a.saida.mkdir(parents=True, exist_ok=True)
    ff = _ff.exe('ffmpeg')
    so = {x for x in a.so.split(',') if x}
    saida_json = a.saida / 'plano.json'
    anterior = {c['id']: c for c in json.loads(saida_json.read_text(encoding='utf-8'))['cortes']} if saida_json.exists() else {}
    for corte in plano['cortes']:
        if so and corte['id'] not in so:
            continue
        anterior[corte['id']] = montar_corte(corte, fontes, infos, a, ff)
    ordem = [c['id'] for c in plano['cortes']]
    final = sorted(anterior.values(), key=lambda c: ordem.index(c['id']) if c['id'] in ordem else 999)
    saida_json.write_text(json.dumps(dict(cortes=final), ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'plano.json com {len(final)} corte(s) em {a.saida}')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError, KeyError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
