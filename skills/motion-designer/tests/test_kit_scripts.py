"""Testes do ataque.py (precisa de numpy e FFmpeg) e da folha_de_quadros.py (precisa de Pillow)."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path

try:
    import numpy as np
except ImportError:
    np = None
try:
    from PIL import Image
except ImportError:
    Image = None

KIT = Path(__file__).resolve().parents[1] / "kit"
TEM_FF = bool(shutil.which("ffmpeg"))


def py(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")


def gravar_wav(caminho: Path, x: "np.ndarray", sr: int = 48000) -> None:
    with wave.open(str(caminho), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


@unittest.skipIf(np is None or not TEM_FF, "precisa de numpy e ffmpeg")
class Ataque(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="md_ataque_"))
        sr = 48000
        t = np.arange(int(1.2 * sr)) / sr
        # 0,30 s de silêncio, subida até o pico em 0,50 s, decaimento até ~0,9 s
        env = np.interp(t, [0.0, 0.30, 0.31, 0.50, 0.90, 0.95], [0, 0, 0.3, 1.0, 0.06, 0.0])
        gravar_wav(cls.tmp / "pop.wav", 0.8 * env * np.sin(2 * np.pi * 440 * t))
        gravar_wav(cls.tmp / "mudo.wav", np.zeros(sr))

    def medidas(self, *nomes):
        r = py(KIT / "audio" / "ataque.py", *[str(self.tmp / n) for n in nomes], "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)

    def test_mede_inicio_pico_e_fim(self):
        m = self.medidas("pop.wav")[0]
        self.assertAlmostEqual(m["duracao"], 1.2, places=2)
        self.assertAlmostEqual(m["inicio"], 0.31, delta=0.03)
        self.assertAlmostEqual(m["pico"], 0.50, delta=0.03)
        self.assertTrue(0.85 <= m["fim"] <= 0.95, m)

    def test_arquivo_mudo_nao_inventa_pontos(self):
        m = self.medidas("mudo.wav")[0]
        self.assertIsNone(m["pico"])

    def test_para_o_pico_cair_no_evento_o_arquivo_comeca_antes(self):
        m = self.medidas("pop.wav")[0]
        evento = 2.0
        inicio_do_arquivo = evento - m["pico"]
        self.assertAlmostEqual(inicio_do_arquivo, 1.5, delta=0.03)


@unittest.skipIf(Image is None, "precisa de Pillow")
class FolhaDeQuadros(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="md_folha_"))
        cls.cores = [(220, 30, 30), (30, 200, 60), (40, 60, 230)]
        for i, c in enumerate(cls.cores, 1):
            Image.new("RGB", (320, 180), c).save(cls.tmp / f"{i:02d}.png")
        (cls.tmp / "legendas.json").write_text(json.dumps([
            {"tempo": "0 a 3 s", "titulo": "Gancho", "texto": "o objeto assenta", "move": "câmera recua devagar", "vira": "o disco cresce"},
            {"titulo": "Processo"}, {"titulo": "Fecho", "texto": "marca estável"}]), encoding="utf-8")

    def test_gera_a_folha_com_os_quadros_nas_posicoes_certas(self):
        saida = self.tmp / "board.png"
        r = py(KIT / "folha_de_quadros.py", str(self.tmp), "--saida", str(saida), "--legendas", str(self.tmp / "legendas.json"), "--colunas", "3")
        self.assertEqual(r.returncode, 0, r.stderr)
        im = Image.open(saida).convert("RGB")
        self.assertEqual(im.width, 30 * 2 + 3 * 640 + 2 * 28)
        # o centro de cada quadro tem a cor da imagem de origem (ordem 01, 02, 03)
        for i, cor in enumerate(self.cores):
            x = 30 + i * (640 + 28) + 320
            y = 30 + 180
            px = im.getpixel((x, y))
            self.assertTrue(all(abs(a - b) < 12 for a, b in zip(px, cor)), f"quadro {i + 1}: {px} != {cor}")

    def test_sem_imagens_da_erro_claro(self):
        vazia = self.tmp / "vazia"
        vazia.mkdir()
        r = py(KIT / "folha_de_quadros.py", str(vazia), "--saida", str(self.tmp / "x.png"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Nenhuma imagem", r.stderr + r.stdout)


if __name__ == "__main__":
    unittest.main()
