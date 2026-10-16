# Arquivos gerados

Para `--saida PASTA --nome NOME`, tudo fica em `PASTA/NOME/`.

| Arquivo | Conteúdo |
|---|---|
| `transcricao.txt` | Texto corrido. |
| `legendas.srt` | Legendas agrupadas (até 42 caracteres e 2,5 s por linha, quebra em pausas > 0,6 s e no fim de frase). |
| `transcricao.json` | `text`, `words` (cada uma com `word`, `start`, `end`, `source_start`, `source_end`), `segments`, modelo, idioma e assinatura. |
| `legendas.remotion.json` | Lista de `{text, startMs, endMs, timestampMs, confidence}` por palavra, pronta para o formato `Caption[]` do Remotion. |
| `preparacao.json` | Manifesto dos blocos de áudio (também criado com `--preparar-apenas`, que não usa a API). |
| `cache/` | Áudio dos blocos e respostas da Groq, para retomar sem pagar de novo. Pode ser apagada depois. |

## Tempos

- `start`/`end`: segundos **relativos ao início do trecho** transcrito (se usou `--inicio 88`, o 0 é o segundo 88 do original).
- `source_start`/`source_end`: segundos no arquivo original.
- Em `legendas.remotion.json` os tempos são em milissegundos, relativos ao trecho.

## Comportamento de segurança dos dados

- A mídia original nunca é modificada.
- Só áudio mono 16 kHz em blocos é enviado à Groq. O vídeo não é enviado.
- Se a pasta `PASTA/NOME` já tem outra transcrição, o comando recusa; use outro `--nome` ou `--refazer`.
