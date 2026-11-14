---
name: editar-youtube
description: Direção para editar vídeos longos de YouTube (pessoa falando para a câmera, gravação de tela com rosto no canto, motion no corpo ou uma mistura) com abertura forte, ritmo que prende e lembretes para seguir - identifica o tipo de vídeo, limpa a fala (silêncios, erros e takes repetidos, escolhendo o melhor) com emenda por sobreposição de imagem e áudio, planeja os primeiros 5 a 10 segundos como um gancho dinâmico que mostra o que vem sem entregar o final, o meio de acordo com o estilo da pessoa e as chamadas para seguir no começo e perto do fim. Use sempre que pedirem para editar, montar, dar dinâmica, melhorar a retenção, criar o gancho ou a abertura, tirar silêncios e erros, ou colocar motions e lembrete de inscrição num vídeo de YouTube, mesmo que o pedido seja vago como "edita meu vídeo". Dá direção e não entrega elementos prontos, porque o estilo é da pessoa. Traz scripts de limpeza que usam FFmpeg e Python. Os motions são criados com a skill do Remotion.
---

# Editar vídeo de YouTube

Direção para editar um vídeo longo de YouTube sem improviso: identificar o tipo de vídeo, limpar a fala, abrir com um gancho forte, manter a pessoa curiosa até o fim e lembrá-la de seguir nos momentos certos. **Nenhum elemento é imposto** (animação, cor, fonte, formato do texto): o estilo é da pessoa. Esta skill dá o que importa e por quê; quem cria os elementos é você, no Remotion, com a identidade dela.

Cuida da **edição**, não do roteiro, da thumbnail nem do título.

## Princípios

- **A abertura é o vídeo.** Os primeiros 5 a 10 segundos precisam ser muito dinâmicos, atraentes e **bem feitos**. É onde mais vale caprichar.
- **Instigue, não entregue.** A abertura diz o que a pessoa vai ver ou aprender e, às vezes, mostra o que vem, mas **deixa o "como" e o final para o decorrer**. Cada trecho seguinte alimenta a vontade de continuar até descobrir.
- **O tipo de vídeo e o estilo da pessoa mandam no meio.** Não há fórmula: o que serve para quem fala para a câmera atrapalha numa gravação de tela.
- **Corte com sobreposição em todo corte,** e com mais cuidado nos **momentos-chave** (abertura, viradas, revelação, troca de seção): o próximo take entra com imagem e áudio juntos, antes de a fala anterior acabar. É isso que dá dinâmica.
- **Limpar sem cansar.** Tire erros, repetições e silêncios, mas um vídeo longo precisa respirar onde a ideia pede.
- **Lembrete para seguir, no tempo certo.** Cedo, perto do fim e no final (`references/chamadas-para-seguir.md`).
- **Valide o que for novo.** Se vai criar uma abertura ou uma linguagem visual que a pessoa ainda não viu, mostre um quadro ou um trecho curto de baixa resolução e peça a opinião dela antes de seguir. Na dúvida, pergunte.

## Pergunte primeiro (uma mensagem curta, até 4 perguntas)

1. **Qual o tipo do vídeo?** Pessoa falando para a câmera, gravação de tela com rosto no canto, motion no corpo (narração com animações) ou uma mistura. Se ela não souber dizer, identifique olhando quadros (`references/tipos-de-video.md`).
2. **O que o vídeo promete e qual é o final?** O tema, o que a pessoa vai mostrar ou ensinar e a revelação que prende até o fim. É a matéria-prima da abertura.
3. **Estilo de edição e identidade:** vídeos anteriores ou referências que ela gosta, cores, fontes, logo. Se ela já tem um guia de estilo, use-o. **Nunca imponha** o estilo de outra pessoa nem sugira cor por conta própria.
4. **Ela fala o pedido para seguir ou inscrever-se no vídeo?** Onde? (Se não, a edição coloca; veja `references/chamadas-para-seguir.md`.)

Se o pedido for vago, **não bloqueie**: faça as perguntas e siga com padrões que você declara em uma linha.

## Fluxo

