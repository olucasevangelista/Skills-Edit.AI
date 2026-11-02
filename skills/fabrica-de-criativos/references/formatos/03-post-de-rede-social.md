# 03. Post de Rede Social

**Também pedido como:** choquei, post de rede social, estilo post de notícia no X, print de publicação animado.

## Assinatura visual

Um **cartão de perfil no topo** (fundo branco, **avatar redondo e nome do perfil**) com a **frase de impacto escrita embaixo**, e a **mídia ocupando o resto da tela**: **um vídeo**, **dois vídeos lado a lado** ou **um vídeo e uma imagem**, conforme o assunto. A assinatura é a **manchete como publicação**: o texto de cima diz o que o vídeo de baixo vai mostrar.

## Ideal quando

- O gancho é uma **frase forte ou uma manchete** (uma afirmação, um dado, uma polêmica do nicho) que cabe em um texto curto.
- Há uma **imagem de destaque** que ilustra o post.
- Quer-se uma estética **orgânica**, de quem comenta o assunto do momento.

## Evite quando

- O "post" **simularia uma publicação de uma pessoa ou de um veículo real**, ou atribuiria um endosso a um perfil existente.
- A manchete afirmaria como **fato** algo que não é (uma "notícia" ou "pesquisa" inventada).
- Não há uma frase de impacto: o cartão fica vazio.

## Composição (1080x1920)

| Elemento | Posição e tamanho |
|---|---|
| **Cartão do perfil** | do **topo da tela** até y ≈ 600 a 700 (a altura segue o texto), fundo branco (ou escuro), sombra suave; **o texto e o avatar ficam dentro da zona segura** (o avatar começa em y ≈ 290; o branco acima é só fundo) |
| **Avatar e nome** | avatar redondo de ~92 px com o logo da **Choquei** (marca pronta do kit) ou o **logo do SEU perfil** (ou a letra sobre a cor da marca), nome em caixa alta e negrito, corpo ~46 px, x ≥ 90 |
| **Texto do post** | até **4 linhas**, corpo ~46 px, largura entre x = 90 e x = 960 |
| **Mídia, um vídeo** | de baixo do cartão até o fim da tela, em largura total |
| **Mídia, dois** | duas colunas de ~537 px, com uma linha preta de ~6 px no meio; vale **vídeo e vídeo** ou **vídeo e imagem** (o áudio de só um) |
| **Legenda** (se houver) | y ≈ 1000 a 1100, nunca na base |

(Em um formato horizontal 16:9, o cartão fica à esquerda e a mídia à direita.)

## Elementos e animações

- O cartão **já está na tela desde o primeiro quadro**: a frase de impacto precisa ser lida no gancho. Se quiser entrada, use um deslize curto (até 0,3 s).
- **Destaque** na palavra-chave (cor ou realce) no instante em que a fala a diz.
- **Sem números de curtidas, comentários ou compartilhamentos inventados** (isso seria prova social fabricada): ou não há linha de métricas, ou há só ícones.
- **Sem logotipo de rede social e sem selo de verificado.** O nome e o logo da **Choquei** vêm prontos no kit (`MARCA_CHOQUEI`, arquivo em `assets/marcas/choquei.png`) porque o autor da skill informou que a página tolera esse uso. **Isso não foi verificado e não é uma licença**: quem usa responde por isso, e o anúncio **nunca** deve dizer ou sugerir que a página endossa ou publicou o conteúdo. Para qualquer outro perfil, use o **seu** (`marca` própria).

## Cortes e ritmo

- O cartão fica **2 a 4 s**; depois o vídeo ganha a tela. Emenda com **sobreposição** (`cortes.md`).
- Evento novo a cada ~2 s; o cartão pode voltar (um segundo post, uma imagem nova) como evento.

## Texto e legenda

- O texto do post é a **manchete**: curto, direto, verdadeiro.
- Legenda palavra a palavra do vídeo abaixo do cartão, sem cobrir a boca.

## Som

- Voz em primeiro plano; um efeito curto na entrada do cartão (opcional); música baixa opcional.

## Materiais

- **Peça:** o vídeo principal, a **frase do post** e a **imagem de destaque**; o **nome do perfil** que a pessoa quer usar (o dela ou o da marca).
- **Pode buscar sozinho:** avatar genérico, ícones, a imagem de destaque de uma fonte com licença clara (se a pessoa não tiver), fonte, música.
- **Nunca invente:** uma publicação como se fosse de uma pessoa ou veículo real, métricas, comentários, notícias ou "estudos" que não existem.

## Variações dentro do formato

- Uma mídia, duas lado a lado, ou vídeo e imagem; cartão claro ou escuro.
- Texto do post (o ângulo da manchete); com e sem legenda.
- Quanto tempo a frase fica (ela pode ser trocada no meio por outra).

## Armadilhas e checklist

- [ ] A marca do cartão é a **Choquei pronta do kit** (uso por conta de quem anuncia) ou um perfil **próprio**; nenhum outro perfil real, nenhum selo de verificado.
- [ ] A manchete é **verdadeira** e o anúncio a sustenta.
- [ ] Não há métrica de engajamento inventada.
- [ ] O texto cabe em até 4 linhas e é legível; o cartão está dentro das margens.
- [ ] Um aviso de **publicidade** foi considerado e a pessoa conferiu a política da plataforma.

## Kit

Composição **`PostSocial`** (`kit/formatos/post-social`): o cartão já pronto, **basta trocar a marca, o texto e as mídias**. Props: `marca` (`{ nome, letra, cor, logo }`, o seu perfil; o `logo` é um arquivo em `public/`), `texto`, `midia` (uma ou duas, `{ src, audio, origem, escala, fit }`), `fundoCartao` (`claro` ou `escuro`), `alturaCartao` (opcional; por padrão segue o tamanho do texto), `legendas`, `cores`, `fonte`, `duracaoS`. Sem `logo`, o avatar é a letra sobre a cor da marca. Em `kit/marcas.ts`: `MARCA_CHOQUEI` (padrão do exemplo) e `MARCA_NOTICIA`.

## Apoio

Se a skill `creative-lab` estiver disponível, use as regras de gancho e a `conformidade.md` dela; se a `copystyle` estiver disponível, use-a para medir uma referência do formato.
