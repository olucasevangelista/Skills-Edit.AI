# Regras de ofício

Cada regra aqui evita uma rodada inteira de reedição. O que o usuário pedir por cima vale mais.

## Fala: nenhuma palavra pode ser cortada

O criador ouve o corte inteiro. Uma sílaba comida ("seis quilos" virando "quilos", "produção" virando "produtos") estraga o corte.

- O tempo de palavra da transcrição erra de 0,2 s até mais de 1 s em arquivos longos. Por isso as emendas usam o **volume do áudio**, não o tempo da transcrição.
- Emenda só em SILÊNCIO REAL (abaixo de cerca de −40 dB por pelo menos 60 ms). Sem pausa entre o que fica e o que sai, não corte: mantenha a frase ou mova a emenda para a pausa real mais próxima. O planejador mostra o que entrou ou saiu (`ENTROU`, `SAIU`).
- Marque o fim de trecho no INÍCIO da última palavra no `cortes.json`. Marcar no fim calculado à mão já cortou "quê?" e números como "3,2".
- Transcrição que não leu algarismos ou nomes próprios: confira a grafia no checkpoint, junto, uma vez.
- Antes de entregar: transcreva o MP4 final e rode `verificar.py`. ALERTA ou PENDENTE = não entrega.
- A legenda nunca ganha palavra que não foi falada (dessincroniza). Corrigir a ESCRITA de uma palavra é permitido; inventar, não.

## Voz e áudio

- A voz é uma trilha separada e nunca muta, nem quando entra card, tela cheia ou fundo desfocado.
- Final sem cauda: o corte termina junto com a última palavra. Nada de quadro congelado com música tocando, tela preta ou boom depois da fala. A música acaba junto, com fade curto. Planeje o final pela fala.
- Música em alta qualidade (do YouTube, formato Opus/251; confira o espectro até ~19-20 kHz). Música abafada é percebida.
- A música fica bem abaixo da voz (sério em torno de 23 dB abaixo, meme em torno de 15 dB). Quando a graça é o silêncio, não ponha trilha.
- Riser de gancho bem baixo: alto incomoda.
- SFX só onde a fala pede, literal. SFX sintetizado costuma soar mal; na dúvida, menos.
- Volume: os cortes saem normalizados em −16 LUFS pelo `montar.py`. O alvo de feed de −14 LUFS, com música, é ajustado na exportação final do Remotion.
- Palavrão: áudio intacto; na legenda, com asterisco, se o usuário quiser.

## Imagem e enquadramento

- Cabeça inteira, sempre. Na tela dividida (insert em cima, rosto embaixo) o rosto desce até o cabelo ficar abaixo da faixa; nunca decapitar com o insert.
- Nenhum texto, número ou emoji em cima do rosto, da boca ou dos olhos. Legenda não cobre a boca nem a mão que gesticula.
- Zonas do 9:16: a interface do app cobre o topo (~0 a 8% da altura), a base (~80 a 100%) e a coluna direita (~88 a 100% da largura, de 45 a 85% da altura). Texto e rosto dentro de x 6-86% e y 10-80%.
- Zoom: variação fixa e pequena (~7%) nos jump cuts e nos pontos de ênfase. Só passa disso em pausa engraçada ou momento de impacto. Zoom exagerado cansa.
- Inserts em tela cheia (1,2 a 2,5 s, com texto curto de impacto) prendem mais que insert pequeno. Durante a tela cheia com texto, a legenda some.
- Meme-relâmpago (imagem que pisca na palavra-gatilho) dura ~0,7 s: alongar piora.
- Aula com tela + webcam: a tela compartilhada já é a prova visual; não cubra a faixa de cima com b-roll à toa. Webcam pequena perde qualidade ampliada: inserts bonitos em tela cheia valem muito ali.
- Mais regras e como medir o rosto: `enquadramento.md`.

## Conteúdo e verdade

- Nunca fabrique print de notícia, post, vaga, benchmark, chat ou depoimento como se fosse real. Print real com fonte, ou card claramente estilizado (número grande, bolha desenhada). Nunca invente número que a pessoa não falou.
- Meme com alvo: "brutal", "sobra nada", deboche apontam para COISA (bug, ferramenta, mito) ou para a própria pessoa, nunca para aluno, mulher, aparência ou terceiro.
- Apelidos e persona dos memes vêm da própria pessoa. Não invente apelido.
- Grafia duvidosa: pergunte no checkpoint, junto, uma vez.

## Processo e máquina

- O `montar.py` nunca altera o arquivo de origem e grava tudo na pasta de saída. Se o usuário apagar o original no meio do trabalho, não dá para montar mais cortes: monte todos antes de liberar o arquivo.
- Disco: o `montar.py` apaga os temporários de cada corte ao terminar (`--manter-temporarios` só para depurar). Os cortes montados são pequenos perto do original.
- Não reabra decisões que o usuário já tomou. Perguntar de novo o que ele já respondeu irrita.

## Checklist de QA de cada corte

1. O gancho aparece no primeiro segundo e se entende sem som.
2. Rosto inteiro, sem decapitar, sem borda preta, sem texto em cima.
3. Nada na zona de interface do app.
4. Um sistema de legenda só, legível, na altura certa, sem cobrir a boca.
5. Insert certo na palavra certa (a imagem entra 0 a 0,3 s antes do substantivo).
6. Layout certo em cada trecho (tela + webcam não virou "slide" com o rosto sumido).
7. Final fecha a ideia, sem cauda.
8. Depois da exportação: `verificar.py` sem ALERTA, áudio no alvo, música abaixo da voz.
