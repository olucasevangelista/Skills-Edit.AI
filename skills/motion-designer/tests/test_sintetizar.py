"""Testes do sintetizar.py (precisam de numpy). Verificam duração, pico, eventos audíveis e determinismo."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path

try:
    import numpy as np
except ImportError:  # a síntese é opcional: sem numpy, os testes dela são pulados
    np = None

KIT = Path(__file__).resolve().parents[1] / "kit" / "audio"


def rodar(mapa: Path, saida: Path, check=True):
    r = subprocess.run([sys.executable, str(KIT / "sintetizar.py"), str(mapa), "--saida", str(saida)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode:
        raise AssertionError(f"sintetizar.py falhou ({r.returncode}):\n{r.stdout}\n{r.stderr}")
    return r


def ler(caminho: Path):
    with wave.open(str(caminho), "rb") as w:
        assert w.getnchannels() == 2 and w.getsampwidth() == 2
        taxa, n = w.getframerate(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float64) / 32768.0
    return taxa, x.reshape(-1, 2)


def rms(x, taxa, a, b):
    seg = x[int(a * taxa):int(b * taxa)]
    return float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 0.0


@unittest.skipIf(np is None, "precisa de numpy")
class Sintese(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="md_audio_"))
        cls.mapa = KIT / "mapa-exemplo.json"
        cls.a = cls.tmp / "a"
        rodar(cls.mapa, cls.a)

    def test_duracao_exata_e_estereo(self):
        for nome in ("sfx.wav", "musica.wav", "mix.wav"):
            taxa, x = ler(self.a / nome)
            self.assertEqual(len(x), 12 * taxa, nome)

    def test_pico_da_mistura_abaixo_de_menos_1_dBFS(self):
        _, x = ler(self.a / "mix.wav")
        self.assertLess(np.max(np.abs(x)), 10 ** (-1.0 / 20))
        self.assertGreater(np.max(np.abs(x)), 0.2, "mistura quase muda")

    def test_cada_evento_de_efeito_e_audivel_no_instante_certo(self):
        taxa, x = ler(self.a / "sfx.wav")
        mapa = json.loads(self.mapa.read_text(encoding="utf-8"))
        for ev in mapa["eventos"]:
            antes = rms(x, taxa, ev["t"] - 0.25, ev["t"] - 0.02)
            depois = rms(x, taxa, ev["t"], ev["t"] + 0.15)
            self.assertGreater(depois, 0.003, f"{ev['tipo']} em {ev['t']} s não soa")
            self.assertGreater(depois, 4 * max(antes, 1e-6), f"{ev['tipo']} em {ev['t']} s não se destaca do silêncio")

    def test_trilha_comeca_na_primeira_batida_e_acaba_em_fade(self):
        taxa, x = ler(self.a / "musica.wav")
        self.assertGreater(rms(x, taxa, 0.0, 0.2), 0.01)
        self.assertLess(rms(x, taxa, 11.9, 12.0), 0.2 * rms(x, taxa, 6.0, 6.5))

    def test_mesma_semente_gera_o_mesmo_audio_e_outra_semente_muda(self):
        b = self.tmp / "b"
        rodar(self.mapa, b)
        h = lambda p: hashlib.sha256((p).read_bytes()).hexdigest()  # noqa: E731
        self.assertEqual(h(self.a / "mix.wav"), h(b / "mix.wav"))
        mapa2 = json.loads(self.mapa.read_text(encoding="utf-8"))
        mapa2["semente"] = 99
        m2 = self.tmp / "mapa2.json"
        m2.write_text(json.dumps(mapa2), encoding="utf-8")
        rodar(m2, self.tmp / "c")
        self.assertNotEqual(h(self.a / "mix.wav"), h(self.tmp / "c" / "mix.wav"))

    def test_sem_trilha_gera_so_efeitos_e_mix(self):
        mapa = {"duracao": 2, "eventos": [{"t": 0.5, "tipo": "bumbo"}]}
        m = self.tmp / "so_sfx.json"
        m.write_text(json.dumps(mapa), encoding="utf-8")
        rodar(m, self.tmp / "d")
        self.assertTrue((self.tmp / "d" / "sfx.wav").exists() and (self.tmp / "d" / "mix.wav").exists())
        self.assertFalse((self.tmp / "d" / "musica.wav").exists())

    def test_tipo_desconhecido_da_erro_claro(self):
        m = self.tmp / "ruim.json"
        m.write_text(json.dumps({"duracao": 1, "eventos": [{"t": 0.2, "tipo": "harpa"}]}), encoding="utf-8")
        r = rodar(m, self.tmp / "e", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("harpa", r.stderr + r.stdout)


if __name__ == "__main__":
    unittest.main()
