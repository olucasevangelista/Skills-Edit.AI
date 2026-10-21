# Problemas comuns e o que fazer

| Sintoma | O que fazer |
|---|---|
| Aviso `ENTROU "x"` ou `SAIU "x"` no planejamento | A palavra está colada na fala que fica (sem pausa) ou o tempo da transcrição está deslocado. Veja `ler.py ... --silencio` em volta dela; mude o trecho para incluir ou excluir de propósito, ou marque a emenda à mão em `emendas` |
| Palavra cortada ou "palavra fantasma" na emenda | `verificar.py` acusa. Ouça a emenda, ajuste o trecho ou `bordas`/`emendas` no silêncio real mais próximo e monte só esse corte (`--so`) |
| `verificar.py` acusa palavra faltando que está no vídeo | O Whisper às vezes engole muletas ("né", "tá bom", "o que que"). Ouça o trecho: se está no áudio, é falso alarme. Palavra de conteúdo faltando é real |
| Transcrição inventou texto (mesma palavra repetida, "1. 1. 1.", texto que ninguém falou, geralmente em música ou silêncio longo) | Ouça o trecho e transcreva só ele de novo, isolado |
| Transcrição omitiu uma frase repetida | O Whisper engole repetição. Transcreva o trecho isolado antes de decidir o corte |
| Grafia errada de marca, sigla ou gíria | Confira no checkpoint. Para o corte, só importa no texto esperado de `verificar.py`; para a legenda, corrija a escrita no Remotion |
| `Nao encontrei fala ... (volume abaixo do limiar)` | Áudio baixo: `--limiar -50`. Ruído de fundo alto: `--limiar -42` |
| Pausas ainda grandes no corte | Ruído de fundo subiu o piso: `--limiar -42` ou limpe o áudio antes |
| Corte comendo o começo de uma palavra | Fala muito suave: `--limiar -50` |
| Corte tem estalo na emenda | Aviso do `verificar.py`; monte de novo e, se persistir, mexa em `emendas` para uma pausa mais limpa |
| Volume fora do alvo | `montar.py` normaliza; rode de novo (`--lufs`) |
| Cores lavadas | Vídeo HDR. Se possível, grave de novo em SDR |
| `ffmpeg nao encontrado` | Windows: `winget install Gyan.FFmpeg`; macOS: `brew install ffmpeg`; depois feche e abra o terminal |
| Linha de comando longa demais no Windows | Corte com muitos trechos usa arquivo de filtro, então não deve ocorrer; se ocorrer, mantenha o projeto em um caminho curto |
| Vídeos de tamanhos diferentes no mesmo corte | O corte usa o tamanho do primeiro; os outros entram inteiros, com barras |
| Fonte com rotação de celular (vídeo em pé gravado deitado) | O FFmpeg gira sozinho; confira o `largura` e `altura` do `plano.json` |
| Fonte com taxa de quadros variável (gravação de tela, celular) | O corte sai em taxa fixa (a do original, no máximo 30). Se perceber dessincronia, force `--fps 30` |
