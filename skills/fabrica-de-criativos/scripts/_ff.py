"""Utilitarios de FFmpeg e FFprobe (somente biblioteca padrao). Subprocessos sempre com lista de argumentos."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def configurar_saida() -> None:
    """Evita erro de acento no console do Windows."""
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, 'reconfigure'):
            s.reconfigure(errors='replace')


def exe(nome: str) -> str:
    achou = shutil.which(nome)
    if not achou:
        so = sys.platform
        dica = ('winget install Gyan.FFmpeg   (depois feche e abra o terminal)' if so.startswith('win')
                else 'brew install ffmpeg' if so == 'darwin' else 'sudo apt install ffmpeg')
        raise RuntimeError(f'{nome} nao encontrado no PATH. Instale o FFmpeg: {dica}')
    return achou


def rodar(args: list[str], capturar: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    r = subprocess.run(args, capture_output=capturar, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode:
        cauda = (r.stderr or '').strip()[-1800:]
        raise RuntimeError(f'{Path(args[0]).stem} falhou (codigo {r.returncode}):\n{cauda}')
    return r


def sonda(caminho: Path) -> dict:
    if not Path(caminho).is_file():
        raise FileNotFoundError(f'Arquivo nao encontrado: {caminho}')
    r = rodar([exe('ffprobe'), '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(caminho)])
    return json.loads(r.stdout)


def _fracao(txt: str) -> float:
    try:
        a, b = txt.split('/')
        return float(a) / float(b) if float(b) else 0.0
    except (ValueError, AttributeError):
        return 0.0


def info_basica(caminho: Path) -> dict:
    d = sonda(caminho)
    v = next((s for s in d['streams'] if s['codec_type'] == 'video'), None)
    a = next((s for s in d['streams'] if s['codec_type'] == 'audio'), None)
    rot = 0
    if v:
        for sd in v.get('side_data_list', []) or []:
            if 'rotation' in sd:
                rot = int(round(float(sd['rotation'])))
        rot = rot or int((v.get('tags') or {}).get('rotate', 0) or 0)
    fps_r = _fracao(v.get('r_frame_rate', '0/0')) if v else 0.0
    fps_m = _fracao(v.get('avg_frame_rate', '0/0')) if v else 0.0
    return {
        'duracao': float(d['format']['duration']),
        'tem_video': v is not None, 'tem_audio': a is not None,
        'largura': int(v['width']) if v else 0, 'altura': int(v['height']) if v else 0,
        'fps': fps_m or fps_r, 'fps_nominal': fps_r,
        'vfr': bool(v and fps_r and fps_m and abs(fps_r - fps_m) / fps_r > 0.02),
        'rotacao': rot, 'codec_video': v.get('codec_name') if v else None,
        'codec_audio': a.get('codec_name') if a else None,
        'taxa_audio': int(a.get('sample_rate', 0)) if a else 0,
    }


def envelope_db(caminho: Path, janela_ms: int = 10) -> list[float]:
    """Nivel RMS (dB) de cada janela de `janela_ms` ms do audio, calculado pelo proprio FFmpeg (rapido, sem numpy)."""
    n = int(16000 * janela_ms / 1000)
    # a conversao para 16 kHz mono precisa estar DENTRO da cadeia: opcoes -ac/-ar de saida entram depois dos filtros
    filtro = (f'aformat=sample_rates=16000:channel_layouts=mono,asetnsamples=n={n}:p=0,'
              'astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-')
    r = rodar([exe('ffmpeg'), '-v', 'error', '-i', str(caminho), '-vn', '-af', filtro, '-f', 'null', '-'])
    valores = []
    for linha in r.stdout.splitlines():
        if linha.startswith('lavfi.astats.Overall.RMS_level='):
            t = linha.split('=', 1)[1].strip()
            try:
                v = float(t)
            except ValueError:
                v = -120.0
            valores.append(max(v, -120.0) if v == v else -120.0)
    if not valores:
        raise RuntimeError('Nao consegui ler o volume do audio (o arquivo tem faixa de audio?).')
    return valores


def percentil(valores: list[float], p: float) -> float:
    s = sorted(valores)
    return s[min(len(s) - 1, max(0, int(round(p / 100 * (len(s) - 1)))))]


def flag_filtro_arquivo() -> str:
    """-/filter_complex (FFmpeg 7+) ou -filter_complex_script (antigo). Filtros grandes vao por arquivo
    porque o Windows limita o tamanho da linha de comando."""
    r = rodar([exe('ffmpeg'), '-hide_banner', '-h', 'full'], check=False)
    return '-/filter_complex' if '-/filter_complex' in (r.stdout or '') or 'deprecated, use -/filter_complex' in (r.stdout or '') \
        else '-filter_complex_script'


def perfil_video(qualidade: str = 'boa') -> list[str]:
    """Argumentos de codificacao H.264 (libx264). 'boa' (padrao): medium, CRF 18 | 'maxima': slow, CRF 16."""
    preset, crf = ('slow', '16') if qualidade == 'maxima' else ('medium', '18')
    return ['-c:v', 'libx264', '-preset', preset, '-crf', crf]


def sec(t: float) -> str:
    return f'{t:.3f}'.rstrip('0').rstrip('.') if t == t else 'nan'


def mmss(t: float) -> str:
    t = max(0.0, t)
    return f'{int(t // 60):02d}:{t % 60:05.2f}'
