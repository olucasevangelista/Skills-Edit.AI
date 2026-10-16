"""Testes do cofre de credenciais e do assistente. Nenhum teste toca na chave real do usuario:
usam um cofre em memoria. O teste de cofre REAL (Windows/macOS) so roda com RUN_REAL_KEYRING=1 e usa um
servico descartavel que e apagado no final.

Rode com o Python do ambiente da skill (precisa de keyring e groq):
    <venv>/python -m unittest discover -s tests -v
"""
import argparse
import contextlib
import io
import os
import re
import sys
import unittest
import uuid
from pathlib import Path
from unittest import mock

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / 'scripts'))

import keyring  # noqa: E402
import keyring.backend  # noqa: E402
import keyring.backends.fail  # noqa: E402
import keyring.errors  # noqa: E402

import _credenciais as cred  # noqa: E402
import configurar  # noqa: E402

CHAVE = 'gsk_' + 'A1b2C3d4' * 6          # chave FALSA, so para teste
OUTRA = 'gsk_' + 'Z9y8X7w6' * 6


class Memoria(keyring.backend.KeyringBackend):
    priority = 1
    viable = False        # subclasses se auto-registram no keyring; assim nao entram na selecao do cofre real

    def __init__(self):
        super().__init__()
        self.d = {}

    def get_password(self, service, username):
        return self.d.get((service, username))

    def set_password(self, service, username, password):
        self.d[(service, username)] = password

    def delete_password(self, service, username):
        if (service, username) not in self.d:
            raise keyring.errors.PasswordDeleteError('nao existe')
        del self.d[(service, username)]


class Bloqueado(Memoria):
    def get_password(self, service, username):
        raise keyring.errors.KeyringLocked('cofre bloqueado')


class FalhaAoGravar(Memoria):
    def set_password(self, service, username, password):
        raise keyring.errors.PasswordSetError(f'erro interno com {password}')   # o segredo NAO pode vazar


