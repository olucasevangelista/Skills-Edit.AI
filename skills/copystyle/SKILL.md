---
name: copystyle
description: Estuda vídeos de referência de edição (Reels, TikToks, Shorts ou qualquer vídeo que o usuário queira copiar o estilo, baixados como mp4 no computador) quadro a quadro, com medições e transcrição, e monta o GUIA DE ESTILO com todo o passo a passo replicável - formatos meme e sério, legendas com fonte, tamanho e posição, gancho, inserts, ritmo, música e efeitos com níveis, zonas do 9:16 e checklist de QA - mais os estilos visuais em tokens para o Remotion aplicar e a lista de assets que faltam (música, efeitos, fontes, logo). Use sempre que alguém mandar mp4 de referência ou disser "analisa essas referências", "quero editar igual a esse perfil", "copia o estilo desse vídeo", "monta o guia de edição", "estuda o estilo desses reels", "atualiza meu guia com essas referências novas", mesmo sem dizer a palavra guia. Usa FFmpeg e Python.
---

# CopyStyle

Você transforma vídeos de referência num guia de estilo que outro editor (uma pessoa ou um agente com Remotion e FFmpeg) consegue replicar com precisão. O guia não é opinião: é medição (tempo, tamanho, posição, nível de som, cortes por minuto) mais a leitura do humor e da narrativa, adaptada ao criador. No fim, o criador sabe exatamente o que falta providenciar.

As referências são SEMPRE arquivos mp4 que o criador (ou quem opera a skill) já baixou para o computador. Você não baixa referência da internet.

`<skill>` abaixo é a pasta onde esta skill está instalada. Use `python` (Windows) ou `python3` (macOS). Precisa de Python 3.10+ (só biblioteca padrão) e FFmpeg com `ffprobe`. A transcrição das referências vem da skill `transcrever-groq`.

## Onde fica o resultado

Uma pasta por criador, `copystyle/<nome>/`, na pasta de trabalho do usuário:

- `GUIA-DE-ESTILO.md`: o guia (estrutura em `references/modelo-guia.md`).
- `estilos.json`: legendas e ganchos em tokens (mesmo arquivo de modelo).
- `ASSETS-PENDENTES.md`: o que falta providenciar (`references/assets.md`).
- `referencias/<lote>/`: os vídeos analisados, com `analise/<slug>/` de cada um.

## 1. Briefing do criador

Entreviste seguindo `references/entrevista.md` (no máximo duas rodadas de AskUserQuestion; não pergunte o que o pedido ou os vídeos já respondem). Criador que já tem um guia: pule a entrevista e pergunte só o que mudou (por exemplo, estas referências são para qual tipo de corte?). Grave as respostas no cabeçalho do guia e as preferências declaradas ("odeio zoom", "quero mais meme") na seção de preferências, com a data.

## 2. Medir as referências

```
python <skill>/scripts/analisar.py analisar ref1.mp4 ref2.mp4 --saida copystyle/<nome>/referencias/<lote>/analise
```

`<lote>` é um nome curto e datado (por exemplo `out2026`). Agrupe por autor ou página: cada página tem uma gramática própria. Para cada vídeo sai `meta.json` (duração, tamanho, fps, cortes de cena por minuto), `scenes.json` (instante de cada corte), `sons.json` (volume e picos que podem ser efeitos sonoros) e `sheets/` (folhas de contato 6x3 com o tempo em cada quadro). Corte de cena não pega zoom nem jump cut leve: confira nas folhas.

Transcreva cada referência com a skill `transcrever-groq` (`--saida .../analise --nome <slug>`). O Whisper erra palavra e às vezes "transcreve" música: a legenda queimada no vídeo é a verdade.

Quadro em resolução cheia, para medir fonte, tamanho e posição, ou rajada, para ver uma animação:

