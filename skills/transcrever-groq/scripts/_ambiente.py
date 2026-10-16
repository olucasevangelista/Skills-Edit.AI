"""Sistema operacional, ambiente Python proprio da skill e checagem de dependencias.

Usa so a biblioteca padrao: este modulo roda em qualquer Python 3.10+, antes de groq/keyring existirem.
O ambiente (venv) fica numa pasta do usuario, fora de qualquer projeto, e e compartilhado por todos eles.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

APP = 'transcrever-groq'
NO_REEXEC = 'TRANSCREVER_GROQ_NO_REEXEC'  # evita laco de reexecucao
PYTHON_MINIMO = (3, 10)
REQUIREMENTS = Path(__file__).resolve().parents[1] / 'requirements.txt'


def sistema() -> str:
    if sys.platform.startswith('win'):
        return 'Windows'
    if sys.platform == 'darwin':
        return 'macOS'
    return 'Linux'


def pasta_app() -> Path:
    custom = os.environ.get('TRANSCREVER_GROQ_HOME')
    if custom:
        return Path(custom).expanduser()
    so = sistema()
    if so == 'Windows':
        base = os.environ.get('LOCALAPPDATA')
        return (Path(base) if base else Path.home() / 'AppData' / 'Local') / APP
    if so == 'macOS':
        return Path.home() / 'Library' / 'Application Support' / APP
    base = os.environ.get('XDG_DATA_HOME')
    return (Path(base) if base else Path.home() / '.local' / 'share') / APP


def pasta_venv() -> Path:
    return pasta_app() / 'venv'


def python_do_venv() -> Path:
    sub = ('Scripts', 'python.exe') if sistema() == 'Windows' else ('bin', 'python')
    return pasta_venv().joinpath(*sub)


def em_venv() -> bool:
    try:
        return Path(sys.prefix).resolve() == pasta_venv().resolve()
    except OSError:
        return False


def venv_pronto() -> bool:
    """True se o venv existe e tem groq e keyring instalados."""
    py = python_do_venv()
    if not py.is_file():
        return False
    r = subprocess.run([str(py), '-c', 'import groq, keyring'], capture_output=True)
    return r.returncode == 0


def checar_python() -> tuple[bool, str]:
    v = sys.version_info
    texto = f'Python {v.major}.{v.minor}.{v.micro}'
    if (v.major, v.minor) >= PYTHON_MINIMO:
        return True, texto
    hint = ('Instale uma versao nova em python.org ou com "brew install python".'
            if sistema() == 'macOS' else 'Instale uma versao nova em python.org (ou "winget install Python.Python.3.13").')
    return False, f'{texto} e antigo demais (precisa de 3.10 ou mais). {hint}'


def dica_ffmpeg() -> str:
    so = sistema()
    if so == 'Windows':
        return 'winget install Gyan.FFmpeg   (depois feche e abra o terminal)'
    if so == 'macOS':
        return 'brew install ffmpeg   (se nao tem o Homebrew: https://brew.sh)'
    return 'sudo apt install ffmpeg   (ou o gerenciador da sua distribuicao)'


def checar_ffmpeg() -> list[tuple[str, bool]]:
    return [(nome, shutil.which(nome) is not None) for nome in ('ffmpeg', 'ffprobe')]


def criar_venv(forcar: bool = False, log=print) -> None:
    """Cria o ambiente proprio e instala requirements.txt. Idempotente."""
    if forcar and pasta_venv().exists():
        shutil.rmtree(pasta_venv())
    if venv_pronto():
        log('Ambiente ja pronto: ' + str(pasta_venv()))
        return
    pasta_app().mkdir(parents=True, exist_ok=True)
    log('Criando ambiente Python proprio em ' + str(pasta_venv()) + ' ...')
    venv.EnvBuilder(with_pip=True, clear=False).create(str(pasta_venv()))
    py = str(python_do_venv())
    log('Instalando groq e keyring (pode levar um minuto) ...')
    r = subprocess.run([py, '-m', 'pip', 'install', '--disable-pip-version-check', '--quiet', '-r', str(REQUIREMENTS)],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        raise RuntimeError('Falha ao instalar as dependencias (verifique a internet):\n' + r.stderr.strip()[-1200:])
    if not venv_pronto():
        raise RuntimeError('As dependencias foram instaladas, mas groq/keyring nao carregam. Rode com --forcar para recriar.')
    log('Ambiente pronto.')


def reexecutar_no_venv(script: str, argv: list[str]) -> int:
    """Roda `script` no Python do venv, herdando terminal (entrada interativa funciona) e devolve o codigo de saida."""
    env = {**os.environ, NO_REEXEC: '1'}
    try:
        return subprocess.run([str(python_do_venv()), script, *argv], env=env).returncode
    except KeyboardInterrupt:
        return 130


def deve_reexecutar() -> bool:
    return not em_venv() and not os.environ.get(NO_REEXEC) and python_do_venv().is_file()
