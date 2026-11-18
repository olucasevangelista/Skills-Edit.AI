# Problemas conhecidos

Cada linha é um defeito que já apareceu em motions de verdade. Consulte quando algo parecer errado e leia antes de uma peça 3D ou longa: é mais barato evitar do que descobrir no render final. Os marcados com (3D) ou (canvas) só valem nessas técnicas.

## Movimento

| Sintoma | Causa | Correção |
|---|---|---|
| Cópias fantasma atrás de algo rápido | desfoque de movimento com poucos sub-quadros | cerca de 12 sub-quadros dentro de meia duração do quadro (obturador de 180°); veja `movimento.md` |
| Um "tranco" no meio de um movimento suave | duas curvas emendadas, com a velocidade diferente na junção | uma única curva por chaves para o movimento todo (`track()`) |
| Algo some "estalando" | fade com curva que termina rápido (`in` cúbica) | fade simétrico, de seno, em cerca de 1 s |
| Partes que se movem juntas se sobrepõem | cada uma viaja com uma velocidade própria | uma variável compartilhada (um só ângulo ou progresso); cada parte começa quando a da frente já andou um terço |
| Uma curva vira do avesso durante a transformação | interpolar direto para um destino com curvatura oposta | primeiro leve a curva até a curvatura do destino, depois percorra-a |
| A câmera "hesita" | aproximou e depois afastou do mesmo objeto, ou orbitou e voltou | direção única por assunto; a mudança só acontece quando entra um assunto novo |
| O objeto parece ter pressa | animação feita no tempo do primeiro rascunho | alongue as pausas; viradas rápidas que o olho não acompanha ficam ~50% mais lentas |
| Uma linha fina pisca ou some quando a câmera avança | linha de 1 a 2 px reamostrada pelo zoom | linhas de ~3,5 px, menos opacidade, deslocamentos em pixels inteiros |
| Animação posterizada (poses repetidas) fica irregular | taxa de quadros que não divide o número de poses por segundo | 24 fps para 8 ou 12 poses por segundo |

## Texto, cor e marca

| Sintoma | Causa | Correção |
|---|---|---|
| Título com gradiente ilegível | gradiente de texto sobre fundo de cor | gradiente só sobre fundo escuro; sobre cor, tinta sólida |
| Objeto branco some sobre fundo branco | sem borda entre os dois | contorno fino escuro quando ele chega ao branco |
| Logo final parece torto no quadro | o centro do arquivo não é o centro do que se vê, e a câmera ainda anda | centralize pela caixa do que é visível e deixe o último plano sem deriva |
| Texto aparece com a fonte errada nos primeiros quadros | a fonte não tinha carregado | segure o render até a fonte carregar (`delayRender`) |
| Ícone pixela no zoom final | ele faz parte da textura de um print | refaça como camada vetorial própria, em alta resolução, por cima |
| Sombra no lugar errado numa resolução maior (canvas) | o deslocamento da sombra ignora a escala do desenho | multiplique os deslocamentos pela escala de render |

## 3D

| Sintoma | Causa | Correção |
|---|---|---|
| Quadros pretos ou vazios | o Chromium sem GL não renderiza WebGL | `--gl=angle` em todo quadro e em todo render |
| Texto some atrás de um objeto | a ordem de profundidade o coloca atrás | prioridade de desenho para o texto, ou uma camada 2D por cima da cena |
| Peças atravessam a tampa ou a caixa | saem mais longe do que o corpo permite | esconda-as até a tampa abrir, ou faça-as sair em linha reta antes de girar |
| Detalhes parecem flutuar sobre uma superfície curva | discos chapados sobre uma curva | formas curvas afundadas na superfície |
| Um buraco se fecha | suavização forte, ou a superfície cobre o disco | suavize menos as peças pequenas e confira que o disco fica acima do piso |

## Render e arquivo

| Sintoma | Causa | Correção |
|---|---|---|
| A prévia não bate com o arquivo | algo depende de tempo real, de `Math.random` ou de CSS animation | tudo em função do quadro; renderize o mesmo quadro duas vezes e compare o hash |
| O computador trava no render | várias codificações pesadas ao mesmo tempo | uma ou duas por vez, concorrência baixa em peça com muita sombra, e teste em 1080 antes de subir |
| O render falhou e ninguém viu | `\| tail` esconde o código de saída | confira o código de saída ao final |
| A folha de contato do ffmpeg sai em branco | com `tile`, `-frames:v N` conta folhas, não quadros | limite com `-t`, depois `tile`, depois `-frames:v 1` |
| Faixas duras em volta de um preenchimento | o preenchimento para na borda suavizada | expanda a máscara do preenchimento uns pixels |
