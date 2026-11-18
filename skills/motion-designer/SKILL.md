---
name: motion-designer
description: Direção para criar motion design e motion graphics no Remotion, de dois jeitos - motions explicativos que mostram um processo, uma relação ou uma comparação sincronizados com a fala, e peças inteiras feitas só de objetos animados em 2D ou 3D, como comerciais conceituais, vinhetas e vídeos de produto. Cobre a lógica visual, a estrutura da peça, a direção de arte, o movimento e a câmera, a direção de áudio e a revisão por quadros, e traz um kit opcional de código e uma síntese opcional de trilha e efeitos sonoros. Use sempre que pedirem motion design, motion graphics, animação explicativa, "explica isso com animação", "faz um motion para a aula", vídeo todo animado, comercial conceitual, animação 3D, vinheta animada ou "faz um vídeo só de motion", mesmo que o pedido seja vago. Os motions são feitos e exportados com a skill do Remotion.
---

# Motion Designer

Direção para criar motion design com acabamento: o que mostrar, em que ordem, com que movimento, e como conferir antes de entregar. Serve para dois usos:

- **Explicativo:** um motion dentro de uma aula ou de um vídeo, que faz a pessoa entender uma relação ou um processo.
- **Peça inteira:** um vídeo feito só de objetos animados (2D ou 3D), como um comercial conceitual, uma vinheta ou um vídeo de produto.

A criação e a exportação são feitas no Remotion (skill do Remotion). Esta skill traz o que decide a qualidade: a lógica, a coreografia, a direção de arte, o áudio e a revisão.

`<skill>` abaixo é a pasta onde esta skill está instalada. Os arquivos de `<skill>/kit/` são **opcionais**: o agente copia só o que precisar para o projeto Remotion.

## Princípios

- **Mostre a mudança, não decore.** O espectador tem que perceber o que mudou, por qual ação e com qual consequência. Título e ícone parado não explicam nada.
- **Um movimento principal por vez.** Cada cena tem um objeto herói e uma ideia. O resto serve a ele.
- **Tudo é função do frame.** Posição, estado e câmera dependem só do número do quadro, sem CSS animation, transition, timers ou `useFrame` como relógio. Assim a prévia e o arquivo exportado mostram o mesmo.
- **Dado só se for dado.** Números, proporções e eixos vêm de dados confirmados. Sem dado, é uma ilustração qualitativa, e a peça deixa isso claro quando a aparência puder sugerir medição.
- **Direção vale mais que um pedido esperto.** Uma linha de pedido dá algo genérico. Pergunte pela ideia, pelo estilo e pela personalidade, e trate as notas da pessoa como o trabalho de verdade, não como um retoque no fim.
- **Menos, bem acabado.** Poucos elementos, bem animados e bem espaçados, valem mais que muitos. Usabilidade vence efeito: o que o texto diz tem que ser lido.

## Pergunte primeiro (uma mensagem curta, com AskUserQuestion)

Dê opções concretas, a recomendada primeiro, e siga com o padrão declarado se a pessoa não responder.

1. **Modo:** motion explicativo dentro de um vídeo, ou peça inteira?
2. **Formato e duração:** 9:16, 16:9 ou 1:1; quantos segundos. (Padrão para peça inteira: 9:16, 15 a 30 s.)
3. **Ideia e personalidade (peça inteira):** em uma frase, qual é a ideia, e como a peça deve parecer (calma, enérgica, premium, divertida...)? Há uma referência de que a pessoa goste? Sem isso, o resultado sai genérico. Proponha 2 ou 3 direções se ela não souber dizer.
4. **Identidade:** usar a marca, as cores e a fonte da pessoa, ou criar uma simples? Se a peça é sobre uma marca de terceiros, veja `references/direcao-de-arte.md`.
5. **Técnica:** 2D, 2D com perspectiva ou 3D. Recomende uma e diga o custo (`references/tecnica.md`).
6. **Áudio:** tem trilha e narração; quer só o mapa de som para montar depois; ou quer que eu sintetize uma trilha e efeitos simples? (`references/audio.md`)
7. **Kit:** quer que eu use os arquivos prontos do kit (movimento, câmera 3D, exemplo) ou escrevo tudo do zero? (`references/kit.md`)

## Fluxo

