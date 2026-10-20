"""Testes do colar.py: o clipe de motion tem que aparecer DENTRO da janela e so nela. Precisam de ffmpeg com prores_ks."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import colar  # noqa: E402

TEM_FF = bool(shutil.which('ffmpeg') and shutil.which('ffprobe'))


def py(*args, check=True):
    r = subprocess.run([sys.executable, str(SCRIPTS / 'colar.py'), *map(str, args)], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode:
        raise AssertionError(f'colar.py falhou ({r.returncode}):\n{r.stdout}\n{r.stderr}')
    return r


class Filtro(unittest.TestCase):
    def test_um_overlay_por_clipe_com_janela_e_saida_yuv420p(self):
        f = colar.montar_filtro([dict(arquivo='a.mov', inicio=1.0, duracao=2.0), dict(arquivo='b.mov', inicio=10.5, duracao=3.0)])
        self.assertEqual(f.count('overlay='), 2)
        self.assertIn("between(t,1.0000,3.0000)", f)
        self.assertIn("between(t,10.5000,13.5000)", f)
        self.assertIn('[1:v]format=yuva444p[c0]', f)
        self.assertIn('[2:v]format=yuva444p[c1]', f)
        self.assertIn('[o0][c1]overlay', f)            # o segundo clipe entra sobre o resultado do primeiro
        self.assertTrue(f.rstrip().endswith('format=yuv420p[v]'))

    def test_caminhos_relativos_contam_a_partir_do_manifesto(self):
        base = Path(tempfile.gettempdir()) / 'qualquer'
        m = colar.normalizar([dict(arquivo='clips/a.mov', inicio=0, duracao=1)], base)
        self.assertEqual(Path(m[0]['arquivo']), (base / 'clips' / 'a.mov').resolve())

    def test_validacao_acusa_clipe_inexistente_e_fora_do_video(self):
        with self.assertRaises(ValueError):
            colar.validar([], 10.0)
        with self.assertRaises(FileNotFoundError):
            colar.validar([dict(arquivo='nao_existe.mov', inicio=0, duracao=1)], 10.0)
        with tempfile.TemporaryDirectory() as d:
            arq = Path(d) / 'x.mov'
            arq.write_bytes(b'0')
            with self.assertRaises(ValueError):
                colar.validar([dict(arquivo=str(arq), inicio=50.0, duracao=2.0)], 10.0)


@unittest.skipUnless(TEM_FF, 'ffmpeg/ffprobe nao encontrados')
class PontaAPonta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='colar-test-'))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc2=s=640x360:r=30:d=20',
                        '-f', 'lavfi', '-i', 'sine=f=300:d=20:r=48000', '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-t', '20', str(cls.tmp / 'limpo.mp4')], check=True)
        # clipe ProRes 4444 com transparencia: quadro cheio vermelho a 80% de opacidade, 2 s
        r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=0xFF0000@0.8:s=640x360:d=2:r=30,format=yuva444p10le',
                            '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', str(cls.tmp / 'clip.mov')],
                           capture_output=True, text=True)
        cls.sem_prores = r.returncode != 0
        (cls.tmp / 'manifest.json').write_text(json.dumps([dict(arquivo='clip.mov', inicio=8.0, duracao=2.0, nomes=['t'])]), encoding='utf-8')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def pixel(self, arq, t):
        r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(arq), '-frames:v', '1', '-vf', 'crop=1:1:30:30,format=rgb24',
                            '-f', 'rawvideo', '-'], capture_output=True)
        return tuple(r.stdout[:3])

    def test_motion_aparece_so_dentro_da_janela_e_o_audio_e_copiado(self):
        if self.sem_prores:
            self.skipTest('este FFmpeg nao tem o encoder prores_ks')
        saida = self.tmp / 'final.mp4'
        py(self.tmp / 'limpo.mp4', self.tmp / 'manifest.json', '--saida', saida, '--folha')
        for t in (2.0, 7.5, 10.5, 15.0):               # fora da janela 8 a 10 s: igual ao video limpo
            a, b = self.pixel(self.tmp / 'limpo.mp4', t), self.pixel(saida, t)
            self.assertLess(sum(abs(x - y) for x, y in zip(a, b)), 40, f'mudou fora da janela em {t}s: {a} {b}')
        for t in (8.3, 9.0, 9.7):                      # dentro: tingido de vermelho
            a, b = self.pixel(self.tmp / 'limpo.mp4', t), self.pixel(saida, t)
            self.assertGreater(sum(abs(x - y) for x, y in zip(a, b)), 100, f'motion nao apareceu em {t}s: {a} {b}')
        r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', str(saida)], capture_output=True, text=True)
        self.assertIn('aac', r.stdout)
        self.assertTrue((self.tmp / 'folha_motions.png').is_file())

    def test_clipe_fora_do_video_da_erro_claro(self):
        (self.tmp / 'm2.json').write_text(json.dumps([dict(arquivo='clip.mov', inicio=500.0, duracao=2.0)]), encoding='utf-8')
        r = py(self.tmp / 'limpo.mp4', self.tmp / 'm2.json', '--saida', self.tmp / 'x.mp4', check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn('fora do video', r.stderr)


if __name__ == '__main__':
    unittest.main()
