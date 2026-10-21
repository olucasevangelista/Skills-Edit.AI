# Brief: dissecar vídeos de referência de edição (para agentes)

Você é editor sênior de Reels/TikTok e analista de cultura de internet. Vai dissecar vídeos de referência para que outro editor (uma pessoa ou um agente, com Remotion e FFmpeg) consiga REPLICAR o estilo com precisão nos vídeos de {{criador}} ({{nicho}}; nos memes ele é tratado como {{apelidos_nos_memes}}).

Você enxerga, mas NÃO escuta. Para o som você tem pistas medidas: trate-as como pistas, nunca invente som sem evidência, e marque a confiança (alta/média/baixa).

## Material de cada vídeo (`{{lote}}/analise/<slug>/`)

- `meta.json`: arquivo, duração, resolução, fps, cortes de cena por minuto e duração média de plano.
- `sheets/sheet_NN_<t0>-<t1>.jpg`: folhas de contato 6x3 com o tempo (s) em amarelo em cada quadro (2 quadros por segundo em vídeo de até 60 s, 1 por segundo em vídeo mais longo). LEIA TODAS. Se o tempo não aparecer escrito, a ordem é da esquerda para a direita e de cima para baixo, e o nome da folha diz o intervalo.
- `scenes.json`: instantes de corte de cena (limiar 0,3; zoom e jump cut leve podem não aparecer).
- `sons.json`: volume integrado (LUFS), pico, % do tempo com som e `transientes` (subidas bruscas de volume). Transiente + evento visual no mesmo instante = provável efeito sonoro; sozinho, pode ser batida de música ou início de fala.
- Transcrição da skill de transcrição, quando existir (`<slug>/transcricao.json` ou `.txt`): fala com tempo por palavra. O Whisper erra palavra e às vezes "transcreve" música: a legenda queimada no vídeo é a verdade.

Para detalhe (fonte da legenda, texto pequeno, animação, zoom), tire quadros em resolução cheia:
`python {{skill}}/scripts/analisar.py quadro <video> <t>` ou, para ver a animação,
`python {{skill}}/scripts/analisar.py quadro <video> <t> --rajada 1.5 --fps 10`.
Faça isso em 3 a 8 momentos-chave por vídeo, sempre que a folha não bastar.

## O que analisar (por vídeo)

1. **Ficha**: autor, link, duração, formato (9:16, 1:1 com fundo, letterbox), tema.
2. **Gancho (0-3 s)**: o que aparece, o que está escrito, o que se ouve, por que prende. O primeiro quadro é rosto, meme, texto, print?
3. **Enquadramento**: posição do rosto (fração da altura), plano (close, médio), fundo, zoom dinâmico, tela dividida (onde divide, em fração da altura), moldura.
4. **Legenda falada**: família da fonte (palpite: Montserrat, Poppins, Archivo, Anton, Bebas, Inter, serifadas...), peso, caixa, tamanho em % da largura, centro vertical em fração da altura, palavras por página, cor base e de destaque e o critério do destaque, contorno, sombra, fundo, animação de entrada (pop, escala, fade, palavra que nasce, karaokê), acentos, emoji, palavras-chave com outro estilo. MEÇA no quadro em resolução cheia: altura de uma maiúscula em px / largura do quadro.
5. **Textos fixos e títulos**: manchete, rótulos, setas, círculos, contadores, selos (fonte, tamanho, posição, cor, quanto tempo ficam).
6. **Ritmo**: cortes por minuto, jump cuts (respiros cortados?), duração média de plano, punch-in (quando, quanto), Ken Burns, shake, flash, transições (seco, whip, glitch, fade).
7. **Inserts**: CADA um com entrada e saída, o que é (meme conhecido? template? foto? print de notícia? stock? cena de filme? gif?), como entra (tela cheia, sobreposto, tela dividida, PIP), texto sobre ele, e a FUNÇÃO (ilustrar, piada, reação, ironia, ênfase, prova).
8. **Humor** (meme): qual é a piada, onde está o beat (tempo exato), mecanismo (ironia, exagero, contraste, narrador em terceira pessoa, autodepreciação, silêncio constrangedor, freeze). Como uma fala comum vira piada.
9. **Áudio**: trilha (se o criador ou a legenda dizem o nome; senão gênero e clima pelo que se percebe), quando entra, muda, cai (drop) ou para de repente; nível relativo à voz (estime pelo LUFS e pelo que o `sons.json` mostra e deixe a confiança marcada). Efeitos sonoros: cada provável efeito com tempo, tipo e o evento visual que acompanha, com confiança.
10. **Cor e efeitos**: grade, P&B, saturação, vinheta, grão, câmera lenta, freeze, desfoque, overlays.
11. **Final**: como termina (punchline, preto, loop, CTA, corte seco) e quanto dura depois da última palavra.
12. **Linha do tempo**: tabela `t | visual | texto na tela | áudio | recurso`, granular nos momentos de edição (cada insert, zoom, efeito, troca de música, texto especial).
13. **Receita replicável**: regras objetivas com números ("legenda 2-3 palavras, branca, ativa amarela, centro em y=0,62, fonte ~7% da largura; insert meme em tela cheia 1,5-2,5 s a cada ~10 s; cama de funk slowed ~15 dB abaixo da voz").
14. **Para {{criador}}**: ideias concretas adaptadas ao nicho dele, na persona dele.

## Entrega

- `analise/<slug>/analise.md` para CADA vídeo, detalhado (números, tempos e nomes exatos valem ouro; é consultado depois por um editor).
- `analise/_grupo_<nome>.md`: padrões que se repetem, variações, receita consolidada, lista de memes e inserts, lista de trilhas e efeitos (com a confiança de cada um), e as 10 técnicas mais replicáveis.
- Português do Brasil.
- Resposta final para o orquestrador: até 30 linhas com os achados mais fortes e os caminhos.
