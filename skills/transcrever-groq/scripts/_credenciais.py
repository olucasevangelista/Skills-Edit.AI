"""Unico ponto que fala com o cofre de credenciais do sistema (keyring).

Windows -> Gerenciador de Credenciais | macOS -> Keychain (Acesso as Chaves).
A chave nunca e escrita em arquivo, nunca aparece em argumentos, logs ou mensagens de erro.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

# Identificador unico: o mesmo em todos os projetos. TRANSCREVER_GROQ_SERVICE existe so para os testes
# nao encostarem na chave real.
SERVICE = os.environ.get('TRANSCREVER_GROQ_SERVICE') or 'groq-api'
ACCOUNT = 'default'
ENV_VAR = 'GROQ_API_KEY'


class CofreErro(Exception):
    """Problema com o cofre. `tipo`: sem_biblioteca | sem_backend | bloqueado | falha."""

    def __init__(self, tipo: str, detalhe: str = '') -> None:
        super().__init__(tipo)
        self.tipo = tipo
        self.detalhe = detalhe


@dataclass
class Resultado:
    chave: str | None
    origem: str | None            # 'cofre' | 'variavel' | None
    aviso: str | None = None
    problema: CofreErro | None = None


def limpar_chave(texto: str | None) -> str:
    """Tira espacos, quebras de linha, aspas e um eventual 'GROQ_API_KEY=' colado junto."""
    t = ''.join((texto or '').lstrip('﻿').split())
    if t.upper().startswith(ENV_VAR + '='):
        t = t[len(ENV_VAR) + 1:]
    return t.strip('\'"')


def _so() -> str:
    from _ambiente import sistema
    return sistema()


def nome_do_cofre() -> str:
    return {'Windows': 'Gerenciador de Credenciais do Windows', 'macOS': 'Keychain (Acesso as Chaves) do macOS'}.get(
        _so(), 'cofre de credenciais do sistema')


def _kr():
    try:
        import keyring
        import keyring.errors  # noqa: F401
    except ImportError as error:
        raise CofreErro('sem_biblioteca') from error
    return keyring


def _traduzir(error: Exception, keyring) -> CofreErro:
    errors = keyring.errors
    if isinstance(error, errors.KeyringLocked):
        return CofreErro('bloqueado')
    if isinstance(error, errors.NoKeyringError):
        return CofreErro('sem_backend')
    # So o nome da classe: mensagens de backends nunca entram no texto mostrado ao usuario.
    return CofreErro('falha', type(error).__name__)


def _backend(keyring):
    backend = keyring.get_keyring()
    modulo = type(backend).__module__
    if modulo.startswith('keyring.backends.fail') or modulo.startswith('keyring.backends.null'):
        raise CofreErro('sem_backend')
    return backend


def ler_cofre() -> str | None:
    keyring = _kr()
    try:
        _backend(keyring)
        valor = keyring.get_password(SERVICE, ACCOUNT)
    except CofreErro:
        raise
    except Exception as error:  # noqa: BLE001 - qualquer falha do backend vira CofreErro
        raise _traduzir(error, keyring) from None
    return limpar_chave(valor) or None


def salvar_cofre(chave: str) -> None:
    keyring = _kr()
    try:
        _backend(keyring)
        keyring.set_password(SERVICE, ACCOUNT, chave)
        if keyring.get_password(SERVICE, ACCOUNT) != chave:
            raise CofreErro('falha', 'a leitura de volta nao confere')
    except CofreErro:
        raise
    except Exception as error:  # noqa: BLE001
        raise _traduzir(error, keyring) from None


def apagar_cofre() -> bool:
    """True se apagou, False se nao havia nada."""
    keyring = _kr()
    try:
        _backend(keyring)
        if keyring.get_password(SERVICE, ACCOUNT) is None:
            return False
        keyring.delete_password(SERVICE, ACCOUNT)
        return True
    except CofreErro:
        raise
    except keyring.errors.PasswordDeleteError:
        return False
    except Exception as error:  # noqa: BLE001
        raise _traduzir(error, keyring) from None


def obter_chave() -> Resultado:
    """Ordem: cofre do sistema, depois a variavel de ambiente GROQ_API_KEY."""
    problema = None
    try:
        chave = ler_cofre()
        if chave:
            return Resultado(chave, 'cofre')
    except CofreErro as error:
        problema = error
    env = limpar_chave(os.environ.get(ENV_VAR))
    if env:
        aviso = None
        if problema:
            aviso = (f'Aviso: o cofre do sistema esta indisponivel ({descrever(problema, curto=True)}); '
                     f'usando a variavel de ambiente {ENV_VAR}.')
        return Resultado(env, 'variavel', aviso=aviso, problema=problema)
    return Resultado(None, None, problema=problema)


def descrever(erro: CofreErro, curto: bool = False) -> str:
    so, cofre = _so(), nome_do_cofre()
    if erro.tipo == 'sem_biblioteca':
        return ('o componente keyring nao esta instalado neste Python' if curto else
                'O componente "keyring" nao esta instalado neste Python. Rode "python configurar.py setup" '
                '(ele prepara o ambiente sozinho).')
    if erro.tipo == 'bloqueado':
        if curto:
            return 'cofre bloqueado'
        if so == 'macOS':
            return ('O Keychain esta bloqueado ou negou acesso. Abra "Acesso as Chaves", desbloqueie o chaveiro "login" '
                    'e, quando o macOS perguntar, escolha "Sempre Permitir". Depois tente de novo.')
        return (f'O {cofre} esta bloqueado ou negou acesso. Entre normalmente na sua conta do Windows '
                '(sem sessao remota restrita) e tente de novo.')
    if erro.tipo == 'sem_backend':
        if curto:
            return 'nenhum cofre disponivel'
        if so == 'Linux':
            return ('Nenhum cofre de credenciais foi encontrado. Instale o gnome-keyring ou o KWallet, '
                    f'ou use a variavel de ambiente {ENV_VAR}.')
        return (f'O {cofre} nao esta acessivel nesta sessao (conexao SSH, conta sem perfil ou servico desativado). '
                f'Abra um terminal normal, ou use a variavel de ambiente {ENV_VAR}.')
    extra = f' ({erro.detalhe})' if erro.detalhe else ''
    return (f'O {cofre} retornou um erro{extra}.' if not curto else f'erro no cofre{extra}')


def mensagem_sem_chave(res: Resultado) -> str:
    base = 'Chave da Groq nao configurada.'
    if res.problema:
        base += ' ' + descrever(res.problema)
    return (base + ' Configure uma vez com:  python <pasta-da-skill>/scripts/configurar.py setup'
            f'  (ou defina a variavel de ambiente {ENV_VAR}).')
