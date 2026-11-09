# 05. Professor (Explicação Visual)

**Também pedido como:** professor, explicação visual, lousa, aula curta, explica com animação.

## Assinatura visual

A **pessoa em primeiro plano explicando**, enquanto **gráficos, diagramas, textos e animações aparecem no momento certo da fala** para ilustrar. O fundo tem cara de **lousa ou quadro** e cada elemento entra **quando é dito**. A assinatura é o **didático**: um conceito por vez, fácil de acompanhar.

## Ideal quando

- Há um **conceito, um processo ou uma comparação** para explicar (um mecanismo, "como funciona", "passo a passo").
- A explicação ganha com **uma imagem que se constrói** enquanto a pessoa fala.
- Infoproduto, ferramenta, serviço complexo, educação.

## Evite quando

- Não há o que desenhar: o fundo fica vazio, ou é decoração.
- A explicação precisa de **dados que a pessoa não tem**: não invente números nem eixos (`honestidade.md`).
- O vídeo é só emoção e história.

## Composição (1080x1920)

| Elemento | Posição e tamanho |
|---|---|
| **Fundo** | cor lisa escura ou clara com uma **grade sutil** (lousa); sem textura de marca |
| **Pessoa** | recortada (formato 02) **ou** em uma janela, em baixo à esquerda ou à direita, ocupando ~45% da altura; cabeça inteira acima de y ≈ 1250 |
| **Área da explicação** | a parte de cima e do meio, y de ~300 a ~1100, onde os elementos surgem |
| **Elementos** | texto de 56 a 76 px, setas, formas, ícones, gráficos simples, um **destaque** (círculo ou realce) no que está sendo dito |
| **Legenda** | y ≈ 1120 a 1220, sem cobrir a pessoa |

## Elementos e animações

- **Cada elemento entra na palavra** que o cita, com animação curta (0,25 a 0,4 s), e **fica** o tempo de ser lido.
- **Um conceito por vez:** o quadro limpa ou recua antes do seguinte; não acumule mais de ~4 elementos.
- **Destaques** (círculo, sublinhado, cor) guiam o olho para o que importa agora.
- **Diagramas** com **causa e efeito** visíveis (A leva a B), e **não** uma lista de cartões iguais.

## Cortes e ritmo

- Emenda com **sobreposição** na pessoa (`cortes.md`); evento novo (elemento, destaque, troca de quadro) a cada **~2 a 2,5 s**.
- Reserve um **intervalo estável** (~0,6 a 0,8 s) depois de uma explicação concluída, para a pessoa perceber o resultado.

## Texto e legenda

- Texto dos elementos **curto** (rótulos, palavras-chave), com o **mesmo termo** que a fala usa.
- Legenda palavra a palavra, com realce nos ★.

## Som

- Voz em primeiro plano; um efeito curto quando um elemento-chave entra (opcional); música bem abaixo ou nenhuma.

## Materiais

- **Peça:** o vídeo da pessoa explicando; **dados reais** quando houver números; as imagens do que ela cita.
- **Pode buscar sozinho:** ícones, formas, diagramas desenhados por código, fontes, música.
- **Nunca invente:** números, proporções, gráficos de resultado ou estudos; sem dado, faça uma **ilustração qualitativa** e identifique-a como tal.

## Variações dentro do formato

- Tema claro ou escuro; pessoa recortada ou em janela; posição da pessoa.
- Tipo de diagrama (fluxo, comparação, camadas); quantidade de elementos.
- Com e sem destaque animado.

## Armadilhas e checklist

- [ ] Cada elemento entra na palavra que o cita e fica tempo de ser lido.
- [ ] A relação (A leva a B) é **visível**, não só listada.
- [ ] Os números e gráficos têm base real, ou estão identificados como ilustração.
- [ ] A pessoa não é coberta pelos elementos.
- [ ] Nunca mais de ~4 elementos ao mesmo tempo.

## Estruturas e exemplos

Estruturas possíveis: **lousa ou diagrama em cima e a pessoa embaixo** (um primo da tela dividida, com elementos que explicam o que está sendo dito); os elementos **se constroem na palavra** (um nó aparece quando é citado, uma linha se desenha ligando ao próximo); a legenda fica entre o diagrama e a pessoa. Ilustração **qualitativa**, sem números inventados. Também funciona com a pessoa pequena num canto e os cartões ocupando a tela (modo "miniatura"). Quadros: `references/exemplos/05-professor.jpg` e `mistura-13-caixinha-de-pergunta.jpg` (miniatura e cartões).

## Apoio

Se a skill `motion-designer` estiver disponível, use-a para os motions explicativos (a lógica de estado inicial, ação e estado final, e o kit de movimento); se a `creative-lab` estiver disponível, use as regras de mecanismo e resultado dela. Se não, siga os princípios acima: um movimento principal por vez, tudo calculado por quadro, nenhum dado sem base.
