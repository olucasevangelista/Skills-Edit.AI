# 07. Depoimento

**Também pedido como:** depoimento, testemunho, UGC, relato de cliente.

## Assinatura visual

Uma pessoa **falando direto para a câmera**, em **plano fechado**, com **legenda de destaque** nas frases fortes, **zooms pontuais** e **inserts de prova** (prints, imagens, resultados) que comprovam o que ela diz. A assinatura é a **proximidade**: parece alguém contando algo que aconteceu com ela.

## Ideal quando

- Existe um **relato real de cliente ou usuário** (gravado por ele, ou com a autorização dele).
- Há **provas** para ilustrar (resultado, tela, antes e depois autorizado, número).
- A prova social pesa na decisão.

## Evite quando

- **Não existe um depoimento real.** **Nunca fabrique** um depoimento, uma pessoa ou um resultado (`honestidade.md`); um ator só vale como **dramatização identificada**.
- Não há autorização de imagem de quem aparece.
- O relato promete algo que a oferta não entrega, ou **garante resultado** que é caso isolado.

## Composição (1080x1920)

| Elemento | Posição e tamanho |
|---|---|
| **Vídeo** | tela cheia, `objectFit: cover`; **rosto no terço superior**, olhos em y ≈ 650 a 850, cabeça inteira, **acima da zona de interface da base** |
| **Legenda** | y ≈ 1080 a 1200 (abaixo do rosto, acima da base), palavra a palavra, 2 linhas no máximo; realce de cor nos ★ |
| **Identificação** | uma **tarja** pequena (nome, cidade ou profissão, **só se autorizados**) em y ≈ 330 a 420, que entra aos 0,5 s e fica 3 a 4 s |
| **Insert de prova** | em tela cheia (1 a 2,5 s) ou em um cartão de ~984 x 520 em y ≈ 420 a 940 (abaixo da tarja de identificação); o rosto não fica coberto por mais de ~2 s |

## Elementos e animações

- **Zooms pontuais** (punch-in de 1,0 para 1,12 a 1,2) nas **frases-chave**, com retorno ao neutro depois; **enquadramentos dinâmicos** alternando 1,0 e ~1,07 nos cortes.
- **Inserts de prova** que entram **na palavra** que ilustram: print do resultado, a tela do produto, uma foto, um número grande.
- **Comparação de antes e depois**, **só se real e autorizada**, como insert curto (veja o formato 14).

## Cortes e ritmo

- **Remova pausas e trechos desnecessários** ("é...", repetições, reinícios), mas **preserve a naturalidade**: não deixe a voz robótica.
- **Emenda com sobreposição** em todos os cortes (`cortes.md`); a **pausa emocional** (uma risada, um silêncio antes de uma frase importante) **se mantém**.
- Evento novo (insert, zoom, texto) a cada ~2 a 3 s; o formato é **mais calmo** que os de resposta direta.

## Texto e legenda

- Legenda com **destaque nas frases importantes** (cor ou escala), nunca ocupando mais de 2 linhas.
- Texto de apoio curto, sem repetir a fala. A identificação **só com o que a pessoa autorizou**.

## Som

- Voz limpa em primeiro plano (reduza ruído de sala se necessário, sem alterar o timbre); música **bem baixa** ou nenhuma; efeito curto só no insert de prova.

## Materiais

- **Peça:** a **gravação do depoimento real**, as provas (prints, imagens, números) e a **autorização** de imagem e de identificação.
- **Pode buscar sozinho:** música, ícones, a fonte, mockups para enquadrar um print.
- **Nunca invente:** o depoimento, a pessoa, o resultado, o nome, a cidade, as avaliações, o antes e depois.

## Variações dentro do formato

- Quais frases são ★ (e, portanto, recebem zoom e destaque).
- Com e sem tarja de identificação; com e sem música.
- A prova que abre o vídeo (prova primeiro) contra a que fecha.

## Armadilhas e checklist

- [ ] O depoimento é **real** e a pessoa autorizou o uso da imagem neste anúncio.
- [ ] Nenhuma frase foi cortada de modo que **mude o sentido** do que ela disse.
- [ ] Os inserts são reais e entram na palavra certa.
- [ ] O rosto está inteiro e acima da zona de interface; a legenda não cobre a boca.
- [ ] Não há garantia de resultado escrita na tela.

## Kit

Composição **`Depoimento`** (`kit/formatos/depoimento`). Props: `video`, `legendas`, `titulo`, `cores`, `fonte`, `duracaoS`, mais `identificacao` (`{ nome, descricao }`, opcional), `inserts` (lista de `{ src, deS, ateS, legenda? }`), `zooms` (lista de `{ deS, ateS, escala }`) e `destaques` (palavras a realçar na legenda).

## Apoio

Se a skill `smart-cuts` estiver disponível, use-a para limpar o depoimento (pausas, reinícios, emendas); se a `creative-lab` estiver disponível, use a `conformidade.md` dela para a prova e as promessas.
