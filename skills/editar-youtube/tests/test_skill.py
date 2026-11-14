"""Testes da propria skill editar-youtube: frontmatter, referencias, independencia de outras skills e scripts em dia."""
import re
import unittest
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
SKILLS = RAIZ.parent
SKILL_MD = (RAIZ / 'SKILL.md').read_text(encoding='utf-8')


def ler(p: Path) -> str:
    return p.read_text(encoding='utf-8')


def textos_da_skill():
    for p in RAIZ.rglob('*'):
        if p.is_file() and p.suffix in {'.md'} and '__pycache__' not in p.parts:
            yield p, ler(p)


class Skill(unittest.TestCase):
    def test_frontmatter_valido(self):
        partes = SKILL_MD.split('---')
        d = yaml.safe_load(partes[1])
        self.assertEqual(d['name'], 'editar-youtube')
        self.assertLessEqual(len(d['description']), 1024)
        self.assertIn('YouTube', d['description'])

    def test_todas_as_referencias_existem_e_estao_listadas(self):
        citadas = set(re.findall(r'references/([\w-]+\.md)', SKILL_MD))
        existentes = {p.name for p in (RAIZ / 'references').glob('*.md')}
        self.assertEqual(citadas, existentes)

    def test_scripts_citados_existem(self):
        for nome in set(re.findall(r'scripts/([\w]+\.(?:py|mjs))', SKILL_MD)):
            self.assertTrue((RAIZ / 'scripts' / nome).exists(), nome)

    def test_links_internos_das_referencias_existem(self):
        for p, t in textos_da_skill():
            for nome in re.findall(r'`((?:abertura|meio-e-ritmo|chamadas-para-seguir|limpeza|exportacao|tipos-de-video))\.md`', t):
                self.assertTrue((RAIZ / 'references' / f'{nome}.md').exists(), f'{p.name} cita {nome}.md')

    def test_nao_cita_outras_skills_alem_da_transcricao_e_do_remotion(self):
        proibidas = r'smart-cuts|editar-aula|editar-reels|creative-lab|fabrica-de-criativos|copystyle|raio-x|motion-designer'
        for p, t in textos_da_skill():
            if p.name == 'README.md':
                continue   # o README compara com a base de limpeza das skills irmas
            self.assertIsNone(re.search(proibidas, t), f'{p.name} cita outra skill')

    def test_sem_segredos_nem_termos_proibidos(self):
        for p, t in textos_da_skill():
            self.assertIsNone(re.search(r'gsk_[A-Za-z0-9]{20,}|nubank|inter-conceito', t, re.I), p.name)

    def test_a_direcao_pedida_esta_escrita(self):
        abertura = ler(RAIZ / 'references' / 'abertura.md')
        self.assertIn('5 a 10 segundos', abertura)
        self.assertIn('print', abertura)
        self.assertIn('link', abertura)         # o aviso de que a transcricao troca "print" por "link"
        chamadas = ler(RAIZ / 'references' / 'chamadas-para-seguir.md')
        self.assertIn('20 a 25%', chamadas)
        self.assertIn('70 a 75%', chamadas)
        self.assertIn('no máximo aos 2', chamadas)
        meio = ler(RAIZ / 'references' / 'meio-e-ritmo.md')
        self.assertIn('momentos-chave', meio.lower())
        self.assertIn('sobreposição', meio)

    def test_a_skill_nao_impoe_elementos(self):
        """Nenhuma cor em hexadecimal nem nome de fonte e sugerido pela skill."""
        for p, t in textos_da_skill():
            self.assertIsNone(re.search(r'#[0-9A-Fa-f]{6}\b', t), f'{p.name} sugere cor')


class ScriptsEmDia(unittest.TestCase):
    """Os scripts de corte sao copias da Fabrica de Criativos (a versao com o limiar corrigido): nao podem divergir."""
    IRMA = SKILLS / 'fabrica-de-criativos' / 'scripts'

    @unittest.skipUnless(IRMA.exists(), 'a Fabrica de Criativos nao esta ao lado (skill instalada sozinha)')
    def test_scripts_de_corte_iguais_aos_da_fabrica(self):
        for nome in ('planejar_cortes.py', 'montar.py', 'verificar_cortes.py', 'achar_repeticoes.py', '_ff.py'):
            a = (RAIZ / 'scripts' / nome).read_text(encoding='utf-8').replace('\r\n', '\n')
            b = (self.IRMA / nome).read_text(encoding='utf-8').replace('\r\n', '\n')
            self.assertEqual(a, b, f'{nome} divergiu da versao da Fabrica de Criativos')


if __name__ == '__main__':
    unittest.main(verbosity=2)
