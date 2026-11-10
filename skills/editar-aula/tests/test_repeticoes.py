"""Testes do detector de repeticoes (achar_repeticoes.py) com transcricoes sinteticas. Sem video, sem rede."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import achar_repeticoes as ar  # noqa: E402


class Repeticoes(unittest.TestCase):
    @staticmethod
    def palavras(takes, passo=0.3):
        """takes = [(inicio, 'texto')] -> transcricao.json minima."""
        words = []
        for ini, txt in takes:
            for k, w in enumerate(txt.split()):
                words.append(dict(word=w, start=round(ini + k * passo, 3), end=round(ini + k * passo + passo - 0.05, 3)))
        return dict(words=words)

    def test_tres_tentativas_ficam_com_a_ultima(self):
        d = self.palavras([(1, 'Olá pessoal hoje eu mostro tudo'), (10, 'A melhor parte é que você'),
                           (14, 'A melhor parte é que a skill tira todos os'),
                           (20, 'A melhor parte é que a skill tira todos os silêncios sozinha'), (30, 'No final você publica')])
        r = ar.analisar(d)
        self.assertEqual(len(r['grupos']), 1)
        g = r['grupos'][0]
        self.assertEqual(len(g['tentativas']), 3)
        self.assertEqual(g['tentativas'][g['escolhida'] - g['tentativas'][0]['take']]['ini'], 20.0)
        self.assertAlmostEqual(g['remover'][1], 20.0, places=1)
        self.assertGreater(g['remover'][0], 1.5)   # comeca depois do fim da fala anterior

    def test_ultima_mais_curta_gera_aviso(self):
        d = self.palavras([(1, 'A melhor parte é que a skill tira todos os silêncios sozinha agora'), (10, 'A melhor parte é que você')])
        r = ar.analisar(d)
        self.assertTrue(r['grupos'][0]['avisos'])

    def test_controle_negativo_takes_diferentes_nao_agrupam(self):
        d = self.palavras([(1, 'Primeiro a gente grava o vídeo bruto'), (8, 'Depois o agente tira os silêncios'), (15, 'No final você revisa e publica')])
        r = ar.analisar(d)
        self.assertEqual(r['grupos'], [])
        self.assertEqual(r['reinicios_internos'], [])

    def test_aberturas_comuns_de_duas_palavras_nao_agrupam(self):
        d = self.palavras([(1, 'E então a gente grava o vídeo'), (8, 'E então você revisa tudo no final')])
        self.assertEqual(ar.analisar(d)['grupos'], [])

    def test_tentativas_muito_distantes_nao_agrupam(self):
        d = self.palavras([(1, 'A melhor parte é que você'), (400, 'A melhor parte é que a skill tira tudo')])
        self.assertEqual(ar.analisar(d, janela=120)['grupos'], [])

    def test_reinicio_no_meio_da_fala_sem_pausa(self):
        d = self.palavras([(1, 'Então a gente começa A melhor parte é que você A melhor parte é que a skill tira os silêncios')], passo=0.2)
        # sem pausa entre as palavras: tudo e um take so; "a melhor parte e que" aparece duas vezes
        r = ar.analisar(d)
        self.assertEqual(len(r['reinicios_internos']), 1)
        ri = r['reinicios_internos'][0]
        self.assertAlmostEqual(ri['recomeca_em'], 1 + 10 * 0.2, places=1)     # a 2a "A melhor parte" e a 11a palavra
        self.assertAlmostEqual(ri['remover'][0], 1 + 4 * 0.2 - 0.05 + 0.0, places=1)   # fim da palavra anterior ao 1o "A melhor"

    def test_controle_negativo_estrutura_paralela_nao_e_reinicio(self):
        d = self.palavras([(1, 'Primeiro a gente vai gravar o vídeo depois a gente vai editar tudo com a skill')], passo=0.2)
        self.assertEqual(ar.analisar(d)['reinicios_internos'], [])

    def test_variacao_de_grafia_do_whisper_ainda_agrupa(self):
        d = self.palavras([(1, 'Claude Code é uma ferramenta'), (8, 'Cloud Code é uma ferramenta que edita sozinha')])
        self.assertEqual(len(ar.analisar(d)['grupos']), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
