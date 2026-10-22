# Revisão

Não confie na prévia: confira o que foi renderizado. Estes comandos foram usados e funcionam; troque os nomes pelos do projeto.

## 1. Quadros de diagnóstico

Um quadro por instante-chave: o gancho, cada mudança de estado, a convergência e o último quadro.

```
npx remotion still src/index.ts <IdDaComposicao> out/f120.png --frame=120
```

(Em 3D, acrescente `--gl=angle`.) Monte uma folha de contato para ver a sequência de uma vez:

```
ffmpeg -i out/f20.png -i out/f120.png -i out/f200.png -filter_complex "[0:v]scale=360:-1[a];[1:v]scale=360:-1[b];[2:v]scale=360:-1[c];[a][b][c]hstack=inputs=3" folha.png
```

Olhe a folha e confira: o objeto herói aparece e é reconhecível, a ação corresponde à frase, o texto cabe e se lê, não há quadro vazio nem objeto no lugar errado. Inclua quadros **entre** os instantes-chave: é ali que a câmera e os cruzamentos mostram erros.

## 2. Medidas por pixel

Com Python e a biblioteca Pillow (ou outra de imagem), confira por número o que o olho aceita sem medir:

- **Zona segura:** nenhum pixel claro de texto no topo (0 a 270 px), na base (a partir de 1560 px) ou nas laterais (menos de 90 px e mais de 990 px). Um objeto que **sai de cena** pode cruzar a margem; texto e objeto principal parados, não.
- **Posição do objeto:** o centro do objeto principal está onde o documento de direção diz.
- **Determinismo:** renderize o mesmo quadro duas vezes e compare o hash (`md5sum`). Se for diferente, algo depende de tempo real ou de `Math.random`, e a prévia não bate com o arquivo.

## 3. Arquivo exportado

```
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,nb_frames -of default=nw=1 peca.mp4
```

Confira o número de quadros (duração x taxa), as dimensões e o codec. Se há áudio, meça o volume (`ffmpeg -i peca.mp4 -af ebur128=peak=true -f null -`) e veja `audio.md`. Compare um quadro do arquivo com o mesmo quadro da prévia: devem ser iguais, e cor e texto não podem ter mudado.

Não esconda o código de saída de um render falho com `| tail`: confira o código ao final.

## 4. Checklist

- [ ] O gancho aparece no primeiro segundo e se entende sem som.
- [ ] Um objeto herói e uma ideia por cena; o resto serve a ele.
- [ ] Cada objeto assenta e fica estável tempo suficiente para ser percebido.
- [ ] Texto curto, grande e dentro da zona segura em todos os quadros conferidos.
- [ ] Nada muda de forma ou de lugar para esconder um erro; a continuidade entre objetos não mostra salto.
- [ ] O movimento termina em repouso; a peça termina em um quadro estável, sem fade para preto.
- [ ] Os eventos sonoros caem nos instantes do mapa de som; a trilha termina em fade junto com a imagem.
- [ ] O arquivo exportado tem a duração, as dimensões e o volume esperados.

## 5. O que declarar na entrega

Diga à pessoa o que foi verificado (quadros, medidas, arquivo) e **o que não foi**. Em geral, o que o agente não consegue fazer:

- Assistir a peça em reprodução contínua e ouvir o áudio. Peça à pessoa que faça isso no player, e **não afirme** uma revisão perceptiva que não houve.
- Avaliar o gosto da trilha ou do ritmo.
- Qualquer simplificação técnica que mude a representação (por exemplo, 3D substituído por 2D com perspectiva).
