# Técnica: 2D, 2D com perspectiva ou 3D

Escolha o degrau mais baixo que conta a ideia. Suba só quando houver um motivo.

| Degrau | Como | Quando | Custo aproximado |
|---|---|---|---|
| **2D** | SVG, formas e CSS, composição plana | relações planas: processo, comparação, causa e efeito, partes de um todo | base |
| **2D com perspectiva** | os mesmos elementos, com `perspective` e rotações de poucos graus, sombras largas | quando uma leve sensação de profundidade ajuda e o volume real não importa | baixo |
| **3D de verdade** | three.js via `@remotion/three` (modelo, luz, sombra, câmera) | volume, oclusão, distância ou mudança de ponto de vista fazem parte da explicação, ou a peça é sobre objetos que o público precisa "ver por todos os lados" | cerca de 5 vezes mais código, e render mais pesado |

Perspectiva e paralaxe organizam camadas, mas **não comprovam geometria tridimensional**. Se o pedido é 3D, é 3D.

## Perguntas para decidir

1. A explicação muda se a pessoa vir o objeto de outro ângulo? Se sim, 3D.
2. A ideia é uma sequência de estados ou posições? Se sim, 2D basta.
3. Há prazo e capacidade de render? O 3D pede máquina com boa GPU ou CPU e mais tempo.
4. A pessoa pediu 3D? Então faça 3D, ou diga o que não deu e peça aprovação para a alternativa.

## 3D no Remotion: o que importa

O setup do `<ThreeCanvas>` (largura, altura, luz) está na skill do Remotion. Para uma peça:

- **Câmera e luz** do kit (`kit/camera3d.tsx`): câmera por chaves, ambiente de estúdio, luz principal com sombra e duas luzes de contorno com as cores da paleta.
- **Geometria procedural** (formas arredondadas extrudadas com chanfro) basta para objetos de produto simples. Ela se constrói em código, sem modelos externos.
- **Texto e interface de um objeto** (tela de celular, rótulo de cartão) são desenhados em um canvas 2D e usados como textura. **Espere a fonte carregar** antes de desenhar, e segure o render com `delayRender` até lá.
- **Resolução e custo:** `dpr={1}`, sombras só com a luz principal.
- **Render:** o Chromium precisa de GL. `--gl=angle` funcionou na máquina de teste (Windows) para quadros 3D. Use concorrência baixa (2 a 3) em peças com muitas sombras.
- Conferido: o render do kit de câmera num quadro 3D mínimo funcionou com Remotion 4.0.535, three 0.186.1 e @react-three/fiber 9.8.2. Em outra versão ou máquina, rode a verificação antes de multiplicar as cenas.

## Plano B

Se o 3D não renderiza na máquina, ou estoura o prazo:

1. **Diga isso à pessoa**, com o motivo.
2. Ofereça a alternativa 2D com perspectiva e **identifique o que muda** (por exemplo, "o cartão não gira, só inclina").
3. **Não apresente a alternativa 2D como cumprimento de um pedido explícito de 3D.** Entregue só com a aprovação da pessoa.