class Base(unittest.TestCase):
    backend_cls = Memoria

    def setUp(self):
        self._antes = keyring.get_keyring()
        self.backend = self.backend_cls()
        keyring.set_keyring(self.backend)
        self._env = mock.patch.dict(os.environ, {}, clear=False)
        self._env.start()
        os.environ.pop('GROQ_API_KEY', None)

    def tearDown(self):
        self._env.stop()
        keyring.set_keyring(self._antes)

    def saida(self, fn, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = fn(*args)
        return code, out.getvalue() + err.getvalue()


class LimpezaDaChave(unittest.TestCase):
    def test_remove_espacos_aspas_e_prefixo(self):
        for bruto in (f'  {CHAVE}\n', f'"{CHAVE}"', f"'{CHAVE}'", f'GROQ_API_KEY={CHAVE}', f'{CHAVE[:10]} {CHAVE[10:]}\r\n'):
            self.assertEqual(cred.limpar_chave(bruto), CHAVE)
        self.assertEqual(cred.limpar_chave(None), '')
        self.assertEqual(cred.limpar_chave('   '), '')


class CofreEmMemoria(Base):
    def test_salvar_ler_apagar(self):
        self.assertIsNone(cred.ler_cofre())
        cred.salvar_cofre(CHAVE)
        self.assertEqual(cred.ler_cofre(), CHAVE)
        self.assertEqual(self.backend.d[(cred.SERVICE, cred.ACCOUNT)], CHAVE)
        self.assertTrue(cred.apagar_cofre())
        self.assertIsNone(cred.ler_cofre())
        self.assertFalse(cred.apagar_cofre())

    def test_identificador_e_unico_e_estavel(self):
        self.assertEqual((cred.SERVICE, cred.ACCOUNT), ('groq-api', 'default'))

    def test_cofre_tem_prioridade_sobre_variavel(self):
        cred.salvar_cofre(CHAVE)
        os.environ['GROQ_API_KEY'] = OUTRA
        r = cred.obter_chave()
        self.assertEqual((r.chave, r.origem), (CHAVE, 'cofre'))

    def test_variavel_de_ambiente_como_alternativa(self):
        os.environ['GROQ_API_KEY'] = f' "{OUTRA}" '
        r = cred.obter_chave()
        self.assertEqual((r.chave, r.origem, r.aviso), (OUTRA, 'variavel', None))

    def test_sem_nada_configurado(self):
        r = cred.obter_chave()
        self.assertIsNone(r.chave)
        self.assertIn('nao configurada', cred.mensagem_sem_chave(r))
        self.assertIn('configurar.py setup', cred.mensagem_sem_chave(r))


class CofreBloqueado(Base):
    backend_cls = Bloqueado

    def test_bloqueado_sem_variavel(self):
        r = cred.obter_chave()
        self.assertIsNone(r.chave)
        self.assertEqual(r.problema.tipo, 'bloqueado')
        self.assertIn('bloqueado', cred.mensagem_sem_chave(r))
        code, _ = self.saida(configurar.cmd_status, argparse.Namespace(json=False))
        self.assertEqual(code, 2)

    def test_bloqueado_mas_com_variavel_usa_variavel_e_avisa(self):
        os.environ['GROQ_API_KEY'] = OUTRA
        r = cred.obter_chave()
        self.assertEqual((r.chave, r.origem), (OUTRA, 'variavel'))
        self.assertIn('cofre', r.aviso)
        self.assertNotIn(OUTRA, r.aviso)


class FalhaGravacao(Base):
    backend_cls = FalhaAoGravar

    def test_erro_ao_gravar_nao_vaza_a_chave(self):
        with self.assertRaises(cred.CofreErro) as ctx:
            cred.salvar_cofre(CHAVE)
        texto = cred.descrever(ctx.exception) + ctx.exception.detalhe + str(ctx.exception)
        self.assertNotIn(CHAVE, texto)
        self.assertEqual(ctx.exception.detalhe, 'PasswordSetError')


class SemBackend(Base):
    def setUp(self):
        super().setUp()
        keyring.set_keyring(keyring.backends.fail.Keyring())

    def test_sem_backend_e_reportado(self):
        with self.assertRaises(cred.CofreErro) as ctx:
            cred.ler_cofre()
        self.assertEqual(ctx.exception.tipo, 'sem_backend')
        code, texto = self.saida(configurar.cmd_status, argparse.Namespace(json=True))
        self.assertEqual(code, 2)
        self.assertIn('"problema_no_cofre": "sem_backend"', texto)


class AssistenteNaoVazaChave(Base):
    def test_status_nunca_imprime_a_chave(self):
        cred.salvar_cofre(CHAVE)
        for js in (False, True):
            code, texto = self.saida(configurar.cmd_status, argparse.Namespace(json=js))
            self.assertEqual(code, 0)
            self.assertNotIn(CHAVE, texto)
            self.assertNotIn(CHAVE[:8], texto)
        os.environ['GROQ_API_KEY'] = OUTRA
        _, texto = self.saida(configurar.cmd_status, argparse.Namespace(json=False))
        self.assertNotIn(OUTRA[:8], texto)

    def test_setup_salva_depois_de_validar(self):
        with mock.patch.object(configurar, '_interativo', return_value=True), \
             mock.patch('getpass.getpass', return_value=f'  "{CHAVE}"\n'), \
             mock.patch.object(configurar, 'validar_na_groq', return_value='valida'):
            code, texto = self.saida(configurar.cmd_setup, argparse.Namespace(comando='setup'))
        self.assertEqual(code, 0)
        self.assertEqual(cred.ler_cofre(), CHAVE)
        self.assertNotIn(CHAVE, texto)

    def test_chave_recusada_pela_groq_nao_e_salva(self):
        with mock.patch.object(configurar, '_interativo', return_value=True), \
             mock.patch('getpass.getpass', return_value=CHAVE), \
             mock.patch.object(configurar, 'validar_na_groq', return_value='invalida'):
            code, texto = self.saida(configurar.cmd_setup, argparse.Namespace(comando='setup'))
        self.assertEqual(code, 1)
        self.assertIsNone(cred.ler_cofre())
        self.assertNotIn(CHAVE, texto)

    def test_sem_conexao_pergunta_antes_de_salvar(self):
        with mock.patch.object(configurar, '_interativo', return_value=True), \
             mock.patch('getpass.getpass', return_value=CHAVE), \
             mock.patch.object(configurar, 'validar_na_groq', return_value='indeterminado'), \
             mock.patch('builtins.input', return_value='n'):
            code, _ = self.saida(configurar.cmd_setup, argparse.Namespace(comando='setup'))
        self.assertIsNone(cred.ler_cofre())
        with mock.patch.object(configurar, '_interativo', return_value=True), \
             mock.patch('getpass.getpass', return_value=CHAVE), \
             mock.patch.object(configurar, 'validar_na_groq', return_value='indeterminado'), \
             mock.patch('builtins.input', return_value='s'):
            code, _ = self.saida(configurar.cmd_setup, argparse.Namespace(comando='setup'))
        self.assertEqual(code, 0)
        self.assertEqual(cred.ler_cofre(), CHAVE)

    def test_update_substitui_somente_apos_confirmar(self):
        cred.salvar_cofre(CHAVE)
        with mock.patch.object(configurar, '_interativo', return_value=True), \
             mock.patch('getpass.getpass', return_value=OUTRA), \
             mock.patch.object(configurar, 'validar_na_groq', return_value='valida'), \
             mock.patch('builtins.input', return_value='n'):
            self.saida(configurar.cmd_setup, argparse.Namespace(comando='update'))
        self.assertEqual(cred.ler_cofre(), CHAVE)
        with mock.patch.object(configurar, '_interativo', return_value=True), \
             mock.patch('getpass.getpass', return_value=OUTRA), \
             mock.patch.object(configurar, 'validar_na_groq', return_value='valida'), \
             mock.patch('builtins.input', return_value='s'):
            self.saida(configurar.cmd_setup, argparse.Namespace(comando='update'))
        self.assertEqual(cred.ler_cofre(), OUTRA)

    def test_setup_sem_terminal_interativo_recusa(self):
        with mock.patch.object(configurar, '_interativo', return_value=False):
            code, texto = self.saida(configurar.cmd_setup, argparse.Namespace(comando='setup'))
        self.assertEqual(code, 1)
        self.assertIn('terminal interativo', texto)

    def test_remove(self):
        cred.salvar_cofre(CHAVE)
        code, _ = self.saida(configurar.cmd_remove, argparse.Namespace(sim=True))
        self.assertEqual(code, 0)
        self.assertIsNone(cred.ler_cofre())


class ConfiguracaoPorAgenteViaStdin(Base):
    """Fluxo para agentes: a chave chega pela entrada padrao (nunca por argumento) e nao precisa de terminal interativo."""

    def rodar(self, entrada, estado, comando='setup', sem_validar=False):
        ns = argparse.Namespace(comando=comando, stdin=True, salvar_sem_validar=sem_validar)
        with mock.patch('sys.stdin', io.StringIO(entrada)):
            with mock.patch.object(configurar, '_interativo', return_value=False):
                with mock.patch.object(configurar, 'validar_na_groq', return_value=estado):
                    return self.saida(configurar.cmd_setup, ns)

    def test_chave_valida_e_salva_mesmo_sem_terminal(self):
        code, texto = self.rodar('﻿' + CHAVE + '\r\n', 'valida')      # BOM + CRLF como o PowerShell envia
        self.assertEqual(code, 0)
        self.assertEqual(cred.ler_cofre(), CHAVE)
        self.assertNotIn(CHAVE, texto)
        self.assertNotIn(CHAVE[:8], texto)

    def test_chave_recusada_pela_groq_nao_salva(self):
        code, texto = self.rodar(CHAVE, 'invalida')
        self.assertEqual(code, 1)
        self.assertIsNone(cred.ler_cofre())
        self.assertNotIn(CHAVE, texto)

    def test_sem_conexao_nao_salva_por_padrao_e_salva_com_flag(self):
        code, _ = self.rodar(CHAVE, 'indeterminado')
        self.assertEqual(code, 3)
        self.assertIsNone(cred.ler_cofre())
        code, _ = self.rodar(CHAVE, 'indeterminado', sem_validar=True)
        self.assertEqual(code, 0)
        self.assertEqual(cred.ler_cofre(), CHAVE)

    def test_entrada_vazia(self):
        code, texto = self.rodar('  \n', 'valida')
        self.assertEqual(code, 1)
        self.assertIn('Nenhuma chave', texto)
        self.assertIsNone(cred.ler_cofre())

    def test_setup_com_chave_existente_nao_sobrescreve_mas_update_sim(self):
        cred.salvar_cofre(CHAVE)
        code, _ = self.rodar(OUTRA, 'valida', comando='setup')
        self.assertEqual(code, 0)
        self.assertEqual(cred.ler_cofre(), CHAVE)
        code, _ = self.rodar(OUTRA, 'valida', comando='update')
        self.assertEqual(code, 0)
        self.assertEqual(cred.ler_cofre(), OUTRA)

    def test_falha_do_cofre_retorna_2_sem_vazar(self):
        keyring.set_keyring(FalhaAoGravar())
        code, texto = self.rodar(CHAVE, 'valida')
        self.assertEqual(code, 2)
        self.assertNotIn(CHAVE, texto)


class Higiene(unittest.TestCase):
    def test_nenhuma_chave_real_no_codigo_ou_docs(self):
        padrao = re.compile(r'gsk_[A-Za-z0-9]{20,}')
        for caminho in SKILL.rglob('*'):
            if caminho.is_file() and 'tests' not in caminho.parts and caminho.suffix in {'.py', '.md', '.txt', '.json'}:
                self.assertIsNone(padrao.search(caminho.read_text(encoding='utf-8')), str(caminho))

    def test_sem_dependencia_do_projeto_original(self):
        proibidos = ('cortes', 'editar-video', 'dotenv', 'load_dotenv')
        for caminho in (SKILL / 'scripts').glob('*.py'):
            texto = caminho.read_text(encoding='utf-8').lower()
            for p in proibidos:
                self.assertNotIn(p, texto, f'{caminho.name} menciona {p}')


@unittest.skipUnless(os.environ.get('RUN_REAL_KEYRING') == '1', 'defina RUN_REAL_KEYRING=1 para testar o cofre real do SO')
class CofreRealDoSistema(unittest.TestCase):
    def test_ida_e_volta_no_cofre_do_sistema(self):
        servico = f'groq-api-TEST-{uuid.uuid4().hex[:10]}'
        with mock.patch.object(cred, 'SERVICE', servico):
            try:
                print(f'\n[cofre real] backend: {type(keyring.get_keyring()).__module__}.{type(keyring.get_keyring()).__name__}')
                self.assertIsNone(cred.ler_cofre())
                cred.salvar_cofre(CHAVE)
                self.assertEqual(cred.ler_cofre(), CHAVE)
                self.assertEqual(cred.obter_chave().origem, 'cofre')
                cred.salvar_cofre(OUTRA)                    # update
                self.assertEqual(cred.ler_cofre(), OUTRA)
            finally:
                cred.apagar_cofre()
            self.assertIsNone(cred.ler_cofre())


if __name__ == '__main__':
    unittest.main()
