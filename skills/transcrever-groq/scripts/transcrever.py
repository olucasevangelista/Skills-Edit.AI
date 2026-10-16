#!/usr/bin/env python3
"""Transcricao com Groq (Whisper) -> SRT, TXT, JSON e legendas para Remotion; aceita videos longos.

A midia original nunca e alterada. So blocos de audio mono 16 kHz sao enviados a Groq.
A chave vem do cofre do sistema (configure uma vez com configurar.py setup) ou da variavel GROQ_API_KEY.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _ambiente as amb  # noqa: E402
import _credenciais as cred  # noqa: E402
from _midia import executar, gravar_json, inspecionar, nome_seguro, programa, tempo  # noqa: E402


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Transcreve video/audio na Groq e exporta legendas sincronizadas.')
    parser.add_argument('arquivo', type=Path, help='Caminho do MP4, MOV, MP3, WAV ou outro arquivo local.')
    parser.add_argument('--saida', type=Path, required=True,
                        help='Pasta onde as transcricoes serao gravadas (obrigatorio; cria uma subpasta por --nome).')
    parser.add_argument('--nome', help='Nome da subpasta da transcricao; padrao: nome do arquivo.')
    parser.add_argument('--inicio', type=tempo, default=0.0, help='Inicio no original: segundos, MM:SS ou HH:MM:SS.')
    parser.add_argument('--fim', type=tempo, help='Fim no original. Se omitido, usa o final do arquivo.')
    parser.add_argument('--modelo', help='Padrao: GROQ_MODEL ou whisper-large-v3-turbo.')
    parser.add_argument('--idioma', help='Codigo do idioma; padrao: GROQ_LANGUAGE ou pt.')
    parser.add_argument('--contexto', default='', help='Contexto curto e grafia de nomes para melhorar a transcricao.')
    parser.add_argument('--bloco-segundos', type=int, default=600, help='Duracao por bloco, de 10 a 600 segundos.')
    parser.add_argument('--sobreposicao', type=float, default=1.0, help='Contexto extra em cada borda; de 0 a 3 segundos.')
    parser.add_argument('--preparar-apenas', action='store_true', help='Extrai audio e gera manifesto sem chamar API nem exigir chave.')
    parser.add_argument('--refazer', action='store_true', help='Refaz chamadas e substitui uma transcricao existente.')
    return parser.parse_args()


def planejar(inicio: float, fim: float, tamanho: int, sobreposicao: float) -> list[dict]:
    chunks = []
    for i in range(math.ceil((fim-inicio)/tamanho)):
        core_start = inicio+i*tamanho
        core_end = min(fim, core_start+tamanho)
        chunks.append({'index': i, 'core_start': core_start, 'core_end': core_end,
                       'start': max(inicio, core_start-sobreposicao),
                       'end': min(fim, core_end+sobreposicao)})
    return chunks


def preparar(source: Path, output: Path, chunks: list[dict]) -> None:
    folder = output / 'audio'
    folder.mkdir(parents=True, exist_ok=True)
    for chunk in chunks:
        target = folder / f'{chunk["index"]:04d}.flac'
        if not target.exists():
            temporary = target.with_suffix('.tmp.flac')
            executar([programa('ffmpeg'), '-hide_banner', '-loglevel', 'error', '-y',
                      '-ss', str(chunk['start']), '-i', str(source), '-t', str(chunk['end']-chunk['start']),
                      '-map', '0:a:0', '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'flac', str(temporary)])
            temporary.replace(target)
        if target.stat().st_size >= 24_000_000:
            raise RuntimeError('Bloco acima do limite de upload. Diminua --bloco-segundos.')
        chunk['audio'] = str(target)


def transcrever(client, chunks: list[dict], cache: Path, model: str, language: str, prompt: str, refazer: bool) -> list[dict]:
    results = []
    cache.mkdir(parents=True, exist_ok=True)
    for chunk in chunks:
        audio = Path(chunk['audio'])
        signature = hashlib.sha256(audio.read_bytes()).hexdigest()
        request_key = {'sha256': signature, 'model': model, 'language': language, 'prompt': prompt}
        checkpoint = cache / f'{chunk["index"]:04d}.json'
        cached = json.loads(checkpoint.read_text(encoding='utf-8')) if checkpoint.exists() else None
        if not refazer and cached and cached.get('request') == request_key:
            raw = cached['response']
            print(f'Bloco {chunk["index"]+1}/{len(chunks)}: reutilizado.', flush=True)
        else:
            print(f'Bloco {chunk["index"]+1}/{len(chunks)}: transcrevendo...', flush=True)
            with audio.open('rb') as stream:
                kwargs = {'file': (audio.name, stream), 'model': model, 'language': language,
                          'response_format': 'verbose_json', 'timestamp_granularities': ['word', 'segment'],
                          'temperature': 0.0}
                if prompt:
                    kwargs['prompt'] = prompt
                response = client.audio.transcriptions.create(**kwargs)
            raw = response.model_dump(mode='json')
            gravar_json(checkpoint, {'request': request_key, 'response': raw})
        if raw.get('text', '').strip() and not raw.get('words'):
            raise RuntimeError('A API retornou texto sem tempos por palavra. Resposta preservada no cache; nao foram inventados tempos.')
        results.append({'chunk': chunk, 'response': raw})
    return results


def reunir(results: list[dict], range_start: float, range_end: float) -> list[dict]:
    words = []
    for item in results:
        chunk = item['chunk']
        for word in item['response'].get('words', []):
            text = str(word.get('word', '')).strip()
            start, end = float(word['start']), float(word['end'])
            if not text or not math.isfinite(start) or not math.isfinite(end) or end <= start:
                continue
            absolute_start = chunk['start'] + start
            absolute_end = chunk['start'] + end
            midpoint = (absolute_start+absolute_end)/2
            # Each overlapped word belongs to one non-overlapping core interval.
            if not chunk['core_start'] <= midpoint < chunk['core_end']:
                continue
            absolute_start, absolute_end = max(range_start, absolute_start), min(range_end, absolute_end)
            if absolute_end <= absolute_start:
                continue
            words.append({'word': text, 'start': round(absolute_start-range_start, 6),
                          'end': round(absolute_end-range_start, 6),
                          'source_start': round(absolute_start, 6), 'source_end': round(absolute_end, 6)})
    words.sort(key=lambda w: (w['start'], w['end']))
    clean = []
    for word in words:
        if clean and clean[-1]['word'].casefold().strip('.,!?;:') == word['word'].casefold().strip('.,!?;:') and abs(clean[-1]['start']-word['start']) < 0.15:
            continue
        clean.append(word)
    return clean


def agrupar(words: list[dict], max_chars: int = 42, max_seconds: float = 2.5) -> list[dict]:
    groups, current = [], []

    def finish():
        if current:
            groups.append({'start': current[0]['start'], 'end': current[-1]['end'],
                           'text': ' '.join(w['word'] for w in current)})
            current.clear()

    for word in words:
        if current and (len(' '.join(w['word'] for w in current))+1+len(word['word']) > max_chars
                        or word['end']-current[0]['start'] > max_seconds
                        or word['start']-current[-1]['end'] > 0.6):
            finish()
        current.append(word)
        if word['word'].endswith(('.', '!', '?')):
            finish()
    finish()
    # Avoid overlapping SRT cues when the ASR estimates overlapping word spans.
    for i in range(len(groups)-1):
        groups[i]['end'] = min(groups[i]['end'], groups[i+1]['start'])
    return [g for g in groups if g['end'] > g['start']]


def srt_time(seconds: float) -> str:
    milliseconds = max(0, round(seconds*1000))
    h, remain = divmod(milliseconds, 3_600_000)
    m, remain = divmod(remain, 60_000)
    s, ms = divmod(remain, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'


def exportar(output: Path, words: list[dict], source: dict, model: str, language: str, signature: str) -> None:
    groups = agrupar(words)
    text = ' '.join(w['word'] for w in words)
    gravar_json(output / 'transcricao.json', {'source': source, 'model': model, 'language': language,
                'signature': signature, 'text': text, 'words': words, 'segments': groups,
                'timing': 'start/end em segundos relativos ao trecho; source_start/source_end relativos ao original.'})
    captions = [{'text': ' '+w['word'], 'startMs': round(w['start']*1000), 'endMs': round(w['end']*1000),
                 'timestampMs': round((w['start']+w['end'])*500), 'confidence': None} for w in words]
    gravar_json(output / 'legendas.remotion.json', captions)
    (output / 'transcricao.txt').write_text(text+'\n', encoding='utf-8')
    (output / 'legendas.srt').write_text('\n\n'.join(
        f'{i+1}\n{srt_time(g["start"])} --> {srt_time(g["end"])}\n{g["text"]}' for i, g in enumerate(groups))+'\n', encoding='utf-8')


def main() -> int:
    args = argumentos()
    # Com o ambiente proprio criado por configurar.py, roda nele (groq e keyring ja instalados).
    if not args.preparar_apenas and amb.deve_reexecutar():
        return amb.reexecutar_no_venv(str(Path(__file__).resolve()), sys.argv[1:])
    if not 10 <= args.bloco_segundos <= 600:
        raise ValueError('--bloco-segundos deve estar entre 10 e 600.')
    if not 0 <= args.sobreposicao <= 3:
        raise ValueError('--sobreposicao deve estar entre 0 e 3.')
    key = ''
    if not args.preparar_apenas:
        resultado = cred.obter_chave()
        if resultado.aviso:
            print(resultado.aviso, file=sys.stderr)
        if not resultado.chave:
            raise ValueError(cred.mensagem_sem_chave(resultado) + ' Nenhuma chamada foi feita.')
        key = resultado.chave
    model = args.modelo or os.getenv('GROQ_MODEL') or 'whisper-large-v3-turbo'
    language = args.idioma or os.getenv('GROQ_LANGUAGE') or 'pt'
    source = args.arquivo.expanduser().resolve()
    probe = inspecionar(source)
    if not any(s['codec_type'] == 'audio' for s in probe['streams']):
        raise ValueError('O arquivo nao tem faixa de audio.')
    duration = float(probe['format']['duration'])
    end = duration if args.fim is None else args.fim
    if not 0 <= args.inicio < end <= duration+0.001:
        raise ValueError(f'Intervalo invalido. O arquivo tem {duration:.3f} segundos.')
    end = min(end, duration)
    output = args.saida.expanduser().resolve() / nome_seguro(args.nome or source.stem)
    output.mkdir(parents=True, exist_ok=True)
    stat = source.stat()
    config = {'path': str(source), 'size': stat.st_size, 'mtime_ns': stat.st_mtime_ns,
              'start': args.inicio, 'end': end, 'block': args.bloco_segundos, 'overlap': args.sobreposicao,
              'model': model, 'language': language, 'prompt': args.contexto}
    signature = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
    final = output / 'transcricao.json'
    if final.exists() and not args.refazer and not args.preparar_apenas:
        previous = json.loads(final.read_text(encoding='utf-8'))
        if previous.get('signature') != signature:
            raise ValueError('Essa pasta ja tem outra transcricao. Use outro --nome ou --refazer.')
        print(f'Transcricao ja concluida: {output}. Use --refazer para substituir.')
        return 0
    work = output / 'cache' / signature[:16]
    chunks = planejar(args.inicio, end, args.bloco_segundos, args.sobreposicao)
    preparar(source, work, chunks)
    source_info = {'path': str(source), 'duration': duration, 'range_start': args.inicio,
                   'range_end': end, 'clip_duration': end-args.inicio}
    gravar_json(output / 'preparacao.json', {'source': source_info, 'model': model, 'language': language,
                                            'chunks': chunks, 'signature': signature})
    print(f'Audio preparado: {len(chunks)} bloco(s), {end-args.inicio:.2f}s.', flush=True)
    if args.preparar_apenas:
        print(f'Modo local: nenhuma chamada a API. Manifesto em {output / "preparacao.json"}')
        return 0
    try:
        from groq import Groq, APIConnectionError, APIStatusError, APITimeoutError
    except ImportError as error:
        raise RuntimeError('A biblioteca groq nao esta instalada neste Python. '
                           'Rode uma vez:  python <pasta-da-skill>/scripts/configurar.py setup') from error
    client = Groq(api_key=key, timeout=120.0, max_retries=3)
    try:
        results = transcrever(client, chunks, work / 'responses', model, language, args.contexto, args.refazer)
    except (APIConnectionError, APITimeoutError) as error:
        raise RuntimeError('Falha de conexao com a Groq. Os blocos concluidos foram preservados; execute novamente para retomar.') from error
    except APIStatusError as error:
        raise RuntimeError(f'Groq retornou HTTP {error.status_code}. Confira chave, cota e acesso ao modelo '
                           '(troque a chave com configurar.py update). Blocos concluidos preservados.') from error
    finally:
        client.close()
    words = reunir(results, args.inicio, end)
    if not words:
        raise RuntimeError('Nenhuma fala com tempos por palavra foi detectada. Respostas preservadas no cache.')
    exportar(output, words, source_info, model, language, signature)
    print(f'Concluido: {len(words)} palavras.\nArquivos: {output}')
    return 0


if __name__ == '__main__':
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, 'reconfigure'):
            _stream.reconfigure(errors='replace')
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print('\nInterrompido. Execute novamente para retomar pelos blocos em cache.', file=sys.stderr)
        raise SystemExit(130)
    except Exception as error:
        # Erros do SDK sao convertidos acima, entao cabecalhos de autorizacao nunca entram nos logs.
        print(f'Erro: {error}', file=sys.stderr)
        raise SystemExit(1)
