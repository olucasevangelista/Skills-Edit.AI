---
name: fabrica-de-criativos
description: Fábrica de Criativos - guia de edição de criativos de anúncio em vídeo em 16 formatos (tela dividida, fundo verde, post de rede social, notícia, professor, motion design, depoimento, react, videochamada, corte de podcast, telejornal, tutorial de tela, conversa de chat, antes e depois, cinema e caixinha de pergunta). Dá direção, estruturas possíveis e exemplos para você editar no Remotion, misturando formatos e adaptando à oferta, à narrativa e à marca. Use sempre que pedirem para editar um criativo ou anúncio em um desses formatos, fazer versões ou variações, ou o mesmo vídeo em vários formatos, ou citarem estilo choquei, jornal nacional, meet, whatsapp ou react. Também limpa a gravação falada antes da montagem - tira silêncios, erros e takes repetidos escolhendo o melhor, com emenda por sobreposição - e serve para pedidos como tirar os silêncios. Os scripts usam FFmpeg e Python.
---

# Fábrica de Criativos

Um **guia** para editar criativos de anúncio em vídeo, em vários formatos, com IA. A pessoa escolhe o formato (ou pede ajuda), manda o material e orienta; **você edita tudo no Remotion**, com a skill do Remotion. Esta skill dá o conhecimento (o que cada formato é, que estruturas existem, o que importa num bom criativo, exemplos reais) e os arquivos de apoio; **não traz template nem script que edite por você**, justamente para não limitar o seu trabalho. As únicas peças de código são **componentes avulsos para reaproveitar** (`assets/componentes/`: a caixinha de pergunta, a manchete de notícia, o cenário e o título de telejornal, e a emenda com sobreposição), que você copia e adapta. Elas não decidem estilo nem formato.

`<skill>` abaixo é a pasta onde esta skill está instalada.

## Princípios

1. **É direção, não molde.** Os formatos, as medidas e as estruturas são **pontos de partida e opções**. Se a oferta, a narrativa ou o estilo da pessoa pede outra coisa, faça outra coisa.
2. **Misturar é uma opção.** Um vídeo pode seguir **um formato do começo ao fim** (um post de rede social ou uma caixinha de pergunta pode ser o vídeo inteiro, orgânico, com só o cartão em cima, os cortes e a legenda) ou **combinar** formatos e modos (gancho num, corpo em outros, ilustração em tela cheia). O estilo visual (motion moderno, recortes de papel, stop motion) também é da pessoa. Veja `references/base/mistura-de-formatos.md`.
3. **Adapte, não copie.** Os exemplos (`references/exemplos/`) mostram estrutura e ritmo. As cores, as fontes e o desenho dos elementos neles são do autor dos exemplos, **não do formato**: use a identidade da pessoa e **nunca sugira uma cor** só porque ela aparece num exemplo.
4. **Os elementos nascem da fala.** Textos, selos e ilustrações entram na palavra que os citam. Trocar de modo é uma escolha, não uma regra.
5. **Valide com a pessoa.** Ao construir um formato ou uma mistura que ela ainda não viu, **gere um exemplo curto** (um quadro, ou um trecho em baixa resolução, só com o vídeo e também com a parte estática) e **peça a opinião dela antes de seguir**. Se tiver dúvida, pergunte.
6. **Honestidade.** Nunca invente depoimento, resultado, antes e depois, notícia, conversa ou participante como se fosse real (`references/base/honestidade.md`).

## Receita rápida

