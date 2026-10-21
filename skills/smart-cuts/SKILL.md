---
name: smart-cuts
description: Transforma um ou mais vídeos longos (live, aula, podcast, vídeo do YouTube, call) em cortes prontos para virar Reels, TikToks e Shorts - escolhe os melhores momentos pela transcrição, tira loops, devaneios e pausas, e emenda cada corte no estilo de edição profissional, com o take seguinte entrando colado na voz e com imagem e áudio sobrepostos antes de a fala anterior acabar, sem nenhuma palavra cortada. Entrega um mp4 limpo por corte mais um plano com texto, tempos, ganchos e enquadramento para a legenda, o gancho, os inserts, a música e o formato 9:16 serem feitos depois no Remotion. Use sempre que pedirem "gera cortes", "corta esse vídeo", "edita essa live", "faz uns reels disso", "cortes desse mp4", "transforma essa aula em cortes", "junta trechos desses vídeos num corte só", ou mandarem um mp4 longo pedindo conteúdo curto, mesmo sem dizer a palavra corte. Também para ajustar cortes já feitos, como "o fim do corte 2 comeu palavra" ou "tira essa parte do c3". Usa FFmpeg e Python.
---

# Smart Cuts

Direção para tirar cortes de um vídeo longo com critério: escolher o que vale, emendar sem a pessoa perceber e entregar o material pronto para receber legenda, gancho e inserts. A Smart Cuts **corta e emenda**. Legenda, gancho, inserts, música, formato vertical e exportação final são feitos no Remotion (skill do Remotion), a partir do plano que ela entrega.

`<skill>` abaixo é a pasta onde esta skill está instalada. Use `python` (Windows) ou `python3` (macOS). Precisa de Python 3.10+ (só biblioteca padrão) e FFmpeg com `ffprobe`.

## Princípios

- **Nenhuma palavra cortada.** O criador ouve o corte inteiro. Uma sílaba comida estraga o corte e a confiança no editor.
- **A emenda não aparece.** O take seguinte entra colado no começo da voz, sem respiro, e imagem e áudio dele entram juntos, um pouco antes de a fala anterior acabar (`references/emenda.md`).
- **Gancho primeiro, arco completo.** O corte abre numa frase que prende e fecha a ideia. Quem vê só o corte entende e sai com algo.
- **Qualidade antes de quantidade.** Corte que só funciona com três minutos de contexto não é corte. Live fraca rende pouco, e tudo bem.
- **O criador decide o que importa.** Pergunte pouco, junto e uma vez. Não reabra o que ele já respondeu.

## Pergunte primeiro (uma mensagem curta)

1. **Que vídeo é esse?** Câmera falando, aula ou live com tela compartilhada e webcam, ou podcast com mais de uma pessoa. Isso decide o enquadramento (`references/enquadramento.md`).
2. **Sério ou meme?** Um corte nunca mistura os dois estilos. Sério: explicação, história, números, opinião com argumento. Meme: a pessoa vira personagem (indignada, se gabando, errando ao vivo, bordão, exagero).
3. **Duração e quantidade.** Padrão sem pedido: sério 45 a 90 s, meme 15 a 60 s; levante todos os bons candidatos e recomende os melhores.
4. **Tom e vocabulário:** como a pessoa fala, palavras que ela não usaria, nomes e siglas que aparecem. Se ela já tem um guia ou preferências de edição, leia como texto livre.

## Fluxo

1. **Transcreva** com a skill `transcrever-groq`, com tempo por palavra: `python <skill transcrever-groq>/scripts/transcrever.py video.mp4 --saida trabalho/transcricoes --nome aula`. A transcrição pode omitir frases repetidas e muletas, e os tempos escorregam 0,2 a 0,5 s em arquivos longos; por isso as emendas são calculadas pelo volume do áudio, e o corte final é transcrito de novo para conferir.
2. **Leia o material todo** (`python <skill>/scripts/ler.py trabalho/transcricoes/aula/transcricao.json`) e levante os candidatos. Critérios e armadilhas em `references/escolha-de-cortes.md`.
3. **Aprove uma vez com o usuário** (checkpoint único): tabela com id, estilo, gancho, duração e o porquê em uma linha, mais as dúvidas de grafia de nomes e siglas, todas juntas. Legenda queimada não tem errata.
4. **Marque os trechos** em `cortes.json` (`references/plano.md`). Para marcar uma emenda com precisão, veja os silêncios reais: `python <skill>/scripts/ler.py transcricao.json 120 180 --video video.mp4 --silencio`.
5. **Planeje:** `python <skill>/scripts/planejar_cortes.py cortes.json --saida trabalho`. Ele mostra o texto final de cada corte e os avisos. **Leia o texto em voz alta na cabeça**: a costura precisa soar natural. Avisos `ENTROU` e `SAIU` dizem que uma palavra entrou ou saiu por estar colada na fala; resolva antes de montar.
6. **Monte:** `python <skill>/scripts/montar.py trabalho/plano_cortes.json --saida trabalho`. Gera `<id>.mp4` de cada corte e o `plano.json`.
7. **Confira de ouvido:** transcreva cada corte final (`--nome <id>`, na mesma pasta de transcrições) e rode `python <skill>/scripts/verificar.py trabalho/plano.json --transcricoes trabalho/transcricoes`. Ele mede duração, sincronia, volume, pausas e estalos e compara a fala. **ALERTA ou PENDENTE: não entregue.** Corrija a emenda e monte só aquele corte (`--so c2`).
8. **Entregue** os cortes limpos e o `plano.json`, com os enquadramentos medidos. Legenda, gancho, inserts, música, 9:16 e a exportação final são feitos no Remotion; use os tempos da transcrição do corte final para a legenda.

## Antes de entregar, confira

- O gancho aparece no primeiro segundo e se entende sem som.
- Cada corte fecha a ideia, sem cauda depois da última palavra.
- `verificar.py` sem ALERTA nem PENDENTE, volume parecido do começo ao fim.
- Nada inventado: nenhum print, número ou depoimento fabricado (`references/regras-de-oficio.md`).
- O `plano.json` tem o rosto medido de cada corte e o layout de cada trecho, quando for tela com webcam.

## Referências (abra só o que precisar)

- `references/escolha-de-cortes.md`: o que faz um bom corte, loops e devaneios, compilação de vários trechos, ganchos.
- `references/emenda.md`: o estilo de emenda por sobreposição e o ritmo das pausas.
- `references/regras-de-oficio.md`: fala, voz e áudio, imagem, conteúdo e verdade, checklist de QA.
- `references/enquadramento.md`: regras do 9:16, como tirar um quadro e medir o rosto, para o Remotion aplicar.
- `references/plano.md`: formato do `cortes.json` (o que você escreve) e do `plano.json` (o que a skill entrega).
- `references/problemas.md`: sintomas comuns e o que fazer.
