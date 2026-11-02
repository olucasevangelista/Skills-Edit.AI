# 02. Fundo Verde (Recorte)

**Também pedido como:** fundo verde, green screen, pessoa recortada, apresentador na frente do conteúdo.

## Assinatura visual

A **pessoa recortada em primeiro plano**, sobre uma **sequência de fundos** (páginas, prints, vídeos, composições) que **mudam com o assunto**. A pessoa pode ser **redimensionada e reposicionada** ao longo do vídeo, com uma **sombra** que a integra ao fundo. É a sensação de "apresentador na frente da matéria".

## Ideal quando

- A pessoa fala sobre algo que pode ser **mostrado atrás dela**: uma página, um dado, um produto, uma tela, um lugar.
- O conteúdo de fundo **é a prova** (uma publicação pública, uma tela, uma imagem) e a pessoa o comenta.
- Há um bom recorte possível (veja abaixo).

## Evite quando

- **Não há como recortar bem** a pessoa (cabelo fino, fundo bagunçado, roupa da cor do fundo, movimentos de mão muito rápidos): **a borda ruim denuncia** o formato e queima o anúncio.
- A fala é emocional e pede o rosto sem artifício.
- O fundo seria **conteúdo de terceiros** sem direito de uso.

## Composição (1080x1920)

| Elemento | Posição e tamanho |
|---|---|
| **Fundo** | tela cheia (imagem, vídeo, página), com desfoque leve ou escurecimento de ~15% quando o texto da pessoa precisa de contraste |
| **Pessoa** | recortada, **55% a 75% da altura**, ancorada em baixo ao centro, à esquerda ou à direita; **cabeça inteira**, centro da cabeça em y ≈ 650 a 950, dentro da zona segura |
| **Sombra** | uma elipse suave no "chão" e uma sombra projetada difusa (`0 20px 40px` a ~35% de preto) para integrar |
| **Legenda** | y ≈ 1100 a 1220, sobre o corpo da pessoa ou ao lado dela, nunca na base |
| **Texto de apoio** | na área do fundo que sobra, dentro das margens |

## Elementos e animações

- **Mudança de fundo na palavra** que cita o assunto: fade curto ou deslize de 0,2 a 0,3 s.
- **A pessoa muda de lado e de tamanho** em eventos (de centro para a esquerda enquanto o fundo ganha destaque; ampliar nos ★).
- **Destaque no fundo** (círculo, seta, zoom na região citada).

## Como recortar a pessoa

Teste **num trecho curto** antes de fazer o vídeo inteiro, e olhe a borda **ampliada**, sobre fundo claro **e** escuro. Caminhos, na ordem:

1. **A pessoa foi gravada em fundo uniforme** (verde, azul ou uma cor lisa): `chromakey` do FFmpeg, com `despill`, exportando **WebM VP9 com transparência** (leve; o `<Video>` do Remotion lê direto).
   `ffmpeg -i entrada.mp4 -vf "chromakey=0x00FF00:0.15:0.05,despill=type=green,format=yuva420p" -c:v libvpx-vp9 -auto-alt-ref 0 -b:v 3M -c:a libopus pessoa.webm`
   (para outra cor lisa: `colorkey=0xRRGGBB:0.2:0.1`; ajuste a semelhança e a suavização olhando a borda.) Num fundo verde sintético, esse comando tirou o fundo e manteve a pele e a roupa; uma faixa verde clara colada na roupa só ficou atenuada. **Não use ProRes** (`.mov`): o `<Video>` do `@remotion/media` não o decodifica sem registro extra; se precisar de ProRes, use `<OffthreadVideo transparent>`.
2. **Fundo qualquer:** `scripts/recortar_pessoa.py` (`python recortar_pessoa.py entrada.mp4 pessoa.webm --de 20 --ate 28`). Usa um modelo de segmentação de pessoa (`rembg`, instalado uma vez com `pip install rembg onnxruntime pillow`; o modelo de ~176 MB baixa na primeira execução) e salva o mesmo WebM com transparência e o áudio original. Em CPU leva cerca de 0,8 s por quadro (8 s de vídeo levam alguns minutos): **recorte só o trecho que vai usar**. Num trecho real de 3 s (câmera parada, fundo de ambiente), a máscara ficou estável entre os quadros e o corpo saiu limpo; a **cadeira atrás saiu com contorno difuso e há um halo suave na borda** sobre fundo claro. Isso não é fundo verde de estúdio: confira sempre a borda ampliada.
3. Se a ferramenta de recorte do **HyperFrames** (`remove-background`) estiver disponível, ela também produz um vídeo transparente (não foi testada aqui).

Seja honesto sobre o resultado: se a borda ficou ruim em algum trecho, **diga** e ofereça outro formato (por exemplo, Tela Dividida), em vez de entregar um recorte com cara de erro.

## Cortes e ritmo

- Emenda com **sobreposição** na pessoa (`cortes.md`); o fundo troca em **evento visual** a cada ~1,5 a 2,5 s.
- Mantenha o fundo **estável** quando a pessoa diz a frase mais importante.

## Texto e legenda

- Legenda palavra a palavra, com realce nos ★, sobre o corpo da pessoa (contraste alto, contorno).
- Título curto no topo do fundo, y ≥ 270.

## Som

- Voz em primeiro plano; efeito curto na troca de fundo (opcional); música opcional bem abaixo.

## Materiais

- **Peça:** o vídeo da pessoa (de preferência em fundo uniforme, com boa luz e a pessoa longe do fundo) e os materiais para compor o fundo.
- **Pode buscar sozinho:** imagens e vídeos de apoio com licença clara, prints de páginas **públicas** citadas, texturas, música.
- **Nunca invente:** uma publicação, notícia ou página de pessoa real, nem um print de resultado.

## Variações dentro do formato

- Onde a pessoa fica (esquerda, centro, direita) e o tamanho dela.
- Desfoque e escurecimento do fundo; com e sem sombra.
- Estilo da troca de fundo.

## Armadilhas e checklist

- [ ] A **borda** do recorte está limpa em todos os trechos (conferida ampliada).
- [ ] Não há "halo" verde ou cintilação no cabelo.
- [ ] A sombra integra a pessoa ao fundo.
- [ ] O fundo não é conteúdo de terceiros sem direito.
- [ ] A pessoa e a legenda ficam dentro da zona segura.

## Kit

Sem kit nesta versão. Monte com os componentes de `kit/componentes` (`Legenda`, `Titulo`, `Movimento`); o vídeo recortado entra como `<Video>` com transparência sobre o fundo.

## Apoio

Se a skill `copystyle` estiver disponível, use-a para medir uma referência do formato (tamanho e posição da pessoa, ritmo das trocas); se a `creative-lab` estiver disponível, use as regras de gancho dela.
