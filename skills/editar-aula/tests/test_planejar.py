"""Testes do planejador de cortes com volumes sinteticos (sem video, sem rede)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import planejar_cortes as pc  # noqa: E402

J = pc.JANELA


def env_de(blocos, total):
    """blocos = [(inicio, fim)] com voz (-20 dB); resto silencio (-80 dB). total em segundos."""
    n = int(round(total / J))
    e = [-80.0] * n
    for a, b in blocos:
        for i in range(int(round(a / J)), int(round(b / J))):
            e[i] = -20.0
    return e


def final_gap(plano, i, faixas_a_fim, faixas_b_ini):
    """pausa audivel entre o ultimo som do trecho i e o primeiro som do i+1, no tempo final."""
    s1, s2 = plano['segmentos'][i], plano['segmentos'][i + 1]
    return (s1['fim'] - faixas_a_fim) + (faixas_b_ini - s2['ini']) - s1['d']


class FaixasDeFala(unittest.TestCase):
    def test_acha_trechos_fecha_buracos_e_ignora_estalos(self):
        env = env_de([(1.0, 3.0), (3.05, 4.0), (6.0, 6.02), (8.0, 9.0)], 10)   # buraco de 50 ms e estalo de 20 ms
        f = pc.faixas_de_fala(env, -46)
        self.assertEqual(len(f), 2)
        self.assertAlmostEqual(f[0][0], 1.0, places=2)
        self.assertAlmostEqual(f[0][1], 4.0, places=2)

    def test_limiar_automatico_fica_entre_menos46_e_menos38(self):
        self.assertEqual(pc.limiar_auto(env_de([(1, 2)], 5)), -46.0)         # piso muito baixo -> padrao
        self.assertEqual(pc.limiar_auto([-30.0] * 1000), -38.0)               # piso alto -> teto


class Pausas(unittest.TestCase):
    def setUp(self):
        self.params = pc.ESTILOS['aula']
        self.faixas = [(1.0, 5.0), (7.0, 12.0)]      # pausa de 2,0 s
        self.plano = pc.planejar(14.0, self.faixas, self.params)

    def test_pausa_longa_vira_a_pausa_final_do_estilo(self):
        self.assertEqual(len(self.plano['segmentos']), 2)
        g = final_gap(self.plano, 0, 5.0, 7.0)
        self.assertAlmostEqual(g, self.params['pausa_final'], places=2)

    def test_a_duracao_final_bate_com_a_soma_menos_as_sobreposicoes(self):
        segs = self.plano['segmentos']
        esperado = sum(s['fim'] - s['ini'] for s in segs) - sum(s['d'] for s in segs[:-1])
        self.assertAlmostEqual(self.plano['duracao_final'], esperado, places=2)
        self.assertLess(self.plano['duracao_final'], 14.0)

    def test_pausa_curta_nao_e_cortada(self):
        plano = pc.planejar(10.0, [(1.0, 3.0), (3.4, 6.0)], self.params)       # pausa 0,4 s < 0,55
        self.assertEqual(len(plano['segmentos']), 1)

    def test_estilo_curto_corta_mais(self):
        a = pc.planejar(14.0, [(1, 3), (3.5, 6), (6.6, 9)], pc.ESTILOS['aula'])
        b = pc.planejar(14.0, [(1, 3), (3.5, 6), (6.6, 9)], pc.ESTILOS['curto'])
        self.assertLess(b['duracao_final'], a['duracao_final'])

    def test_sem_fala_da_erro_claro(self):
        with self.assertRaises(ValueError):
            pc.planejar(5.0, [], self.params)


class Emendas(unittest.TestCase):
    def setUp(self):
        self.params = pc.ESTILOS['aula']
        # fala A (1-4), erro (5-8), fala B (9-12)
        self.faixas = [(1.0, 4.0), (5.0, 8.0), (9.0, 12.0)]

    def test_remover_erro_cria_emenda_com_sobreposicao_de_fala(self):
        plano = pc.planejar(14.0, self.faixas, self.params, remocoes=[(5.1, 8.2)])
        self.assertEqual(len(plano['segmentos']), 2)
        self.assertEqual(plano['segmentos'][0]['tipo'], 'emenda')
        g = final_gap(plano, 0, 4.0, 9.0)
        self.assertAlmostEqual(g, self.params['emenda_gap'], places=2)      # negativo: as vozes se sobrepoem
        self.assertLess(g, 0)
        self.assertAlmostEqual(plano['segmentos'][0]['d'], self.params['sobrep_emenda'], places=3)

    def test_proximo_trecho_comeca_colado_no_inicio_da_fala(self):
        plano = pc.planejar(14.0, self.faixas, self.params, remocoes=[(5.1, 8.2)])
        folga = 9.0 - plano['segmentos'][1]['ini']
        self.assertAlmostEqual(folga, pc.FOLGA, places=3)       # sem respiro antes da primeira palavra

    def test_o_trecho_anterior_so_termina_depois_da_ultima_palavra(self):
        plano = pc.planejar(14.0, self.faixas, self.params, remocoes=[(5.1, 8.2)])
        self.assertGreaterEqual(plano['segmentos'][0]['fim'], 4.0)

    def test_remocao_alinha_aos_limites_reais_mesmo_com_tempos_deslocados(self):
        # a transcricao erra em ~0,4 s: pede 5,5-8,6 em vez de 5,0-8,0
        plano = pc.planejar(14.0, self.faixas, self.params, remocoes=[(4.4, 8.5)])
        self.assertEqual(len(plano['segmentos']), 2)
        self.assertEqual(plano['remocoes_alinhadas'][0]['alinhado'], [4.0, 9.0])

    def test_remocao_que_nao_acha_pausa_gera_aviso(self):
        plano = pc.planejar(14.0, self.faixas, self.params, remocoes=[(20.0, 30.0)])
        self.assertTrue(any('alinhar' in a for a in plano['avisos']))
        self.assertTrue(all(sg['tipo'] != 'emenda' for sg in plano['segmentos']))   # nenhuma emenda de erro foi criada

    def test_trecho_curto_demais_e_unido_ao_vizinho(self):
        # uma palavra de 0,15 s entre duas pausas longas nao comporta sobreposicao nos dois lados
        faixas = [(1.0, 4.0), (6.0, 6.15), (8.0, 11.0)]
        plano = pc.planejar(13.0, faixas, self.params)
        for i, s in enumerate(plano['segmentos']):
            d_ant = plano['segmentos'][i - 1]['d'] if i else 0
            self.assertGreaterEqual(s['fim'] - s['ini'], 2 * max(s['d'], d_ant) + 0.05)


class Entradas(unittest.TestCase):
    def test_parse_de_remocoes(self):
        self.assertEqual(pc.parse_remocoes('62.0-71.5, 2:00-2:11'), [(62.0, 71.5), (120.0, 131.0)])
        self.assertEqual(pc.parse_remocoes(''), [])


if __name__ == '__main__':
    unittest.main()
