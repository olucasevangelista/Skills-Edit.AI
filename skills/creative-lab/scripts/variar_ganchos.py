#!/usr/bin/env python3
"""Junta cada gancho ao mesmo corpo de anuncio e gera uma variante por gancho, para teste de criativos.

A emenda gancho -> corpo usa sobreposicao: o corpo entra colado no comeco da voz e IMAGEM e AUDIO dele entram juntos,
um pouco antes de a fala do gancho acabar (a frase do gancho termina inteira). Os instantes vem do VOLUME do audio.
O corpo e codificado uma vez so e reaproveitado sem recodificar; o volume de todas as variantes vai para o mesmo alvo
(diferenca de volume entre criativos de teste enviesa o resultado).

Saidas em --saida: <prefixo>__<gancho>.mp4 de cada variante e matriz.csv (para a planilha do teste).

Uso:
  python variar_ganchos.py --corpo corpo.mp4 --ganchos g1.mp4 g2.mp4 --saida pasta [--prefixo anuncio]
  python variar_ganchos.py --corpo corpo.mp4 --ganchos pasta_dos_ganchos --saida pasta
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _fala  # noqa: E402
import _ff  # noqa: E402

FOLGA = 0.025          # s antes da primeira consoante do corpo (para nao comer o comeco da palavra)
CAUDA = 0.10           # s depois da ultima palavra do gancho (decaimento natural)
FADE_ENTRADA = 0.03    # s: fade de entrada do corpo no audio (so para evitar estalo)
FADE_FINAL = 0.10      # s: fade de saida no fim do anuncio
EXT_VIDEO = {'.mp4', '.mov', '.m4v', '.mkv', '.webm'}
COLUNAS = ['variante', 'arquivo', 'gancho', 'duracao_gancho_s', 'duracao_total_s', 'emenda_em_s', 'lufs',
           'hook_rate', 'hold_rate', 'ctr', 'observacoes']


def nome_seguro(txt: str) -> str:
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', txt).strip('_') or 'gancho'


def expandir(ganchos: list[Path]) -> list[Path]:
    out: list[Path] = []
    for g in ganchos:
        if g.is_dir():
            out += sorted(p for p in g.iterdir() if p.suffix.lower() in EXT_VIDEO)
        else:
            out.append(g)
    return out


def tamanho(info: dict) -> tuple[int, int]:
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


def faixas(video: Path) -> list[tuple[float, float]]:
    env = _ff.envelope_db(video)
    return _fala.faixas_de_fala(env, _fala.limiar_auto(env))


def filtro_video(info: dict, w: int, h: int, fps: float) -> str:
    f = f'fps={fps:g}'
    if tamanho(info) != (w, h):   # outro tamanho: cabe inteiro, com barras (nao corta nem distorce)
        f += f',scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2'
    return f + ',setsar=1,format=yuv420p'


def _rodar(args: list[str]) -> None:
    _ff.rodar(args)


def codificar_video(ff: str, origem: Path, ini: float, quadros: int, filtro: str, fps: float, qualidade: str, destino: Path) -> list[str]:
    return [ff, '-v', 'error', '-y', '-ss', f'{ini:.4f}', '-i', str(origem), '-map', '0:v:0', '-an', '-vf', filtro,
            '-frames:v', str(quadros), *_ff.perfil_video(qualidade), '-g', str(int(round(fps * 2))), str(destino)]


def extrair_audio(ff: str, origem: Path, ini: float, dur: float | None, destino: Path) -> None:
    args = [ff, '-v', 'error', '-y', '-ss', f'{ini:.4f}']
    if dur is not None:
        args += ['-t', f'{dur:.4f}']
    _ff.rodar([*args, '-i', str(origem), '-vn', '-map', '0:a:0', '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s16le', str(destino)])


def normalizar(ff: str, entrada: Path, saida: Path, lufs: float) -> None:
    """loudnorm em duas passadas (a segunda com os valores medidos na primeira)."""
    m = _ff.rodar([ff, '-hide_banner', '-i', str(entrada), '-af', f'loudnorm=I={lufs}:TP=-1.5:LRA=11:print_format=json',
                   '-f', 'null', '-'], check=False).stderr
    med = json.loads(m[m.rindex('{'):m.rindex('}') + 1])
    ln = (f'loudnorm=I={lufs}:TP=-1.5:LRA=11:measured_I={med["input_i"]}:measured_TP={med["input_tp"]}:'
          f'measured_LRA={med["input_lra"]}:measured_thresh={med["input_thresh"]}:offset={med["target_offset"]}:linear=true,'
          'alimiter=limit=0.84:level=false')
    _ff.rodar([ff, '-v', 'error', '-y', '-i', str(entrada), '-af', ln, '-ar', '48000', str(saida)])


def medir_lufs(ff: str, video: Path) -> float:
    r = _ff.rodar([ff, '-hide_banner', '-i', str(video), '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'], check=False)
    resumo = r.stderr[r.stderr.rfind('Summary:'):]
    m = re.search(r'I:\s+(-?[\d.]+) LUFS', resumo)
    return float(m.group(1)) if m else float('nan')


def main() -> int:
    _ff.configurar_saida()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--corpo', type=Path, required=True, help='o corpo do anuncio (o que e igual em todas as variantes)')
    ap.add_argument('--ganchos', type=Path, nargs='+', required=True, help='arquivos de gancho, ou uma pasta com eles')
    ap.add_argument('--saida', type=Path, required=True)
    ap.add_argument('--prefixo', help='inicio do nome dos arquivos (padrao: o nome do corpo)')
    ap.add_argument('--sobreposicao', type=float, default=0.22, help='s de sobreposicao na emenda (padrao 0.22)')
    ap.add_argument('--lufs', type=float, default=-14.0, help='volume alvo de todas as variantes (padrao -14)')
    ap.add_argument('--qualidade', choices=['boa', 'maxima'], default='boa', help='boa: CRF 18 | maxima: CRF 16, mais lento')
    ap.add_argument('--fps', type=float, help='padrao: o do corpo, no maximo 30')
    ap.add_argument('--max-lado', type=int, default=1920, help='reduz se o maior lado passar disso (padrao 1920)')
    ap.add_argument('--separador', default=';', help='separador do matriz.csv (padrao ";", que o Excel em portugues abre direto)')
    ap.add_argument('--manter-temporarios', action='store_true')
    a = ap.parse_args()

    ganchos = expandir(a.ganchos)
    if not ganchos:
        raise ValueError('Nenhum gancho encontrado (arquivo de video ou pasta com videos).')
    for g in [a.corpo, *ganchos]:
        if not g.is_file():
            raise FileNotFoundError(f'Arquivo nao encontrado: {g}')
    ff = _ff.exe('ffmpeg')
    ic = _ff.info_basica(a.corpo)
    if not (ic['tem_video'] and ic['tem_audio']):
        raise ValueError('O corpo precisa ter imagem e audio.')
    w, h = dimensoes_saida(ic, a.max_lado)
    fps = escolher_fps(ic, a.fps)
    aviso: dict[str, list[str]] = {}
    prefixo = nome_seguro(a.prefixo or a.corpo.stem)
    a.saida.mkdir(parents=True, exist_ok=True)
    tmp = a.saida / '_tmp_ganchos'
    tmp.mkdir(exist_ok=True)
    t0 = time.time()

    # corpo: onde a voz comeca
    fc = faixas(a.corpo)
    if fc:
        b0 = max(0.0, fc[0][0] - FOLGA)
    else:
        b0 = 0.0
        aviso.setdefault('corpo', []).append('nao achei voz no corpo; usei o comeco do arquivo')
    dur_corpo = ic['duracao'] - b0
    nq_corpo = max(1, round(dur_corpo * fps))
    print(f'corpo: {a.corpo.name} | {w}x{h} a {fps:g} fps | voz comeca em {b0 + FOLGA:.2f} s | {len(ganchos)} gancho(s)', flush=True)

    # gancho: onde a voz termina, e o que vai para o video (ate o instante da sobreposicao)
    plano = []
    usados: dict[str, int] = {}
    for k, g in enumerate(ganchos):
        ig = _ff.info_basica(g)
        if not (ig['tem_video'] and ig['tem_audio']):
            raise ValueError(f'O gancho {g.name} precisa ter imagem e audio.')
        avisos = []
        if abs(tamanho(ig)[0] / tamanho(ig)[1] - w / h) > 0.01:
            avisos.append(f'proporcao {tamanho(ig)[0]}x{tamanho(ig)[1]} diferente do corpo ({w}x{h}): entrou inteiro, com barras')
        fg = faixas(g)
        if fg:
            a_fim = min(ig['duracao'], fg[-1][1] + CAUDA)
        else:
            a_fim = ig['duracao']
            avisos.append('nao achei voz no gancho; usei o arquivo inteiro')
        d = min(a.sobreposicao, a_fim / 2 - 0.03, dur_corpo / 2 - 0.03)
        if d < 0.05:
            raise ValueError(f'O gancho {g.name} ({a_fim:.2f} s de voz) e curto demais para a sobreposicao.')
        if d < a.sobreposicao - 1e-6:
            avisos.append(f'gancho curto: sobreposicao reduzida para {d:.2f} s')
        nome = nome_seguro(g.stem)
        usados[nome] = usados.get(nome, 0) + 1
        if usados[nome] > 1:
            nome = f'{nome}_{usados[nome]}'
        plano.append(dict(k=k, arquivo=g, info=ig, nome=nome, a_fim=a_fim, d=d, quadros=max(1, round((a_fim - d) * fps)), avisos=avisos))

    # video: o corpo uma vez; cada gancho ate o instante da sobreposicao; tudo emendado sem recodificar o corpo
    jobs = [codificar_video(ff, a.corpo, b0, nq_corpo, filtro_video(ic, w, h, fps), fps, a.qualidade, tmp / 'corpo_v.mp4')]
    for p in plano:
        jobs.append(codificar_video(ff, p['arquivo'], 0.0, p['quadros'], filtro_video(p['info'], w, h, fps), fps, a.qualidade, tmp / f'g{p["k"]:03d}_v.mp4'))
    with ThreadPoolExecutor(max_workers=max(2, (os.cpu_count() or 4) // 2)) as ex:
        list(ex.map(_rodar, jobs))
    extrair_audio(ff, a.corpo, b0, None, tmp / 'corpo_a.wav')
    print(f'  video do corpo e dos ganchos pronto ({time.time() - t0:.0f} s)', flush=True)

    linhas = []
    for p in plano:
        k, d, a_fim = p['k'], p['d'], p['a_fim']
        total = (a_fim - d) + dur_corpo
        (tmp / f'lista{k:03d}.txt').write_text(f"file 'g{k:03d}_v.mp4'\nfile 'corpo_v.mp4'\n", encoding='utf-8')
        _ff.rodar([ff, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(tmp / f'lista{k:03d}.txt'), '-c', 'copy', str(tmp / f'v{k:03d}.mp4')])
        # audio: o final do gancho desce enquanto a voz do corpo entra (a imagem do corpo entra no mesmo instante)
        extrair_audio(ff, p['arquivo'], 0.0, a_fim, tmp / f'g{k:03d}_a.wav')
        filtro = (f'[0:a]afade=t=in:d=0.01[h];[1:a]afade=t=in:d={FADE_ENTRADA}[b];'
                  f'[h][b]acrossfade=d={d:.4f}:c1=qsin:c2=nofade[x];[x]afade=t=out:st={max(0.0, total - FADE_FINAL):.4f}:d={FADE_FINAL}[mix]')
        (tmp / f'filtro{k:03d}.txt').write_text(filtro, encoding='utf-8')
        flag = _ff.flag_filtro_arquivo()
        cwd = os.getcwd()
        os.chdir(tmp)   # nomes curtos: a linha de comando do Windows tem limite de tamanho
        try:
            _ff.rodar([ff, '-v', 'error', '-y', '-i', f'g{k:03d}_a.wav', '-i', 'corpo_a.wav', flag, f'filtro{k:03d}.txt', '-map', '[mix]',
                       '-c:a', 'pcm_s16le', f'e{k:03d}.wav'])
        finally:
            os.chdir(cwd)
        normalizar(ff, tmp / f'e{k:03d}.wav', tmp / f'n{k:03d}.wav', a.lufs)
        saida = a.saida / f'{prefixo}__{p["nome"]}.mp4'
        _ff.rodar([ff, '-v', 'error', '-y', '-i', str(tmp / f'v{k:03d}.mp4'), '-i', str(tmp / f'n{k:03d}.wav'), '-map', '0:v', '-map', '1:a',
                   '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', f'{total:.4f}', '-movflags', '+faststart', str(saida)])
        real = float(_ff.sonda(saida)['format']['duration'])
        lufs = medir_lufs(ff, saida)
        if abs(real - total) > 0.25:
            p['avisos'].append(f'duracao {real:.2f} s difere da prevista ({total:.2f} s)')
        if abs(lufs - a.lufs) > 1.5:
            p['avisos'].append(f'volume {lufs:.1f} LUFS fora do alvo ({a.lufs:g})')
        linhas.append({'variante': f'{prefixo}__{p["nome"]}', 'arquivo': saida.name, 'gancho': p['arquivo'].name,
                       'duracao_gancho_s': f'{a_fim - d:.2f}', 'duracao_total_s': f'{real:.2f}', 'emenda_em_s': f'{a_fim - d:.2f}',
                       'lufs': f'{lufs:.1f}', 'hook_rate': '', 'hold_rate': '', 'ctr': '', 'observacoes': '; '.join(p['avisos'])})
        print(f'  [{p["nome"]}] {saida.name} | {real:.1f} s | emenda em {a_fim - d:.2f} s | {lufs:.1f} LUFS'
              + (f' | AVISO: {"; ".join(p["avisos"])}' if p['avisos'] else ''), flush=True)

    with open(a.saida / 'matriz.csv', 'w', newline='', encoding='utf-8-sig') as f:
        wr = csv.DictWriter(f, fieldnames=COLUNAS, delimiter=a.separador)
        wr.writeheader()
        wr.writerows(linhas)
    if not a.manter_temporarios:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'{len(linhas)} variante(s) em {a.saida} ({time.time() - t0:.0f} s) | matriz.csv com as colunas das metricas em branco')
    for av in aviso.get('corpo', []):
        print('AVISO:', av)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError, KeyError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
