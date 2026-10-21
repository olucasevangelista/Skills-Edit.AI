"""Testes do analisar.py com video sintetico (cores que mudam e estalos de som). Precisam de ffmpeg com drawtext opcional."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import analisar  # noqa: E402

TEM_FF = bool(shutil.which('ffmpeg') and shutil.which('ffprobe'))


def py(*args, check=True):
    r = subprocess.run([sys.executable, str(SCRIPTS / 'analisar.py'), *map(str, args)], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode:
        raise AssertionError(f'analisar.py falhou ({r.returncode}):\n{r.stdout}\n{r.stderr}')
    return r


def criar_video(pasta: Path, vertical=True, dur=12) -> Path:
    """12 s, preto e branco alternando a cada 3 s (3 cortes de cena em 3, 6 e 9 s), tom continuo baixo e um estalo forte em 4 s."""
    mp4 = pasta / ('ref_vertical.mp4' if vertical else 'ref_horizontal.mp4')
    tam = '180x320' if vertical else '320x180'
    video = (f"color=c=black:s={tam}:r=25:d={dur},"
             "drawbox=x=0:y=0:w=iw:h=ih:color=white:t=fill:enable='between(t,3,6)',"
             "drawbox=x=0:y=0:w=iw:h=ih:color=white:t=fill:enable='gte(t,9)',format=yuv420p")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', video, '-f', 'lavfi', '-i', f'sine=f=200:d={dur}',
                    '-filter_complex', f"[1:a]volume=0.02[a1];sine=f=1000:d=0.1,adelay=4000|4000,apad=whole_dur={dur}[a2];[a1][a2]amix=inputs=2:normalize=0[a]",
                    '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-c:a', 'aac', '-shortest', str(mp4)], check=True)
    return mp4


@unittest.skipUnless(TEM_FF, 'precisa de ffmpeg e ffprobe')
class Analisar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='copystyle_'))
        cls.v = criar_video(cls.tmp)
        cls.h = criar_video(cls.tmp, vertical=False)
        cls.out = cls.tmp / 'analise'
        py('analisar', cls.v, cls.h, '--saida', cls.out)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_meta_conta_cortes_de_cena_e_formato(self):
        m = json.loads((self.out / 'ref_vertical' / 'meta.json').read_text(encoding='utf-8'))
        self.assertEqual(m['formato'], 'vertical')
        self.assertEqual((m['largura'], m['altura']), (180, 320))
        self.assertEqual(m['cortes_de_cena'], 3)
        self.assertAlmostEqual(m['cortes_por_minuto'], 15.0, places=1)
        h = json.loads((self.out / 'ref_horizontal' / 'meta.json').read_text(encoding='utf-8'))
        self.assertEqual(h['formato'], 'horizontal/quadrado')

    def test_scenes_tem_os_instantes_dos_cortes(self):
        cortes = json.loads((self.out / 'ref_vertical' / 'scenes.json').read_text(encoding='utf-8'))
        for esperado, achado in zip([3, 6, 9], cortes):
            self.assertAlmostEqual(achado, esperado, delta=0.1)

    def test_folhas_de_contato_nomeadas_pelo_intervalo(self):
        nomes = sorted(p.name for p in (self.out / 'ref_vertical' / 'sheets').glob('*.jpg'))
        # 12 s a 2 quadros por segundo = 24 quadros = 2 folhas de 18 (9 s cada)
        self.assertEqual(len(nomes), 2)
        self.assertTrue(nomes[0].startswith('sheet_01_0-9'))
        self.assertTrue(nomes[1].startswith('sheet_02_9-12'))

    def test_sons_acha_o_estalo_forte_em_4_s(self):
        s = json.loads((self.out / 'ref_vertical' / 'sons.json').read_text(encoding='utf-8'))
        self.assertTrue(any(abs(t['t'] - 4.0) < 0.1 for t in s['transientes']), s['transientes'])
        self.assertIsNotNone(s['lufs'])

    def test_quadro_e_rajada_em_resolucao_cheia(self):
        png = self.tmp / 'q.png'
        py('quadro', self.v, 4.0, '--saida', png)
        self.assertTrue(png.exists() and png.stat().st_size > 100)
        pasta = self.tmp / 'rajada'
        py('quadro', self.v, 2.0, '--rajada', 1.0, '--fps', 5, '--saida', pasta)
        self.assertEqual(len(list(pasta.glob('f_*.png'))), 5)


if __name__ == '__main__':
    unittest.main()
