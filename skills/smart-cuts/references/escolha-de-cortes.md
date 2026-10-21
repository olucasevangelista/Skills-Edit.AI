# Escolher os cortes

## O que faz um bom corte

1. **Gancho nos primeiros 1 a 3 s:** frase que cria curiosidade, tensão, promessa, número ou contradição. O corte COMEÇA na frase-gancho, mesmo que no vídeo ela venha depois do contexto (dá para pôr um trecho posterior na frente se a fala continuar fazendo sentido; prefira a ordem original).
2. **Arco completo:** a ideia abre e fecha. Quem vê só o corte entende e sai com algo (resposta, número, punchline, conclusão).
3. **Valor, emoção ou humor:** explicação clara, história, opinião forte com argumento, resultado concreto, momento engraçado, erro ao vivo.
4. **Duração:** a que o usuário pediu. Sem pedido: sério 45 a 90 s, meme 15 a 60 s. Corte que só funciona com 3 min de contexto não é corte.
5. **Densidade:** depois de tirar pausas e loops, a fala corre. Muito "é... né... então..." vira cansativo; escolha outro trecho ou corte mais.

Sério ou meme: se a pessoa vira personagem (indignada, se gabando, zoando, errando ao vivo, bordão, exagero, contradição engraçada), é meme. Explicação densa, história, números e opinião com argumento são sérios. Um corte nunca mistura os dois estilos.

## Loops e devaneios saem

A pessoa abre um parêntese e volta ("...a melhor área para começar. Inclusive... [devaneio]... Como eu estava falando, o motivo é simples. Primeiro...") → corte do fim da frase anterior direto para a retomada ("...para começar. Primeiro..."). Também saem:

- frase repetida (a mesma frase dita duas vezes seguidas, ou o mesmo exemplo recontado);
- "beleza? tá bom?" soltos, pergunta ao chat sem resposta, tangente, "deixa eu ver aqui", leitura de comentário fora do assunto.

Cuidados: a costura tem que soar natural (mesma entonação, mesma ideia). Não junte duas frases que mudam o sentido do que foi dito. Não tire a palavra que conecta ("então", "só que") se a frase seguinte depende dela. Leia o texto final que o `planejar_cortes.py` imprime.

## Compilação (vários trechos ou vários vídeos)

Quando o mesmo tema aparece em momentos diferentes (ou em vídeos diferentes), um corte pode juntar 2 a 5 trechos com a fala fluindo ("as 3 vezes que ele falou de custo", "a evolução da opinião dela sobre um assunto"). Cada trecho tem que se sustentar e a transição tem que fazer sentido. Para trechos de vídeos diferentes, use `fontes` no `cortes.json` (`plano.md`). Se os vídeos têm tamanhos diferentes, o corte usa o tamanho do primeiro e os outros entram inteiros, com barras. O plano pode marcar a passagem de um vídeo para o outro com um flash ou separador, que será feito no Remotion.

## Quantos e como apresentar

Padrão sem pedido explícito: leia tudo, levante TODOS os bons candidatos e recomende os melhores. Referência: um vídeo de 30 a 60 min costuma render 6 a 9 cortes, uns dois terços sérios e um terço memes, mas a qualidade manda; conteúdo fraco rende menos. No checkpoint mostre a tabela com id, estilo, gancho, duração e o porquê em uma linha, e deixe o usuário escolher.

## Ganchos

- Curto, concreto, com tensão: número, contradição, promessa, pergunta, choque.
- Em CAIXA ALTA, até ~8 palavras, na voz da pessoa. Sem clickbait que o corte não entrega.
- Sério: afirmação forte ou paradoxo ("PAREI DE USAR PLANILHA EM UMA SEMANA", "NÃO PRECISA SABER PROGRAMAR").
- Meme: narrador em terceira pessoa zoando a pessoa, com a gíria viva dela ("FULANO QUEIMANDO DINHEIRO NA LIVE"). Use o apelido que a própria pessoa usa; se não souber, pergunte. Não invente apelido.
- Nada de palavra que a pessoa não usaria.

## Como o plano chama cada corte

`id` curto, minúsculo, sem espaço: prefixo do vídeo + tema (`aula1_planilha`, `live3_custo`). O id vira o nome do arquivo.
