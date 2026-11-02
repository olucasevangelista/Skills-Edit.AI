---
name: fabrica-de-criativos
description: Fábrica de Criativos - 15 formatos de edição de anúncio em vídeo para aplicar com IA em minutos e fazer variações de criativo, com tela dividida, fundo verde (recorte), post de rede social, notícia, professor (explicação visual), motion design, depoimento, react, videochamada, corte de podcast, telejornal, tutorial de tela, conversa de chat, antes e depois e cinema. A pessoa escolhe o formato (ou pede ajuda para escolher) e manda o material; a skill monta a edição no Remotion, com um kit de composições para os formatos principais, emenda de cortes com sobreposição, legenda, zonas seguras e prova honesta. Use sempre que pedirem para editar um criativo ou anúncio em um desses formatos, fazer versões ou variações, ou o mesmo vídeo em vários formatos, ou citarem estilo choquei, jornal nacional, meet, whatsapp ou react. Os scripts usam FFmpeg e Python.
---

# Fábrica de Criativos

15 formatos de edição para anúncios em vídeo, executados com IA. A pessoa escolhe o formato, manda o material e orienta a edição; você constrói a composição, os cortes, as animações e o ritmo **característicos do formato escolhido**, e pode refazer o mesmo material em **outros formatos** para gerar variações.

O foco é **automatizar a edição** e a **variação**, não ensinar a gravar anúncios. Cada formato tem uma **assinatura visual própria**: não os trate como variações do mesmo layout.

`<skill>` abaixo é a pasta onde esta skill está instalada. O kit Remotion (`kit/`) é **opcional**: pergunte à pessoa se quer usá-lo ou se prefere montar do zero.

## Receita rápida

- **Formato primeiro.** Escolha (ou recomende) um dos 15 e abra **só o arquivo dele** em `references/formatos/`. Os arquivos de `references/base/` valem para todos.
- **Cortes:** emenda com sobreposição, sem respiro e sem áudio cortado seco: o próximo take entra colado na voz, **imagem e áudio juntos**, antes de a fala anterior acabar (~0,1 a 0,25 s).
- **Ritmo:** evento visual novo nos primeiros 5 s a cada ~1 a 1,5 s; depois, no máximo a cada ~2,5 s (cada formato diz as exceções).
- **Legenda sempre** (palavra a palavra, com realce nos ★), fora da base; texto e rosto dentro das zonas seguras (topo ~270 px, base ~670 px, laterais ~90 px; confirme na plataforma).
- **Materiais são uma solicitação, não uma exigência**: peça, mas siga com o que existe e **busque sozinho** o que ajudar (música, imagens de apoio), registrando a origem (`base/materiais.md`).
- **Honestidade:** nunca invente depoimento, resultado, antes e depois, notícia, conversa ou participante como se fosse real (`base/honestidade.md`).

## Pergunte primeiro (até 4 perguntas curtas, de uma vez)

1. **Qual formato?** Ou "me ajuda a escolher": descreva o material e eu recomendo.
2. **Que material já existe?** Vídeo bruto, imagens, áudio, roteiro, gravação de tela, depoimento, conversa.
3. **Plataforma, duração e identidade:** cores, fonte, nome da marca ou do perfil.
4. **Quantas variações** e em quais formatos (se a pessoa quer testar).

Se o pedido for vago, **não bloqueie**: faça as perguntas e siga com padrões que você declara em uma linha.

## Os 15 formatos

Abra o arquivo do formato escolhido. **Kit** marca os que têm composição pronta em `kit/formatos/`.

| # | Formato | Ideal quando | Evite quando | Material mínimo | Arquivo |
|---|---|---|---|---|---|
| 01 | **Tela Dividida** (kit) | há algo para mostrar enquanto a pessoa fala (tela, produto, prova) | não há nada para mostrar em cima | vídeo da pessoa + imagens ou vídeos de apoio | `01-tela-dividida.md` |
| 02 | **Fundo Verde** (recorte) | a pessoa fala de algo que cabe atrás dela (página, dado, produto) | o recorte da pessoa não fica limpo | vídeo da pessoa + materiais de fundo | `02-fundo-verde.md` |
| 03 | **Post de Rede Social** (kit) | o gancho é uma manchete ou frase de impacto verdadeira | o post imitaria um perfil real ou afirmaria o que não é fato | vídeo + frase do post + imagem | `03-post-de-rede-social.md` |
| 04 | **Notícia** (kit) | há um fato, dado ou novidade **verdadeiros** do nicho | a "notícia" seria inventada ou imitaria um veículo | vídeo + manchete + apoio real | `04-noticia.md` |
| 05 | **Professor** (explicação visual) | há um conceito ou processo para explicar | não há o que desenhar ou faltam dados | vídeo explicando + dados reais | `05-professor.md` |
| 06 | **Motion Design** | não há pessoa para gravar ou o produto é abstrato | o anúncio precisa de prova humana | narração ou roteiro + identidade | `06-motion-design.md` |
| 07 | **Depoimento** (kit) | existe um relato **real** de cliente, com provas | não há depoimento real ou autorização | gravação real + provas + autorização | `07-depoimento.md` |
| 08 | **React** (kit) | a pessoa vai comentar ou rebater um conteúdo | o conteúdo é de terceiro sem direito de uso | conteúdo comentado + gravação da reação | `08-react.md` |
| 09 | **Videochamada** | há uma conversa **gravada de verdade** | seria encenação passada como real | gravação da conversa + autorização | `09-videochamada.md` |
| 10 | **Corte de Podcast** | há um trecho forte que se sustenta sozinho | depende de muito contexto ou não há autorização | gravação do podcast ou entrevista | `10-corte-de-podcast.md` |
| 11 | **Telejornal** | quer autoridade formal sobre um fato **verdadeiro** | simularia um telejornal real ou uma notícia inventada | vídeo do apresentador + roteiro + apoio | `11-telejornal.md` |
| 12 | **Tutorial de Tela** | é software ou app e o fluxo cabe na tela | a tela tem dados sensíveis ou é longa demais | gravação de tela + narração | `12-tutorial-de-tela.md` |
| 13 | **Conversa de Chat** (kit) | a mensagem é uma história curta em diálogo | a conversa seria apresentada como real sem ser | roteiro da conversa ou mensagens autorizadas | `13-conversa-de-chat.md` |
| 14 | **Antes e Depois** (kit) | há duas situações **reais** comparáveis | só existe uma delas ou o assunto é sensível sem prova | as duas situações, reais | `14-antes-e-depois.md` |
| 15 | **Cinema** (kit) | o vídeo é emocional e pede peso e respiro | a resposta direta precisa de ritmo apertado | vídeo principal + música | `15-cinema.md` |

