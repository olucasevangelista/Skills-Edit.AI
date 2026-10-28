"""Testes do variar_ganchos.py com midia sintetica (cada trecho tem um tom e uma cor). Precisam de ffmpeg."""
import csv
import hashlib
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

TEM_FF = bool(shutil.which('ffmpeg') and shutil.which('ffprobe'))
SR, FPS = 48000, 25
CORPO_F, CORPO_VOZ, CORPO_DUR = 440, (0.8, 5.6), 6.0     # tom, voz de/ate, duracao
G1 = dict(f=880, voz=(0.2, 2.4), dur=3.0, cor='red', tam='320x240')
G2 = dict(f=1320, voz=(0.1, 1.6), dur=2.0, cor='green', tam='320x240')
G3 = dict(f=660, voz=(0.2, 1.8), dur=2.5, cor='yellow', tam='240x240')   # outra proporcao


def escrever_wav(caminho: Path, f: int, voz, dur: float) -> None:
    n = int(dur * SR)
    x = [0] * n
    a, b = int(voz[0] * SR), int(voz[1] * SR)
    for i in range(a, b):
        rampa = min(1.0, (i - a) / (0.005 * SR), (b - i) / (0.005 * SR))
        x[i] = int(14000 * rampa * math.sin(2 * math.pi * f * i / SR))
    with wave.open(str(caminho), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(struct.pack(f'<{n}h', *x))


def criar(pasta: Path, nome: str, f: int, voz, dur: float, video: str, tam: str) -> Path:
    wav = pasta / f'{nome}.wav'
    escrever_wav(wav, f, voz, dur)
    mp4 = pasta / f'{nome}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'{video},scale={tam.replace("x", ":")},format=yuv420p', '-i', str(wav),
                    '-c:v', 'libx264', '-c:a', 'aac', '-shortest', str(mp4)], check=True)
    return mp4


def criar_corpo(pasta: Path) -> Path:
    # azul de 0 a 3 s, branco de 3 a 6 s (para comparar o corpo entre variantes)
    video = (f'color=c=blue:s=320x240:r={FPS}:d={CORPO_DUR},'
             "drawbox=x=0:y=0:w=iw:h=ih:color=white:t=fill:enable='gte(t,3)'")
    return criar(pasta, 'corpo', CORPO_F, CORPO_VOZ, CORPO_DUR, video, '320x240')


def criar_gancho(pasta: Path, nome: str, g: dict) -> Path:
    video = f'color=c={g["cor"]}:s={g["tam"]}:r={FPS}:d={g["dur"]}'
    return criar(pasta, nome, g['f'], g['voz'], g['dur'], video, g['tam'])


