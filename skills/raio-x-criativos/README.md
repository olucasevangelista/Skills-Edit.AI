# raio-x-criativos

Faz o **raio-x de um criativo de anúncio em vídeo**: a engenharia reversa de **por que ele chama atenção** (o gancho, no áudio e no visual), **por que retém** (o corpo: ritmo, promessa segurada, storytelling, novos ganchos) e **por que leva à página** (CTA, oferta, urgência). Também **compara o criativo com a página de vendas** para checar a coerência, e aponta os **pontos fracos** de um criativo que não performou.

O resultado é um relatório com **hipóteses ranqueadas**, cada uma com a evidência por segundo, a confiança e o teste para validar. A skill **não afirma que um criativo funciona**: isso só os dados de desempenho do usuário dizem.

A transcrição vem da skill `transcrever-groq`.

## Instalar

```
npx skills add olucasevangelista/Skills-Edit.AI --skill raio-x-criativos -g
```

Depois, no chat do agente, chame `/raio-x-criativos` e mande o criativo ("faz o raio-x desse anúncio"), com os dados de desempenho e a página de vendas, se tiver.

## O que precisa

**Python 3.10+** (só biblioteca padrão) e **FFmpeg** com `ffprobe` (`winget install Gyan.FFmpeg` no Windows, `brew install ffmpeg` no macOS). O resto é método.

## Conteúdo

| Arquivo | Para quê |
|---|---|
| `references/metodo.md` | as camadas, áudio e visual separados, o formato da hipótese, o que não se pode afirmar, uso ético |
| `references/gancho.md` | como analisar o gancho e o vocabulário de hipóteses |
| `references/retencao.md` | o que segura a pessoa, como ler o mapa de ritmo, sinais de queda |
| `references/conversao-e-cta.md` | CTA, oferta (presente, desconto, pré-venda, promoção), urgência, garantia |
| `references/pagina-e-coerencia.md` | a comparação entre o criativo e a página |
| `references/veredito-e-dados.md` | que dados pedir, como ler, criativo que não funciona, como validar |
| `references/modelo-relatorio.md` | o `ANALISE.md` e a síntese de vários criativos |
| `references/brief-agente.md` | brief para analisar em paralelo com agentes |
| `scripts/analisar.py` | mede o criativo: cortes de cena, picos de som, folhas de contato com tempo, janelas e o mapa de ritmo |

## O script

| Comando | O que faz |
|---|---|
| `analisar.py analisar <videos> --saida <pasta>` | por vídeo: duração, tamanho, fps, cortes de cena por minuto, volume e picos de som, folhas de contato com o tempo em cada quadro |
| `analisar.py quadro <video> <t> [--rajada 1.5 --fps 10]` | um quadro (ou uma rajada) em resolução cheia, para ler texto na tela |
| `analisar.py janela <video> --de A --ate B --fps N` | folha de contato de uma janela de tempo com o tempo escrito (o gancho, o final com o CTA) |
| `analisar.py mapa <video> --transcricao transcricao.json --saida <pasta>` | mapa de ritmo (`mapa_ritmo.json` e `.md`): cortes, palavras, volume e som por janela, mais um resumo |

O script **mede**; não avalia qualidade. Nenhum valor do mapa é "bom" ou "ruim" por si.

## Estado dos testes

| Item | Situação |
|---|---|
| Testes automáticos do script (18) | Passando no Windows 11, com vídeo sintético de números conhecidos (cortes em 1, 2 e 8 s; fala em três rajadas; dez palavras em instantes marcados) |
| Controles negativos | Alterei o script de três jeitos (janela dos 3 primeiros segundos, deslocamento do `--de` da janela, limite de pausa) e **cada alteração foi pega por um teste específico** |
| Mapa de ritmo | Cortes nos 3 e 5 primeiros segundos, maior trecho sem corte, palavras (total, por minuto, nos 3 primeiros e nos 5 últimos segundos), pausas de fala, tempo com som e volume por trecho: todos conferidos contra os valores construídos |
| Mídia real (os primeiros 45 s de um vídeo seu de 1080p60, com a transcrição que já existia) | Palavras (165), palavras por minuto (220), palavras nos 3 primeiros e nos 5 últimos segundos (12 e 22), primeira palavra e a pausa de 0,46 s **batem exatamente** com a contagem independente feita direto na transcrição. A folha do gancho saiu com 24 quadros e o tempo absoluto escrito em cada um. O script avisou que 1.981 palavras da transcrição eram posteriores ao fim do clipe e as ignorou |
| **A análise (a direção)** | **Não foi testada com agente nem com um criativo de anúncio real.** O vídeo usado na mídia real não é um anúncio: só se conferiu a medição, não a interpretação |
| **Os "porquês"** | **Nenhum foi validado contra desempenho real.** A skill produz hipóteses |
| **macOS** | **Não testado** |

Rodar os testes: `python -m unittest discover -s tests` (precisa de FFmpeg).

## Limites que vale conhecer

- **É uma leitura por hipóteses.** Sem dados de desempenho do usuário, não há veredito. Com dados, o veredito vem deles, e a skill não inventa faixas de "bom" e "ruim".
- **Não escuta o áudio.** Música e efeitos sonoros entram como hipótese por indício (picos de volume, o que se vê) ou pelo que o usuário contar.
- **O detector de cortes de cena não pega zoom nem jump cut leve**, e planos de brilho parecido podem passar batidos. As folhas de contato servem para conferir.
- **A transcrição pode errar palavras e omitir repetições.** A legenda queimada no vídeo, se houver, é a verdade.
- **"Som" no mapa** é o quanto da janela tem som acima do limiar (voz, música ou efeito): com música contínua, o silêncio não aparece. As pausas de fala vêm da transcrição.
- A página é lida como **dado**; nem tudo o que está nela precisa estar no criativo.
- O criativo vem como arquivo que o usuário já tem. A skill não baixa anúncio, e o objetivo é entender princípios, não reproduzir o criativo de terceiros.
