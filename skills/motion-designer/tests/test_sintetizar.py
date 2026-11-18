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


def rodar(mapa: Path, saida: Path, *extra: str, check=True):
    r = subprocess.run([sys.executable, str(KIT / "sintetizar.py"), str(mapa), "--saida", str(saida), *extra],
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


@unittest.skipIf(np is None, "precisa de numpy")
class SomPorEvento(unittest.TestCase):
    """O som lê os instantes do mesmo EVENTOS da animação: mudou o tempo, o som acompanha."""
    EXEMPLO = KIT.parent / "exemplo" / "config.ts"

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="md_eventos_"))

    def sfx(self, mapa: dict, nome: str, *extra: str):
        m = self.tmp / f"{nome}.json"
        m.write_text(json.dumps(mapa), encoding="utf-8")
        rodar(m, self.tmp / nome, *extra)
        return ler(self.tmp / nome / "sfx.wav")

    def test_evento_por_nome_gera_o_mesmo_audio_que_o_instante_digitado(self):
        rodar(KIT / "mapa-eventos-exemplo.json", self.tmp / "nome", "--eventos", str(self.EXEMPLO), "--fps", "30")
        rodar(KIT / "mapa-exemplo.json", self.tmp / "segundos")
        h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
        self.assertEqual(h(self.tmp / "nome" / "mix.wav"), h(self.tmp / "segundos" / "mix.wav"))

    def test_mudar_o_tempo_do_evento_move_o_som(self):
        mapa = {"duracao": 4, "eventos": [{"evento": "batida", "tipo": "bumbo"}]}
        for t in (1.0, 2.5):
            ev = self.tmp / f"ev{t}.json"
            ev.write_text(json.dumps({"batida": t}), encoding="utf-8")
            taxa, x = self.sfx(mapa, f"move{t}", "--eventos", str(ev))
            self.assertGreater(rms(x, taxa, t, t + 0.15), 4 * max(rms(x, taxa, t - 0.5, t - 0.05), 1e-6), f"o som não caiu em {t} s")

    def test_fps_encaixa_o_evento_no_quadro(self):
        taxa, x = self.sfx({"duracao": 3, "eventos": [{"t": 1.01, "tipo": "bumbo"}]}, "grade", "--fps", "30")
        self.assertGreater(rms(x, taxa, 1.0, 1.1), 0.003)
        self.assertLess(rms(x, taxa, 0.9, 0.995), 0.001, "o som deveria começar no quadro 30 (1,000 s), não antes")

    def test_deslocamento_ajusta_o_evento(self):
        ev = self.tmp / "desl_eventos.json"
        ev.write_text(json.dumps({"batida": 2.0}), encoding="utf-8")
        taxa, x = self.sfx({"duracao": 4, "eventos": [{"evento": "batida", "deslocamento": -0.5, "tipo": "bumbo"}]}, "desl", "--eventos", str(ev))
        self.assertGreater(rms(x, taxa, 1.5, 1.65), 0.003)
        self.assertLess(rms(x, taxa, 1.9, 2.1), 0.0005, "não deveria soar no instante original")

    def test_evento_desconhecido_da_erro_claro_com_os_nomes_que_existem(self):
        m = self.tmp / "desc.json"
        m.write_text(json.dumps({"duracao": 2, "eventos": [{"evento": "nao.existe", "tipo": "clique"}]}), encoding="utf-8")
        r = rodar(m, self.tmp / "desc", "--eventos", str(self.EXEMPLO), check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("nao.existe", r.stderr + r.stdout)
        self.assertIn("etapa.separa", r.stderr + r.stdout)

    def test_evento_sem_passar_a_lista_pede_o_arquivo(self):
        m = self.tmp / "sem.json"
        m.write_text(json.dumps({"duracao": 2, "eventos": [{"evento": "x", "tipo": "clique"}]}), encoding="utf-8")
        r = rodar(m, self.tmp / "sem", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--eventos", r.stderr + r.stdout)

    def test_evento_e_t_juntos_sao_ambiguos(self):
        ev = self.tmp / "amb_ev.json"
        ev.write_text(json.dumps({"x": 1.0}), encoding="utf-8")
        m = self.tmp / "amb.json"
        m.write_text(json.dumps({"duracao": 2, "eventos": [{"evento": "x", "t": 1.0, "tipo": "clique"}]}), encoding="utf-8")
        r = rodar(m, self.tmp / "amb", "--eventos", str(ev), check=False)
        self.assertNotEqual(r.returncode, 0)

    def test_config_com_expressao_em_vez_de_numero_da_erro_claro(self):
        cfg = self.tmp / "config.ts"
        cfg.write_text('export const EVENTOS = {\n  "a": 1.5,\n  "b": ETAPAS[0].t,\n} as const;\n', encoding="utf-8")
        m = self.tmp / "expr.json"
        m.write_text(json.dumps({"duracao": 2, "eventos": [{"evento": "a", "tipo": "clique"}]}), encoding="utf-8")
        r = rodar(m, self.tmp / "expr", "--eventos", str(cfg), check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("EVENTOS", r.stderr + r.stdout)


if __name__ == "__main__":
    unittest.main()
