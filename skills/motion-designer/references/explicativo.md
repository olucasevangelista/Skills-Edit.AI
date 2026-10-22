# Motion explicativo

O motion explicativo converte uma ideia em uma **mudança observável**. Quem assiste deve perceber o que mudou, por qual ação e com qual consequência, sem precisar ler uma lista de instruções.

Se a ideia não pede transformação, uma imagem clara pode bastar. Não acrescente movimento só para preencher a duração.

## 1. Defina a lógica visual

Leia ou transcreva a fala real. Para cada trecho que pede explicação, escreva em uma linha cada:

- **Estado inicial:** o que existe antes.
- **Ação:** o que acontece, e o que causa.
- **Estado final:** o que existe depois.
- **O que precisa continuar reconhecível:** o objeto que a pessoa acompanha do começo ao fim.

Use a relação que o conteúdo expressa. Não transforme correlação em causalidade nem ilustração em dado medido.

## 2. Escolha a representação pela relação

| Relação | Como mostrar | Evite |
|---|---|---|
| **Processo** | Uma peça percorre as etapas e muda de estado a cada uma | Mostrar todas as etapas como cartões iguais, lado a lado, sem nada percorrendo |
| **Causa e efeito** | A ação vem antes do resultado, com um vínculo visível entre os dois (linha, deslocamento, contato) | O efeito aparecer sem que nada o provoque |
| **Comparação** | Mesma escala, mesmo enquadramento e mesma base; destaque só a diferença que importa | Escalas ou enquadramentos diferentes que distorcem a diferença |
| **Partes de um todo** | Separe e reúna os mesmos componentes, mantendo a correspondência entre eles | Peças que mudam de forma ao reunir |
| **Relação espacial** | Use profundidade quando distância, volume, oclusão ou ponto de vista fazem parte da explicação | 3D só pelo efeito |

Exemplo de uma representação ruim e a boa: "o pedido passa por três etapas".

- Ruim: três cartões iguais com título e ícone, que aparecem juntos.
- Bom: um pacote percorre três estações. Em cada uma, ele muda de estado de um jeito visível (ganha cor, ganha uma fita, ganha uma seta de envio).

Um ícone deve executar uma ação ligada ao significado: componentes se conectam, um trajeto é percorrido, uma seleção muda o resultado. Dar escala a um ícone parado não explica o processo.

## 3. Coreografe pela compreensão

- **Apresente o objeto antes de pedir que a pessoa acompanhe a transformação.** O objeto entra, assenta e só então muda.
- **Sincronize com a frase.** O objeto chega **antes** da palavra (cerca de 0,3 a 0,5 s) e a mudança de estado acontece **na** palavra. Os instantes das palavras vêm da transcrição ou do roteiro, e ficam no `config.ts`.
- **Reserve um intervalo estável** (cerca de 0,6 a 0,8 s) para perceber o resultado antes da próxima ação.
- **Um movimento principal por vez.** Se duas coisas se movem, uma delas é fundo.
- **Mostre a etapa difícil inteira.** O início, o efeito e a conclusão precisam existir na montagem final, sem corte que esconda a parte complicada.
- **Texto só do que ajuda a ler a cena:** rótulo curto da etapa, uma frase de apoio. O texto não repete a fala palavra por palavra.

## 4. Números e rótulos

Números, proporções, eixos e rótulos devem vir de dados confirmados. Sem dados, construa uma ilustração **qualitativa** e identifique esse caráter na peça (por exemplo, "ilustração") quando a aparência puder sugerir medição.

## 5. Aceite observável

- A ação visual corresponde à frase e não sugere informação nova.
- Os objetos mantêm identidade e continuidade.
- A relação fica clara em reprodução normal e em tamanho de celular.
- Texto e elementos essenciais permanecem legíveis durante o movimento.
- O arquivo exportado mostra a mesma transformação da prévia.

## Técnica

Use SVG, formas e composição 2D para relações planas. Perspectiva e paralaxe organizam camadas, mas não comprovam geometria tridimensional. Se volume ou mudança de ponto de vista justificarem 3D de verdade, veja `tecnica.md`.

Teste a relação mais difícil antes de multiplicar as cenas.
