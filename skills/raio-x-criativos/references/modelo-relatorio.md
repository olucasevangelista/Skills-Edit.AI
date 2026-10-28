# Modelo do relatório (`ANALISE.md`)

Um arquivo por criativo, em `raio-x/<nome>/ANALISE.md`. Escreva em português do Brasil, em frases diretas, com tabelas onde houver tempo e número. **Todo achado tem instante e evidência.** O texto entre `{{ }}` é para trocar; o conteúdo abaixo é um modelo de estrutura, não uma análise.

```markdown
# Raio-X: {{nome do criativo}}

## 1. Veredito
{{Até 3 linhas: o que é o criativo, se funciona e COM BASE EM QUÊ, e o principal motivo (como hipótese).}}
Exemplos de formulação honesta:
- "Com os dados que você trouxe (hook rate X, CTR Y, que você diz serem bons na conta), o criativo funciona. A hipótese mais forte é ..."
- "Sem dados de desempenho: leitura por hipóteses, sem veredito."

## 2. Ficha
| Item | Valor |
|---|---|
| De quem é | {{do usuário / de outra marca}} |
| Plataforma e período | {{...}} |
| Duração, formato | {{... s, vertical}} |
| Objetivo | {{venda direta, lead, instalação}} |
| Oferta | {{o que é e o que se vende}} |
| Página | {{link, ou "não enviada"}} |
| Dados do usuário | {{hook rate, hold rate, CTR, custo por resultado, gasto, impressões; ou "não enviados"}} |
| Música | {{o que o usuário contou, ou "não informada"}} |

## 3. Linha do tempo
| t (s) | Áudio (o que se fala) | Visual (o que aparece) | Função |
|---|---|---|---|
| 0,0 | "{{fala literal}}" | {{o que se vê}} | gancho |
| ... | | | |
(Use o mapa de ritmo e as folhas. Uma linha por mudança relevante, não uma por segundo.)

## 4. Gancho
**Áudio:** {{...}} | **Visual:** {{...}} | **Os dois juntos:** {{reforça / contrasta / completa / atrapalha}}
Hipóteses (formato: afirmação, evidência com instante, confiança, como validar):
- H1. ...

## 5. Retenção
Números do mapa de ritmo: {{cortes por minuto, maior trecho sem corte (de, até), palavras por minuto, pausas}}
O que pode estar segurando: ...
Onde pode cair (hipótese): {{instantes}}
Hipóteses: - H...

## 6. Conversão e CTA
CTA (falado e visual, instantes): {{...}} | Oferta e motivo para agir agora: {{...}} | Últimos 5 s: {{...}}
Hipóteses: - H...

## 7. Coerência com a página
| Item | No criativo (instante) | Na página | Situação |
|---|---|---|---|
| Promessa | ... | ... | coerente / discrepância / só na página |
Discrepâncias: {{os dois trechos lado a lado}}
O que a página mostra do público, do produto e da oferta: {{poucas linhas}}
(Se a página não foi enviada: "não checada".)

## 8. Hipóteses ranqueadas
| # | Hipótese | Evidência (instante) | Confiança | Como validar |
|---|---|---|---|---|
| 1 | | | | |

## 9. Pontos fracos e o que testar
- {{ponto fraco, com instante e evidência}} -> {{teste, uma variável por vez}}
(Se o criativo performou bem, "o que manter" no lugar de pontos fracos.)

## 10. Padrões que se reaproveitam
{{Princípios, não cópia: por exemplo, "promessa específica nos 2 primeiros segundos", "novo gancho a cada trecho".}}

## 11. Limites desta análise
- Não escutei o áudio: {{música e efeitos são hipóteses}}.
- O detector de cortes não pega zoom nem jump cut leve.
- {{A transcrição pode ter erros}}; {{não li a página / li a página em tal data}}.
- Isto é uma leitura por hipóteses: só os dados dizem se funciona.
```

## Síntese de vários criativos (`_grupo_<nome>.md`)

Quando o usuário manda vários criativos (da mesma marca, do mesmo nicho, ou os que funcionaram e os que não):

1. **Tabela resumo:** criativo | duração | tipo de gancho | cortes por minuto | CTA | dados (se houver) | veredito.
2. **O que se repete** (nos que funcionam, se houver dados): gancho, promessa, estrutura, forma de segurar, tipo de CTA e de oferta. Cada padrão com **os criativos e os instantes** em que aparece.
3. **O que difere entre os que funcionam e os que não** (**só com dados**): o que os vencedores têm que os outros não têm. Cuidado: com poucos criativos, é correlação fraca; diga o tamanho da amostra.
4. **Padrões mais prováveis**, ranqueados, e **o que testar** primeiro.
5. **Limites:** quantos criativos, quais dados, o que não foi possível saber.