- **Formato primeiro** (ou mistura): abra o arquivo dele em `references/formatos/`. Os arquivos de `references/base/` valem para todos.
- **Limpe a fala primeiro** (`references/base/limpar-a-fala.md`): escolha a melhor tentativa entre as repetições e tire erros e silêncios com os scripts, que medem o áudio. Entre uma frase e outra sobra no máximo ~0,1 s: **silêncio de 0,5 a 1 s que sobrou é defeito**. Depois transcreva o `limpo.mp4` e monte o formato em cima.
- **Cortes:** emenda com sobreposição, sem respiro e sem áudio cortado seco: o próximo take entra colado na voz, **imagem e áudio juntos**, antes de a fala anterior acabar (~0,1 a 0,25 s).
- **Ritmo:** evento visual novo nos primeiros 5 s a cada ~1 a 1,5 s; depois, no máximo a cada ~2,5 s (cada formato diz as exceções).
- **Legenda** simples e constante, fora da base; texto e rosto dentro das zonas seguras (topo ~270 px, base ~670 px, laterais ~90 px; confirme na plataforma).
- **Materiais são uma solicitação, não uma exigência**: peça, mas siga com o que existe e **busque sozinho** o que ajudar (música, imagens de apoio), registrando a origem (`base/materiais.md`).
- **Prévias leves:** quadros e vídeos de baixa resolução (`--scale=0.5`, um processo só) antes do render final, para não pesar a máquina da pessoa.

## Pergunte primeiro (até 4 perguntas curtas, de uma vez)

1. **Qual formato (ou mistura)?** Ou "me ajuda a escolher": descreva o material e eu recomendo.
2. **Que material já existe?** Vídeo bruto, imagens, áudio, roteiro, gravação de tela, depoimento, conversa.
3. **Plataforma, duração e identidade:** cores, fonte, nome da marca ou do perfil (**as dela**).
4. **Quantas variações** e em quais formatos (se a pessoa quer testar).

Se o pedido for vago, **não bloqueie**: faça as perguntas e siga com padrões que você declara em uma linha.

## Os formatos

Abra o arquivo do formato escolhido. Cada um traz a assinatura visual, quando usar, as **estruturas possíveis**, o que evitar e o checklist.

| # | Formato | Ideal quando | Evite quando | Material mínimo | Arquivo |
|---|---|---|---|---|---|
| 01 | **Tela Dividida** | há algo para mostrar enquanto a pessoa fala (tela, produto, prova) | não há nada para mostrar | vídeo da pessoa + imagens ou vídeos de apoio | `01-tela-dividida.md` |
| 02 | **Fundo Verde** (recorte) | a pessoa fala de algo que cabe atrás dela (página, dado, produto) | o recorte da pessoa não fica limpo | vídeo da pessoa + materiais de fundo | `02-fundo-verde.md` |
| 03 | **Post de Rede Social** | o gancho é uma manchete ou frase de impacto verdadeira | o post imitaria um perfil real ou afirmaria o que não é fato | vídeo + frase do post (+ imagem ou oferta) | `03-post-de-rede-social.md` |
| 04 | **Notícia** | há um fato, dado ou novidade **verdadeiros** do nicho | a "notícia" seria inventada ou imitaria um veículo | vídeo + manchete + apoio real | `04-noticia.md` |
| 05 | **Professor** (explicação visual) | há um conceito ou processo para explicar | não há o que desenhar ou faltam dados | vídeo explicando + dados reais | `05-professor.md` |
| 06 | **Motion Design** | não há pessoa para gravar ou o produto é abstrato | o anúncio precisa de prova humana | narração ou roteiro + identidade | `06-motion-design.md` |
| 07 | **Depoimento** | existe um relato **real** de cliente, com provas | não há depoimento real ou autorização | gravação real + provas + autorização | `07-depoimento.md` |
| 08 | **React** | a pessoa vai comentar ou rebater um conteúdo | o conteúdo é de terceiro sem direito de uso | conteúdo comentado + gravação da reação | `08-react.md` |
| 09 | **Videochamada** | há uma conversa **gravada de verdade** | seria encenação passada como real | gravação da conversa + autorização | `09-videochamada.md` |
| 10 | **Corte de Podcast** | há um trecho forte que se sustenta sozinho | depende de muito contexto ou não há autorização | gravação do podcast ou entrevista | `10-corte-de-podcast.md` |
| 11 | **Telejornal** | quer autoridade formal sobre um fato **verdadeiro** | simularia um telejornal real ou uma notícia inventada | vídeo do apresentador + roteiro + apoio | `11-telejornal.md` |
| 12 | **Tutorial de Tela** | é software ou app e o fluxo cabe na tela | a tela tem dados sensíveis ou é longa demais | gravação de tela + narração | `12-tutorial-de-tela.md` |
| 13 | **Conversa de Chat** | a mensagem é uma história curta em diálogo | a conversa seria apresentada como real sem ser | roteiro da conversa ou mensagens autorizadas | `13-conversa-de-chat.md` |
| 14 | **Antes e Depois** | há duas situações **reais** comparáveis | só existe uma delas ou o assunto é sensível sem prova | as duas situações, reais | `14-antes-e-depois.md` |
| 15 | **Cinema** | o vídeo é emocional e pede peso e respiro | a resposta direta precisa de ritmo apertado | vídeo principal + música | `15-cinema.md` |
| 16 | **Caixinha de Pergunta** | o gancho é uma dúvida ou objeção que a pessoa responde | a pergunta seria atribuída a alguém real sem ser verdade | vídeo da pessoa + a pergunta | `16-caixinha-de-pergunta.md` |

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
| Quer um gancho com cara de conteúdo orgânico | Caixinha de Pergunta ou Post de Rede Social |

