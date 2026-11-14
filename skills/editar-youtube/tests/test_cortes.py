"""Testes da limpeza de fala (planejar_cortes, montar, verificar_cortes) e do detector de repeticoes.
Usam audio sintetico (rajadas de tom como "fala", ruido de sala e pausas conhecidas). Precisam de ffmpeg e ffprobe."""
import json
import math
import random
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import achar_repeticoes as ar  # noqa: E402
import planejar_cortes as pc  # noqa: E402

TEM_FF = bool(shutil.which('ffmpeg') and shutil.which('ffprobe'))
SR = 16000


def py(script, *args):
    return subprocess.run([sys.executable, '-I', str(SCRIPTS / script), *map(str, args)], capture_output=True, text=True,
                          encoding='utf-8', errors='replace')


def db(x):
    return 10 ** (x / 20)


def gravacao_sintetica(destino: Path, ruido_db: float, falas, total: float):
    """mp4 (imagem + audio). `falas` = [(inicio, fim)]: rajadas de tom com envelope suave ("voz") sobre ruido de sala."""
    rnd = random.Random(7)
    n = int(total * SR)
    x = [0.0] * n
    for ini, fim in falas:
        a, b = int(ini * SR), int(fim * SR)
        for i in range(a, min(n, b)):
            t = i / SR
            env = min(1.0, (i - a) / (0.02 * SR), (b - i) / (0.03 * SR))
            # sílabas: modulacao de ~4 Hz que nunca zera (a voz real tem vales curtos)
            x[i] = db(-16) * env * (0.65 + 0.35 * math.sin(2 * math.pi * 4 * t)) * math.sin(2 * math.pi * 180 * t)
    ruido = [rnd.gauss(0, 1) for _ in range(n)]
    media = [sum(ruido[max(0, i - 3):i + 4]) / 7 for i in range(n)]
    rms = math.sqrt(sum(v * v for v in media) / n)
    g = db(ruido_db) / rms
    sinal = [max(-1.0, min(1.0, x[i] + media[i] * g)) for i in range(n)]
    wav = destino.with_suffix('.wav')
    with wave.open(str(wav), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(struct.pack(f'<{n}h', *[int(v * 32767) for v in sinal]))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'testsrc2=size=320x568:rate=30:duration={total}',
                    '-i', str(wav), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '28', '-c:a', 'aac', '-shortest', str(destino)],
                   check=True)
    return destino


# 6 frases, pausas de 0,6 a 1,1 s entre elas (as que o editor "sente" como quebra de ritmo)
FALAS = [(0.8, 3.0), (3.8, 6.4), (7.2, 9.0), (9.6, 12.5), (13.4, 15.0), (15.7, 18.0)]
TOTAL = 19.0


def pausas_de(faixas):
    return [b[0] - a[1] for a, b in zip(faixas, faixas[1:])]


class Limiar(unittest.TestCase):
    def env(self, piso, fala, n_fala=300, n_pausa=300):
        return [fala] * n_fala + [piso] * n_pausa + [fala] * n_fala + [piso] * n_pausa

    def test_audio_limpo_continua_em_menos_46(self):
        self.assertEqual(pc.limiar_auto(self.env(-62, -19)), -46.0)

    def test_sala_ruidosa_fica_entre_o_ruido_e_a_fala(self):
        thr = pc.limiar_auto(self.env(-34, -19))
        self.assertGreater(thr, -34 + 3)
        self.assertLess(thr, -19 - 8)

    def test_o_limiar_antigo_falhava_em_sala_ruidosa(self):
        """Documenta o defeito corrigido: um teto fixo de -38 dB deixa o ruido (-34 dB) acima do limiar."""
        antigo = max(-46.0, min(-38.0, -34 + 12.0))
        self.assertLess(antigo, -34)   # tudo acima do limiar = "fala continua"