### Como escolher quando a pessoa não sabe

| Situação | Recomende |
|---|---|
| Pessoa falando para a câmera e provas para mostrar | Tela Dividida, Depoimento ou Cinema |
| Só tem gravação de tela | Tutorial de Tela |
| Tem uma conversa ou podcast gravado | Corte de Podcast ou Videochamada |
| Só tem narração ou roteiro, sem imagem | Motion Design ou Conversa de Chat |
| Tem duas situações reais para comparar | Antes e Depois |
| Quer comentar um conteúdo | React |
| Tem uma manchete forte e **verdadeira** | Post de Rede Social, Notícia ou Telejornal |
| Quer emoção e marca premium | Cinema |
| Quer explicar um conceito | Professor |
| Quer a pessoa na frente do conteúdo | Fundo Verde |

Dê **a recomendação e o motivo em uma linha**; se a pessoa quer testar, sugira **3 a 5 formatos de assinatura diferente** que o material permita.

## Fluxo

1. Faça as perguntas e escolha o formato.
2. Transcreva a fala com tempo por palavra, marque ★ / normal / baixa e monte a **tabela de eventos** (`base/fluxo.md`).
3. Monte: com o **kit** (troque os props da composição do formato) ou do zero, seguindo o arquivo do formato.
4. **Prévia** antes do render; exporte o final quando a pessoa pedir.
5. **Verifique** (`scripts/verificar_saida.py`, quadros, checklist do formato) e entregue com o `MATERIAIS.md`.

## Apoio de outras skills

Se estiverem disponíveis, use-as; se não estiverem, **siga o procedimento embutido** em `references/base/` e no arquivo do formato.

| Tarefa | Skill, se disponível |
|---|---|
| Transcrever com tempo por palavra | `transcrever-groq` |
| Escolher trechos, tirar loops e emendar | `smart-cuts` |
| Motion e animações explicativas | `motion-designer` |
| Regras de gancho, retenção, resultado, mecanismo e conformidade de anúncio | `creative-lab` |
| Medir uma referência de estilo | `copystyle` |
| Entender por que um criativo funciona | `raio-x-criativos` |
| Criar e exportar no Remotion | a skill do Remotion |

**Regra:** **nunca diga ao usuário que uma skill não está instalada, nem que está usando um plano B.** Faça o trabalho com o que tem, sem comentar a ausência.

## Variações

O mesmo material em vários formatos, ou o mesmo corpo com vários ganchos: **uma variável por vez**, mesmo volume, matriz do teste (`base/variacoes.md`).

## Entrega (curta de propósito)

- Perguntas e suposições: até 5 linhas.
- O plano em tabela (`Início (s) | Evento | Fala`).
- Verificação: até 3 linhas, com o que **não** foi verificado.
- O arquivo, o `MATERIAIS.md` e o que a pessoa precisa **confirmar** (direitos, autorização, políticas da plataforma).

## Referências (abra só o que precisar)

- `references/formatos/NN-*.md`: o formato escolhido.
- `references/base/fluxo.md`: do material ao arquivo final.
- `references/base/cortes.md`: emenda com sobreposição, pausas e ritmo.
- `references/base/legenda-e-zonas.md`: legenda, texto, inserts, zonas seguras.
- `references/base/materiais.md`: o que pedir e o que buscar, e como registrar.
- `references/base/honestidade.md`: prova real, dramatização, formatos que imitam uma linguagem.
- `references/base/variacoes.md`: variações e teste.
- `references/base/revisao.md`: revisão e checklist de saída.
- `kit/README.md`: o kit Remotion (componentes e as composições dos formatos).
- `scripts/verificar_saida.py`: mede o arquivo final. `scripts/recortar_pessoa.py`: recorta a pessoa de qualquer fundo (formatos 02 e 05). `scripts/instalar_kit.py`: instala o kit (código, fontes e marcas) num projeto Remotion.

Os números (zonas, ritmo, medidas de composição) são **pontos de partida**: se a referência da pessoa pede outro, siga a referência. **Nenhuma recomendação aqui foi medida em desempenho de anúncio.**
