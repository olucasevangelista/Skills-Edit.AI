# 10. Corte de Podcast

**Também pedido como:** corte de podcast, corte de entrevista, trecho de podcast, clipe de conversa.

## Assinatura visual

Um **trecho de podcast ou entrevista** em formato vertical, **sempre com o rosto de quem está falando em foco**. É um formato mais de **gravação** do que de **edição**: o trabalho principal é escolher o trecho, **enquadrar** e **legendar**. Dependendo do momento, a tela mostra **todos os participantes juntos** (dois, três ou quatro) ou o **participante que está falando**, e o corte acompanha isso.

## Ideal quando

- Existe uma **gravação de podcast ou entrevista** com um momento forte (uma resposta que resolve uma objeção, um insight, um resultado contado, uma opinião).
- O trecho **se sustenta sozinho**, com um começo e um fim.
- O contexto **precisa ser preservado** (uma pergunta e a resposta).

## Evite quando

- O trecho depende de **muito contexto** que o anúncio não dá.
- A gravação tem **um só ângulo e baixa qualidade** (rosto pequeno, som ruim): o recorte vertical piora.
- O **conteúdo é de terceiros** (um convidado ou outro programa) sem autorização para anúncio.

## Composição (pontos de partida, 1080x1920)

**Regra do formato: o rosto de quem fala está sempre na tela.** As estruturas:

- **A. Tela cheia em quem fala:** o recorte vertical 9:16 do **rosto do falante**, com troca de pessoa a cada fala. Olhos no terço superior, cabeça inteira, centro do rosto em y ≈ 700 a 950.
- **B. Todos juntos:** a tela mostra os participantes (dois, três ou quatro) em quadros empilhados ou em grade, com destaque em quem fala. Bom para trechos com troca rápida.
- **C. Mistura dos dois:** começa nos participantes juntos e vai até quem fala, e volta.

| Elemento | Como pensar |
|---|---|
| **Legenda** | é o principal acabamento do formato: palavra a palavra, abaixo do meio da tela, nunca na base |
| **Tarja de nome** (opcional) | y ≈ 330 a 420, **só com nomes autorizados** |

**Reenquadramento é manual.** O Remotion não detecta rosto. Para cada pessoa, tire um quadro (`ffmpeg -ss <t> -i podcast.mp4 -frames:v 1 q.png`), meça o centro do rosto e a altura da cabeça, e aplique como `objectPosition` e escala (ou `crop`) no recorte.

**Depois de enquadrado e legendado, pode misturar** com outros modos e formatos: ilustrações ou motion, uma tela inteira coberta por um desenho que explica o que o participante diz (a linha do formato Professor), tela dividida, inserts.

## Elementos e animações

- **Troca de enquadramento** em cada fala, com **sobreposição** (`cortes.md`): a imagem e o áudio de quem entra chegam juntos, antes de o outro terminar.
- **Zoom** de ênfase (1,12 a 1,2) nas frases ★, com retorno ao neutro; alternar 1,0 e ~1,07 nos cortes de jump.
- **Destaque de frase:** uma frase importante aparece em texto grande por 1 a 2 s.
- **Inserts** de apoio (imagem, print, número) entrando **na palavra** que os cita.

## Cortes e ritmo

- **Preserve o contexto:** inclua a pergunta que dá sentido à resposta; não corte uma fala no meio de uma ideia nem mude o sentido.
- **Remova** pausas longas, reinícios e "é..." isolados; **mantenha** a pausa que dá peso a uma frase. Quem limpa é o `limpar-a-fala.md` (estilo `curto` ou `aula`).
- Evento novo (troca, zoom, insert, texto) a cada **~2 a 2,5 s**; marco grande a cada ~6 a 8 s.

## Texto e legenda

- Legenda dinâmica palavra a palavra, com realce nos ★; atribuição de **quem fala** só com o que foi autorizado.
- Gancho em texto nos primeiros 3 s, complementando a fala.

## Som

- Falas **niveladas** entre os participantes; ruído de sala reduzido; música **bem abaixo** da voz ou nenhuma; efeito curto só em marcos.

## Materiais

- **Peça:** a **gravação do podcast ou da entrevista** (de preferência com uma câmera por pessoa) e a **autorização** de uso da imagem e da fala dos participantes em anúncio.
- **Pode buscar sozinho:** imagens de apoio, ícones, música, a fonte.
- **Nunca invente:** falas, perguntas, atribuições de frase a quem não disse, nomes de convidados.

## Variações dentro do formato

- Modo A (tela cheia) ou B (empilhado).
- Quais frases são ★ (e recebem destaque e zoom).
- O trecho: outra resposta do mesmo episódio com o mesmo formato.

## Armadilhas e checklist

- [ ] O trecho tem começo e fim e **se sustenta sem o resto do episódio**.
- [ ] O **sentido** das falas não foi alterado pelos cortes.
- [ ] O rosto de quem fala está inteiro e no terço superior; a troca acompanha a fala.
- [ ] **Autorização** de todos os participantes.
- [ ] A legenda está certa nos nomes e termos.

## Estruturas e exemplos

Sem quadro de exemplo (o autor disse que não é preciso: o formato é de gravação). Resumo: o rosto de quem fala sempre aparece; ora todos os participantes, ora só quem fala; o acabamento principal é a legenda; depois pode misturar motion, ilustração em tela cheia (como no formato Professor), tela dividida e inserts.

## Apoio

Se a skill `smart-cuts` estiver disponível, **use-a**: ela escolhe os trechos, tira os loops, emenda com sobreposição e entrega os cortes com o enquadramento medido; a partir dela, monte o visual. Se não, siga `cortes.md` e o reenquadramento manual acima.
