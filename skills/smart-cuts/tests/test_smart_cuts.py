"""Testes da Smart Cuts. Os de ponta a ponta usam midia sintetica (cada take tem um tom e uma cor) e precisam de ffmpeg."""
import json
import math
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
import _fala  # noqa: E402
import planejar_cortes as pc  # noqa: E402
import verificar as vf  # noqa: E402

TEM_FF = bool(shutil.which('ffmpeg') and shutil.which('ffprobe'))
SR, FPS = 48000, 25

# linha do tempo do bruto sintetico (s): palavra, inicio, fim, tom (Hz)
# A (vermelho, 440): um dois tres | lixo (verde, 1320): lixo bobagem | B (azul, 880): quatro cinco ... pausa ... seis
PALAVRAS = [('um', 0.5, 0.9, 440), ('dois', 1.0, 1.4, 440), ('tres', 1.5, 1.9, 440),
            ('lixo', 2.6, 3.0, 1320), ('bobagem', 3.1, 3.4, 1320),
            ('quatro', 4.0, 4.4, 880), ('cinco', 4.5, 4.9, 880), ('seis', 5.4, 5.8, 880)]
DURACAO = 6.5


def escrever_wav(caminho: Path, palavras=PALAVRAS, dur=DURACAO) -> None:
    n = int(dur * SR)
    x = [0] * n
    for _, a, b, f in palavras:
        i0, i1 = int(a * SR), int(b * SR)
        for i in range(i0, i1):
            rampa = min(1.0, (i - i0) / (0.005 * SR), (i1 - i) / (0.005 * SR))
            x[i] = int(16000 * rampa * math.sin(2 * math.pi * f * i / SR))
    with wave.open(str(caminho), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(struct.pack(f'<{n}h', *x))


def criar_fonte(pasta: Path) -> Path:
    wav = pasta / 'fonte.wav'
    escrever_wav(wav)
    mp4 = pasta / 'fonte.mp4'
    cores = ("color=c=black:s=320x240:r=25:d=6.5,"
             "drawbox=x=0:y=0:w=iw:h=ih:color=red:t=fill:enable='between(t,0,2.3)',"
             "drawbox=x=0:y=0:w=iw:h=ih:color=green:t=fill:enable='between(t,2.3,3.7)',"
             "drawbox=x=0:y=0:w=iw:h=ih:color=blue:t=fill:enable='gte(t,3.7)',format=yuv420p")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', cores, '-i', str(wav), '-c:v', 'libx264', '-c:a', 'aac',
                    '-shortest', str(mp4)], check=True)
    return mp4


def transcricao(pasta: Path, nome='transcricao.json', palavras=PALAVRAS) -> Path:
    ws = [dict(word=p, start=a, end=b, source_start=a, source_end=b) for p, a, b, _ in palavras]
    caminho = pasta / nome
    caminho.write_text(json.dumps(dict(text=' '.join(p[0] for p in palavras), words=ws)), encoding='utf-8')
    return caminho


def py(script, *args, check=True):
    r = subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode:
        raise AssertionError(f'{script} falhou ({r.returncode}):\n{r.stdout}\n{r.stderr}')
    return r


def goertzel(x, f):
    k = 2 * math.cos(2 * math.pi * f / SR)
    s1 = s2 = 0.0
    for v in x:
        s0 = v + k * s1 - s2
        s1, s2 = s0, s1
    return (s1 * s1 + s2 * s2 - k * s1 * s2) / (len(x) ** 2)


