# Cortes, emendas e ritmo

Vale para todo corte do criativo, em qualquer formato (as exceções estão no arquivo do formato).

## Se há uma skill de cortes

Se a skill `smart-cuts` estiver disponível, use-a para **escolher os trechos** e **emendar** (ela entrega um mp4 limpo por corte e um `plano.json`) e depois monte o formato em cima. Se não estiver, siga o que está abaixo.

## A emenda com sobreposição (padrão)

O corte **não tem respiro e o áudio não é cortado seco**. O próximo take entra **colado no começo da voz** e **começa ainda durante o finalzinho do take anterior**: a **imagem e o áudio novos entram juntos** enquanto a última sílaba da frase anterior termina. Em linguagem de editor, é um L-cut curto. Na linha do tempo, os dois clipes se sobrepõem por cerca de **0,1 a 0,25 s (3 a 8 quadros a 30 fps)**, e as vozes se sobrepõem de propósito só por esse instante.

Em cada junção:

1. **Deixe o take anterior terminar.** Corte-o só depois da última palavra e do decaimento natural dela, nunca no meio da sílaba.
2. **Corte o início do próximo rente à fala:** sem respiro, sem inspiração, sem ruído de sala. Comece no instante em que a voz começa, com no máximo ~20 a 30 ms de folga.
3. **Sobreponha** a primeira palavra do próximo take ao finalzinho da última do anterior (0,1 a 0,25 s).
4. **Áudio:** o do take anterior desce suavemente durante a sobreposição; o do novo entra com um fade de 10 a 30 ms (só para evitar estalo). Confira que a soma das vozes não estoura.
5. **Imagem:** corta no mesmo instante em que o áudio novo entra (ou dissolve em 2 a 4 quadros).
6. **Ajuste ao material:** se a última palavra termina seca, use o mínimo (~0,1 s); se tem decaimento longo, até ~0,25 s.
7. **Vale também onde pausas dentro de um take são encurtadas.**

Não é o padrão: o áudio cortando seco (mesmo com a imagem entrando antes), nem o próximo take começando com respiro e pausa.

## Onde cai a emenda

- **Em silêncio real**, medido no áudio, não pelo tempo da transcrição (que escorrega 0,2 a 0,5 s em arquivos longos). Para achar os silêncios:
  `ffmpeg -i video.mp4 -af silencedetect=noise=-40dB:d=0.06 -f null -`
- Sem pausa entre o que fica e o que sai (palavras coladas), mantenha a frase ou mova a emenda para a pausa real mais próxima.
- **Nenhuma palavra cortada.** Marque o fim de um trecho no **início** da última palavra que fica; depois confira transcrevendo o resultado.

## Como fazer no Remotion

- Cada take é uma `<Sequence>` com o seu `<Video>` (`trimBefore` no início da voz).
- A sequência seguinte começa `sobreposicao` quadros **antes** do fim da anterior (`from = fimAnterior - sobreposicao`).
- O áudio do take anterior leva um `volume` em rampa descendente nesse intervalo; o novo entra com uma rampa curta.
- O kit tem o componente que faz isso (`kit/componentes/Movimento.ts` traz as curvas).

## Pausas e ritmo

- **Pausa longa** dentro de um take é encurtada (acima de ~0,25 s fica ~0,1 s), com a mesma sobreposição, sobre o silêncio.
- **Quando a graça é o silêncio** (pausa dramática, piada, depoimento emocional), **mantenha**. Os formatos mais calmos (Cinema, Depoimento) pedem mais respiro: está no arquivo deles.
- **Evento visual novo** (insert, texto, zoom, troca de plano, tela dividida, motion): nos primeiros 5 s, a cada ~1 a 1,5 s; depois, no máximo a cada ~2,5 s. Marco grande a cada ~6 a 8 s. Nunca o mesmo tipo três vezes seguidas.
- **Zoom:** punch-in de ênfase só em ★ (cerca de 1,12 a 1,2), e **todo zoom volta ao neutro**. Em cortes de jump, alterne o enquadramento (1,0 e ~1,05) para o salto sumir.
- O detector de cortes de cena não pega zoom nem jump cut leve: confira nas folhas de contato.
