---
name: creative-lab
description: Direção para editar anúncios em vídeo (Meta Ads, TikTok Ads, Reels e Shorts patrocinados) pensada para reter e mostrar o resultado prometido - gancho com promessa visível, ritmo apertado, inserts, motion e tela dividida, destaque do mecanismo único, uso da página de vendas para entender a copy e variação de criativos para teste (trocar o gancho de um mesmo corpo, variar formato e edição), com um script que junta vários ganchos a um corpo. Use sempre que pedirem para editar, melhorar, turbinar ou testar um anúncio ou criativo, para dar mais retenção a um vídeo de venda, ou para "variar o gancho", "fazer 10 versões com ganchos diferentes" e "teste de criativos", mesmo sem dizer a palavra anúncio. Funciona com qualquer ferramenta de edição. Cuida da edição e do visual, não do roteiro falado. O script usa FFmpeg e Python.
---

# Creative Lab

Uma **estrela norte** para edição de anúncio em vídeo: o que faz o espectador parar, ficar e entender o que o produto faz por ele. O *como* depende da ferramenta; o gosto e o que é importante são do usuário. Os motions e as animações são feitos no Remotion (skill do Remotion). Cuida da **edição**, não de escrever o roteiro falado.

`<skill>` abaixo é a pasta onde esta skill está instalada. O script precisa de Python 3.10+ e FFmpeg; o resto é direção.

## Receita rápida (o essencial)

- **Gancho (0 a 3 s):** em até 1,5 s a pessoa entende **o que é, para quem e qual resultado**. A âncora do assunto (produto, ferramenta, resultado) entra em destaque no primeiro segundo, mais um texto curto (até ~6 palavras) que **complementa** a fala, sem repeti-la.
- **Resultado visível:** mostre o resultado prometido e o **quanto ele ajuda**, sempre com prova real. A forma depende do tipo de oferta (`references/resultado-e-mecanismo.md`).
- **Mecanismo único:** se o anúncio o cita, destaque o nome e mostre **o que ele faz** (causa e efeito), 2 a 3 vezes, com o mesmo termo e a mesma cor.
- **Ritmo:** mais apertado que em Reels. Nos primeiros 5 s, um evento visual novo a cada ~1 a 1,5 s; depois, no máximo a cada 2,5 s. Evento = insert, texto novo, mudança de zoom, troca de plano, tela dividida ou cheia, motion. Marco grande a cada ~6 a 8 s.
- **Cortes entre takes: nada de respiro e nada de áudio cortando seco.** O próximo take entra colado no começo da voz e **imagem e áudio entram juntos**, antes de a fala anterior acabar (~0,1 a 0,25 s de sobreposição). Vale em todo corte, inclusive na junção do gancho com o corpo.
- **Retenção:** abra uma promessa cedo e a resolva depois; renove o interesse a cada seção do anúncio (re-gancho).
- **Texto:** legenda sempre (muita gente assiste sem som). Texto de ênfase dura 0,4 s + 0,3 s por palavra (mínimo 1 s).
- **Zonas seguras (1080x1920, ponto de partida conservador):** topo ~270 px, base ~670 px, laterais ~90 px (direita ~120). Variam entre fontes e plataformas: confirme na especificação atual ou num print da interface.
- **CTA:** claro, curto e visível nos últimos segundos, sem fade que sugira "acabou".
- **A página é direção, não checklist:** não coloque na tela objeção, prova, mecanismo ou oferta que a fala não traz. O anúncio chama a atenção e leva à oferta; a página faz o resto.
- **Honestidade:** nunca fabrique resultado, depoimento, antes e depois, número ou print (`references/conformidade.md`).

## Pergunte primeiro (no máximo 4 perguntas curtas, de uma vez)

