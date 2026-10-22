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
- Aproximação lenta e contínua nas cenas de apresentação (distância cai aos poucos); afastamento e órbita na convergência.
- **Tremida mínima** no alvo (`drift`, de 2 a 3 centésimos) tira o aspecto de câmera de computador sem parecer câmera de mão.
- **Lente deslocada** (`shiftPx`): sobe o assunto para dentro da zona segura sem mexer na composição. Positivo sobe o assunto (medido: 110 px de deslocamento levou o centro do objeto de 960 para 858 px).
- Distâncias e ângulos mudam por cena: o objeto não pode ficar enquadrado igual o vídeo inteiro.
- O alvo deve estar sempre dentro do quadro. Confira com quadros de diagnóstico nos instantes entre as chaves, não só nas chaves.

## Sincronia com o som

Se a peça tem trilha, os eventos grandes (entrada de objeto, troca de cena) caem **na batida**. A 120 BPM, uma batida a cada 15 quadros (a 30 fps). Veja `audio.md`.
