# 13. Conversa de Chat

**Também pedido como:** conversa de whatsapp, chat, mensagens, print de conversa animado.

## Assinatura visual

Uma **interface de aplicativo de mensagens genérica** em que **balões surgem em sequência**, com **"digitando..."**, rolagem da conversa e mensagens que ganham destaque. A assinatura é o **ritmo de leitura**: a pessoa lê a conversa acontecendo, mensagem por mensagem.

## Ideal quando

- A mensagem é uma **história curta em diálogo**: uma dúvida e a resposta, um cliente e o suporte, uma objeção e a resolução.
- Há um **roteiro de conversa** (ou mensagens reais **autorizadas**).
- Quer-se uma estética **orgânica e próxima**, que se confunde com o feed, sem pessoa na câmera.

## Evite quando

- A conversa seria **apresentada como real** sem ser: **conversa fictícia deve ser indicada como dramatização**. Não a apresente como depoimento.
- As mensagens reais **não foram autorizadas** nem anonimizadas: nunca exponha nome, número ou foto de uma pessoa real sem permissão.
- A mensagem precisa de rosto e emoção (prefira Depoimento).

## Composição (1080x1920)

| Elemento | Posição e tamanho |
|---|---|
| **Fundo** | cor de fundo de aplicativo de mensagens (clara ou escura), sem textura de marca |
| **Cabeçalho** | uma **faixa do contato** em y de 270 a ~400, **na mesma largura da conversa** (x de 90 a 960) e com os **cantos arredondados** (~32 px), sem encostar nas bordas da tela: avatar circular (inicial ou ícone), **nome do contato** inventado ou do anunciante, status ("online") |
| **Área da conversa** | y de ~450 a ~1240, dentro da zona segura; margem lateral de 90 px à esquerda e 120 px à direita |
| **Balões** | enviados à direita (cor de destaque), recebidos à esquerda (cor neutra); raio ~28 px; largura máxima ~70% da área; corpo do texto de **44 a 52 px**; horário pequeno em cada balão |
| **Indicador "digitando"** | três pontos animados num balão recebido, por 0,6 a 1,2 s antes de cada resposta |
| **Parte de baixo** | o espaço de y ≈ 1250 até a borda **fica livre de propósito**: é a zona em que a interface do app cobre a tela. Não ponha mensagem ali |
| **Aviso** | "Dramatização" (ou "Conversa encenada"), pequeno e legível, abaixo do cabeçalho ou no fim, dentro da zona segura |

## Elementos e animações

- **Entrada do balão:** `pop` curto (12 a 16 quadros, leve overshoot) e sobe da base da área da conversa.
- **Rolagem:** quando a conversa passa da área visível, o conjunto sobe suavemente (curva `out`, ~0,3 s).
- **Mídia na conversa:** imagem, áudio (forma de onda animada e duração), vídeo curto.
- **Destaque:** a mensagem-chave ganha um zoom discreto ou um realce de cor no instante em que é dita.
- **Sem logotipo, nome ou ícone de nenhum aplicativo real**, e sem "selo de verificado".

## Cortes e ritmo

- O tempo de cada mensagem **é o tempo de leitura**: 0,4 s + 0,3 s por palavra, mínimo 1 s, mais a pausa do "digitando".
- Evento novo (mensagem, mídia, destaque) a cada ~1,5 a 2,5 s. Não acelere além do que dá para ler.
- Se há narração por cima, as mensagens entram **na palavra** que as cita.

## Texto e legenda

- O texto é o das mensagens (ortografia do roteiro, sem corrigir o jeito de escrever da pessoa, a menos que ela peça).
- **Sem legenda da narração por cima do chat**, a não ser que a narração diga algo que não está nas mensagens.

## Som

- Som de notificação **discreto** na chegada de cada mensagem recebida (opcional); um clique suave nas enviadas.
- Música bem baixa ou nenhuma. Se há narração, ela vem na frente.

## Materiais

- **Peça:** o **roteiro da conversa** (quem diz o quê, na ordem) ou as mensagens reais **autorizadas**; imagens e áudios que entram na conversa; o nome do contato.
- **Pode buscar sozinho:** avatar genérico, ícones, sons de notificação, fonte, música.
- **Nunca invente:** a conversa como se fosse real, nome ou número de pessoas reais, "prints" de clientes, resultados na conversa que a pessoa não confirmou.

## Variações dentro do formato

- Tema claro e escuro; densidade (mensagens por tela).
- Quem fala primeiro; com e sem mídia; com e sem narração por cima.
- O ponto onde a mensagem-chave aparece (gancho no primeiro balão ou na virada).

## Armadilhas e checklist

- [ ] O aviso de **dramatização** está lá, legível, se a conversa é encenada.
- [ ] Nenhum nome, número ou foto de pessoa real sem autorização.
- [ ] Cada mensagem fica o tempo de ser lida.
- [ ] A rolagem não esconde a mensagem-chave.
- [ ] Não há logotipo ou selo de aplicativo real.

## Kit

Composição **`Chat`** (`kit/formatos/chat`). Props: `cores`, `fonte`, `duracaoS`, mais `contato` (`{ nome, status }`), `mensagens` (lista de `{ de: "eu" | "outro", texto, tempoS, imagem?, digitandoS? }`), `avisoDramatizacao`, `narracao` (áudio opcional) e `tema`.

## Apoio

Se a skill `creative-lab` estiver disponível, use a regra de gancho dela para a primeira mensagem; se a `motion-designer` estiver disponível, use as curvas e a estrutura dela.
