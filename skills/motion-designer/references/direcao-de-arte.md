# Direção de arte

## Cor

- **Três cores neutras ou de marca e uma de destaque.** O destaque é a única cor viva e fica reservado a ênfase curta (uma palavra da frase, o objeto que importa). Cerca de 70 a 80% do quadro em superfícies neutras, 5 a 10% em destaque.
- **Contraste legível.** Texto claro sobre fundo escuro, ou o contrário, com contraste de pelo menos 4,5:1 para texto normal e 3:1 para texto grande. Confira os pares de cor, em especial branco sobre cor viva.
- Não use cor viva como cor de texto corrido.

## Fundo

- Um **gradiente** simples (de duas cores próximas) e **um único foco de luz** suave, longe da área do texto, que se move devagar. Vários focos competem.
- Fundo escuro funciona bem para objetos luminosos; fundo claro funciona bem para objetos escuros e sombras visíveis. Escolha um por peça e mantenha.
- Evite textura e efeitos que roubem a leitura. Vinheta leve nas bordas ajuda a concentrar o olhar.

## Tipografia

- **Uma família**, no máximo dois pesos fortes (por exemplo 600 e 700). Fonte livre (Google Fonts ou licença aberta), carregada no projeto e **aguardada antes de desenhar** (principalmente quando o texto vira textura de um objeto).
- Tamanhos num quadro de 1080 de largura: frase principal 90 a 125 px, apoio 60 a 90 px, rótulos 40 a 55 px, legenda e aviso nunca abaixo de 28 px.
- Entrelinha curta (1,05 a 1,15) e espaçamento de letras levemente negativo nos títulos grandes.

## Profundidade (2D e 3D)

- **2D:** sombras suaves e largas (deslocadas para baixo), camadas com contraste de brilho, e no máximo uma perspectiva leve (rotação de poucos graus) em um objeto herói.
- **3D:** uma luz principal com sombra, mais duas luzes de contorno coloridas, com as cores da paleta. Reflexos suaves de estúdio, mapeamento de tom neutro (preserva as cores), sombras suaves num piso invisível. Veja `kit/camera3d.tsx`.
- **Material:** formas arredondadas e bordas chanfradas pegam luz e parecem objetos. Cantos vivos e faces chapadas parecem desenho.

## Zona segura

Em 9:16 para Reels, Stories e Shorts: topo 270 px, base 360 px, laterais 90 px (num quadro de 1080x1920). Texto e objeto principal ficam dentro dessas margens.

## Marcas reais

Quando a peça é sobre uma marca de terceiros:

- Consulte a cor nos **tokens publicados no CSS oficial** da marca (anote a fonte e a data da consulta).
- Use **fonte livre** semelhante no lugar da proprietária. Não presuma licença da fonte da marca.
- **Não reutilize logo, símbolo, fonte ou arquivo** da marca. Se o nome aparece, aparece como texto simples. Se precisar de um símbolo, desenhe o seu como forma abstrata.
- **Interface, cartão e celular são fictícios** e abstratos: sem captura de aplicativo real, sem saldo, taxa, bandeira ou condição comercial.
- Mantenha **"conceito independente, não oficial"** dentro da peça (no encerramento) e na documentação.

## O que evitar

- Muitos neons e brilhos competindo; glow em tudo.
- Mais de uma ideia por cena; mais de uma frase por cena.
- Ícones genéricos de robôs, circuitos e cérebros quando não há relação com a ideia.
- Efeito que atrapalha a leitura. Se houver conflito entre efeito e leitura, a leitura vence.