def tempos_de_entrada_e_saida(mp4: Path):
    """(quando o quadro vira azul, quando o tom de B aparece, quando o tom de A some), em segundos."""
    v = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(mp4), '-vf', 'scale=8:6', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       capture_output=True).stdout
    q = 8 * 6 * 3
    quadros = [v[i:i + q] for i in range(0, len(v) - q + 1, q)]
    t_azul = next(i for i, f in enumerate(quadros) if f[2] > 150 and f[0] < 100) / FPS
    a = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(mp4), '-vn', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    amostras = struct.unpack(f'<{len(a) // 2}h', a)
    jan = int(0.01 * SR)   # janelas de 10 ms
    p440 = [goertzel(amostras[i:i + jan], 440) for i in range(0, len(amostras) - jan, jan)]
    p880 = [goertzel(amostras[i:i + jan], 880) for i in range(0, len(amostras) - jan, jan)]
    m440, m880 = max(p440), max(p880)
    t_b = next(i for i, p in enumerate(p880) if p > 0.15 * m880) * 0.01
    t_a_fim = max(i for i, p in enumerate(p440) if p > 0.15 * m440) * 0.01 + 0.01
    return t_azul, t_b, t_a_fim


class Puro(unittest.TestCase):
    def test_faixas_de_fala_separam_pausa_de_60ms(self):
        env = [-80.0] * 300
        for i in range(50, 100):
            env[i] = -20.0
        for i in range(106, 150):      # 60 ms de silencio entre as duas
            env[i] = -20.0
        f = _fala.faixas_de_fala(env, -40.0)
        self.assertEqual(len(f), 2)
        self.assertAlmostEqual(f[0][1], 1.0, places=2)
        self.assertAlmostEqual(f[1][0], 1.06, places=2)

    def test_silencios_reais_exigem_60ms(self):
        env = [-20.0] * 100
        for i in range(10, 14):        # 40 ms: nao conta
            env[i] = -80.0
        for i in range(40, 50):        # 100 ms: conta
            env[i] = -80.0
        s = _fala.silencios(env, -40.0, 0, 1.0)
        self.assertEqual(len(s), 1)
        self.assertAlmostEqual(s[0][0], 0.40, places=2)

    def test_tempos_cumulativos_descontam_a_sobreposicao(self):
        segs = [dict(ini=0, fim=2.0, d=0.2), dict(ini=5, fim=6.0, d=0.1), dict(ini=9, fim=10.0, d=0)]
        T, total = pc.calcular_tempos(segs)
        self.assertEqual([round(t, 3) for t in T], [0.0, 1.8, 2.7])
        self.assertAlmostEqual(total, 3.7)

    def test_comparar_fala_acusa_palavra_de_conteudo_faltando(self):
        faltando, sobrando, fim = vf.comparar_fala('um dois três quatro cinco seis', 'um três quatro cinco seis')
        self.assertEqual(len(faltando), 1)
        self.assertIn('dois', faltando[0])
        self.assertEqual(fim, '')

    def test_comparar_fala_ignora_muleta_e_aponta_fim_cortado(self):
        faltando, _, fim = vf.comparar_fala('é isso aí então vamos começar agora', 'isso aí então vamos começar')
        self.assertTrue(fim)
        faltando2, _, _ = vf.comparar_fala('né vamos lá', 'vamos lá')
        self.assertEqual(faltando2, [])

    def test_palavra_colada_na_fala_entra_e_e_avisada(self):
        # "x y z" sem silencio entre as palavras: pedir so "z" traz as vizinhas junto
        ws = [dict(word='x', start=1.0, end=1.3), dict(word='y', start=1.3, end=1.6), dict(word='z', start=1.6, end=2.0),
              dict(word='w', start=3.0, end=3.4)]
        ctx = {'f1': pc.contexto_fonte(ws, [(1.0, 2.0), (3.0, 3.4)], 5.0)}
        r = pc.planejar_corte(dict(id='c', trechos=[[1.6, 1.6]]), ctx, pc.ESTILOS['curto'], 'f1')
        self.assertTrue(any(a.startswith('ENTROU "x"') for a in r['avisos']))
        self.assertTrue(any(a.startswith('ENTROU "y"') for a in r['avisos']))

    def test_trecho_sem_voz_perto_e_erro_claro(self):
        ws = [dict(word='x', start=1.0, end=1.3)]
        ctx = {'f1': pc.contexto_fonte(ws, [(4.0, 4.3)], 6.0)}
        with self.assertRaises(ValueError):
            pc.planejar_corte(dict(id='c', trechos=[[1.0, 1.0]]), ctx, pc.ESTILOS['curto'], 'f1')

    def test_emenda_inexistente_e_erro_claro(self):
        ws = [dict(word='a', start=1.0, end=1.5)]
        ctx = {'f1': pc.contexto_fonte(ws, [(1.0, 1.5)], 3.0)}
        with self.assertRaises(ValueError) as e:
            pc.planejar_corte(dict(id='c', trechos=[[1.0, 1.0]], emendas={'0': [1.6, 2.0]}), ctx, pc.ESTILOS['curto'], 'f1')
        self.assertIn('nao existe', str(e.exception))

    def test_emenda_tem_sobreposicao_e_cauda_curta(self):
        ws = [dict(word='a', start=1.0, end=1.5), dict(word='b', start=3.0, end=3.5), dict(word='c', start=5.0, end=5.5)]
        ctx = {'f1': pc.contexto_fonte(ws, [(1.0, 1.5), (3.0, 3.5), (5.0, 5.5)], 8.0)}
        r = pc.planejar_corte(dict(id='c', trechos=[[1.0, 1.0], [5.0, 5.0]]), ctx, pc.ESTILOS['curto'], 'f1')
        s0, s1 = r['segmentos']
        self.assertAlmostEqual(s0['d'], 0.22)
        self.assertAlmostEqual(s0['fim'], 1.5 + 0.095, places=3)            # a frase anterior termina inteira
        self.assertAlmostEqual(s1['ini'], 5.0 - 0.025, places=3)            # o seguinte entra colado na voz
        self.assertEqual(r['texto'], 'a c')
        self.assertEqual(r['avisos'], [])


