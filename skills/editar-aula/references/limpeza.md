# Limpeza: o que remover e como

## O que remover (decidindo pela transcrição)

- **Reinício de frase:** a pessoa começa, erra e repete. Mantenha a **última versão completa** e remova o começo errado. Confirme que a última versão não foi cortada no fim.
- **Takes repetidos:** a mesma passagem gravada duas ou três vezes. Fique com a melhor, em geral a última; na dúvida, pergunte.
- **Comentários fora da aula:** "peraí", "deixa eu refazer", conversa com outra pessoa, barulho que interrompe.
- **Pausas longas** e silêncios: o script cuida sozinho.
- **Muletas ("é...", "hã", "né"):** só saem as que ficam **isoladas entre pausas** (vão embora junto com a pausa). As que ficam no meio da frase só podem ser removidas se aparecerem na transcrição, e o Whisper costuma omiti-las. **Não prometa tirar todas.**

Não remova hesitação natural curta, respiração entre ideias nem pausas de ênfase: o estilo `aula` já mantém ~0,3 s de pausa. Aula cortada demais cansa.

## Como indicar o que remover

`--remover "62-71.5,2:00-2:11"` com tempos do **vídeo bruto** (segundos ou mm:ss). Os tempos da transcrição escorregam 0,2 a 0,5 s em arquivos longos; por isso o script **alinha cada pedido aos limites reais da fala**: começa no fim da fala mais próxima do início e termina no começo da fala mais próxima do fim. O `plano_cortes.md` mostra "pedido" e "alinhado": confira.

Se o erro está no **meio de uma fala contínua**, sem pausa nas bordas, o script avisa que não conseguiu alinhar. Ajuste os tempos olhando o volume, ou use `--sem-alinhar` (corta exatamente onde você disse).

Se a transcrição desconfiar de falta (poucas palavras para o tempo), transcreva o trecho isolado antes de decidir: o Whisper às vezes **engole uma frase repetida** e o plano ficaria errado.

## Estilos de corte

| Estilo | Pausa a partir de | Fica com | Para quê |
|---|---|---|---|
| `aula` (padrão) | 0,55 s | 0,30 s | fala natural, didática |
| `curto` | 0,22 s | 0,08 s | ritmo rápido, vídeos curtos |
| `suave` | 0,90 s | 0,55 s | entrevista, tom mais calmo |

Ajustes finos: `--pausa-minima`, `--pausa-final`, `--sobreposicao-emenda`, `--emenda-gap`, `--limiar` (silêncio, em dB).

## Emenda por sobreposição

Todo corte segue o mesmo desenho: o trecho novo entra **colado no começo da fala** (sem respiro nem silêncio antes) e **começa ainda durante o finalzinho do anterior**, com a imagem trocando junto com o áudio novo. A frase anterior termina inteira e a próxima já está falando.

- **Em remoção de erro** (emenda), as vozes se sobrepõem de propósito por ~0,1 s e o clipe novo entra 0,22 s antes do fim do anterior.
- **Em pausa encurtada,** a sobreposição acontece sobre o silêncio (0,12 s): é só uma emenda sem estalo.
- No áudio, o trecho anterior desce suavemente durante a sobreposição e o novo entra com um fade de 30 ms, só para evitar estalo.
- Os instantes vêm do **volume do áudio**, não da transcrição.

## Qualidade

`montar.py` grava em H.264 com qualidade alta (padrão `boa`; `--qualidade maxima` é um pouco melhor e mais lento) e a taxa de quadros vai para no máximo 30 (`--fps`). Imagens com mais de 1920 px no lado maior são reduzidas (`--max-lado` para manter). O áudio é normalizado para -16 LUFS.

## Problemas comuns

| Sintoma | O que fazer |
|---|---|
| Cores lavadas | Vídeo HDR; o diagnóstico avisa. Se possível, regrave em SDR |
| Pausas ainda grandes | Ruído de fundo alto subiu o piso: use `--limiar -42` ou limpe o áudio antes |
| Corte comendo o começo de uma palavra | Fala muito suave: use `--limiar -50` |
| "Nao encontrei fala" | Volume baixo demais: `--limiar -55` |
| Volume final fora de -16 LUFS | `verificar.py` mostra; rode `montar.py` de novo (ele normaliza) |
| FFmpeg não encontrado | Instale: Windows `winget install Gyan.FFmpeg`, macOS `brew install ffmpeg`, e reabra o terminal |

## Verificação

`verificar.py` **mede** o resultado: duração contra o plano, sincronia entre vídeo e áudio, volume (alvo -16 LUFS), pausas que sobraram e estalos nas emendas. Depois disso, o melhor teste de conteúdo é **transcrever o vídeo já limpo**: se uma frase importante sumiu ou apareceu duplicada, a transcrição mostra, e os tempos finais exatos já servem para posicionar os motions.
