# Fábrica de Criativos

Um **guia** para o agente editar criativos de anúncio em vídeo em **16 formatos** (e em misturas deles), a partir do mesmo material, e fazer **variações**. Quem edita é o agente, no **Remotion**: a skill dá direção, estruturas possíveis, exemplos reais e arquivos de apoio, e **não traz template nem script que edite por ele**, para não limitar a estética nem o trabalho. Foco em edição e variação, não em copy.

Os formatos: Tela Dividida, Fundo Verde (recorte), Post de Rede Social, Notícia, Professor, Motion Design, Depoimento, React, Videochamada, Corte de Podcast, Telejornal, Tutorial de Tela, Conversa de Chat, Antes e Depois, Cinema e Caixinha de Pergunta.

## Instalar

```
npx skills add olucasevangelista/Skills-Edit.AI --skill fabrica-de-criativos -g
```

## Como é feita

- `SKILL.md`: princípios (guia e não molde; misturar formatos; adaptar à marca da pessoa; validar com ela), perguntas iniciais, a tabela dos formatos e o fluxo.
- `references/formatos/`: um arquivo por formato, no mesmo modelo (assinatura visual, quando usar, composição, estruturas possíveis, animações, cortes, texto, som, materiais, variações, checklist, estruturas e exemplos, apoio). **Atualizar um formato é editar um arquivo**; um novo formato é um arquivo novo e uma linha no índice.
- `references/exemplos/`: quadros de criativos reais (misturas completas e um por formato) com o que observar em cada um.
- `references/base/`: o que é comum (misturar formatos, emenda com sobreposição, legenda e zonas, materiais, honestidade, variações, revisão).
- `assets/`: o logo da Choquei (formato 03) e `componentes/` com peças de código do Remotion para reaproveitar (caixinha de pergunta, manchete de notícia, cenário e título de telejornal, e emenda com sobreposição). Elas são peças soltas, não editores.
- `scripts/`: `verificar_saida.py` (mede o arquivo final) e `recortar_pessoa.py` (recorta a pessoa com RVM e grava a posição da cabeça), como apoio.

**Materiais:** cada formato diz o que pedir, mas o agente tem liberdade de buscar sozinho o que couber (música, imagens e vídeos de apoio com licença clara) e registra a origem e a licença em `MATERIAIS.md`. Nunca inventa depoimento, resultado, antes e depois, notícia ou conversa real.

**Outras skills:** usa `transcrever-groq`, `smart-cuts`, `motion-designer`, `creative-lab`, `copystyle`, `raio-x-criativos` e a skill do Remotion quando estão instaladas; sem elas, segue o procedimento embutido, sem comentar a ausência.

## O que foi testado (e o que não foi)

- `tests/validar_formatos.py` (16 testes): os 16 arquivos seguem o modelo, o índice do `SKILL.md` bate com os arquivos, os quadros e caminhos citados existem, não sobrou kit nem template, nenhuma marca real é nome de formato, nenhum texto revela a ausência de uma skill, o frontmatter é válido, sem segredos. Um erro plantado de propósito foi pego.
- `tests/test_verificar_saida.py` (11 testes, com vídeo sintético): tamanho, taxa de quadros, duração, áudio, volume, quadro preto e imagem congelada.
- `tests/verificar_componentes.py <projeto Remotion>` (22 verificações): os componentes compilam; o cenário do telejornal se mexe e o título renderiza; a caixinha fica no alto, centralizada, com o texto centralizado (digitada e fixa); a manchete entra com a caixa antes do texto (cerca de 0,5 s) dentro das margens, e o modo deslize funciona; a emenda faz imagem e áudio entrarem juntos antes de a voz anterior acabar.
- `scripts/recortar_pessoa.py` (RVM) foi rodado em 3 s de vídeo real com GPU: recorte limpo, ~5 quadros por segundo, áudio preservado e `pessoa_cabeca.json` gerado. Em CPU não foi medido.

**Não testado ou limitado:**

- **Nenhum formato foi testado com um agente seguindo a skill do início ao fim.** Os exemplos em `references/exemplos/` foram feitos no Remotion pelo autor; a skill descreve a estrutura deles, mas isso não prova que um agente a reproduz bem.
- O guia veio de 13 exemplos do autor (quatro criativos completos e nove demonstrações de formato). Os formatos Depoimento, React, Videochamada e Corte de Podcast **ainda não têm quadro de exemplo**.
- macOS e Linux não foram testados.
- Os números de composição, ritmo e zona segura são **pontos de partida**; nenhum foi medido em desempenho de anúncio.
- **As políticas atuais das plataformas não foram conferidas.** Os formatos de notícia, telejornal, depoimento e antes e depois mandam a pessoa conferir as regras e identificar dramatização e publicidade.
- O logo da Choquei é uma **marca de terceiro**: o autor informou que a página tolera o uso, mas isso não foi verificado e não é licença.
