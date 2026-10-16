"""Utilitarios locais de midia. Todos os subprocessos usam lista de argumentos, sem shell."""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
from pathlib import Path


def tempo(value: str) -> float:
    try:
        parts = value.replace(',', '.').split(':')
        if not 1 <= len(parts) <= 3:
            raise ValueError
        numbers = [float(x) for x in parts]
        if any(not math.isfinite(n) or n < 0 for n in numbers):
            raise ValueError
        if len(numbers) > 1 and any(n >= 60 for n in numbers[1:]):
            raise ValueError
        total = 0.0
        for n in numbers:
            total = total * 60 + n
        return total
    except ValueError as error:
        raise argparse.ArgumentTypeError('Use segundos, MM:SS ou HH:MM:SS, com valores positivos.') from error


def nome_seguro(value: str) -> str:
    cleaned = re.sub(r'[^\w.-]+', '-', value, flags=re.UNICODE).strip('.-')[:100]
    if not cleaned:
        raise ValueError('O nome precisa conter letras ou numeros.')
    if cleaned.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL', *(f'COM{i}' for i in range(1, 10)), *(f'LPT{i}' for i in range(1, 10))}:
        cleaned = 'video-' + cleaned
    return cleaned


def programa(name: str) -> str:
    found = shutil.which(name)
    if not found:
        raise RuntimeError(f'{name} nao encontrado no PATH. Instale o FFmpeg e reabra o terminal '
                           '(rode "python configurar.py ambiente" para ver o comando de instalacao).')
    return found


def executar(args: list[str]) -> str:
    result = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise RuntimeError(f'{Path(args[0]).name}: {result.stderr.strip()[-1600:]}')
    return result.stdout


def inspecionar(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f'Arquivo nao encontrado: {path}')
    return json.loads(executar([programa('ffprobe'), '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)]))


def gravar_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(path)
