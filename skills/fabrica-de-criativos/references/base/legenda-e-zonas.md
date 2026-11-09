# Legenda, texto e zonas seguras

## Legenda

- **Legenda sempre** (muita gente assiste sem som), a menos que o formato peça o contrário (o arquivo do formato diz).
- **Palavra a palavra, ou 3 a 5 palavras por vez**, no máximo 2 linhas, com **realce da palavra-chave** (cor ou escala) nos trechos ★.
- **Contraste alto** sobre qualquer fundo: contorno, sombra ou pílula de fundo. Tamanho que se lê de relance (a partir de ~60 px de corpo num quadro de 1080 de largura).
- **Não cubra** a boca, os olhos nem a mão que gesticula. A legenda **nunca** vai para a base da tela.
- **Nunca coloque na legenda uma palavra que não foi dita.** Corrigir a **escrita** de uma palavra é permitido; inventar, não.
- Se você tem o `legendas.remotion.json` (lista `{text, startMs, endMs, timestampMs, confidence}` por palavra), a skill do Remotion (componentes de legenda) o lê direto. **O estilo da legenda é da pessoa**: esta skill não traz um estilo pronto.
- Fonte livre (Google Fonts ou licença aberta), carregada no projeto e **aguardada antes de renderizar**. Cores e fontes da identidade da pessoa, do começo ao fim e em todas as variações de um mesmo teste.

### Direção observada nos exemplos (não é um molde)

- O **grupo de palavras aparece de uma vez**, **parado no mesmo lugar** (centralizado, sem subir nem mudar de posição), no máximo **2 linhas**.
- **Só a palavra falada no momento** ganha destaque (uma pílula de cor atrás dela, acompanhando a fala); as outras ficam neutras, com sombra suave.
- Posição: **abaixo do meio da tela** (nos exemplos, centro em torno de y 1320 de 1920), **acima da zona de interface da base**, longe das bordas (~840 px de largura).
- Com o rosto em **tela cheia**, a legenda **desce para o queixo** para não cobrir a boca; com a pessoa embaixo ou pequena, ela fica sobre o conteúdo mais livre.
- Uma legenda simples e **constante** vale mais que uma legenda cheia de efeito. Formatos como a notícia e o telejornal podem dispensá-la ou mudá-la.

## Texto de ênfase (fora da legenda)

- Curto: manchete de até ~6 palavras, em até 3 linhas.
- **Tempo em tela:** 0,4 s + 0,3 s por palavra, mínimo 1 s. Texto que sai antes de ser lido é pior que nenhum.
- Um texto novo não entra enquanto o anterior ainda está sendo lido, a menos que o antigo já esteja saindo.
- O texto **complementa** a fala (promessa ou curiosidade), não a repete.
- Entra no **início da palavra que ilustra** (±0,1 s).

## Zonas seguras (referência para 1080x1920)

As interfaces de Reels, Stories, TikTok e Shorts cobrem partes da tela com nome, descrição, botão de ação e ícones. **Os valores variam entre as fontes e entre as versões dos apps.** Ponto de partida **conservador**:

| Borda | Deixe livre |
|---|---|
| **Topo** | ~270 px |
| **Base** | ~670 px (alguns guias usam menos, de ~320 a ~670 px) |
| **Laterais** | ~90 px, e ~120 px na direita (coluna de botões) |

Texto importante, logo, legenda, CTA e o **rosto** ficam dentro desse miolo. **Confirme na especificação atual da plataforma ou num print da interface**, e ajuste. Para o feed 4:5, mantenha o essencial no centro e longe das bordas.

Cada formato diz onde **as áreas de vídeo** ficam em relação a essas margens: o fundo de um vídeo pode ir até a borda; o texto e o rosto, não.

## Inserts

| Insert | Quando entra |
|---|---|
| Imagem ou foto | a fala cita algo concreto |
| Logo | cita uma marca ou ferramenta (fonte oficial, SVG ou PNG transparente, confira visualmente) |
| Gráfico ou número grande | traz um dado real |
| Gravação ou print de tela | fala de um resultado, interface ou passo |
| Ícone | descreve uma ação ou conceito |
| Depoimento ou prova | cita uma pessoa real e o que ela obteve |

Dura **1 a 2,5 s**, entra na palavra que ilustra, não cobre boca e olhos por mais de ~2 s. Material **real do usuário** vence imagem genérica. Prova (print, resultado) fica o tempo de ser lida (0,4 s + 0,3 s por palavra, mínimo 1,5 s).

## Logos de terceiros

Só como **identificação editorial**, de fonte oficial, sem distorcer nem trocar cores. Se não achar, use o nome em texto limpo em vez de improvisar um logo parecido. Marca de terceiros em anúncio pode ter regras de uso: confirme que o uso é permitido.
