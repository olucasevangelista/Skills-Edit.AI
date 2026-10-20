---
name: editar-reels
description: Guia de edição de vídeos curtos verticais (Reels do Instagram, TikTok, YouTube Shorts) pensado para retenção e resultado - gancho forte nos primeiros segundos, ritmo com uma novidade visual a cada 2 a 3 segundos, zoom com hierarquia de ênfase, inserts (imagem, gráfico, logo), texto e tela dividida. Use sempre que o usuário pedir para editar, montar, planejar a edição, dar dinâmica, melhorar a retenção, criar o gancho visual ou "turbinar" um reel, short ou TikTok, ou quando uma edição estiver parada, monótona ou sem gancho, mesmo que o pedido seja vago ("edita esse vídeo", "melhora esse reel") e mesmo que ele não diga "skill". Funciona com qualquer ferramenta de edição (Remotion, HyperFrames, CapCut, Premiere, After Effects...). Cuida da edição e do visual, não do roteiro falado. Se o vídeo é sobre uma ferramenta ou marca (ex.: Claude), já abre com ela em destaque.
---

# Editar Reels

Uma **estrela norte** para edição de vídeo curto: o que faz reter e quando aplicar cada recurso. O *como* depende da ferramenta; o gosto e o que é importante são do usuário. Sem componentes nem visual prontos.

## Receita rápida (o essencial, já dá para trabalhar só com isto)

- **Gancho (0 a 3 s):** logo ou nome do assunto em destaque no 1º segundo (se o vídeo é sobre uma marca ou ferramenta; senão, a palavra-chave) **mais** um texto curto (até ~6 palavras) que **complementa** a fala em vez de repetir: se a fala anuncia a novidade ("o Claude acabou de lançar um recurso"), o texto promete o ganho ou a curiosidade ("Chega de repetir prompt"), nunca reapresenta o anúncio ("Novo recurso do Claude"). Alternativa: tela dividida com a prova (tela, resultado).
- **Ritmo:** um evento visual novo **a cada no máximo 3 s, ideal ~2 s**. Evento = insert, texto novo, mudança de zoom, corte, tela dividida ou cheia. Legenda e zoom lento sozinhos não contam. Alterne os tipos e ponha um marco grande (tela dividida, tela cheia, texto gigante) a cada ~8 a 10 s.
- **Cortes entre takes: nada de corte seco nem de respiro.** O próximo take entra colado no começo da fala (sem respiro nem silêncio antes) e já começa durante o finalzinho do anterior (~0,1 a 0,25 s de sobreposição; as vozes se sobrepõem de propósito). A frase anterior termina inteira e a imagem corta junto com o áudio novo. Em todo corte; detalhes em `references/ritmo-e-zoom.md`.
- **Ênfase é relativa:** marque cada trecho como ★ chave, normal ou baixa. ★ = punch-in (~1,12 a 1,2) + texto grande + insert; baixa = volta a 1,0, sem texto nem insert. **Todo zoom tem retorno ao neutro.** ★ em no máximo ~30% do tempo, senão a ênfase se anula.
- **Insert** ilustra a palavra falada e entra nela (±0,1 s); dura 1 a 2,5 s.
- **Texto em tela:** fica 0,4 s + 0,3 s por palavra (mínimo 1 s). Zonas seguras em 1080×1920: topo 220 px, base 420 px, lateral direita 120 px livres.
- **Logos:** peça ao usuário; senão busque na web (SVG ou PNG transparente, fonte oficial, confira visualmente). Se não achar, pergunte ou use o nome em texto limpo. Nunca improvise um logo parecido.
- **Som:** voz sempre em primeiro plano; efeito sonoro curto só nos marcos grandes.

## Fluxo

1. **Pergunte de uma vez, em no máximo 3 perguntas curtas, só o que faltar:**
   - *Identidade visual:* use a do projeto ou a informada. Se não existe: "quer que eu crie uma identidade simples ou prefere enviar a sua (logo, cores, fontes ou um print)?" Nunca imponha a de outra pessoa.
   - *Referências e materiais:* "tem algum reel que você curte o estilo, ou prints e gravações de tela do que está falando?"
   - *Mensagem principal:* se não estiver clara, qual é a frase mais importante do vídeo.

   Se o pedido for vago, **não bloqueie**: faça as perguntas e já siga com padrões que você declara em uma linha ("assumi identidade neutra escura, sem referências"). Se faltar a fala com tempos, peça a transcrição (a skill `transcrever-groq` serve, se estiver instalada).
2. **Marque ★ / normal / baixa** sobre a transcrição com tempos. Isso decide onde vão zoom, texto e insert.
3. **Monte a tabela de eventos** com a receita acima.
4. **Autoverificação rápida:** calcule as lacunas entre eventos (nenhuma > 3 s), confira gancho (âncora + complemento) e retorno de todo zoom. Corrija antes de mostrar.
5. **Prévia antes do render:** só exporte o arquivo final quando o usuário pedir.

## Formato da entrega (curto de propósito)

- Perguntas e suposições: até 5 linhas.
- Tabela `Início (s) | Evento | Fala`, **uma linha curta por evento**, sem parágrafos dentro da tabela.
- Verificação: até 3 linhas (maior lacuna antes e depois, escolhas de gosto que ficam para o usuário).

O usuário quer a edição, não um ensaio: não escreva justificativas longas. Aprofunde só se ele pedir.

## Revisar uma edição que já existe

Peça ou extraia a lista de eventos com tempos, calcule as lacunas e aponte-as pelo tempo exato ("de 12 s a 17 s não acontece nada"). Proponha o que entra em cada uma usando o que a fala diz ali, e inclua o retorno de qualquer zoom que fica parado.

## Referências (abra só se precisar de detalhe; não leia todas por padrão)

- `references/gancho.md`: padrões de gancho visual e como escolher.
- `references/ritmo-e-zoom.md`: valores de zoom, sincronia, cortes com sobreposição (como fazer em cada junção), tempo de leitura.
- `references/inserts-texto-e-logos.md`: tipos de insert, legendas, zonas seguras, como buscar logos.
- `references/verificador.md`: auditoria completa, para revisar uma edição existente ou quando pedirem rigor.

Os números desta skill (3 s, 2 s, zoom, margens) são pontos de partida, não leis: se a referência do usuário pede outro ritmo, siga a referência.
