# 16. Caixinha de Pergunta

**Também pedido como:** caixinha de perguntas, pergunta de story, "faça uma pergunta", gancho em pergunta.

## Assinatura visual

Um **cartão no estilo da caixinha de perguntas de um story** (um cabeçalho escuro com "Faça uma pergunta" e um corpo claro com a pergunta escrita) **por cima do vídeo da pessoa**. A pergunta é **digitada palavra a palavra no instante em que é falada**, e a pessoa responde. A caixinha precisa estar **no começo** do vídeo. Depois disso o vídeo é livre: pode **seguir inteiro no formato** (a pessoa em tela cheia, com a caixinha em cima, cortes e legenda: um vídeo **orgânico, com pouca cara de anúncio**) ou virar outro formato ou mistura.

## Ideal quando

- O gancho é uma **dúvida ou objeção comum** do público ("é verdade que...?", "dá pra...?") e a pessoa responde em seguida.
- Quer-se um vídeo **orgânico**, com cara de conteúdo e não de anúncio. Com a caixinha, o vídeo costuma ser mais orgânico, e **pode ser só isso**: o vídeo inteiro com a caixinha em cima, cortes e legenda.
- O vídeo pode seguir em **qualquer outro formato** depois da resposta (tela cheia, blocos de motion, tela dividida, miniatura com cartões).

## Evite quando

- A pergunta seria apresentada como **de uma pessoa real** ("um seguidor perguntou") sem ser verdade: a pergunta é do roteiro; se for encenada, não diga que alguém perguntou.
- Não há uma pergunta clara: o cartão fica vazio.
- A resposta é longa e precisa de muita informação visual logo no começo.

## Composição (pontos de partida, 1080x1920)

| Elemento | Como pensar |
|---|---|
| **Vídeo da pessoa** | tela cheia por baixo da caixinha |
| **Véu** | um escurecido leve (~25 a 30%) no vídeo enquanto a caixinha está na tela, para o cartão ler |
| **Cartão** | **sempre no alto** (a primeira coisa que a pessoa vê ao escanear o vídeo), centralizado na horizontal, **largura ~780 px (x de ~150 a ~930)**; cabeçalho escuro (~110 px) com "Faça uma pergunta" e corpo claro (altura mínima ~210 px) com a pergunta em ~46 px; cantos bem arredondados (~38 px) e sombra. **O texto fica centralizado dentro do cartão** |
| **Altura do cartão** | direção, não regra: **mais para cima do que parece necessário**, porque o cartão **cresce para baixo** enquanto o texto aparece. Pense no cartão com o texto completo: o ideal é a borda de baixo terminar **antes das sobrancelhas**; **cobrir até ~70% da testa é tranquilo**, e cobrir mais só se não houver espaço. Sem colar na margem de cima, para não ser cortado. Se a pessoa gravou já deixando espaço no alto, use-o |
| **Legenda** | enquanto o rosto está em tela cheia, desça-a para o queixo; a pergunta já está escrita no cartão, então a legenda pode esperar a resposta |

## Elementos e animações

- **Entrada do cartão** (~0,3 a 0,8 s): pop com leve overshoot, escala de ~0,7 a 1, uma pequena rotação (~-3°) que se endireita.
- **Texto digitado:** cada palavra aparece **no instante em que é falada** (use o tempo por palavra da transcrição), com um cursor piscando.
- **Saída** (~0,4 s depois que a pergunta termina): o cartão sobe e some, e o véu clareia.
- Depois da pergunta, a **resposta** pode abrir com selos pequenos sobre o rosto (REC, uma palavra de destaque), seguir em tela cheia ou mudar de modo: **não precisa mudar**.

## Cortes e ritmo

- A caixinha fica na tela por **~4 a 6 s** (o tempo da pergunta), no começo; pode também **ficar o vídeo todo** como uma moldura em cima, se o vídeo for orgânico.
- Emenda com **sobreposição** entre a pergunta e a resposta (`cortes.md`).
- O gancho já é um evento: o primeiro elemento novo depois da caixinha deve chegar em ~1,5 s.

## Texto e legenda

- A pergunta é **curta** (até ~12 palavras) e **diz o que o anúncio sustenta**.
- Ortografia correta; a pergunta escrita é exatamente a que é falada.

## Som

- Voz em primeiro plano; um "pop" discreto na entrada do cartão é opcional. Sem música alta.

## Materiais

- **Peça:** o vídeo da pessoa e a **pergunta** (ou a objeção a que ela responde).
- **Pode buscar sozinho:** som de entrada, fonte.
- **Nunca invente:** que um seguidor, cliente ou pessoa real fez a pergunta.

## Variações dentro do formato

- A caixinha só no começo, ou que volte num ponto de virada com uma segunda pergunta.
- Cartão claro ou escuro; posição (topo, meio); digitado ou inteiro de uma vez.
- O que vem depois da resposta: tela cheia, miniatura com cartões, blocos de motion, tela dividida.

## Armadilhas e checklist

- [ ] A caixinha está **no começo** do vídeo.
- [ ] A pergunta é do roteiro e **não é atribuída** a uma pessoa real.
- [ ] O texto digitado acompanha a fala, palavra a palavra.
- [ ] O cartão está **no alto**, centralizado, com o texto centralizado; dentro das margens (x de 90 a 960); a borda de baixo (com o texto completo) fica antes das sobrancelhas, ou cobre no máximo o que for preciso da testa; não cobre os olhos.
- [ ] O resto do vídeo foi pensado: a caixinha é só o gancho.

## Estruturas e exemplos

**Código para reaproveitar:** `assets/componentes/CaixaPergunta.tsx` é a caixinha pronta como componente do Remotion (cabeçalho "Faça uma pergunta", corpo claro, entrada com leve rotação, saída, véu atrás). **Copie para o seu projeto e ajuste**; ele é uma peça, não um editor: a composição, os cortes e a legenda continuam sendo seus. O formato da caixinha é padrão e quase não muda, por isso vale reaproveitar. Dois modos de texto: **`digitado`** (as palavras aparecem no instante em que são faladas: passe `palavras` com o tempo de cada uma, da transcrição) e **`fixo`** (o texto já inteiro, o formato mais comum do Instagram). Testado: compila no TypeScript e renderiza nos dois modos.

Quadro de demonstração: `references/exemplos/mistura-13-caixinha-de-pergunta.jpg`. Nele, a caixinha ocupa os primeiros ~5 s sobre a pessoa em tela cheia, e o resto do criativo mistura tela cheia com selos, miniatura da pessoa com cartões, blocos de cor em tela cheia, passos, grade de variações, preço e CTA. É um exemplo de **gancho de um formato e corpo livre**.

## Apoio

Se a skill `creative-lab` estiver disponível, use as regras de gancho dela; se a `transcrever-groq` estiver disponível, use-a para o tempo por palavra que sincroniza a pergunta com a fala.