1. **Entenda o material:** rode o diagnóstico (formato, volume, fala), tenha uma transcrição com tempo por palavra (a skill `transcrever-groq` serve, se estiver instalada) e identifique o tipo de vídeo, **por trecho** se ele alterna.
2. **Limpe a fala** (`references/limpeza.md`): primeiro escolha o que fica (takes repetidos, erros), depois encurte as pausas e emende com sobreposição. Resultado: `limpo.mp4`. **Transcreva o `limpo.mp4`**: os tempos das palavras passam a ser os do vídeo final.
3. **Faça o mapa do vídeo** sobre a transcrição limpa: candidatos a gancho, momentos-chave (viradas, a demonstração principal, a revelação), seções, onde a tela está em ação e onde está parada, trechos conceituais que pedem um motion.
4. **Planeje a abertura** (`references/abertura.md`): o que prometer, o que mostrar, como abrir e qual o momento do meio do vídeo que vale antecipar.
5. **Planeje o meio** (`references/meio-e-ritmo.md`) de acordo com o tipo e o estilo, e as **chamadas para seguir** (`references/chamadas-para-seguir.md`).
6. **Combine uma vez com o usuário** antes de executar: a abertura (mostre uma prévia leve), a tabela `Início | Evento | Fala` e o que será removido. Se ele já pediu para fazer tudo, siga direto, mas valide a abertura se ela for nova para ele.
7. **Execute:** crie os elementos no Remotion (skill do Remotion) usando o `limpo.mp4`. Para exportar, escolha o caminho em `references/exportacao.md`.
8. **Confira e entregue** com a lista abaixo.

## Antes de entregar, confira

- A abertura, vista sozinha, **dá vontade de continuar**, diz o que vem e **não entrega o final**. Está bonita, legível e bem feita.
- Nenhum silêncio de meio segundo ou mais sobrou entre as frases (o verificador mede). Frases importantes não foram cortadas e nada ficou duplicado: transcreva o vídeo limpo e leia.
- Cada corte tem a sobreposição (imagem e áudio do take seguinte entram juntos, antes de a fala anterior acabar), e nenhum ficou seco.
- Em gravação de tela, **nada cobre a área da tela** enquanto a pessoa mostra, clica ou digita; o rosto do canto fica visível.
- As chamadas para seguir entraram nos momentos certos e não cobrem o conteúdo.
- Os textos têm tempo de leitura (0,4 s + 0,3 s por palavra, mínimo 1 s) e as cores e fontes seguem a identidade da pessoa do começo ao fim.
- Volume parecido do começo ao fim. Veja um quadro de cada motion no vídeo final.

## Scripts (opcionais)

Use `python` (Windows) ou `python3` (macOS). `<skill>` é a pasta onde esta skill está instalada. Precisam de Python 3.10+ (só biblioteca padrão, exceto o recorte) e FFmpeg. A saída vai sempre para outra pasta e o original não é alterado.

- `python <skill>/scripts/diagnosticar.py bruto.mp4` mostra formato, volume, fala e avisos.
- `python <skill>/scripts/achar_repeticoes.py transcricao.json` aponta takes repetidos e sugere o que remover (confirme lendo; ele não ouve o áudio).
- `python <skill>/scripts/planejar_cortes.py bruto.mp4 --saida limpeza --estilo curto --remover "62-71.5"` planeja os cortes medindo o áudio.
- `python <skill>/scripts/montar.py limpeza/cortes.json --saida limpeza` gera `limpo.mp4` e o mapa de tempos (`timeline.json`).
- `python <skill>/scripts/verificar_cortes.py limpeza/limpo.mp4 --timeline limpeza/timeline.json` mede duração, volume, pausas que sobraram e estalos.
- `recortar_pessoa.py` recorta a pessoa do fundo (precisa de PyTorch; use num trecho curto, como a abertura).
- `clips.mjs` e `colar.py`: exportação rápida dos elementos que só colocam coisas por cima (`references/exportacao.md`).

## Referências (abra só o que precisar)

- `references/tipos-de-video.md`: como identificar o tipo e o que cada um pede.
- `references/abertura.md`: os primeiros 5 a 10 segundos e a curiosidade até o fim.
- `references/meio-e-ritmo.md`: o meio por tipo de vídeo, os momentos-chave e a emenda com sobreposição.
- `references/chamadas-para-seguir.md`: onde lembrar a pessoa de seguir ou inscrever-se.
- `references/limpeza.md`: da gravação bruta ao `limpo.mp4` (melhor take, erros, silêncios, emendas, verificação).
- `references/exportacao.md`: exportação rápida e quando não usar.

Os números desta skill são **pontos de partida**, não leis: se o estilo ou a referência da pessoa pede outro, siga a pessoa. **Nenhuma recomendação aqui foi medida em desempenho de vídeo.**
