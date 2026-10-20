#!/usr/bin/env python3
"""Diagnostico rapido de uma aula bruta: formato, volume, fala x silencio e avisos que mudam a edicao.

Uso:
  python diagnosticar.py aula.mp4
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ff  # noqa: E402
import planejar_cortes as pc  # noqa: E402


def main() -> int:
    _ff.configurar_saida()
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    video = Path(sys.argv[1])
    info = _ff.info_basica(video)
    dados = _ff.sonda(video)
    v = next((s for s in dados['streams'] if s['codec_type'] == 'video'), {})
    avisos = []
    w, h = (info['altura'], info['largura']) if info['rotacao'] in (90, 270, -90, -270) else (info['largura'], info['altura'])
    print(f'Arquivo: {video.name}')
    print(f'Duracao: {_ff.mmss(info["duracao"])} | imagem: {w}x{h} a {info["fps"]:.2f} fps ({info["codec_video"]}) | '
          f'audio: {info["codec_audio"]} {info["taxa_audio"]} Hz')
    if not info['tem_audio']:
        print('ERRO: sem faixa de audio. Esta skill precisa da fala para cortar.')
        return 1
    if not info['tem_video']:
        avisos.append('So audio (sem imagem): a edicao sera de limpeza do audio; os motions precisam de uma imagem de fundo.')
    if info['vfr']:
        avisos.append('Taxa de quadros variavel (gravacao de celular ou de tela): sera convertida para taxa fixa na montagem.')
    if info['rotacao']:
        avisos.append(f'Video girado ({info["rotacao"]} graus): a montagem aplica a rotacao automaticamente.')
    if v.get('color_transfer') in ('arib-std-b67', 'smpte2084'):
        avisos.append('Video HDR (HLG/PQ): as cores podem ficar lavadas no resultado. Se for gravacao de celular, prefira gravar em SDR.')
    if max(w, h) > 1920:
        avisos.append(f'Imagem acima de 1920 px ({w}x{h}): sera reduzida para acelerar. Use --max-lado para manter.')
    env = _ff.envelope_db(video)
    piso, fala = _ff.percentil(env, 10), _ff.percentil(env, 90)
    thr = pc.limiar_auto(env)
    faixas = pc.faixas_de_fala(env, thr)
    voz = sum(b - a for a, b in faixas)
    pausas = [faixas[i + 1][0] - faixas[i][1] for i in range(len(faixas) - 1)]
    longas = [p for p in pausas if p > 0.55]
    print(f'Volume: piso de ruido {piso:.0f} dB, fala {fala:.0f} dB | limiar de silencio sugerido: {thr:.0f} dB')
    print(f'Fala: {voz / info["duracao"] * 100:.0f}% do tempo | pausas acima de 0,55 s: {len(longas)} '
          f'(somam {sum(longas):.0f} s) | maior pausa: {max(pausas) if pausas else 0:.1f} s')
    if fala < -32:
        avisos.append(f'Fala baixa ({fala:.0f} dB): o volume sera normalizado, mas o ruido de fundo tambem sobe.')
    if piso > -50:
        avisos.append(f'Ruido de fundo alto ({piso:.0f} dB): os cortes de pausa ficam menos precisos. Considere limpar o audio antes.')
    if voz / info['duracao'] < 0.35:
        avisos.append('Pouca fala no arquivo (menos de 35%): confira se o audio certo foi usado.')
    for a in avisos:
        print('AVISO:', a)
    print('Pergunta para o usuario: qual o formato da aula (camera, tela com rosto, slides ou so audio)?')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, FileNotFoundError) as e:
        print(f'Erro: {e}', file=sys.stderr)
        raise SystemExit(1)
