# Verificador (auditoria do anúncio)

Rode isto **antes de mostrar** qualquer edição ao usuário, e também ao revisar um anúncio que já existe. A ideia é trocar "acho que está dinâmico" por uma checagem. Não depende de ferramenta: basta ter a lista de eventos com tempo (de um projeto em código, de uma timeline ou estimada a partir das legendas com tempo).

## Passo 1: tabela de eventos

Liste **todos** os eventos visuais em ordem:

| # | Início (s) | Tipo | Duração | Fala naquele instante | Nível (★/normal/baixa) |
|---|---|---|---|---|---|
| 1 | 0,0 | Âncora (interface) + texto de gancho | 2,5 | "Você ainda monta essa planilha à mão?" | ★ |
| 2 | 1,2 | Punch-in | 0,3 | "…à mão?" | ★ |

Tipos: insert, texto novo, zoom (punch-in ou saída), troca de plano, tela dividida ou cheia, motion, outro.

## Passo 2: cálculos

1. **Lacuna** = início do evento seguinte menos o início do atual. Marque:
   - **> 2,5 s: falha** (corrigir);
   - 1,5 a 2,5 s: aceitável;
   - ≤ 1,5 s: ideal nos primeiros 5 s; ≤ 2 s depois.
2. **Maior lacuna** e **lacuna média**. Meta: nenhuma falha; média perto de 2 s (e menor nos primeiros 5 s).
3. **Variedade:** nenhum tipo de evento 3 vezes seguidas; marco grande a cada ~6 a 8 s; re-gancho (evento forte de tipo diferente) a cada troca de parte.
4. **Zoom:** o zoom máximo só aparece em trechos ★; há pelo menos um retorno ao neutro depois de cada ênfase; trechos de baixa relevância não têm zoom nem insert.
5. **Proporção de ★:** em geral até ~30% do tempo.

## Passo 3: checklist

**Gancho**
- [ ] Há um evento visual nos primeiros 1,5 s?
- [ ] A âncora do assunto (produto, resultado, interface) está em destaque no primeiro segundo?
- [ ] A **promessa é visível** (o resultado aparece ou fica claro)?
- [ ] O texto de gancho complementa a fala (não repete) e fica 2 a 3 s?
- [ ] O corpo do anúncio **sustenta** o que o gancho promete?

**Resultado e mecanismo**
- [ ] Se o anúncio promete um resultado: ele aparece, com **prova real**, e o quanto ajuda está concreto (número real, base certa)?
- [ ] Se o anúncio cita o mecanismo: nome em texto no instante da fala, uma animação do que ele faz, 2 a 3 repetições com o mesmo termo e a mesma cor?
- [ ] Nada na tela afirma mais do que a fala?
- [ ] **Nada foi colocado na tela só porque está na página** (objeção, prova, mecanismo ou oferta que a fala não traz)? Tudo o que aparece é dito no anúncio ou foi pedido pelo usuário.

**Conteúdo**
- [ ] Cada corte entre takes entra colado no começo da fala (sem respiro) e começa durante o finalzinho do take anterior (~0,1 a 0,25 s), com **imagem e áudio juntos**, a frase anterior terminando inteira e sem estalo?
- [ ] Cada insert aparece na palavra que ilustra (±0,1 s) e dura 1 a 2,5 s?
- [ ] Todo texto tem tempo de leitura (0,4 s + 0,3 s por palavra)?
- [ ] Nenhum elemento importante (texto, rosto, logo, CTA) fora da zona segura?
- [ ] Contraste suficiente nos textos sobre qualquer fundo? Legenda presente?
- [ ] Identidade visual consistente do começo ao fim?

**Som**
- [ ] A voz está limpa e sempre em primeiro plano?
- [ ] Efeitos discretos, só nos marcos grandes?
- [ ] Volume final coerente (referência entre −14 e −16 LUFS)?

**Fechamento**
- [ ] Os últimos 2 a 3 s mantêm a energia? A oferta e o CTA estão claros e visíveis?

**Honestidade**
- [ ] Todo resultado, depoimento, número e print é real, ou está identificado como ilustração?
- [ ] Houve autorização de imagem de quem aparece? As políticas da plataforma para esse tipo de produto foram conferidas pelo usuário?

**Variações (se for um teste)**
- [ ] Só **uma** coisa muda entre as variantes?
- [ ] O corpo é idêntico, o volume é igual (diferença de até ~1 dB) e a legenda é a mesma?
- [ ] A ponte entre cada gancho e o corpo faz sentido lida em voz alta?
- [ ] A matriz do teste registra o que mudou e o que ficou igual?

## Passo 4: corrigir e relatar

Para cada falha, corrija **usando o que a fala diz naquele trecho**:

- Lacuna > 2,5 s → insira um evento no meio da lacuna: insert que ilustra a palavra mais concreta do trecho, texto-chave, mudança de zoom ou um motion curto. Evite repetir o tipo do vizinho.
- Zoom em trecho de baixa relevância → remova.
- Texto curto demais em tela → alongue ou corte palavras.
- Gancho que o corpo não sustenta → avise o usuário e proponha um gancho que antecipe uma parte real do corpo.

Ao entregar, inclua um **relatório curto**: maior lacuna antes e depois, o que foi ajustado e o que ficou como escolha de gosto. Exemplo:

> Verificação: maior lacuna 3,4 s → 1,9 s (inseri a gravação de tela em 11,2 s e um punch-in em 13,0 s). Resultado visível no segundo 1. Mecanismo citado 3 vezes, mesmo termo e cor. Escolha sua: o CTA final está em verde; posso trocar para a cor da marca.
