---
name: raio-x-criativos
description: Faz o raio-x (a engenharia reversa) de um criativo de anúncio em vídeo - analisa por que ele chama atenção (o gancho, no áudio e no visual), por que retém (o corpo, com ritmo, promessa segurada, storytelling e novos ganchos) e por que leva à página (CTA, oferta, urgência), compara o criativo com a página de vendas para checar a coerência e entrega um relatório com hipóteses ranqueadas, a evidência de cada uma por segundo e o que testar. Também aponta os pontos fracos de um criativo que não performou. Use sempre que mandarem um anúncio, criativo ou vídeo de venda para analisar, "fazer o raio-x", "entender por que funciona", "por que esse criativo não está performando", "engenharia reversa do criativo" ou "o que esse anúncio faz certo", mesmo sem dizer a palavra criativo. Usa FFmpeg e Python.
---

# Raio-X de Criativos

Você abre um criativo de anúncio em vídeo e explica **por que ele funciona, ou por que não funciona**: o que faz a pessoa **parar** (gancho), **ficar** (retenção) e **ir para a página** (conversão). Também confere se o criativo é **coerente com a página de vendas** que ele leva.

O criativo é sempre um **arquivo mp4 que o usuário já tem**; você não baixa anúncio da internet. O objetivo é entender **princípios**, não reproduzir o criativo de ninguém.

`<skill>` abaixo é a pasta onde esta skill está instalada. Use `python` (Windows) ou `python3` (macOS). O script precisa de Python 3.10+ e FFmpeg com `ffprobe`; o resto é método.

## A regra central: hipótese, não veredito

Olhando só para o vídeo, **você não sabe se ele funciona**: funcionar é um resultado de campanha (público, verba, oferta, época). Então:

- **Cada achado é uma hipótese**, com a **afirmação**, a **evidência** (o instante e o que se vê ou ouve), a **confiança** (alta, média ou baixa) e **como validar** (um teste). Nada de "funciona porque X" sem evidência no próprio criativo.
- **Com dados de desempenho do usuário**, o veredito (funciona, não funciona, misto) vem dos dados. **Não invente faixas de "bom" ou "ruim"**: pergunte ao usuário se aquele número é bom na conta dele.
- **Sem dados**, diga com todas as letras que é uma **leitura por hipóteses**, não um veredito.
- **Você não escuta.** Música e efeitos sonoros só entram como hipótese, por indícios (picos de volume, o que se vê) ou pelo que o usuário contar.

Detalhes em `references/metodo.md` e `references/veredito-e-dados.md`.

## Pergunte primeiro (poucas perguntas, de uma vez)

1. **De quem é o criativo** (do usuário ou de outra marca) e **qual o objetivo** (venda direta, lead, instalação, outro).
2. **Dados de desempenho**, se tiver: gasto, impressões, hook rate, hold rate, CTR, custo por resultado ou ROAS, tempo no ar. E **se esses números são bons ou ruins na conta dele**.
3. **A página de vendas** que o criativo leva (link ou o texto colado), para checar a coerência e entender público, produto e oferta.
4. **A música:** tem? Qual o clima? (Você não escuta; o que o usuário contar vale.)
5. Plataforma e período, se souber.

Se o usuário só mandou o vídeo, **não bloqueie**: faça o raio-x e declare o que ficou de fora ("sem dados de desempenho: leitura por hipóteses"; "sem a página: sem a checagem de coerência").

## Fluxo

1. **Transcreva** com a skill `transcrever-groq`, com o tempo de cada palavra:
   `python <skill transcrever-groq>/scripts/transcrever.py criativo.mp4 --saida raio-x/<nome>/transcricao --nome criativo`.
   A transcrição pode errar palavras e omitir repetições; a legenda queimada no vídeo, se houver, é a verdade.
2. **Meça:**
   `python <skill>/scripts/analisar.py analisar criativo.mp4 --saida raio-x/<nome>/medidas` (cortes de cena, picos de som, folhas de contato com o tempo),
   `python <skill>/scripts/analisar.py mapa criativo.mp4 --transcricao raio-x/<nome>/transcricao/criativo/transcricao.json --saida raio-x/<nome>/medidas` (o mapa de ritmo),
   `python <skill>/scripts/analisar.py janela criativo.mp4 --de 0 --ate 3 --fps 8 --saida raio-x/<nome>/medidas/gancho` (o gancho, a 8 quadros por segundo) e outra janela com os **últimos segundos** (o CTA).
   Para ler um texto pequeno na tela: `analisar.py quadro criativo.mp4 <t>`.
3. **Áudio primeiro, visual depois**, nos 3 a 5 primeiros segundos e depois no vídeo todo: o que se **fala** (transcrição) e o que **aparece** (folhas e quadros). Não misture os dois ao anotar.
4. **Hipóteses por camada**, cada uma no formato acima: **gancho** (`references/gancho.md`), **retenção** (`references/retencao.md`, com o mapa de ritmo) e **conversão e CTA** (`references/conversao-e-cta.md`).
5. **Página e coerência** (`references/pagina-e-coerencia.md`): o que o criativo diz e a página confirma, o que o criativo diz e a página não tem, e o que só a página tem.
6. **Veredito honesto** (`references/veredito-e-dados.md`): funciona, não funciona ou indefinido, com base nos dados; pontos fracos com evidência; hipóteses ranqueadas; o que testar.
7. **Relatório** `raio-x/<nome>/ANALISE.md` no modelo de `references/modelo-relatorio.md`. Com **vários criativos**, uma síntese dos padrões (e, com dados, do que separa os que funcionam dos que não funcionam). Para analisá-los em paralelo com agentes, use `references/brief-agente.md`.

## Entrega

Diga ao usuário, em linguagem simples: o veredito em até 3 linhas (com a base dele), as 3 a 5 hipóteses mais fortes (cada uma com o instante da evidência), os pontos fracos, a coerência com a página e o que valeria testar. O relatório completo fica no `ANALISE.md`. **Não escreva um ensaio**: o usuário quer entender e agir.

## Referências (abra só o que precisar)

- `references/metodo.md`: as camadas, áudio e visual separados, o formato da hipótese, o que você não pode afirmar, uso ético.
- `references/gancho.md`: como analisar o gancho e o vocabulário de hipóteses.
- `references/retencao.md`: o que segura a pessoa, como ler o mapa de ritmo, sinais de queda.
- `references/conversao-e-cta.md`: CTA, oferta, urgência, garantia, atrito.
- `references/pagina-e-coerencia.md`: a comparação entre o criativo e a página.
- `references/veredito-e-dados.md`: que dados pedir, como ler, criativo que não funciona, como validar.
- `references/modelo-relatorio.md`: o `ANALISE.md` e a síntese de vários criativos.
- `references/brief-agente.md`: brief para analisar em paralelo com agentes.

Os números do mapa de ritmo (cortes, palavras, pausas) são **medidas**, não notas: nenhum valor é "bom" ou "ruim" por si. Compare com os outros criativos da mesma conta.