Dê **a recomendação e o motivo em uma linha**; se a pessoa quer testar, sugira **3 a 5 formatos (ou misturas) de assinatura diferente** que o material permita.

## Fluxo

1. Faça as perguntas e escolha o formato ou a mistura.
2. Transcreva a fala com tempo por palavra, marque ★ / normal / baixa e monte a **tabela de eventos** (`base/fluxo.md`).
3. **Monte no Remotion**, seguindo o arquivo do formato (estruturas possíveis, composição, animações) e adaptando.
4. **Mostre uma prévia** leve e, se o formato ou a mistura for novo para a pessoa, **peça a validação** dela antes de seguir.
5. Exporte o final quando ela pedir; **verifique** (`scripts/verificar_saida.py`, quadros, checklist do formato) e entregue com o `MATERIAIS.md`.

## Apoio de outras skills

Se estiverem disponíveis, use-as; se não estiverem, **siga o procedimento embutido** em `references/base/` e no arquivo do formato.

| Tarefa | Skill, se disponível |
|---|---|
| Transcrever com tempo por palavra | `transcrever-groq` |
| Escolher os melhores momentos de um vídeo longo e transformá-los em cortes | `smart-cuts` |
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
- `references/exemplos/README.md`: quadros de criativos reais (misturas completas e um por formato), para ver estrutura e ritmo.
- `references/base/mistura-de-formatos.md`: como misturar formatos e alternar modos.
- `references/base/fluxo.md`: do material ao arquivo final.
- `references/base/limpar-a-fala.md`: da gravação bruta ao `limpo.mp4` (melhor take, erros, silêncios, emendas, verificação).
- `references/base/cortes.md`: a regra da emenda com sobreposição, pausas e ritmo.
- `references/base/legenda-e-zonas.md`: legenda, texto, inserts, zonas seguras.
- `references/base/materiais.md`: o que pedir e o que buscar, e como registrar.
- `references/base/honestidade.md`: prova real, dramatização, formatos que imitam uma linguagem.
- `references/base/variacoes.md`: variações e teste.
- `references/base/revisao.md`: revisão e checklist de saída.
- `assets/marcas/choquei.png`: o logo da Choquei, para o formato 03 (uso por conta de quem anuncia; veja o arquivo do formato).
- `assets/componentes/`: peças de código do Remotion para reaproveitar (copie e adapte): `CaixaPergunta.tsx` (formato 16), `MancheteNoticia.tsx` (formato 04), `EstudioTelejornal.tsx` (formato 11) e `TakesSobrepostos.tsx` (a emenda com sobreposição, de `base/cortes.md`).
- `scripts/planejar_cortes.py`, `montar.py`, `verificar_cortes.py` e `achar_repeticoes.py`: limpam a fala do bruto e verificam o resultado (`limpar-a-fala.md`). `scripts/verificar_saida.py`: mede o arquivo final. `scripts/recortar_pessoa.py`: recorta a pessoa de qualquer fundo com RVM e grava onde está a cabeça (formatos 02 e 05), como material de apoio.

Os números (zonas, ritmo, medidas de composição) são **pontos de partida**: se a referência da pessoa pede outro, siga a referência. **Nenhuma recomendação aqui foi medida em desempenho de anúncio.**
