"""Testes do analisar.py com video sintetico de numeros conhecidos. Precisam de ffmpeg.

Video de 12 s a 25 fps: preto 0-1 s, branco 1-2 s, preto 2-8 s, branco 8-12 s  ->  cortes de cena em 1, 2 e 8 s.
Audio: tom em tres rajadas (0,5-2,4 s; 4,0-5,0 s; 9,5-11,5 s), o resto em silencio.
Transcricao fabricada: 10 palavras em instantes conhecidos.
"""
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
import analisar  # noqa: E402

TEM_FF = bool(shutil.which('ffmpeg') and shutil.which('ffprobe'))
SR, DUR = 48000, 12
RAJADAS = [(0.5, 2.4), (4.0, 5.0), (9.5, 11.5)]
PALAVRAS = [('um', 0.5, 0.8), ('dois', 0.9, 1.3), ('tres', 1.4, 1.8), ('quatro', 1.9, 2.4),
            ('cinco', 4.0, 4.4), ('seis', 4.5, 5.0),
            ('sete', 9.5, 10.0), ('oito', 10.1, 10.6), ('nove', 10.7, 11.0), ('dez', 11.1, 11.5)]


def py(*args, check=True):
    r = subprocess.run([sys.executable, str(SCRIPTS / 'analisar.py'), *map(str, args)], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode:
        raise AssertionError(f'analisar.py falhou ({r.returncode}):\n{r.stdout}\n{r.stderr}')
    return r


def criar_wav(caminho: Path) -> None:
    n = DUR * SR
    x = [0] * n
    for a, b in RAJADAS:
        i0, i1 = int(a * SR), int(b * SR)
        for i in range(i0, i1):
            rampa = min(1.0, (i - i0) / (0.005 * SR), (i1 - i) / (0.005 * SR))
            x[i] = int(14000 * rampa * math.sin(2 * math.pi * 440 * i / SR))
    with wave.open(str(caminho), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(struct.pack(f'<{n}h', *x))


def criar_video(pasta: Path, nome: str, brancos: list[tuple[float, float]], com_audio=True) -> Path:
    """Preto, com faixas brancas nos intervalos dados (cada borda de faixa e um corte de cena)."""
    caixas = ''.join(f",drawbox=x=0:y=0:w=iw:h=ih:color=white:t=fill:enable='between(t,{a},{b})'" for a, b in brancos)
    video = f'color=c=black:s=320x240:r=25:d={DUR}{caixas},format=yuv420p'
    mp4 = pasta / f'{nome}.mp4'
    args = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', video]
    if com_audio:
        wav = pasta / f'{nome}.wav'
        criar_wav(wav)
        args += ['-i', str(wav), '-c:a', 'aac', '-shortest']
    subprocess.run([*args, '-c:v', 'libx264', str(mp4)], check=True)
    return mp4


def criar_transcricao(pasta: Path) -> Path:
    ws = [dict(word=p, start=a, end=b, source_start=a, source_end=b) for p, a, b in PALAVRAS]
    t = pasta / 'transcricao.json'
    t.write_text(json.dumps(dict(text=' '.join(p[0] for p in PALAVRAS), words=ws)), encoding='utf-8')
    return t


def cor_do_primeiro_quadro(folha: Path) -> int:
    """Brilho (0 a 255) do centro do primeiro quadro de uma folha de contato."""
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(folha), '-vf', 'crop=100:100:150:100,scale=1:1,format=gray', '-f', 'rawvideo', '-'],
                       capture_output=True)
    return r.stdout[0]


def dimensoes(arq: Path) -> tuple[int, int]:
    d = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', str(arq)],
                       capture_output=True, text=True).stdout.strip().split(',')
    return int(d[0]), int(d[1])