class Planejar(unittest.TestCase):
    P = pc.ESTILOS['curto']

    def test_palavra_solta_entre_pausas_corta_com_emenda_curta(self):
        # "entao" (0,08 s) isolada entre duas pausas de 0,8 s: antes, o corte era desfeito e a pausa ficava inteira
        faixas = [(0.5, 3.0), (3.8, 3.88), (4.68, 7.0)]
        plano = pc.planejar(8.0, faixas, self.P)
        self.assertEqual(len(plano['segmentos']), 3, plano['avisos'])
        self.assertTrue(any('sobreposicao reduzida' in a for a in plano['avisos']))
        final = plano['duracao_final']
        self.assertLess(final, 8.0 - 1.0, 'as duas pausas de 0,8 s precisam ter sido encurtadas')

    def test_pausa_curta_nao_e_cortada(self):
        plano = pc.planejar(5.0, [(0.5, 2.0), (2.15, 4.0)], self.P)
        self.assertEqual(len(plano['segmentos']), 1)


@unittest.skipUnless(TEM_FF, 'precisa de ffmpeg e ffprobe')
class FimAFim(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='fabrica_cortes_'))
        cls.casos = {}
        for nome, ruido in (('silenciosa', -62), ('ruidosa', -36)):
            bruto = gravacao_sintetica(cls.tmp / f'{nome}.mp4', ruido, FALAS, TOTAL)
            pasta = cls.tmp / f'saida_{nome}'
            p = py('planejar_cortes.py', bruto, '--saida', pasta, '--estilo', 'curto')
            m = py('montar.py', pasta / 'cortes.json', '--saida', pasta, '--fps', 30) if p.returncode == 0 else None
            cls.casos[nome] = dict(bruto=bruto, pasta=pasta, plan=p, mont=m)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _duracao(self, arq):
        d = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(arq)],
                                      capture_output=True, text=True).stdout)
        return float(d['format']['duration'])

    def _confere(self, nome):
        c = self.casos[nome]
        self.assertEqual(c['plan'].returncode, 0, c['plan'].stderr)
        self.assertEqual(c['mont'].returncode, 0, c['mont'].stderr)
        limpo = c['pasta'] / 'limpo.mp4'
        # 5 pausas de 0,6 a 1,1 s viram ~0,08 s: o arquivo encolhe pelo menos 3 s
        self.assertLess(self._duracao(limpo), TOTAL - 3.0, f'{nome}: as pausas nao foram cortadas')
        v = py('verificar_cortes.py', limpo, '--timeline', c['pasta'] / 'timeline.json')
        self.assertEqual(v.returncode, 0, v.stdout + v.stderr)
        self.assertIn('Tudo certo', v.stdout)

    def test_sala_silenciosa_corta_as_pausas(self):
        self._confere('silenciosa')

    def test_sala_ruidosa_tambem_corta_as_pausas(self):
        self._confere('ruidosa')

    def test_o_aviso_de_fala_continua_aparece_com_limiar_errado(self):
        c = self.casos['ruidosa']
        r = py('planejar_cortes.py', c['bruto'], '--saida', self.tmp / 'forcado', '--limiar', '-45')
        self.assertIn('fala continua', r.stdout)

    def test_controle_negativo_verificador_reprova_arquivo_com_pausas(self):
        """O arquivo BRUTO (pausas de 0,6 a 1,1 s) tem de ser reprovado pelo verificador no estilo curto."""
        c = self.casos['ruidosa']
        tl = dict(estilo='curto', pausa_min=0.22, pausa_final=0.08, fps=30, duracao_final=TOTAL, trechos=[])
        (self.tmp / 'tl_falso.json').write_text(json.dumps(tl), encoding='utf-8')
        v = py('verificar_cortes.py', c['bruto'], '--timeline', self.tmp / 'tl_falso.json')
        self.assertEqual(v.returncode, 1, v.stdout)
        self.assertIn('sobraram', v.stdout)


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