O passo 3 (storyboard) e a parte de **som por evento** do passo 7 são **só para peça inteira**: anúncio, conteúdo ou vinheta feitos inteiramente de motion. Num motion explicativo dentro de um vídeo com pessoa, pule-os.

1. **Brief e fala real.** Leia ou transcreva a fala (se houver). Para cada trecho que pede explicação, identifique o estado inicial, a ação e o estado final. Em peça inteira, defina o texto de cada cena.
2. **Documento de direção** (`DIRECAO.md`): cenas com tempo e função, textos, objeto herói, paleta, câmera, mapa de som. É a referência que a pessoa aprova. Modelo em `references/peca-inteira.md`.
3. **Storyboard visual (só peça inteira):** um quadro-chave numerado por cena, com o que se move e como vira a próxima (`references/peca-inteira.md`, `kit/folha_de_quadros.py`). A pessoa aprova ou dá notas por número **antes** de qualquer animação.
4. **`config.ts` único** com formato, tempos, textos, cores e posições. As cenas só leem dele. Em peça inteira, os instantes de som ficam em `EVENTOS`.
5. **Teste a cena mais difícil antes de multiplicar as cenas.** Renderize um quadro ou um trecho curto. Se a pessoa pediu aprovação de estilo, mostre antes de seguir.
6. **Cenas**, uma por vez, no orçamento de cada uma. Regras em `references/explicativo.md` ou `references/peca-inteira.md`, mais `direcao-de-arte.md` e `movimento.md`. Se algo parecer errado, veja `references/problemas.md`.
7. **Áudio** conforme a escolha da pessoa. Em peça inteira, o som lê os eventos do `config.ts` e cada som cai no quadro do seu evento (`references/audio.md`).
8. **Revisão por quadros** (`references/revisao.md`): quadros nos instantes-chave **e entre eles**, zona segura, legibilidade.
9. **Exporte** com a skill do Remotion e **verifique o arquivo**: duração, quadros, cor e áudio.
10. **Entregue** dizendo o que foi verificado e o que não foi, e qualquer simplificação técnica que mude a representação. Se a pessoa responder com notas, siga "Rodadas de notas".

## Rodadas de notas

Em qualquer etapa, quando a pessoa der notas:

1. **Guarde a versão atual antes de mexer** (uma cópia da pasta do projeto ou um commit), para ela poder voltar.
2. **Aplique todas as notas** da rodada, não só a primeira, e **reveja os quadros** do que mudou (e, se um tempo mudou, as transições vizinhas).
3. **Diga o que mudou em palavras simples**, nota por nota. Se uma nota não pôde ser cumprida do jeito pedido, diga por quê.
4. **Salve como uma nova versão**, a menos que a pessoa peça para substituir. Nunca apague arquivos dela.

## Antes de entregar, confira

- A ação visual corresponde à frase e não sugere uma informação nova não confirmada.
- Os objetos mantêm identidade e continuidade; nada muda de forma ou de lugar para esconder um erro.
- A relação fica clara em velocidade normal e em tamanho de celular.
- Texto e elementos essenciais ficam dentro da zona segura e legíveis durante o movimento.
- O arquivo exportado mostra o mesmo que a prévia: sem tela vazia, salto ou animação ausente.
- Se a pessoa pediu 3D, é 3D de verdade. Uma alternativa em 2D só entra se ela aprovar, dita como simplificação.

## Referências (abra só o que precisar)

- `references/explicativo.md`: motion que explica, escolha da representação, sincronia com a fala, critérios de aceite.
- `references/peca-inteira.md`: estrutura de uma peça só de motion, orçamento por cena, copy, documento de direção.
- `references/direcao-de-arte.md`: paleta, fonte, fundo, profundidade, luz, material, zona segura, regras de marca.
- `references/movimento.md`: curvas, entradas, câmera, continuidade entre objetos e as regras de câmera e ritmo de uma peça inteira.
- `references/tecnica.md`: escada 2D, 2D com perspectiva e 3D, custos, render do 3D, plano B.
- `references/audio.md`: grade de batidas, mapa de som, som por evento, direção de som de peça inteira, volume, e a síntese opcional.
- `references/revisao.md`: como revisar por quadros e verificar o arquivo exportado.
- `references/problemas.md`: defeitos que já aconteceram e a correção de cada um.
- `references/kit.md`: o que o kit traz e como usar.
