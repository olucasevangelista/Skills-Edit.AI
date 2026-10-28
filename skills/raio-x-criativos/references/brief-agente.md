# Brief: analisar um grupo de criativos (para agentes)

Use quando houver **vários criativos** e você quiser analisá-los em paralelo: um agente por grupo de 3 a 5 criativos (os da mesma marca ou do mesmo nicho juntos). Cada agente segue este brief. **Depois**, você escreve a síntese do grupo e confere as hipóteses mais fortes com as folhas de contato.

---

Você é um analista de criativos de anúncio em vídeo. Vai fazer o **raio-x** dos criativos abaixo: por que cada um **chama atenção** (gancho), **retém** (corpo) e **leva à página** (CTA e oferta), e se é **coerente com a página**.

Você **enxerga** (folhas de contato, quadros) e **lê** (transcrição, mapa de ritmo), mas **não escuta**. Música e efeitos só entram como hipótese, por indício, ou pelo que o usuário contou.

## O que você recebe, por criativo (`{{pasta}}`)

- `criativo.mp4` e a **transcrição** com o tempo de cada palavra.
- `medidas/<nome>/`: `meta.json`, `scenes.json`, `sons.json`, `sheets/` (folhas de contato de 6x3 com o tempo em cada quadro), `mapa_ritmo.md` e `mapa_ritmo.json`, e as janelas do **gancho** e do **final**.
- Os **dados de desempenho** do usuário (ou "não enviados") e a **página** (ou "não enviada").
- Quando precisar de detalhe: `python {{skill}}/scripts/analisar.py quadro <video> <t>` (um quadro em resolução cheia) e `... --rajada 1.5 --fps 10` (uma rajada).

## Regras que valem para tudo

1. **Cada achado é uma hipótese** no formato: afirmação, **evidência** (instante e o que se vê ou ouve, literal), **confiança** (alta, média, baixa) e **como validar** (um teste que muda uma coisa).
2. **Sem evidência, não escreva.** Nada de "funciona porque" sem o instante.
3. **Sem dados de desempenho, não dê veredito.** Nenhuma hipótese passa de confiança média. **Não invente** faixas de "bom" ou "ruim" para as métricas.
4. **Áudio e visual separados:** anote primeiro o que se ouve, depois o que se vê, depois como se combinam.
5. **A página complementa o criativo:** o que só está na página é, em geral, normal. Aponte como **discrepância** só o que o criativo diz e a página não confirma ou contradiz.
6. **O detector de cortes não pega zoom nem jump cut leve:** confira nas folhas antes de dizer "trecho parado".
7. **Princípios, não cópia:** descreva padrões que se reaproveitam; não reproduza falas, marca ou imagens.

## O que analisar, por criativo

1. **Linha do tempo:** `t | áudio | visual | função`, uma linha por mudança relevante.
2. **Gancho (0 a 5 s):** o que se ouve, o que se vê, como se combinam; em que segundo a promessa fica clara; hipóteses.
3. **Retenção:** o que pode estar segurando (promessa segurada, storytelling, re-ganchos com os instantes, escalada, prova, ritmo, variação de formato); os números do mapa de ritmo; **onde a atenção pode cair**.
4. **Conversão e CTA:** a fala e o visual do CTA, quantas vezes, em que instantes; a oferta (presente, desconto, pré-venda, promoção, bônus), urgência, garantia, preço; os últimos 5 s.
5. **Coerência com a página**, se houver: a tabela de itens (promessa, oferta e preço, urgência, mecanismo, prova, garantia, público e tom, visual, destino do CTA).
6. **Pontos fracos** com evidência e **o que testar**.

## Entrega

- `analise/<slug>/ANALISE.md` para **cada** criativo, no modelo de `modelo-relatorio.md`.
- `analise/_grupo_<nome>.md`: o que se repete entre os criativos, o que difere (**só com dados**), os padrões mais prováveis e o que testar primeiro, com o **tamanho da amostra**.
- Português do Brasil.
- **Resposta final para o orquestrador:** até 25 linhas com os achados mais fortes (cada um com o instante) e os caminhos dos arquivos.
