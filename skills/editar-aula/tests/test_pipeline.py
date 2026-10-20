"""Testes de ponta a ponta dos scripts de limpeza com um video sintetico (tom + imagem de teste). Precisam de ffmpeg e ffprobe."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
TEM_FF = bool(shutil.which('ffmpeg') and shutil.which('ffprobe'))


def py(script, *args, check=True):
    r = subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode:
        raise AssertionError(f'{script} falhou ({r.returncode}):\n{r.stdout}\n{r.stderr}')
    return r


def duracao(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


@unittest.skipUnless(TEM_FF, 'ffmpeg/ffprobe nao encontrados')
class Pipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='aula-test-'))
        # 24 s: 1,5 s de tom e 1,5 s de silencio, repetido (pausas de 1,5 s)
        cls.video = cls.tmp / 'bruto.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=f=300:d=24:r=48000',
                        '-f', 'lavfi', '-i', 'testsrc2=s=640x360:r=30:d=24',
                        '-af', "volume='if(lt(mod(t,3),1.5),0.5,0)':eval=frame", '-c:v', 'libx264', '-preset', 'ultrafast',
                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-t', '24', str(cls.video)], check=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def rodar(self, nome, remover=None):
        pasta = self.tmp / nome
        args = [self.video, '--saida', pasta] + (['--remover', remover] if remover else [])
        py('planejar_cortes.py', *args)
        py('montar.py', pasta / 'cortes.json', '--saida', pasta)
        return pasta

    def test_so_pausas_duracao_audio_e_verificacao(self):
        pasta = self.rodar('a')
        plano = json.loads((pasta / 'cortes.json').read_text(encoding='utf-8'))
        self.assertEqual(len(plano['segmentos']), 8)
        self.assertLess(plano['duracao_final'], 24.0)
        self.assertAlmostEqual(duracao(pasta / 'aula_limpa.mp4'), plano['duracao_final'], delta=0.2)
        r = py('verificar.py', pasta / 'aula_limpa.mp4', '--timeline', pasta / 'timeline.json', check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('LUFS', r.stdout)
        self.assertTrue((pasta / 'relatorio_verificacao.md').is_file())

    def test_remocao_de_erro_gera_emenda_na_timeline(self):
        pasta = self.rodar('b', remover='4.4-10.6')   # tira o 2o e o 3o tons
        tl = json.loads((pasta / 'timeline.json').read_text(encoding='utf-8'))
        tipos = [t['tipo_corte_depois'] for t in tl['trechos']]
        self.assertIn('emenda', tipos)
        self.assertLess(tl['duracao_final'], 24.0 - 6.0)

    def test_arquivo_so_de_audio_gera_m4a_limpo(self):
        audio = self.tmp / 'so_audio.m4a'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=f=300:d=12:r=48000',
                        '-af', "volume='if(lt(mod(t,3),1.5),0.5,0)':eval=frame", '-c:a', 'aac', str(audio)], check=True)
        pasta = self.tmp / 'aud'
        py('planejar_cortes.py', audio, '--saida', pasta)
        py('montar.py', pasta / 'cortes.json', '--saida', pasta)
        self.assertTrue((pasta / 'aula_limpa.m4a').is_file())
        r = py('verificar.py', pasta / 'aula_limpa.m4a', '--timeline', pasta / 'timeline.json', check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_arquivo_sem_audio_da_erro_claro(self):
        mudo = self.tmp / 'mudo.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc2=s=320x180:r=30:d=2', '-c:v', 'libx264', str(mudo)], check=True)
        r = py('planejar_cortes.py', mudo, '--saida', self.tmp / 'mudo_out', check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn('audio', (r.stderr + r.stdout).lower())

    def test_arquivo_inexistente_da_erro_claro(self):
        r = py('diagnosticar.py', self.tmp / 'nao_existe.mp4', check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn('nao encontrado', r.stderr.lower())


if __name__ == '__main__':
    unittest.main()