@unittest.skipUnless(TEM_FF, 'precisa de ffmpeg e ffprobe')
class Medicoes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='raiox_'))
        cls.v = criar_video(cls.tmp, 'criativo', [(1, 2), (8, 12)])
        cls.t = criar_transcricao(cls.tmp)
        cls.out = cls.tmp / 'saida'
        py('analisar', cls.v, '--saida', cls.out)
        py('mapa', cls.v, '--transcricao', cls.t, '--saida', cls.out)
        cls.mapa = json.loads((cls.out / 'criativo' / 'mapa_ritmo.json').read_text(encoding='utf-8'))
        cls.r = cls.mapa['resumo']

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_analisar_acha_os_cortes_de_cena(self):
        cortes = json.loads((self.out / 'criativo' / 'scenes.json').read_text(encoding='utf-8'))
        self.assertEqual(len(cortes), 3)
        for esperado, achado in zip([1, 2, 8], cortes):
            self.assertAlmostEqual(achado, esperado, delta=0.1)
        meta = json.loads((self.out / 'criativo' / 'meta.json').read_text(encoding='utf-8'))
        self.assertEqual(meta['cortes_de_cena'], 3)
        self.assertTrue((self.out / 'criativo' / 'sons.json').exists())
        self.assertEqual(len(list((self.out / 'criativo' / 'sheets').glob('*.jpg'))), 2)

    def test_mapa_cortes_nas_janelas_do_gancho_e_do_final(self):
        self.assertEqual(self.r['cortes_de_cena'], 3)
        self.assertEqual(self.r['cortes_nos_3_primeiros_s'], 2)
        self.assertEqual(self.r['cortes_nos_5_primeiros_s'], 2)
        self.assertEqual(self.r['cortes_nos_5_ultimos_s'], 1)

    def test_mapa_maior_trecho_sem_corte(self):
        m = self.r['maior_trecho_sem_corte']
        self.assertAlmostEqual(m['duracao_s'], 6.0, delta=0.15)
        self.assertAlmostEqual(m['de'], 2.0, delta=0.1)
        self.assertAlmostEqual(m['ate'], 8.0, delta=0.1)

    def test_controle_o_maior_trecho_muda_quando_ha_outro_corte(self):
        # dois cortes a mais (5 e 6 s) quebram o trecho de 6 s: o maior passa a ser o final (8 a 12 s = 4 s)
        v2 = criar_video(self.tmp, 'criativo2', [(1, 2), (5, 6), (8, 12)])
        out = self.tmp / 'saida2'
        py('mapa', v2, '--transcricao', self.t, '--saida', out)
        r2 = json.loads((out / 'criativo2' / 'mapa_ritmo.json').read_text(encoding='utf-8'))['resumo']
        self.assertEqual(r2['cortes_de_cena'], 5)
        self.assertAlmostEqual(r2['maior_trecho_sem_corte']['duracao_s'], 4.0, delta=0.15)
        self.assertAlmostEqual(r2['maior_trecho_sem_corte']['de'], 8.0, delta=0.1)
        self.assertNotAlmostEqual(r2['maior_trecho_sem_corte']['duracao_s'], 6.0, delta=1.0)

    def test_mapa_palavras_e_fala(self):
        self.assertEqual(self.r['palavras_total'], 10)
        self.assertEqual(self.r['palavras_por_minuto'], 50)
        self.assertAlmostEqual(self.r['primeira_palavra_s'], 0.5)
        self.assertEqual(self.r['palavras_nos_3_primeiros_s'], 4)
        self.assertEqual(self.r['palavras_nos_5_ultimos_s'], 4)
        self.assertEqual(self.r['pausas_de_fala'], 2)
        self.assertAlmostEqual(self.r['maior_pausa_de_fala_s'], 4.5, delta=0.01)
        self.assertEqual([round(p['duracao_s'], 1) for p in self.mapa['pausas_de_fala']], [1.6, 4.5])

    def test_mapa_tabela_por_janela(self):
        j = self.mapa['janelas']
        self.assertEqual(len(j), 12)
        self.assertEqual([x['palavras'] for x in j][:3], [2, 2, 0])       # 0-1: um dois | 1-2: tres quatro | 2-3: nenhuma
        self.assertEqual(sum(x['cortes'] for x in j), 3)
        self.assertIn('um dois', j[0]['texto'])
        self.assertEqual(j[2]['texto'], '')

    def test_mapa_som_e_volume_seguem_a_atividade_do_audio(self):
        self.assertAlmostEqual(self.r['som_pct_total'], 100 * 4.9 / 12, delta=4)
        v = self.r['volume_medio_db']
        # mesma amplitude em todas as rajadas: o volume medio em potencia acompanha a fracao de tempo com som
        self.assertGreater(v['primeiros_3_s'], v['ultimos_5_s'])
        self.assertGreater(v['ultimos_5_s'], v['meio'])
        j = self.mapa['janelas']
        self.assertGreater(j[0]['som_pct'], 40)     # 0-1 s: a rajada comeca em 0,5 s
        self.assertLess(j[3]['som_pct'], 5)         # 3-4 s: silencio

    def test_markdown_tem_resumo_tabela_e_avisos(self):
        md = (self.out / 'criativo' / 'mapa_ritmo.md').read_text(encoding='utf-8')
        for trecho in ('## Resumo', 'Maior trecho sem corte de cena', '| t (s) | cortes |', '## Avisos', 'zoom nem jump cut'):
            self.assertIn(trecho, md)

    def test_mapa_sem_transcricao_nao_quebra_e_avisa(self):
        out = self.tmp / 'sem_t'
        py('mapa', self.v, '--saida', out)
        m = json.loads((out / 'criativo' / 'mapa_ritmo.json').read_text(encoding='utf-8'))
        self.assertNotIn('palavras_total', m['resumo'])
        self.assertTrue(any('sem transcricao' in a for a in m['avisos']))
        self.assertEqual(m['resumo']['cortes_de_cena'], 3)

    def test_mapa_de_video_sem_audio_avisa(self):
        mudo = criar_video(self.tmp, 'mudo', [(1, 2)], com_audio=False)
        out = self.tmp / 'saida_mudo'
        py('mapa', mudo, '--saida', out)
        m = json.loads((out / 'mudo' / 'mapa_ritmo.json').read_text(encoding='utf-8'))
        self.assertTrue(any('nao tem audio' in a for a in m['avisos']))
        self.assertNotIn('volume_medio_db', m['resumo'])

    def test_janela_do_gancho_gera_uma_folha_de_24_quadros(self):
        out = self.tmp / 'j1'
        py('janela', self.v, '--de', 0, '--ate', 3, '--fps', 8, '--saida', out)
        folhas = sorted(out.glob('janela_*.jpg'))
        self.assertEqual([f.name.split('_')[1] for f in folhas], ['01'])
        self.assertEqual(dimensoes(folhas[0]), (6 * 400, 4 * 300))

    def test_janela_aponta_para_o_trecho_certo_do_video(self):
        for de, ate, nome, esperado_claro in ((0, 1, 'janela_01_0-1.jpg', False), (8, 9, 'janela_01_8-9.jpg', True)):
            out = self.tmp / f'j_{de}'
            py('janela', self.v, '--de', de, '--ate', ate, '--fps', 4, '--saida', out)
            folha = out / nome
            self.assertTrue(folha.exists(), f'esperava {nome}; achei {[p.name for p in out.glob("*.jpg")]}')
            brilho = cor_do_primeiro_quadro(folha)
            self.assertTrue((brilho > 200) == esperado_claro, f'janela {de}-{ate}: brilho {brilho}')

    def test_janela_longa_vira_varias_folhas_e_pouca_janela_uma_folha_curta(self):
        out = self.tmp / 'j2'
        py('janela', self.v, '--de', 0, '--ate', 7, '--fps', 8, '--saida', out)       # 56 quadros = 3 folhas de 24
        self.assertEqual(len(list(out.glob('janela_*.jpg'))), 3)
        out2 = self.tmp / 'j3'
        py('janela', self.v, '--de', 0, '--ate', 1, '--fps', 4, '--saida', out2)      # 4 quadros = 1 linha
        self.assertEqual(dimensoes(next(out2.glob('janela_*.jpg'))), (6 * 400, 300))

    def test_erros_claros(self):
        r = py('janela', self.v, '--de', 5, '--ate', 2, check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn('Janela invalida', r.stderr)
        r = py('janela', self.v, '--de', 0, '--ate', 12, '--fps', 30, check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn('demais', r.stderr)
        r = py('mapa', self.tmp / 'nao_existe.mp4', '--saida', self.tmp / 'x', check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn('Erro', r.stderr)
        vazio = self.tmp / 'vazio.json'
        vazio.write_text('{"words": []}', encoding='utf-8')
        r = py('mapa', self.v, '--transcricao', vazio, '--saida', self.tmp / 'y', check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn('Sem palavras', r.stderr)

    def test_quadro_e_rajada(self):
        png = self.tmp / 'q.png'
        py('quadro', self.v, 1.5, '--saida', png)
        self.assertTrue(png.exists() and png.stat().st_size > 100)
        pasta = self.tmp / 'rajada'
        py('quadro', self.v, 2.0, '--rajada', 1.0, '--fps', 5, '--saida', pasta)
        self.assertEqual(len(list(pasta.glob('f_*.png'))), 5)


class Puro(unittest.TestCase):
    def test_potencia_db_e_media_em_potencia(self):
        self.assertEqual(analisar.potencia_db([-20.0, -20.0]), -20.0)
        self.assertAlmostEqual(analisar.potencia_db([-20.0, -80.0]), -23.0, delta=0.1)      # 10*log10((0,01 + ~0)/2)
        self.assertIsNone(analisar.potencia_db([]))

    def test_palavras_depois_do_fim_do_video_sao_ignoradas_com_aviso(self):
        ws = [dict(word='a', start=1.0, end=1.3), dict(word='b', start=2.0, end=2.3), dict(word='c', start=12.0, end=12.3)]
        m = analisar.calcular_mapa(10.0, [], ws, None, 1.0)
        self.assertEqual(m['resumo']['palavras_total'], 2)
        self.assertEqual(m['resumo']['palavras_por_minuto'], 12)
        self.assertTrue(any('depois do fim do video' in a for a in m['avisos']))

    def test_calcular_mapa_sem_audio_nem_transcricao(self):
        m = analisar.calcular_mapa(10.0, [2.0, 4.0], None, None, 1.0)
        self.assertEqual(m['resumo']['cortes_de_cena'], 2)
        self.assertAlmostEqual(m['resumo']['maior_trecho_sem_corte']['duracao_s'], 6.0)
        self.assertEqual(len(m['janelas']), 10)
        self.assertIsNone(m['janelas'][0]['palavras'])


if __name__ == '__main__':
    unittest.main()
