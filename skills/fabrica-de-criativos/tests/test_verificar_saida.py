"""Testes do verificar_saida.py com video sintetico. Precisam de ffmpeg."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))

TEM_FF = bool(shutil.which('ffmpeg') and shutil.which('ffprobe'))


def py(*args):
    r = subprocess.run([sys.executable, str(SCRIPTS / 'verificar_saida.py'), *map(str, args)], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r


def gerar(pasta: Path, nome: str, video: str, tam='1080x1920', fps=30, dur=6, audio=True, volume_db=-12):
    """Gera um mp4 sintetico. `video` e um filtro lavfi (ja com tamanho)."""
    mp4 = pasta / f'{nome}.mp4'
    args = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'{video},fps={fps},format=yuv420p']
    if audio:
        args += ['-f', 'lavfi', '-i', f'sine=f=440:d={dur},volume={volume_db}dB']
    args += ['-t', str(dur), '-c:v', 'libx264', '-crf', '20'] + (['-c:a', 'aac', '-b:a', '160k'] if audio else ['-an']) + [str(mp4)]
    subprocess.run(args, check=True)
    return mp4


def quadrado_que_se_mexe(quando: str, dur=6) -> str:
    """Fundo liso com um quadrado que anda enquanto `quando` for verdadeiro e fica parado no resto (no overlay, `t` e o tempo)."""
    return (f"color=c=0x2255AA:s=1080x1920:d={dur}[bg];color=c=0xFFC857:s=120x120:d={dur}[bx];"
            f"[bg][bx]overlay=x='if({quando},mod(t*300,900),0)':y=900")


def movimento(tam='1080x1920', dur=6):
    return f'testsrc2=s={tam}:d={dur}'


@unittest.skipUnless(TEM_FF, 'precisa de ffmpeg e ffprobe')
class Verificar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='fabrica_saida_'))
        # som com volume bem proximo de -14 LUFS (medido abaixo e usado como alvo)
        cls.bom = gerar(cls.tmp, 'bom', movimento())
        r = py(cls.bom, '--lufs', '-14', '--tolerancia-lufs', '40', '--json')
        cls.lufs_bom = json.loads(r.stdout)['lufs']

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_arquivo_bom_passa(self):
        r = py(self.bom, '--lufs', f'{self.lufs_bom}', '--duracao', 6)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('Tudo certo', r.stdout)

    def test_volume_fora_do_alvo_e_acusado(self):
        r = py(self.bom, '--lufs', f'{self.lufs_bom - 10}')
        self.assertEqual(r.returncode, 1)
        self.assertIn('fora do alvo', r.stdout)

    def test_tamanho_errado_e_acusado(self):
        mp4 = gerar(self.tmp, 'pequeno', movimento('720x1280'))
        r = py(mp4, '--lufs', f'{self.lufs_bom}')
        self.assertEqual(r.returncode, 1)
        self.assertIn('tamanho 720x1280', r.stdout)

    def test_taxa_de_quadros_errada_e_acusada(self):
        mp4 = gerar(self.tmp, 'fps24', movimento(), fps=24)
        r = py(mp4, '--lufs', f'{self.lufs_bom}')
        self.assertEqual(r.returncode, 1)
        self.assertIn('taxa de quadros', r.stdout)

    def test_duracao_diferente_da_esperada_e_acusada(self):
        r = py(self.bom, '--lufs', f'{self.lufs_bom}', '--duracao', 10)
        self.assertEqual(r.returncode, 1)
        self.assertIn('duracao', r.stdout)

    def test_sem_audio_e_acusado(self):
        mp4 = gerar(self.tmp, 'mudo', movimento(), audio=False)
        r = py(mp4)
        self.assertEqual(r.returncode, 1)
        self.assertIn('nao tem faixa de audio', r.stdout)

    def test_quadro_preto_longo_e_acusado(self):
        # 1 s de imagem, 2 s de preto, 3 s de imagem
        video = (f"testsrc2=s=1080x1920:d=6,drawbox=x=0:y=0:w=iw:h=ih:color=black:t=fill:enable='between(t,1,3)'")
        mp4 = gerar(self.tmp, 'preto', video)
        r = py(mp4, '--lufs', f'{self.lufs_bom}')
        self.assertEqual(r.returncode, 1)
        self.assertIn('quadro preto', r.stdout)

    def test_imagem_congelada_longa_e_acusada(self):
        # os primeiros 4 s sao uma imagem parada; o resto se mexe
        video = quadrado_que_se_mexe("gt(t,4)")
        mp4 = gerar(self.tmp, 'parado', video)
        r = py(mp4, '--lufs', f'{self.lufs_bom}', '--congelado-max', 3)
        self.assertEqual(r.returncode, 1)
        self.assertIn('imagem congelada', r.stdout)

    def test_quadro_final_parado_curto_nao_e_acusado(self):
        # quadro final parado por 2 s (menos que o limite): aceitavel
        video = quadrado_que_se_mexe("lt(t,4)")
        mp4 = gerar(self.tmp, 'final_parado', video)
        r = py(mp4, '--lufs', f'{self.lufs_bom}', '--congelado-max', 3)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_o_fixture_do_quadrado_realmente_se_mexe_e_realmente_para(self):
        mp4 = gerar(self.tmp, 'fixture', quadrado_que_se_mexe("lt(t,4)"))

        def quadro(t):
            return subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', str(mp4), '-frames:v', '1', '-vf', 'scale=108:192', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                                  capture_output=True).stdout
        self.assertNotEqual(quadro(1.0), quadro(2.0), 'o quadrado deveria andar antes dos 4 s')
        self.assertEqual(quadro(4.5), quadro(5.5), 'o quadrado deveria estar parado depois dos 4 s')

    def test_saida_json(self):
        r = py(self.bom, '--lufs', f'{self.lufs_bom}', '--json')
        d = json.loads(r.stdout)
        self.assertEqual(d['problemas'], [])
        self.assertIsNotNone(d['lufs'])


if __name__ == '__main__':
    unittest.main()
