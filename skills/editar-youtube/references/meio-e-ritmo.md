# O meio do vídeo: ritmo, tipo de vídeo e momentos-chave

Depois da abertura, o que manda é **o estilo de edição da pessoa e o tipo do vídeo**. Não há fórmula. Pergunte pelas referências ou olhe os vídeos anteriores dela; na falta disso, comece simples e declare o que assumiu.

## Por tipo de vídeo

**Só a pessoa falando.** É onde entram, de vez em quando, motion designs, inserts (imagem, print, ícone), textos em destaque e zoom, para dar ritmo, **quando fazem sentido** e no estilo dela. Um motion deve ter função: ilustrar uma ideia, mostrar uma prova, marcar uma virada. Enfeite sem função cansa.

**Gravação de tela.** A tela é o conteúdo; enquanto a pessoa mostra, clica ou digita, não entra nada por cima dela. Motion só quando a explicação é **conceitual ou técnica e a pessoa não está desenhando na tela**: por exemplo, ela explica a arquitetura de vários servidores com só o terminal aberto. Aí o motion mostra a ideia (isso se liga àquilo) enquanto a narração segue, e depois a imagem volta para a tela. Detalhes em `tipos-de-video.md`.

**Motion no corpo.** O ritmo vem da troca de cenas e elementos acompanhando a fala: cada animação entra na palavra que ilustra (±0,1 s).

**Mistura.** Trate cada trecho pela regra do seu tipo.

### Quanto de novidade visual

Sem número fixo: o estilo da pessoa manda. Se ela não tem referência, um ponto de partida (**não medido**) é uma mudança visual a cada ~10 s no meio do vídeo (zoom, insert, texto, motion, troca de enquadramento), mais denso na abertura e nos momentos-chave, e **nenhum trecho longo de imagem parada sem nada novo**. Dinâmico não é frenético: vídeo longo precisa respirar onde a ideia pede (uma explicação mais calma pode usar o estilo de corte `aula`; veja `limpeza.md`).

## Momentos-chave

São os pontos em que o vídeo vira: a abertura, uma virada de assunto, a **demonstração principal**, a **revelação** do que foi prometido e o final. Ali:

- **A emenda com sobreposição é decisiva:** faça-a com cuidado (a sobreposição inteira, imagem e áudio entrando juntos) e **combine com uma mudança visual** (zoom, troca de plano, elemento novo), para o corte parecer escolhido e dar energia.
- Dê um destaque proporcional (texto, zoom, som) para o espectador sentir que algo importante começou.

## A emenda com sobreposição (em todo corte)

Em todo corte da fala, o próximo take entra **colado no começo da voz**, sem respiro, e começa ainda durante o finalzinho do anterior: **imagem e áudio novos entram juntos** (~0,1 a 0,25 s de sobreposição; as vozes se sobrepõem de propósito por esse instante). Nunca só a imagem, nunca só o áudio, nunca corte seco.

- **Dentro de um mesmo arquivo:** o `montar.py` aplica isso em todas as emendas (`limpeza.md`).
- **Entre arquivos diferentes** (a pessoa e a gravação de tela, duas partes gravadas em dias diferentes): use a emenda do `limpeza.md`, seção "Casos".
- **Entre um tipo de cena e outro** (rosto, tela, motion) com a narração contínua, o áudio já é contínuo; o corte de imagem cai na palavra que o motiva.

## O final

Normalmente o final tem a pessoa em tela cheia. Se fizer sentido, dê a esse trecho um destaque: um motion, um texto, um zoom. É também onde cai o último lembrete para seguir (`chamadas-para-seguir.md`). Termine sem cauda depois da última fala.

## Zoom e texto

- Todo zoom volta ao tamanho normal; zoom que só aumenta aperta o enquadramento e corta a cabeça.
- Texto na tela tem tempo de leitura (0,4 s + 0,3 s por palavra, mínimo 1 s) e não cobre rosto nem o conteúdo da tela.
- Legenda só se o estilo da pessoa usa.