1. **Oferta e promessa em uma frase**, e para quem é.
2. **A página de vendas** (link ou o texto colado), para eu ter uma **direção** sobre o público e o que importa para ele. Ela complementa o anúncio: **só entra na tela o que o anúncio já diz ou o que você pedir** (`references/copy-da-pagina.md`).
3. **Material e prova real que existem:** telas, depoimentos, resultados, antes e depois autorizados, gravações do produto.
4. **Identidade, plataforma e duração** do anúncio.

Se o pedido for vago, **não bloqueie**: faça as perguntas e siga com padrões que você declara em uma linha. Se faltar a fala com tempos, peça a transcrição (a skill `transcrever-groq` serve, se estiver instalada).

## Modos de trabalho

1. **Editar um anúncio:** o fluxo abaixo.
2. **Revisar um anúncio que já existe:** rode `references/verificador.md`; aponte lacunas pelo tempo exato e proponha o que entra em cada uma.
3. **Variar o gancho de um anúncio (visual):** mesma fala, outros tratamentos de **tipos diferentes**.
4. **Testar vários ganchos sobre um mesmo corpo:** cada gancho é um clipe; o script junta cada um ao corpo.
5. **Variar formato ou edição:** ritmo, legenda, formato, duração, uma coisa por vez.

Os modos 3 a 5 estão em `references/variacoes.md`.

## Fluxo (editar um anúncio)

1. Faça as perguntas e, se houver página, anote o **mapa de copy** só como direção (`copy-da-pagina.md`): o anúncio não precisa ter tudo o que a página tem.
2. **Marque ★ / normal / baixa** sobre a transcrição com tempos: o que é promessa, mecanismo, prova e oferta é ★.
3. **Monte a tabela de eventos** com a receita acima e as anatomias de `anuncio-e-retencao.md`.
4. **Autoverificação:** lacunas entre eventos (nenhuma > 2,5 s), gancho (âncora, promessa visível, texto), resultado e mecanismo presentes, retorno de todo zoom, zonas seguras. Corrija antes de mostrar.
5. **Prévia antes do render:** só exporte o arquivo final quando o usuário pedir.

## Variar ganchos com o script

```
python <skill>/scripts/variar_ganchos.py --corpo corpo.mp4 --ganchos g1.mp4 g2.mp4 g3.mp4 --saida variantes --prefixo anuncio
```

Gera um anúncio por gancho, com a emenda por sobreposição, todos no mesmo volume, e uma `matriz.csv` para a planilha do teste. O gancho em si (texto, tela dividida, motion) você cria no Remotion ou no editor da pessoa. Detalhes em `references/variacoes.md`.

## Formato da entrega (curto de propósito)

- Perguntas e suposições: até 5 linhas.
- Tabela `Início (s) | Evento | Fala`, **uma linha curta por evento**.
- Verificação: até 3 linhas (maior lacuna antes e depois, o que ficou como escolha de gosto).

O usuário quer a edição, não um ensaio.

## Referências (abra só o que precisar)

- `references/anuncio-e-retencao.md`: anatomia do anúncio, ritmo, loops abertos, zoom, a emenda com sobreposição, texto e som.
- `references/gancho.md`: padrões de gancho, como escolher por tipo de oferta, regras do texto.
- `references/resultado-e-mecanismo.md`: mostrar o resultado e o quanto ajuda; destacar o mecanismo único.
- `references/copy-da-pagina.md`: pedir a página, mapa de copy, como a copy decide a edição.
- `references/variacoes.md`: teste de criativos, matriz, os modos de variação, o script, métricas.
- `references/inserts-texto-e-zonas.md`: inserts, legendas, zonas seguras, logos.
- `references/conformidade.md`: prova honesta, antes e depois, promessas sensíveis.
- `references/verificador.md`: auditoria do anúncio.

Os números desta skill (ritmo, zoom, margens) são pontos de partida, não leis: se a referência do usuário pede outro ritmo, siga a referência. **Nenhuma recomendação aqui foi medida em desempenho de anúncio:** quem diz o que funciona é o teste.
