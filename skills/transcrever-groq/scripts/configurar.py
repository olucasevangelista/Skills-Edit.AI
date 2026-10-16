#!/usr/bin/env python3
"""Configuracao unica da chave da Groq no cofre do sistema (Windows e macOS).

Comandos:
  ambiente   confere Python/FFmpeg e prepara o ambiente proprio (sem pedir chave)
  setup      prepara o ambiente e guarda a chave no cofre (digitada oculta; ou --stdin, para agentes)
  status     mostra se a chave esta configurada e de onde vem (nunca mostra a chave)
  update     troca a chave guardada
  remove     apaga a chave do cofre

A chave nunca passa por argumentos de linha de comando, arquivos ou logs.
Para agentes: printf '%s' "$CHAVE" | python configurar.py setup --stdin   (PowerShell: '$CHAVE' | python configurar.py setup --stdin)
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _ambiente as amb  # noqa: E402
import _credenciais as cred  # noqa: E402

PRECISA_VENV = {'setup', 'update', 'status', 'remove'}


def say(text: str = '') -> None:
    try:
        print(text, flush=True)
    except OSError:  # saida fechada (ex.: `| head`): nao e erro da ferramenta
        pass


def _interativo() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def sim_nao(pergunta: str, padrao: bool = False) -> bool:
    resposta = input(f'{pergunta} [{"S/n" if padrao else "s/N"}] ').strip().lower()
    return padrao if not resposta else resposta in {'s', 'sim', 'y', 'yes'}


# ---------------------------------------------------------------- ambiente
def relatorio_ambiente() -> bool:
    """Imprime o diagnostico. Devolve False se algo impede de continuar (Python antigo)."""
    say(f'Sistema: {amb.sistema()}')
    ok, texto = amb.checar_python()
    say(f'{"[ok]" if ok else "[ERRO]"} {texto}')
    for nome, achou in amb.checar_ffmpeg():
        say(f'{"[ok]" if achou else "[FALTA]"} {nome}')
    if not all(a for _, a in amb.checar_ffmpeg()):
        say('       Para instalar o FFmpeg:  ' + amb.dica_ffmpeg())
        say('       (a transcricao precisa dele para extrair o audio do video)')
    return ok


def cmd_ambiente(args: argparse.Namespace) -> int:
    if not relatorio_ambiente():
        return 1
    try:
        amb.criar_venv(forcar=args.forcar, log=say)
    except (RuntimeError, OSError) as error:
        say(f'[ERRO] {error}')
        return 1
    return 0


# ---------------------------------------------------------------- chave
def validar_na_groq(chave: str) -> str:
    """'valida' | 'invalida' | 'indeterminado'. Faz uma unica chamada leve (listar modelos)."""
    import groq
    client = groq.Groq(api_key=chave, timeout=20.0, max_retries=1)
    try:
        client.models.list()
        return 'valida'
    except groq.AuthenticationError:
        return 'invalida'
    except groq.PermissionDeniedError:
        return 'invalida'
    except Exception:  # noqa: BLE001 - sem rede, cota, etc.: nao da para afirmar nada
        return 'indeterminado'
    finally:
        client.close()


def pedir_chave() -> str | None:
    """Pede a chave oculta, valida e devolve (ou None se o usuario desistir)."""
    for tentativa in range(3):
        try:
            bruto = getpass.getpass('Cole sua chave da Groq (nao aparece enquanto voce cola) e tecle Enter: ')
        except (EOFError, KeyboardInterrupt):
            say('\nCancelado. Nada foi salvo.')
            return None
        chave = cred.limpar_chave(bruto)
        del bruto
        if not chave:
            say('Nada foi digitado. Tente de novo (ou Ctrl+C para sair).')
            continue
        if not chave.startswith('gsk_'):
            say('Aviso: chaves da Groq normalmente comecam com "gsk_". Confira se copiou a chave certa.')
        say('Conferindo a chave com a Groq ...')
        estado = validar_na_groq(chave)
        if estado == 'valida':
            say('[ok] A Groq aceitou a chave.')
            return chave
        if estado == 'invalida':
            say('[ERRO] A Groq recusou essa chave (invalida ou revogada). Gere outra em console.groq.com/keys.')
            continue
        say('Nao consegui validar agora (sem internet, limite de uso ou instabilidade).')
        if sim_nao('Salvar mesmo assim, sem validar?'):
            return chave
    say('Sem chave valida depois de 3 tentativas. Nada foi salvo.')
    return None


def chave_via_stdin(sem_validar: bool) -> tuple[str | None, int]:
    """Le a chave da entrada padrao (nunca de argumento), valida e devolve (chave, codigo_de_saida_se_falhar)."""
    chave = cred.limpar_chave(sys.stdin.read(4096))
    if not chave:
        say('[ERRO] Nenhuma chave foi recebida na entrada padrao.')
        return None, 1
    if not chave.startswith('gsk_'):
        say('Aviso: chaves da Groq normalmente comecam com "gsk_".')
    say('Conferindo a chave com a Groq ...')
    estado = validar_na_groq(chave)
    if estado == 'valida':
        say('[ok] A Groq aceitou a chave.')
        return chave, 0
    if estado == 'invalida':
        say('[ERRO] A Groq recusou essa chave (invalida ou revogada). Nada foi salvo. Gere outra em console.groq.com/keys.')
        return None, 1
    if sem_validar:
        say('Nao consegui validar agora; guardando sem validar, como pedido.')
        return chave, 0
    say('[ERRO] Nao consegui validar a chave agora (sem internet, limite de uso ou instabilidade). Nada foi salvo.')
    say('       Tente de novo; se a internet esta ok, repita com --salvar-sem-validar.')
    return None, 3


def cmd_setup(args: argparse.Namespace) -> int:
    trocar = args.comando == 'update'
    via_stdin = bool(getattr(args, 'stdin', False))
    if not via_stdin and not _interativo():
        say('[ERRO] Sem terminal interativo. Rode num terminal normal (PowerShell / Terminal) para digitar a chave oculta,')
        say('       ou use --stdin e envie a chave pela entrada padrao (e assim que um agente configura).')
        say('       Nunca passe a chave como argumento de comando.')
        return 1
    say(f'Sistema: {amb.sistema()}  |  Cofre: {cred.nome_do_cofre()}')
    try:
        atual = cred.ler_cofre()
    except cred.CofreErro as erro:
        say('[ERRO] ' + cred.descrever(erro))
        return 2
    if atual and not trocar:
        say('A chave ja esta configurada neste computador. Para substituir, rode:  configurar.py update')
        return 0
    if atual and trocar and not via_stdin and not sim_nao('Ja existe uma chave guardada. Substituir pela nova?'):
        say('Mantida a chave atual.')
        return 0
    if via_stdin:
        chave, falha = chave_via_stdin(bool(getattr(args, 'salvar_sem_validar', False)))
    else:
        chave, falha = pedir_chave(), 1
    if not chave:
        return falha
    try:
        cred.salvar_cofre(chave)
    except cred.CofreErro as erro:
        say('[ERRO] Nao consegui guardar a chave. ' + cred.descrever(erro))
        return 2
    finally:
        del chave
    say(f'[ok] Chave guardada no {cred.nome_do_cofre()}.')
    say('Pronto: nas proximas vezes basta rodar a transcricao. Nao precisa configurar de novo, em nenhum projeto.')
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    res = cred.obter_chave()
    if res.aviso:
        print(res.aviso, file=sys.stderr)
    if args.json:
        print(json.dumps({
            'configurada': bool(res.chave),
            'origem': res.origem,
            'problema_no_cofre': res.problema.tipo if res.problema else None,
            'ambiente_pronto': amb.venv_pronto(),
            'sistema': amb.sistema(),
        }, ensure_ascii=False))
    else:
        if res.chave:
            onde = ('cofre do sistema (' + cred.nome_do_cofre() + ')') if res.origem == 'cofre' else \
                f'variavel de ambiente {cred.ENV_VAR}'
            say(f'[ok] Chave da Groq configurada. Origem: {onde}.')
        else:
            say('[FALTA] ' + cred.mensagem_sem_chave(res))
        say(('[ok]' if amb.venv_pronto() else '[FALTA]') + ' ambiente proprio (groq + keyring)'
            + ('' if amb.venv_pronto() else '  -> rode: configurar.py setup'))
    if res.chave:
        return 0
    return 2 if res.problema and res.problema.tipo in {'bloqueado', 'sem_backend', 'falha'} else 1


def cmd_remove(args: argparse.Namespace) -> int:
    if not args.sim and not sim_nao('Apagar a chave da Groq guardada no cofre deste computador?'):
        say('Nada foi apagado.')
        return 0
    try:
        apagou = cred.apagar_cofre()
    except cred.CofreErro as erro:
        say('[ERRO] ' + cred.descrever(erro))
        return 2
    say('[ok] Chave removida do cofre.' if apagou else 'Nao havia chave guardada no cofre.')
    if os.environ.get(cred.ENV_VAR):
        say(f'Obs.: a variavel de ambiente {cred.ENV_VAR} continua definida nesta sessao.')
    return 0


# ---------------------------------------------------------------- main
def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='comando', required=True)
    a = sub.add_parser('ambiente', help='confere Python/FFmpeg e prepara o ambiente proprio')
    a.add_argument('--forcar', action='store_true', help='recria o ambiente do zero')
    for nome, ajuda in (('setup', 'prepara o ambiente e guarda a chave (primeira vez)'), ('update', 'troca a chave guardada')):
        c = sub.add_parser(nome, help=ajuda)
        c.add_argument('--stdin', action='store_true',
                       help='le a chave da entrada padrao (para agentes: nao usa argumento de comando nem pede digitacao)')
        c.add_argument('--salvar-sem-validar', action='store_true',
                       help='com --stdin: guarda mesmo se a Groq nao puder ser consultada agora (sem internet)')
    s = sub.add_parser('status', help='mostra se a chave esta configurada (sem revelar)')
    s.add_argument('--json', action='store_true', help='saida em JSON, para agentes')
    r = sub.add_parser('remove', help='apaga a chave do cofre')
    r.add_argument('--sim', action='store_true', help='nao pergunta confirmacao')
    return p


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(errors='replace')
    args = parser().parse_args()
    if args.comando == 'ambiente':
        return cmd_ambiente(args)

    # Os demais comandos usam keyring/groq: rodam no ambiente proprio.
    if amb.deve_reexecutar() and amb.venv_pronto():
        return amb.reexecutar_no_venv(str(Path(__file__).resolve()), sys.argv[1:])
    if args.comando in {'setup', 'update'} and not amb.em_venv():
        if not relatorio_ambiente():
            return 1
        try:
            amb.criar_venv(log=say)
        except (RuntimeError, OSError) as error:
            say(f'[ERRO] {error}')
            return 1
        return amb.reexecutar_no_venv(str(Path(__file__).resolve()), sys.argv[1:])

    return {'setup': cmd_setup, 'update': cmd_setup, 'status': cmd_status, 'remove': cmd_remove}[args.comando](args)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print('\nInterrompido.', file=sys.stderr)
        raise SystemExit(130)
