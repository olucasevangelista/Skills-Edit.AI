---
name: editar-aula
description: Direção para editar aulas gravadas (câmera, gravação de tela com rosto, slides com voz ou só áudio) com padrão e qualidade - o que limpar (erros, reinícios, pausas), como dividir em seções com capítulos e onde colocar títulos, destaques de termos-chave e motions explicativos sem cobrir o que o aluno precisa ver. Use sempre que o usuário pedir para editar, limpar, cortar pausas e erros, dar acabamento, colocar títulos ou destaques, ou preparar uma aula, curso, treinamento, webinar ou gravação de tela para publicar, mesmo que o pedido seja vago como "edita essa aula". Traz também scripts opcionais de limpeza que usam FFmpeg e Python. Os motions são criados com a skill do Remotion.
---

# Editar aula

Direção para editar uma aula gravada sem improviso: o que limpar, como estruturar, onde cabe cada tipo de motion e o que nunca fazer. O objetivo é uma aula clara, bem estruturada e entregue em poucos minutos de trabalho.

## Princípios

- **Clareza acima de enfeite.** O aluno precisa entender a aula e enxergar o que ela mostra. Motion que atrapalha é pior que nenhum.
- **Aula pede calma.** Poucos motions, bem espaçados. Cada um precisa ter uma função: orientar (títulos), fixar (destaques) ou ilustrar (explicativos).
- **Limpar sem cansar.** Tire erros, reinícios e pausas longas, mas preserve a respiração natural da fala. Aula cortada demais cansa.
- **A estrutura aparece.** Seções com título e capítulos para o aluno se orientar.
- **O usuário decide o que importa.** Pergunte pouco e siga com padrões declarados se ele não responder.

## Pergunte primeiro (uma mensagem curta)

1. **Qual o formato da aula?** Câmera falando, gravação de tela com rosto no canto, slides com voz ou só áudio. O formato decide onde cabe motion (`references/formatos.md`).
2. **Identidade visual:** use a do projeto, se existir. Se não, pergunte se quer que você crie uma simples ou se prefere enviar a sua (logo, cores, fontes).

## Fluxo

1. **Entenda o material:** formato, duração e uma transcrição com tempo por palavra (a skill `transcrever-groq` serve, se estiver instalada). A transcrição pode omitir frases repetidas e muletas; desconfie de trechos curtos demais para o tempo.
2. **Decida o que cortar** lendo a transcrição: reinícios de frase (fique com a última versão completa), takes repetidos, comentários fora da aula e pausas longas. Critérios em `references/limpeza.md`.
3. **Estruture:** divida em seções, dê um título curto a cada uma e anote o tempo de cada início para os capítulos.
4. **Planeje os motions** dentro do orçamento (`references/motions.md`): título da aula, título de cada seção, destaques de termos-chave e, só quando a ideia for densa, um motion explicativo.
5. **Combine uma vez com o usuário** antes de executar: duração antes e depois, o que será removido, as seções e a lista de motions com o tempo de cada. Se ele já pediu para fazer tudo, siga direto.
6. **Execute:** limpe o vídeo (os scripts abaixo ajudam) e crie os motions no Remotion (skill do Remotion). Para **exportar**, escolha: motions que só **colocam coisas por cima** (títulos, destaques, listas, cartelas) usam a **exportação rápida**, que renderiza só os segundos com motion (`references/exportacao.md`); motions que **transformam o vídeo** (zoom, tela dividida) pedem o render direto no Remotion, com o vídeo dentro da composição.
7. **Confira e entregue** com a lista abaixo, junto de `capitulos.txt` (um por linha, `00:00 Título`).

## Antes de entregar, confira

- Nenhum motion cobre o que o aluno precisa ver (principalmente em gravação de tela).
- Frases importantes não foram cortadas e nada ficou duplicado (transcrever o vídeo limpo mostra isso).
- Pausas e volume estão naturais; o volume é parecido do começo ao fim.
- Os textos dos motions são curtos, legíveis e têm tempo de ser lidos.
- Veja um quadro de cada motion no vídeo final (a exportação rápida gera `folha_motions.png` para isso).
- Cores e fontes seguem a identidade do projeto do começo ao fim.

## Scripts de limpeza (opcionais)

Cortes e áudio (os dois últimos, a exportação dos motions). Use `python` (Windows) ou `python3` (macOS); precisam de FFmpeg. A saída vai sempre para outra pasta e o original não é alterado.

- `python <skill>/scripts/diagnosticar.py aula.mp4` mostra formato, volume e avisos.
- `python <skill>/scripts/planejar_cortes.py aula.mp4 --saida trabalho --remover "62-71.5,120-131"` planeja os cortes (os tempos podem vir da transcrição: o script os alinha ao som real).
- `python <skill>/scripts/montar.py trabalho/cortes.json --saida trabalho` gera `aula_limpa.mp4`.
- `python <skill>/scripts/verificar.py trabalho/aula_limpa.mp4 --timeline trabalho/timeline.json` mede duração, volume, pausas e estalos.
- Exportação rápida dos motions: `clips.mjs` e `colar.py` (`references/exportacao.md`).

Os cortes usam emenda por sobreposição: o trecho novo entra colado no começo da fala, sem respiro, e começa ainda no finalzinho do anterior. Detalhes em `references/limpeza.md`.

## Referências (abra só o que precisar)

- `references/formatos.md`: o que fazer em cada formato de aula e como não atrapalhar a tela.
- `references/limpeza.md`: o que remover, estilos de corte e problemas comuns.
- `references/motions.md`: tipos de motion, orçamento e como escolher o que destacar.
- `references/exportacao.md`: exportação rápida dos motions (só as janelas com motion) e quando não usar.