```
python <skill>/scripts/analisar.py quadro ref1.mp4 12.5
python <skill>/scripts/analisar.py quadro ref1.mp4 12.5 --rajada 1.5 --fps 10
```

## 3. Dissecar (visão, com agentes)

Lance agentes em paralelo, um por grupo de 3 a 5 vídeos (mesmo autor juntos), cada um seguindo `references/brief-analise.md` (passe o caminho do brief, da pasta do lote, a lista de slugs e o que você sabe do criador). Cada agente escreve `analise/<slug>/analise.md` por vídeo e `analise/_grupo_<nome>.md` com a síntese, e responde curto. Eles enxergam mas não escutam: o som é pista (volume, picos, transcrição, o que o criador disse), sempre com a confiança marcada.

Enquanto trabalham, abra você mesmo 2 ou 3 folhas de contato de cada grupo para ter opinião própria na síntese.

## 4. Tendências (se houver meme nas referências)

Gíria e meme envelhecem em semanas. Pesquise o vocabulário vivo do mês no nicho e no idioma do criador (WebSearch; se precisar ver algo que só aparece logado, como áudio em alta no Instagram, use o navegador do usuário pela skill de Chrome) e grave `referencias/<lote>/tendencias-<mes-ano>.md`: o que usar, o que está morto, emojis, e a regra de segurança (deboche aponta para coisa ou para o próprio criador, nunca para pessoa, aparência ou grupo).

## 5. Escrever o guia

Escreva `GUIA-DE-ESTILO.md` seguindo `references/modelo-guia.md`: quem fala e como chamar, vocabulário vivo, decisão meme x sério, cada formato com estrutura e números, caixa de efeitos, sistemas de legenda com tokens, áudio com níveis, formato sério com modos de tela, zonas do 9:16, checklist de QA, índice das referências e o mapa para o Remotion (cada técnica vira um tipo de elemento com seus números). Atualização de guia existente: mescle, suba a versão e date as mudanças; nunca apague as preferências do criador.

## 6. Estilos visuais

Traduza as legendas e ganchos medidos em `estilos.json` (tokens em `references/modelo-guia.md`). Fonte: identifique a família (ou a Google Font mais parecida). Confira cada estilo contra um quadro real da referência: monte um quadro de teste no Remotion (skill do Remotion) com o texto do criador e compare lado a lado com o quadro medido (`analisar.py quadro`). Ajuste tamanho, posição, peso e sombra até bater, em até 3 rodadas.

## 7. Assets: baixar o que der, pedir o resto

Siga `references/assets.md`: música, efeitos sonoros, pack visual, fontes e marca. O que é gratuito e de boa qualidade você providencia; o que é pago, pessoal ou que você não achou vai para `ASSETS-PENDENTES.md`, com o que é, onde aparece no guia e o substituto provisório.

## 8. Entrega

Diga ao criador, em linguagem simples: onde está o guia, os 5 a 8 achados mais fortes das referências, o que já foi providenciado e a lista do que ele precisa mandar (com o caminho exato de onde colocar). O guia serve para qualquer editor, humano ou agente. Se ele quiser compartilhar com um editor humano, ofereça publicar como página.

## Antes de entregar, confira

- Todo número do guia vem de uma medição (tempo, px, % da largura, dB), e cada receita cita a referência de onde saiu.
- O guia não contradiz as regras básicas de edição para redes sociais (nada de texto em cima do rosto, final sem cauda depois da fala) sem o criador pedir.
- Som marcado como "provável" ou "não identificado" quando não há evidência; nenhuma trilha ou efeito inventado.
- Os estilos de `estilos.json` foram conferidos contra quadros reais.

## Referências (abra só o que precisar)

- `references/entrevista.md`: passo 1.
- `references/brief-analise.md`: passo 3 (passe para cada agente).
- `references/modelo-guia.md`: passos 5 e 6 (estrutura do guia, mapa para o Remotion, `estilos.json`).
- `references/assets.md`: passo 7.
