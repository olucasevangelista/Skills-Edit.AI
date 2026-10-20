# Verificador (auditoria da edição)

Rode isto **antes de mostrar** qualquer edição ao usuário, e também ao revisar uma edição que já existe. A ideia é trocar "acho que está dinâmico" por uma checagem. Não depende de ferramenta: basta ter a lista de eventos com tempo (de um projeto em código, de uma timeline ou estimada a partir das legendas com tempo).

## Passo 1: tabela de eventos

Liste **todos** os eventos visuais em ordem:

| # | Início (s) | Tipo | Duração | Fala naquele instante | Nível (★/normal/baixa) |
|---|---|---|---|---|---|
| 1 | 0,0 | Logo em destaque + texto de gancho | 2,5 | "Hoje eu vou te mostrar o Claude…" | ★ |
| 2 | 2,4 | Punch-in | 0,3 | "…que faz isso sozinho" | ★ |

Tipos: insert, texto novo, zoom (punch-in ou saída), corte de câmera, tela dividida/cheia, outro.

## Passo 2: cálculos

1. **Lacuna** = início do evento seguinte menos o início do atual. Marque:
   - **> 3,0 s: falha** (corrigir);
   - 2,0 a 3,0 s: aceitável;
   - ≤ 2,0 s: ideal.
2. **Maior lacuna** do vídeo e **lacuna média**. Meta: nenhuma falha; média perto de 2 s.
3. **Variedade:** nenhum tipo de evento 3 vezes seguidas; há eventos grandes a cada ~8 a 10 s.
4. **Zoom:** o zoom máximo só aparece em trechos ★; há pelo menos um retorno ao neutro após cada ênfase; trechos de baixa relevância não têm zoom nem insert.
5. **Proporção de ★:** em geral até ~30% do tempo. Acima disso, reveja a marcação.

## Passo 3: checklist

**Gancho**
- [ ] Há um evento visual nos primeiros 1,5 s?
- [ ] Se o assunto é uma marca ou ferramenta, o logo ou nome dela está em destaque no primeiro segundo?
- [ ] O texto de gancho complementa a fala (não repete) e fica 2 a 3 s?

**Conteúdo**
- [ ] Cada corte entre takes entra colado no começo da fala (sem respiro nem silêncio antes) e começa durante o finalzinho do take anterior (~0,1 a 0,25 s de sobreposição), com a frase anterior terminando inteira e sem estalo?
- [ ] Cada insert aparece na palavra que ilustra (±0,1 s) e dura 1 a 2,5 s?
- [ ] Todo texto tem tempo de leitura suficiente (0,4 s + 0,3 s por palavra)?
- [ ] Nenhum elemento importante fora da zona segura?
- [ ] Contraste suficiente em todos os textos sobre qualquer fundo?
- [ ] Identidade visual (cores, fontes) consistente do começo ao fim?

**Som**
- [ ] A voz está limpa e sempre em primeiro plano?
- [ ] Efeitos sonoros discretos, só nos eventos grandes?
- [ ] Volume final coerente (como referência, entre -14 e -16 LUFS)?

**Fechamento**
- [ ] Os últimos 2 a 3 s mantêm energia? A chamada para ação, se houver, está clara?

## Passo 4: corrigir e relatar

Para cada falha, aplique a correção **usando o que a fala diz naquele trecho**:
- Lacuna > 3 s → insira um evento no meio da lacuna: insert que ilustra a palavra mais concreta do trecho, texto-chave, ou mudança de zoom. Evite repetir o tipo do evento vizinho.
- Zoom em trecho de baixa relevância → remova.
- Texto curto demais em tela → alongue ou corte palavras.

Ao entregar, inclua um **relatório curto**: maior lacuna antes e depois, o que foi ajustado e o que ficou como escolha de gosto (para o usuário decidir). Exemplo:

> Verificação: maior lacuna 4,1 s → 2,4 s (inseri o gráfico em 11,2 s e um punch-in em 13,0 s). Logo do Claude no primeiro segundo. 5 de 22 eventos grandes. Escolha sua: o texto de gancho está em azul; posso trocar para branco.
