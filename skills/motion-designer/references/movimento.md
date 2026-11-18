# Movimento e câmera

Tudo é função do frame: dado o número do quadro, o resultado é sempre o mesmo, em qualquer ordem de renderização. Sem CSS animation, transition, timers ou `useFrame` como relógio.

## Tempos de referência (a 30 fps)

| O quê | Quadros |
|---|---|
| Entrada de um texto | 12 a 16 |
| Entrada de um objeto (com leve overshoot) | 14 a 20 |
| Defasagem entre linhas ou elementos em sequência | 3 a 7 |
| Repouso depois de uma entrada, para a pessoa perceber | 18 a 24 |
| Mudança de estado de um objeto | 8 a 12 |
| Saída | 8 a 14, e mais rápida que a entrada |

## Curvas

| Curva | Para quê | No kit |
|---|---|---|
| **out** (começa rápida, freia no fim) | entradas | `EASE.out` |
| **inOut** | deslocamentos de ponto a ponto | `EASE.inOut` |
| **in** (começa devagar, acelera) | saídas | `EASE.in` |
| **spring** com leve overshoot | objeto que "assenta" e dá peso | `pop()` |
| **curva por chaves** (PCHIP) | câmera, rotação, posição com várias paradas; velocidade contínua e sem overshoot | `track()` |

- Todo movimento **termina em repouso**. Nada para de forma abrupta, e nada fica "tremendo" no fim.
- **Overshoot pouco:** amortecimento alto (cerca de 12 a 15). Quicar demais parece brinquedo.
- Para **dar vida a um objeto parado**, use `drift()` com amplitude pequena (alguns pixels, ou alguns centésimos de unidade no 3D). Mais que isso distrai.
- **Impacto:** quando um objeto "bate" (cai, encaixa), `squash()` achata e alarga por meio segundo. Dose baixa: 5 a 12%.

## Continuidade entre objetos

Quando um objeto dá lugar a outro (por exemplo um cartão que vira um celular), **o espectador não pode ver um salto**:

- Use **uma única curva de rotação** compartilhada pelos dois: o primeiro gira até ficar de perfil, o segundo assume a mesma rotação (somada de 180°) com a mesma velocidade angular.
- Durante uma janela curta (cerca de 12 quadros) os dois coexistem em dissolve.
- Se as silhuetas forem diferentes, **deforme o primeiro** (escala não uniforme) até igualar a silhueta do segundo antes da troca.
- Um brilho curto (screen) sobre a troca ajuda a esconder a emenda sem esconder a etapa.

## Câmera (3D)

- **Coordenadas esféricas ao redor de um alvo** (azimute, elevação, distância, alvo, campo de visão), com **chaves** ao longo do tempo e `track()` entre elas. O kit tem `CamKey` e `camState()`.
- Aproximação lenta e contínua nas cenas de apresentação (distância cai aos poucos); afastamento e órbita na convergência, que é um **assunto novo** (todos os objetos reunidos). No mesmo assunto, a direção não se inverte (seção seguinte).
- **Tremida mínima** no alvo (`drift`, de 2 a 3 centésimos) tira o aspecto de câmera de computador sem parecer câmera de mão.
- **Lente deslocada** (`shiftPx`): sobe o assunto para dentro da zona segura sem mexer na composição. Positivo sobe o assunto (medido: 110 px de deslocamento levou o centro do objeto de 960 para 858 px).
- Distâncias e ângulos mudam por cena: o objeto não pode ficar enquadrado igual o vídeo inteiro.
- O alvo deve estar sempre dentro do quadro. Confira com quadros de diagnóstico nos instantes entre as chaves, não só nas chaves.

## Câmera e ritmo de uma peça inteira

Valem sobretudo para peças feitas só de motion (anúncio, conteúdo, vinheta), onde a câmera e o ritmo são o vídeo. Num motion explicativo curto dentro de um vídeo com pessoa, use só o que couber.

| Regra | Como |
|---|---|
| **Uma câmera contínua** | Em cada cena a câmera faz um só gesto: **rápido no começo e devagar por muito tempo** (o recuo de abertura freia em curva exponencial; depois vêm empurrões suaves). Nunca um pico de velocidade no meio. |
| **A direção não se inverte no mesmo assunto** | Aproximar e depois afastar do mesmo objeto, ou orbitar, parar e voltar, parece hesitação. Giros de até 90° são bons. Se algo precisa terminar de frente, deixe uma deriva lenta **chegar** lá, em vez de parar e girar de volta. Mudar de direção só faz sentido quando entra um assunto novo. |
| **Uma curva por movimento** | Emendar duas curvas cria uma quina na velocidade. Passe todas as chaves de um movimento por um único `track()`. |
| **Mais devagar do que parece certo** | O primeiro rascunho quase sempre sai rápido demais. Dê mais repouso às cenas e retarde em ~50% as viradas que o olho não acompanha. |
| **Sempre algo se movendo** | Mesmo nos repousos, uma deriva lenta ou um empurrão leve. Um quadro parado entre dois movimentos grandes parece travado. Continua valendo **um movimento principal por vez**: o resto é fundo. |
| **Antecipação** | Antes de um objeto crescer, sair ou saltar, comprima-o cerca de 8% por um instante (uma pose antes). É diferente do `squash` de impacto, que vem depois de uma batida. |
| **Varie o ângulo em movimentos longos** | Um travelling ou uma rolagem com o mesmo ângulo do começo ao fim parece estático. Comece alto à esquerda e termine alto à direita, por exemplo. |
| **Desfoque de movimento** | Faça a média de ~12 sub-quadros dentro de meia duração do quadro (obturador de 180°). Com 5, aparecem cópias fantasma. Custa até 12 vezes o tempo de render: ligue só no render final e só onde há movimento rápido. O Remotion tem um pacote próprio para isso: confira a documentação. |
| **Profundidade de campo rasa (3D)** | Assunto nítido e fundo desfocado dão cara de filmado. É cara de renderizar: use no objeto herói e nos planos em que o fundo atrapalha. |
| **Fim estável** | O último plano não tem deriva de câmera, e o logo fica centralizado pela caixa do que se vê. |

Os defeitos que mais aparecem nesses movimentos estão em `problemas.md`.

## Sincronia com o som

Se a peça tem trilha, os eventos grandes (entrada de objeto, troca de cena) caem **na batida**. A 120 BPM, uma batida a cada 15 quadros (a 30 fps). Veja `audio.md`.