@unittest.skipUnless(TEM_FF, 'precisa de ffmpeg e ffprobe')
class PontaAPonta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='smartcuts_'))
        cls.fonte = criar_fonte(cls.tmp)
        cls.transc = transcricao(cls.tmp)
        cls.cortes = cls.tmp / 'cortes.json'
        # A inteiro (um dois tres), tira "lixo bobagem", B (quatro cinco) + pausa + seis. Fim marcado no INICIO da ultima palavra.
        cls.cortes.write_text(json.dumps(dict(video='fonte.mp4', transcricao='transcricao.json', cortes=[
            dict(id='c1', estilo='serio', gancho='UM DOIS TRES', porque='teste', trechos=[[0.5, 1.5], [4.0, 5.4]],
                 rosto=dict(cx=160, cy=100, h=80))])), encoding='utf-8')
        cls.out = cls.tmp / 'saida'
        py('planejar_cortes.py', cls.cortes, '--saida', cls.out)
        cls.plano = json.loads((cls.out / 'plano_cortes.json').read_text(encoding='utf-8'))
        py('montar.py', cls.out / 'plano_cortes.json', '--saida', cls.out, '--trabalhadores', 2)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_plano_tira_o_lixo_e_encurta_a_pausa(self):
        c = self.plano['cortes'][0]
        self.assertEqual(c['texto'], 'um dois tres quatro cinco seis')
        self.assertEqual(c['avisos'], [])
        self.assertEqual([s['tipo'] for s in c['segmentos']], ['emenda', 'pausa', None])
        for s in c['segmentos']:
            self.assertFalse(2.3 < s['ini'] < 3.7 and 2.3 < s['fim'] < 3.7)
        # a pausa de 0,5 s entre "cinco" e "seis" ficou com ~0,08 s
        s1, s2 = c['segmentos'][1], c['segmentos'][2]
        fim_cinco = s1['final_ini'] + (4.9 - s1['ini'])
        inicio_seis = s2['final_ini'] + (5.4 - s2['ini'])
        self.assertAlmostEqual(inicio_seis - fim_cinco, 0.08, places=1)

    def test_imagem_e_audio_do_proximo_trecho_entram_juntos_antes_do_anterior_acabar(self):
        t_azul, t_b, t_a_fim = tempos_de_entrada_e_saida(self.out / 'c1.mp4')
        self.assertLess(abs(t_azul - t_b), 0.06, f'imagem em {t_azul:.3f} s e audio em {t_b:.3f} s: precisam entrar juntos')
        self.assertLess(t_azul, t_a_fim - 0.04, 'a imagem nova tem que entrar antes de a fala anterior acabar')
        self.assertLess(t_b, t_a_fim - 0.04, 'o audio novo tem que entrar antes de a fala anterior acabar')
        self.assertLess(t_a_fim - t_b, 0.30, 'as vozes se sobrepoem por pouco tempo')

    def test_plano_json_entrega_o_que_o_remotion_precisa(self):
        p = json.loads((self.out / 'plano.json').read_text(encoding='utf-8'))['cortes'][0]
        self.assertEqual((p['largura'], p['altura'], p['fps']), (320, 240, 25.0))
        self.assertEqual(p['arquivo'], 'c1.mp4')
        self.assertEqual(p['rosto'], dict(cx=160, cy=100, h=80))
        self.assertEqual(len(p['emendas']), 2)
        self.assertEqual(p['texto'], 'um dois tres quatro cinco seis')
        self.assertTrue((self.out / 'c1.mp4').exists())

    def test_verificar_libera_quando_a_fala_final_bate(self):
        tr = self.tmp / 'transc_ok' / 'c1'
        tr.mkdir(parents=True)
        transcricao(tr, palavras=[(p, a, b, f) for p, a, b, f in PALAVRAS if p not in ('lixo', 'bobagem')])
        r = py('verificar.py', self.out / 'plano.json', '--transcricoes', self.tmp / 'transc_ok', check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('Tudo certo', r.stdout)

    def test_verificar_acusa_palavra_cortada_e_pendencia(self):
        tr = self.tmp / 'transc_ruim' / 'c1'
        tr.mkdir(parents=True)
        transcricao(tr, palavras=[(p, a, b, f) for p, a, b, f in PALAVRAS if p not in ('lixo', 'bobagem', 'cinco')])
        r = py('verificar.py', self.out / 'plano.json', '--transcricoes', self.tmp / 'transc_ruim', check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn('ALERTA esperado e nao ouvido', r.stdout)
        r2 = py('verificar.py', self.out / 'plano.json', check=False)
        self.assertEqual(r2.returncode, 1)
        self.assertIn('PENDENTE', r2.stdout)

    def test_planejar_so_um_corte_mantem_os_outros_no_plano(self):
        spec = json.loads(self.cortes.read_text(encoding='utf-8'))
        spec['cortes'].append(dict(id='c2', estilo='meme', gancho='SEIS', trechos=[[4.0, 5.4]]))
        cortes2 = self.tmp / 'cortes2.json'
        cortes2.write_text(json.dumps(spec), encoding='utf-8')
        out = self.tmp / 'saida_so'
        py('planejar_cortes.py', cortes2, '--saida', out)
        py('planejar_cortes.py', cortes2, '--saida', out, '--so', 'c2', '--estilo', 'suave')
        plano = json.loads((out / 'plano_cortes.json').read_text(encoding='utf-8'))
        self.assertEqual([c['id'] for c in plano['cortes']], ['c1', 'c2'])
        self.assertEqual([c['estilo_pausa'] for c in plano['cortes']], ['curto', 'suave'])

    def test_ler_mostra_silencios_reais(self):
        r = py('ler.py', self.transc, 0, 6.5, '--video', self.fonte, '--silencio')
        self.assertIn('SIL', r.stdout)
        self.assertIn('lixo@2.60-3.00', r.stdout)


if __name__ == '__main__':
    unittest.main()
