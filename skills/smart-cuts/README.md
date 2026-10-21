# smart-cuts

Direção e scripts para transformar vídeos longos (live, aula, podcast, vídeo do YouTube, call) em cortes para Reels, TikTok e Shorts: escolher os melhores momentos pela transcrição, tirar loops, devaneios e pausas, e emendar cada corte com o take seguinte entrando colado na voz, com imagem e áudio sobrepostos antes de a fala anterior acabar, sem cortar nenhuma palavra.

A Smart Cuts entrega um mp4 limpo por corte (no formato do vídeo original) e um `plano.json` com o texto, os tempos, os ganchos e o enquadramento de cada um. Legenda, gancho, inserts, música, formato vertical e exportação final são feitos com a skill do Remotion, a partir desse plano. A transcrição vem da skill `transcrever-groq`.

## O que precisa

**Python 3.10+** (só biblioteca padrão) e **FFmpeg** com `ffprobe` (`winget install Gyan.FFmpeg` no Windows, `brew install ffmpeg` no macOS). Nada mais é instalado: não há motor, modelo nem ambiente próprio.

## Scripts

| Script | Para quê |
|---|---|
| `ler.py` | texto corrido com tempo, palavras com tempo e os silêncios reais do áudio, para escolher trechos e emendas |
| `planejar_cortes.py` | transforma os trechos escolhidos em segmentos do vídeo bruto com emendas em silêncio real; mostra o texto final e avisos |
| `montar.py` | gera um mp4 por corte, com emenda por sobreposição de imagem e áudio, e o `plano.json` |
| `verificar.py` | mede duração, sincronia, volume, pausas e estalos, e compara a fala do corte final com a esperada |

## Estado dos testes

| Item | Situação |
|---|---|
| Testes automáticos (16) | Passando no Windows 11. Usam mídia sintética (cada take com um tom e uma cor) |
| Sobreposição de imagem e áudio | Medida no teste sintético: o quadro do take novo e o áudio dele entram com ~0,03 s de diferença e ~0,09 s antes de o áudio anterior acabar. Um controle sem sobreposição reprova no mesmo teste |
| Vídeo real (9 min, 1080p60, câmera e tela) | 2 cortes montados em ~25 s: duração igual ao plano, -15,9 LUFS, 0 estalos em 8 emendas; a imagem trocou em cada emenda no instante previsto. A conferência de fala contra a transcrição do corte final **não foi feita nesse teste real** (exige a transcrição de cada corte pela API) |
| **macOS** | **Não testado** |
| Vídeos de várias horas | Não testados |
| Mais de um vídeo no mesmo corte, aula com tela e webcam | Cobertos só pelo código e pelos testes unitários, sem vídeo real |

Rodar os testes: `python -m unittest discover -s tests` (precisa de FFmpeg).

## Limites que vale conhecer

- Os tempos de palavra da transcrição têm erro (o Whisper costuma pôr o início de uma palavra no fim da anterior, e erra mais em arquivos longos). Por isso as emendas usam o volume do áudio, e a conferência final transcreve o corte pronto. Fala contínua, sem pausa de 60 ms entre duas palavras, não permite emenda limpa ali: o planejador avisa (`ENTROU`/`SAIU`).
- Palavra pronunciada muito baixo pode ficar abaixo do limiar de silêncio. Ajuste com `--limiar`.
