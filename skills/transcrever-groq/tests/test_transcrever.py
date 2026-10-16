"""Regressao do porte: mesma logica de blocos, tempos e exportacao do script original, sem rede.
Tambem testa o comportamento sem chave e a independencia do diretorio de trabalho.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / 'scripts' / 'transcrever.py'
sys.path.insert(0, str(SKILL / 'scripts'))

import httpx  # noqa: E402
from groq import Groq  # noqa: E402

from _midia import nome_seguro, tempo  # noqa: E402
from transcrever import agrupar, exportar, planejar, reunir, srt_time, transcrever  # noqa: E402

TEM_FFMPEG = shutil.which('ffmpeg') and shutil.which('ffprobe')


class PortedPipelineTests(unittest.TestCase):
    def test_parse_time_and_reject_invalid_values(self):
        self.assertEqual(tempo('1:02:03.5'), 3723.5)
        self.assertEqual(tempo('90'), 90)
        for bad in ('-1', '1:60', 'abc', '1:2:3:4'):
            with self.assertRaises(Exception):
                tempo(bad)

    def test_windows_names(self):
        self.assertEqual(nome_seguro('con'), 'video-con')
        self.assertEqual(nome_seguro('Meu video: final?'), 'Meu-video-final')

    def test_chunk_ownership_has_no_gaps_with_context(self):
        chunks = planejar(100, 125, 10, 1)
        self.assertEqual([(c['start'], c['end']) for c in chunks], [(100, 111), (109, 121), (119, 125)])
        self.assertEqual([(c['core_start'], c['core_end']) for c in chunks], [(100, 110), (110, 120), (120, 125)])

    def test_overlapping_chunks_preserve_original_and_clip_times(self):
        chunks = planejar(100, 120, 10, 1)
        first = {'chunk': chunks[0], 'response': {'words': [
            {'word': 'uma', 'start': 9.0, 'end': 9.7},
            {'word': 'empresa', 'start': 10.2, 'end': 10.7}]}}
        second = {'chunk': chunks[1], 'response': {'words': [
            {'word': 'uma', 'start': 0.0, 'end': 0.7},
            {'word': 'empresa', 'start': 1.2, 'end': 1.7}]}}
        words = reunir([first, second], 100, 120)
        self.assertEqual([w['word'] for w in words], ['uma', 'empresa'])
        self.assertEqual(words[1]['start'], 10.2)
        self.assertEqual(words[1]['source_start'], 110.2)

    def test_repeated_words_in_speech_are_preserved(self):
        chunk = planejar(0, 10, 10, 1)[0]
        result = reunir([{'chunk': chunk, 'response': {'words': [
            {'word': 'nao', 'start': 1.0, 'end': 1.3}, {'word': 'nao', 'start': 1.5, 'end': 1.8}]}}], 0, 10)
        self.assertEqual(len(result), 2)

    def test_subtitle_timing_rolls_over_without_invalid_milliseconds(self):
        self.assertEqual(srt_time(59.9996), '00:01:00,000')
        self.assertEqual(srt_time(3600.001), '01:00:00,001')

    def test_captions_do_not_bridge_long_silences(self):
        words = [{'word': 'Empresa.', 'start': 0.0, 'end': 0.5},
                 {'word': 'Trabalho.', 'start': 5.0, 'end': 5.8}]
        groups = agrupar(words)
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]['end'], 0.5)

    def test_exports_are_valid_remotion_json_and_srt(self):
        words = [{'word': 'Voce', 'start': 0.1, 'end': 0.4, 'source_start': 100.1, 'source_end': 100.4},
                 {'word': 'empreende.', 'start': 0.4, 'end': 1.2, 'source_start': 100.4, 'source_end': 101.2}]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            exportar(path, words, {'range_start': 100}, 'whisper-large-v3-turbo', 'pt', 'test')
            captions = json.loads((path/'legendas.remotion.json').read_text(encoding='utf-8'))
            self.assertEqual(captions[0]['startMs'], 100)
            self.assertEqual(set(captions[0]), {'text', 'startMs', 'endMs', 'timestampMs', 'confidence'})
            self.assertIn('00:00:00,100 --> 00:00:01,200', (path/'legendas.srt').read_text(encoding='utf-8'))
            self.assertEqual({p.name for p in path.iterdir()},
                             {'transcricao.json', 'transcricao.txt', 'legendas.srt', 'legendas.remotion.json'})

    def test_real_groq_sdk_multipart_and_cache_resume_without_network(self):
        calls = []

        def respond(request):
            body = request.read()
            self.assertIn(b'whisper-large-v3-turbo', body)
            self.assertIn(b'verbose_json', body)
            self.assertIn(b'timestamp_granularities', body)
            self.assertIn(b'word', body)
            calls.append(request.url.path)
            return httpx.Response(200, json={'text': 'Uma empresa.', 'language': 'portuguese', 'duration': 2,
                'words': [{'word': 'Uma', 'start': 0, 'end': 0.4}, {'word': 'empresa.', 'start': 0.4, 'end': 1.5}], 'segments': []})

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            audio = path/'audio.flac'
            audio.write_bytes(b'fLaC-test-fixture')
            chunk = {**planejar(0, 2, 10, 1)[0], 'audio': str(audio)}
            with Groq(api_key='test-local-only', max_retries=0,
                      http_client=httpx.Client(transport=httpx.MockTransport(respond))) as client:
                a = transcrever(client, [chunk], path/'cache', 'whisper-large-v3-turbo', 'pt', '', False)
                b = transcrever(client, [chunk], path/'cache', 'whisper-large-v3-turbo', 'pt', '', False)
            self.assertEqual(len(calls), 1)
            self.assertEqual(a, b)


@unittest.skipUnless(TEM_FFMPEG, 'ffmpeg/ffprobe nao encontrados')
class LinhaDeComando(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='transcrever-test-'))
        cls.audio = cls.tmp / 'tom.wav'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=2', str(cls.audio)], check=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def rodar(self, args, cwd, env_extra=None):
        env = {k: v for k, v in os.environ.items() if k != 'GROQ_API_KEY'}
        env.update({'TRANSCREVER_GROQ_SERVICE': 'groq-api-TEST-inexistente', 'TRANSCREVER_GROQ_NO_REEXEC': '1'})
        env.update(env_extra or {})
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd, env=env, capture_output=True, text=True, encoding='utf-8')

    def test_sem_chave_falha_claro_sem_criar_nada_e_sem_rede(self):
        saida = self.tmp / 'saida-sem-chave'
        r = self.rodar([str(self.audio), '--saida', str(saida)], cwd=self.tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn('nao configurada', r.stderr)
        self.assertIn('Nenhuma chamada foi feita', r.stderr)
        self.assertIn('configurar.py setup', r.stderr)
        self.assertFalse(saida.exists())

    def test_saida_e_obrigatoria(self):
        r = self.rodar([str(self.audio)], cwd=self.tmp)
        self.assertEqual(r.returncode, 2)
        self.assertIn('--saida', r.stderr)

    def test_funciona_de_qualquer_diretorio_com_caminhos_relativos(self):
        outro = self.tmp / 'outro-projeto' / 'sub'
        outro.mkdir(parents=True)
        shutil.copy(self.audio, outro / 'meu audio.wav')
        r = self.rodar(['meu audio.wav', '--saida', 'transcricoes', '--nome', 'teste', '--preparar-apenas'], cwd=outro)
        self.assertEqual(r.returncode, 0, r.stderr)
        manifesto = json.loads((outro / 'transcricoes' / 'teste' / 'preparacao.json').read_text(encoding='utf-8'))
        self.assertEqual(manifesto['model'], 'whisper-large-v3-turbo')
        self.assertEqual(manifesto['language'], 'pt')
        self.assertEqual(len(manifesto['chunks']), 1)
        self.assertTrue(Path(manifesto['chunks'][0]['audio']).is_file())

    def test_chave_da_variavel_chega_a_etapa_de_rede_sem_aparecer_na_saida(self):
        # Chave falsa + proxy inexistente: deve passar da checagem de chave, falhar na conexao e NAO ecoar a chave.
        falsa = 'gsk_' + 'Q1w2E3r4' * 6
        saida = self.tmp / 'saida-rede'
        r = self.rodar([str(self.audio), '--saida', str(saida)], cwd=self.tmp,
                       env_extra={'GROQ_API_KEY': falsa, 'HTTPS_PROXY': 'http://127.0.0.1:9', 'HTTP_PROXY': 'http://127.0.0.1:9',
                                  'ALL_PROXY': 'http://127.0.0.1:9', 'NO_PROXY': ''})
        self.assertEqual(r.returncode, 1)
        self.assertNotIn(falsa, r.stdout + r.stderr)
        self.assertNotIn('nao configurada', r.stderr)
        self.assertIn('conexao', r.stderr.lower())


if __name__ == '__main__':
    unittest.main()