def py(*args, check=True):
    r = subprocess.run([sys.executable, str(SCRIPTS / 'variar_ganchos.py'), *map(str, args)], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode:
        raise AssertionError(f'variar_ganchos.py falhou ({r.returncode}):\n{r.stdout}\n{r.stderr}')
    return r


def goertzel(x, f):
    k = 2 * math.cos(2 * math.pi * f / SR)
    s1 = s2 = 0.0
    for v in x:
        s0 = v + k * s1 - s2
        s1, s2 = s0, s1
    return (s1 * s1 + s2 * s2 - k * s1 * s2) / (len(x) ** 2)


def frames(mp4: Path, lado=(8, 6)):
    v = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(mp4), '-vf', f'scale={lado[0]}:{lado[1]}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       capture_output=True).stdout
    q = lado[0] * lado[1] * 3
    return [v[i:i + q] for i in range(0, len(v) - q + 1, q)]


def entrada_do_corpo(mp4: Path, f_gancho: int):
    """(quando o quadro vira azul do corpo, quando o tom do corpo aparece no audio, quando o tom do gancho some), em segundos."""
    fr = frames(mp4)
    t_video = next(i for i, f in enumerate(fr) if f[2] > 150 and f[0] < 100 and f[1] < 100) / FPS
    a = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(mp4), '-vn', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    x = struct.unpack(f'<{len(a) // 2}h', a)
    jan = int(0.01 * SR)
    pc = [goertzel(x[i:i + jan], CORPO_F) for i in range(0, len(x) - jan, jan)]
    pg = [goertzel(x[i:i + jan], f_gancho) for i in range(0, len(x) - jan, jan)]
    t_audio = next(i for i, p in enumerate(pc) if p > 0.15 * max(pc)) * 0.01
    t_fim_g = max(i for i, p in enumerate(pg) if p > 0.15 * max(pg)) * 0.01 + 0.01
    return t_video, t_audio, t_fim_g


def ler_matriz(caminho: Path):
    with open(caminho, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


@unittest.skipUnless(TEM_FF, 'precisa de ffmpeg e ffprobe')
class Variar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='creativelab_'))
        cls.corpo = criar_corpo(cls.tmp)
        cls.g1, cls.g2, cls.g3 = (criar_gancho(cls.tmp, n, g) for n, g in (('g1', G1), ('g2', G2), ('g3', G3)))
        cls.out = cls.tmp / 'saida'
        py('--corpo', cls.corpo, '--ganchos', cls.g1, cls.g2, cls.g3, '--saida', cls.out, '--prefixo', 'anuncio')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_uma_variante_por_gancho_com_nome_certo(self):
        nomes = sorted(p.name for p in self.out.glob('*.mp4'))
        self.assertEqual(nomes, ['anuncio__g1.mp4', 'anuncio__g2.mp4', 'anuncio__g3.mp4'])
        self.assertFalse((self.out / '_tmp_ganchos').exists(), 'temporarios deveriam ser apagados')

    def test_imagem_e_audio_do_corpo_entram_juntos_antes_do_gancho_acabar(self):
        for nome, g in (('g1', G1), ('g2', G2)):
            t_video, t_audio, t_fim_g = entrada_do_corpo(self.out / f'anuncio__{nome}.mp4', g['f'])
            self.assertLess(abs(t_video - t_audio), 0.07, f'{nome}: imagem em {t_video:.3f} s e audio em {t_audio:.3f} s precisam entrar juntos')
            self.assertLess(t_audio, t_fim_g - 0.04, f'{nome}: o corpo tem que entrar antes de a fala do gancho acabar')
            self.assertLess(t_fim_g - t_audio, 0.30, f'{nome}: as vozes se sobrepoem por pouco tempo')

    def test_controle_sem_sobreposicao_reprova(self):
        out = self.tmp / 'sem_sobreposicao'
        py('--corpo', self.corpo, '--ganchos', self.g1, '--saida', out, '--sobreposicao', '0.05', '--prefixo', 'x')
        _, t_audio, t_fim_g = entrada_do_corpo(out / 'x__g1.mp4', G1['f'])
        self.assertGreaterEqual(t_audio, t_fim_g - 0.04, 'com sobreposicao minima, o corpo NAO deveria entrar antes do fim da fala do gancho')

    def test_duracao_bate_com_a_calculada(self):
        for linha in ler_matriz(self.out / 'matriz.csv'):
            g = {'g1': G1, 'g2': G2, 'g3': G3}[linha['gancho'].split('.')[0]]
            esperado = (g['voz'][1] + 0.10 - 0.22) + (CORPO_DUR - (CORPO_VOZ[0] - 0.025))
            self.assertAlmostEqual(float(linha['duracao_total_s']), esperado, delta=0.15, msg=linha['gancho'])

    def test_volume_no_alvo_e_igual_entre_variantes(self):
        lufs = [float(l['lufs']) for l in ler_matriz(self.out / 'matriz.csv')]
        for v in lufs:
            self.assertLess(abs(v + 14.0), 1.5, f'LUFS {v} fora do alvo -14')
        self.assertLess(max(lufs) - min(lufs), 1.0, f'variantes com volumes diferentes: {lufs}')

    def test_o_corpo_e_identico_em_todas_as_variantes(self):
        def quadro_do_corpo(nome, g):
            fr = frames(self.out / f'anuncio__{nome}.mp4')
            emenda = g['voz'][1] + 0.10 - 0.22
            i = round((emenda + (4.0 - (CORPO_VOZ[0] - 0.025))) * FPS)     # o instante 4,0 s do corpo (branco)
            return hashlib.md5(fr[i]).hexdigest(), fr[i]
        h1, f1 = quadro_do_corpo('g1', G1)
        h2, f2 = quadro_do_corpo('g2', G2)
        self.assertEqual(h1, h2, 'o mesmo quadro do corpo tem que ser igual nas variantes')
        self.assertTrue(f1[0] > 200 and f1[1] > 200 and f1[2] > 200, 'o quadro do corpo em 4 s deveria ser branco')

    def test_gancho_de_outra_proporcao_sai_no_tamanho_do_corpo(self):
        d = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0',
                            str(self.out / 'anuncio__g3.mp4')], capture_output=True, text=True).stdout.strip()
        self.assertEqual(d, '320,240')
        linha = next(l for l in ler_matriz(self.out / 'matriz.csv') if l['gancho'] == 'g3.mp4')
        self.assertIn('proporcao', linha['observacoes'])

    def test_matriz_tem_colunas_das_metricas_em_branco(self):
        with open(self.out / 'matriz.csv', encoding='utf-8-sig', newline='') as f:
            leitor = csv.DictReader(f, delimiter=';')
            linhas = list(leitor)
            cols = leitor.fieldnames
        for c in ('variante', 'arquivo', 'gancho', 'emenda_em_s', 'lufs', 'hook_rate', 'hold_rate', 'ctr'):
            self.assertIn(c, cols)
        self.assertEqual(len(linhas), 3)
        self.assertTrue(all(l['hook_rate'] == '' and l['hold_rate'] == '' and l['ctr'] == '' for l in linhas))

    def test_aceita_uma_pasta_de_ganchos(self):
        pasta = self.tmp / 'pasta_ganchos'
        pasta.mkdir()
        shutil.copy(self.g1, pasta / 'a_um.mp4')
        shutil.copy(self.g2, pasta / 'b_dois.mp4')
        out = self.tmp / 'saida_pasta'
        py('--corpo', self.corpo, '--ganchos', pasta, '--saida', out)
        self.assertEqual(sorted(p.name for p in out.glob('*.mp4')), ['corpo__a_um.mp4', 'corpo__b_dois.mp4'])

    def test_erro_claro_sem_audio_no_gancho(self):
        mudo = self.tmp / 'mudo.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=c=red:s=320x240:r={FPS}:d=2', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(mudo)], check=True)
        r = py('--corpo', self.corpo, '--ganchos', mudo, '--saida', self.tmp / 'x', check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn('imagem e audio', r.stderr)


class Puro(unittest.TestCase):
    def test_faixas_de_fala_acham_o_comeco_e_o_fim_da_voz(self):
        env = [-80.0] * 400
        for i in range(80, 300):
            env[i] = -20.0
        f = _fala.faixas_de_fala(env, -40.0)
        self.assertEqual(len(f), 1)
        self.assertAlmostEqual(f[0][0], 0.80, places=2)
        self.assertAlmostEqual(f[0][1], 3.00, places=2)


if __name__ == '__main__':
    unittest.main()
