# Cortes, emendas e ritmo

Vale para todo corte do criativo, em qualquer formato (as exceções estão no arquivo do formato).

**Para tirar erros, repetições e silêncios de uma gravação falada, siga `limpar-a-fala.md`**: lá estão os scripts que fazem isso medindo o áudio (`planejar_cortes.py`, `montar.py`, `verificar_cortes.py`, `achar_repeticoes.py`). Esta página descreve a **regra** da emenda; não a refaça à mão com `silenceremove` do FFmpeg, que corta seco e deixa pausa.

## Se há uma skill de cortes

Se a skill `smart-cuts` estiver disponível, use-a para **escolher os melhores momentos de um vídeo longo** e emendar cada um (ela entrega um mp4 limpo por corte e um `plano.json`) e depois monte o formato em cima. Para **limpar a gravação de um criativo** (erros, repetições, silêncios), o caminho é `limpar-a-fala.md`, que já vem na skill.

## A emenda com sobreposição (padrão)

Imagem e áudio do take seguinte entram **juntos**, colados no começo da voz, antes de o take anterior acabar. O desenho, os valores, o passo a passo de cada junção e onde cai a emenda estão em `emenda.md`.

## Como fazer no Remotion

- Cada take é uma `<Sequence>` com o seu `<Video>` (`trimBefore` no início da voz).
- A sequência seguinte começa `sobreposicao` quadros **antes** do fim da anterior (`from = fimAnterior - sobreposicao`).
- O áudio do take anterior leva um `volume` em rampa descendente nesse intervalo; o novo entra com uma rampa curta.
- Há uma peça para reaproveitar: `assets/componentes/TakesSobrepostos.tsx` (a sobreposição em `Sequence`s, a rampa de volume do take anterior e o fade curto do novo, mais `duracaoDosTakes`). Copie e ajuste; o enquadramento e o resto da composição são seus. Testado: imagem e áudio do take novo entram juntos, antes de a voz anterior acabar.

## Pausas e ritmo

- **Pausa longa** dentro de um take é encurtada seguindo a mesma regra (`emenda.md`, seção "Pausas dentro do mesmo take"). **Um silêncio de 0,5 a 1 s que sobrou no criativo é defeito**: quebra o ritmo. O `verificar_cortes.py` reprova.
- **Quando a graça é o silêncio** (pausa dramática, piada, depoimento emocional), **mantenha**. Os formatos mais calmos (Cinema, Depoimento) pedem mais respiro: está no arquivo deles.
- **Evento visual novo** (insert, texto, zoom, troca de plano, tela dividida, motion): nos primeiros 5 s, a cada ~1 a 1,5 s; depois, no máximo a cada ~2,5 s. Marco grande a cada ~6 a 8 s. Nunca o mesmo tipo três vezes seguidas.
- **Zoom:** punch-in de ênfase só em ★ (cerca de 1,12 a 1,2), e **todo zoom volta ao neutro**. Em cortes de jump, alterne o enquadramento (1,0 e ~1,05) para o salto sumir.
- O detector de cortes de cena não pega zoom nem jump cut leve: confira nas folhas de contato.
