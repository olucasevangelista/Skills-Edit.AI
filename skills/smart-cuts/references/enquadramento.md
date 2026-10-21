# Enquadramento (direção para o Remotion)

A Smart Cuts entrega cortes **no formato do vídeo original** (por exemplo 16:9). Passar para o vertical (1080x1920) e posicionar rosto, tela e webcam é feito no Remotion. O Remotion não detecta rosto nem reenquadra sozinho: ele só oferece ferramentas manuais, como `objectFit` e `objectPosition` no vídeo, as props `cropLeft`, `cropRight`, `cropTop` e `cropBottom` (no `<Video>` de `@remotion/media`, entre outros) e transformações de escala e deslocamento. Quem decide o enquadramento é você: olha um quadro, mede onde está o rosto e grava no plano. A skill do Remotion explica como aplicar.

## Como medir (um quadro por corte, no mínimo)

1. Tire um quadro em resolução cheia, no meio de um trecho com a pessoa falando:
   `ffmpeg -ss 12.5 -i trabalho/c1.mp4 -frames:v 1 trabalho/quadros/c1_a.png`
2. Olhe a imagem e anote o rosto em **pixels do vídeo do corte** (largura e altura constam no `plano.json`): `cx` e `cy` (centro da cabeça) e `h` (altura da cabeça, do alto do cabelo ao queixo).
3. Corte com trechos de lugares diferentes, câmera que muda de lugar ou mais de uma pessoa: um quadro por trecho (ou por pessoa) e um rosto para cada.
4. Grave no `cortes.json` de cada corte, no campo `rosto` (ou `rostos` por trecho), e em `layout` quando o formato muda (`plano.md`). O `montar.py` repassa esses campos ao `plano.json`.

## Regras

- **Cabeça inteira, sempre.** O 9:16 corta nas laterais: confira que a cabeça cabe na largura e que sobra espaço acima.
- **Zonas do 9:16:** a interface do app cobre o topo (~0 a 8% da altura), a base (~80 a 100%) e a coluna direita (~88 a 100% da largura, de 45 a 85% da altura). Rosto e texto ficam em x 6-86% e y 10-80%.
- **Câmera falando (talking head):** o vídeo cobre o 9:16 (vídeo em pé: pela largura; vídeo deitado: pela altura) centralizado no rosto. Nos jump cuts alternar a escala entre 1,00 e ~1,07 dá dinâmica sem cansar.
- **Aula ou live com tela e webcam:** a tela compartilhada fica na faixa de cima (largura inteira, proporção 16:9) e a webcam embaixo, com a cabeça inteira. Webcam pequena ou baixa ocupa a área de baixo toda, para a legenda não cair nos olhos. Quando a explicação é só a tela, use a tela inteira com fundo desfocado; quando é só a pessoa, o rosto em tela cheia. Anote no plano qual layout vale em cada trecho (`layout`).
- **Podcast ou conversa:** enquadre quem fala e troque quando a fala troca. Descubra quem fala pelo texto e pelos quadros; anote o rosto de cada pessoa.
- **Banner ou marca queimada sobre a câmera:** enquadre só a região limpa (`rect` com x, y, largura e altura da câmera sem o banner).
- **Nada em cima do rosto, da boca e dos olhos:** número, emoji, legenda. Legenda também não cobre a mão que gesticula.
- **Rosto de perfil, luz ruim ou webcam minúscula:** não force; use o quadro, meça à mão e aceite um zoom menor.

## O que gravar no plano

```json
"rosto": {"cx": 960, "cy": 420, "h": 300},
"layout": [{"de": 0, "ate": 18.4, "modo": "pessoa"}, {"de": 18.4, "ate": 41.0, "modo": "tela+webcam", "tela": [14, 50, 990, 616], "cam": [1008, 56, 264, 608]}]
```

Tempos do `layout` em segundos **do corte final**. Coordenadas em pixels do vídeo do corte.
