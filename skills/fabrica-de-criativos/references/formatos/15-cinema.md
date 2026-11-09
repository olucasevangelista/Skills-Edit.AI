# 15. Cinema

**Também pedido como:** cinematográfico, cinematic, vídeo emocional com janela.

## Assinatura visual

Canvas **vertical preto**, o vídeo numa **janela horizontal (ou quase quadrada) com cantos arredondados**, centralizada, com **margens amplas** acima e abaixo e uma **frase de impacto no topo**, em branco, em tipografia editorial. Cortes calmos, música emocional e tratamento de cor: a atmosfera é de curta-metragem, não de feed.

## Ideal quando

- Vídeo **emocional, inspirador, reflexivo ou dramático**: história de transformação, bastidor, manifesto, depoimento do fundador.
- A mensagem precisa de **peso e respiro**, não de pressa.
- Marca que quer parecer **premium** e editorial.

## Evite quando

- O anúncio é de **resposta direta e agressiva** (oferta, urgência) e precisa de ritmo apertado.
- O vídeo-base é pobre (som ruim, enquadramento ruim): a janela e o fundo preto expõem isso.
- Há **muita informação** para ler: o formato é de poucas palavras.

## Composição (1080x1920)

| Elemento | Posição e tamanho |
|---|---|
| **Fundo** | preto (`#000000` ou um quase-preto) em toda a tela |
| **Janela do vídeo** | **quadrada (1:1), ~984 x 984**, centralizada, com o topo em y ≈ 500 (abaixo do título); **bordas a ~48 px das laterais**; **raio de 24 a 36 px**. A janela maior dá mais espaço para o vídeo e para o rosto: **mantenha o rosto acima de y ≈ 1250** (a parte de baixo da janela pode passar da zona de interface, é só imagem). Alternativas: 4:5 (~984 x 1230) para vídeo vertical, ou 16:9 (~984 x 554) só se a pessoa pedir uma janela baixa |
| **Margens** | amplas em cima e embaixo; o vazio é parte do formato |
| **Título** | na parte de cima, **centralizado**, em branco, 2 ou 3 linhas curtas (até ~8 palavras), corpo de 64 a 84 px, **tipografia editorial** (serifada ou grotesca fina), y ≥ 300 |
| **Legenda** (se houver) | discreta, corpo de 48 a 56 px, sobre a parte de baixo da janela, **acima de y ≈ 1250**; é uma camada por cima (`children`) |

- Se o vídeo é vertical, a janela quadrada (ou 4:5) com o enquadramento mais fechado no rosto funciona melhor; não estique.

## Elementos e animações

- **Minimalistas.** Título entra com um fade de 0,5 a 0,8 s (sem pop); a janela aparece com um fade ou uma leve escala de 0,96 para 1,0.
- **Zoom suave** (1,0 para ~1,06 em vários segundos) ou movimento muito discreto; nada de punch brusco.
- **Tratamento de cor:** dessaturação leve, contraste um pouco maior e uma granulação muito discreta; o mesmo em todo o vídeo.
- **Tratamento de áudio:** voz limpa, um pouco de calor (graves), reverb muito leve opcional; nada que mude a inteligibilidade.

## Cortes e ritmo

- **Cortes intencionais**, que respeitam as **pausas e o peso das falas**: aqui **a pausa mantém**, não se encurta. Emenda com sobreposição só quando a pausa não é parte do impacto.
- Menos eventos: o formato **dispensa a regra de um evento visual a cada ~2 s**; o evento é a frase, a música e a respiração. Ainda assim, evite mais de ~6 s sem nada mudar (um zoom lento conta como vida, não como evento).
- Final **sem cauda longa**: a música desce com a última frase.

## Texto e legenda

- **O título é a legenda do vídeo inteiro**: uma frase que dá o tom, não o resumo da fala.
- Se a pessoa pede legenda, em corpo menor e abaixo da janela; sem destaque colorido, no máximo em itálico ou peso.

## Som

- **Música de fundo emocional, inspiradora, reflexiva ou dramática, escolhida por você** para acompanhar o tom do vídeo (`materiais.md`: licença clara, boa qualidade), **bem abaixo da voz** (cerca de 20 dB), com entrada e saída suaves e um fade nos últimos 0,7 s.
- Efeitos sonoros mínimos ou nenhum.

## Materiais

- **Peça:** o vídeo principal; a frase de título, se tiver; a música, se a pessoa já escolheu uma.
- **Pode buscar sozinho:** a **música** (escolha pelo clima), texturas e granulação, fontes.
- **Nunca invente:** a história, o resultado ou o depoimento que o vídeo conta.

## Variações dentro do formato

- Proporção da janela (quadrada, 4:5 ou, se pedirem, 16:9); raio dos cantos.
- Tipografia do título e a cor (branco, marfim); com ou sem legenda.
- Trilha (clima) e o tratamento de cor.

## Armadilhas e checklist

- [ ] A janela está centralizada e **não** preenche a tela inteira.
- [ ] O título é curto, legível, dentro da zona segura, e **não repete** a fala.
- [ ] As pausas de impacto estão mantidas.
- [ ] A música está abaixo da voz e termina em fade junto com a imagem.
- [ ] O tratamento de cor é o mesmo do começo ao fim e não "lava" o rosto.
- [ ] A música tem **licença confirmada** para anúncio (`MATERIAIS.md`).

## Estruturas e exemplos

Estrutura do exemplo do autor: **fundo preto**; **título em duas linhas** em tipografia editorial (a segunda linha começa apagada e é revelada); **janela de cantos arredondados** (**quadrada ou quase quadrada** dá mais espaço ao vídeo do que uma janela baixa e retangular); **legenda discreta abaixo** da janela, com uma pílula de destaque; trilha própria; **pausas mantidas**. Quadro: `references/exemplos/15-cinema.jpg`.

## Apoio

Se a skill `creative-lab` estiver disponível, use a regra de fechamento e de CTA dela; se a skill `transcrever-groq` estiver disponível, use-a para a legenda.
