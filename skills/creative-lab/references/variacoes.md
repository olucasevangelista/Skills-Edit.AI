# Variações e teste de criativos

O mesmo anúncio com versões diferentes de gancho, formato ou edição, para o teste mostrar o que funciona com aquele público. Esta skill **não promete** que um tipo de gancho converta mais: ela produz versões bem feitas e **comparáveis**.

## 1. Regra de ouro: uma variável por vez

Mude **uma** coisa e mantenha o resto idêntico. Se o gancho, o CTA e o ritmo mudam juntos, o resultado não diz qual deles fez a diferença.

| Eixo | O que varia | O que fica igual |
|---|---|---|
| **Ângulo do gancho** | dor, desejo, prova, curiosidade, mecanismo, mito, objeção, autoridade | o corpo, o CTA, o formato |
| **Tratamento visual do gancho** | prova primeiro, tela dividida, demonstração, texto em destaque, motion | a fala, o corpo, o CTA |
| **Formato** | pessoa falando, gravação de tela, motion, UGC, depoimento | a mensagem e a oferta |
| **Edição** | ritmo (mais ou menos eventos), estilo da legenda, com ou sem música | a fala e a estrutura |
| **CTA** | o texto e o momento | todo o resto |
| **Duração** | versão curta e versão longa | o gancho e o CTA |

## 2. Modo A: variar o gancho visual (mesma fala)

A pessoa tem um anúncio com um gancho do tipo X e quer outros. Você cria **2 a 3 tratamentos de tipos diferentes** (não três versões do mesmo tipo), com a **mesma fala** nos primeiros segundos:

1. Identifique o tipo do gancho atual (`gancho.md`).
2. Proponha, em uma tabela curta, outros 2 ou 3 tipos que o material permita:

   | # | Tipo | Ângulo que testa | O que aparece nos 3 primeiros segundos | Material que precisa |
   |---|---|---|---|---|

3. Depois da aprovação, crie cada tratamento (texto, tela dividida, motion no Remotion ou no editor) e exporte uma versão por tratamento, com o resto do anúncio igual.

## 3. Modo B: um corpo e vários ganchos

A pessoa manda o **corpo** (o anúncio sem gancho, ou a parte que fica igual) e quer **N anúncios**, cada um com um gancho diferente.

1. **Defina os ganchos** com ângulos distintos (tabela como a do modo A, com a coluna "o que se fala"). Uma primeira rodada com **3 a 5 ângulos diferentes** ensina mais que 10 variações do mesmo ângulo.
2. **Crie cada gancho como um clipe separado**, com voz (e imagem, texto, tela dividida ou motion). Mesmo formato e mesma taxa de quadros do corpo, sempre que der. O gancho termina **inteiro**: a última palavra completa.
3. **Cheque a ponte:** leia as últimas palavras do gancho junto com as primeiras do corpo. Se a frase continua com sentido, siga. Se quebra, avise e proponha outro fim para o gancho ou outro começo para o corpo.
4. **Rode o script**, que junta cada gancho ao corpo:

```
python <skill>/scripts/variar_ganchos.py --corpo corpo.mp4 --ganchos g1.mp4 g2.mp4 g3.mp4 --saida variantes --prefixo anuncio
```

Também aceita uma **pasta** com os ganchos (`--ganchos pasta_dos_ganchos`).

**O que o script faz:** acha onde a voz do corpo começa e onde a voz de cada gancho termina (pelo volume); codifica o corpo uma vez e reaproveita; emenda cada gancho com **sobreposição** (a imagem e o áudio do corpo entram juntos, antes de a fala do gancho acabar); leva **todas as variantes ao mesmo volume** (−14 LUFS por padrão, ajustável com `--lufs`), porque volumes diferentes enviesam o teste; e grava um `matriz.csv`.

**Saídas:** `anuncio__g1.mp4`, `anuncio__g2.mp4`, ... e `matriz.csv` (separado por ponto e vírgula, abre direto no Excel em português; `--separador ","` muda).

**Limites a conhecer:**

- O corpo e os ganchos precisam ter **imagem e áudio**. Gancho sem voz detectada usa o arquivo inteiro e o script avisa.
- O corpo deve **começar com a fala** (o script corta o silêncio antes dela).
- Gancho de **outra proporção** entra inteiro, com barras, e o script avisa. Prefira criar o gancho no formato do corpo.
- O script só **junta**. Criar o gancho é com você (Remotion ou o editor da pessoa).
- Confira cada variante antes de entregar (`verificador.md`): a emenda e o volume são medidos pelo script, mas o sentido da ponte é seu.

## 4. Modo C: variar formato ou edição

Mesma regra: uma variável por vez. Exemplos:

- **Edição:** a versão "ritmo apertado" (mais eventos, cortes mais curtos) contra a versão com menos eventos; legenda de um estilo contra outro; com e sem música.
- **Formato:** o mesmo roteiro com a pessoa falando para a câmera, com gravação de tela, ou com motion.
- **Duração:** uma versão de ~15 s e outra de ~30 s, com o mesmo gancho e o mesmo CTA.

Para cada versão, anote na matriz **o que mudou e o que ficou igual**. Mantenha o volume final igual entre elas.

## 5. Matriz do teste

Uma tabela por rodada. O script já preenche as colunas de arquivo; as outras são da pessoa:

| Variante | Gancho (tipo e ângulo) | O que muda | O que não muda | Data de entrada | Hook rate | Hold rate | CTR | Observações |
|---|---|---|---|---|---|---|---|---|

## 6. Métricas e como ler

- **Hook rate** = visualizações de 3 s ÷ impressões. Diz se o começo **parou o scroll**.
- **Hold rate** diz se o anúncio **segurou** a pessoa depois do começo. **As fontes definem de formas diferentes** (por exemplo ThruPlays ÷ visualizações de 3 s, ou visualizações de 15 s ÷ visualizações de 3 s). **Escolha uma definição e use a mesma em todas as variantes.**
- Nenhum dos dois é uma coluna nativa das plataformas: quem anuncia calcula a partir das colunas.
- Compare as variantes **sob as mesmas condições** (mesmo público, mesmo período, verba parecida) e espere impressões suficientes antes de concluir; esta skill não define esse número.
- Hook rate alto com hold rate baixo costuma indicar um **gancho que promete mais do que o corpo entrega**. Hook rate baixo indica que o **começo** não está parando o scroll. São pistas para a próxima rodada, não sentenças.

## 7. Nomes de arquivo

`<anuncio>__<gancho>.mp4`, em minúsculas, sem espaço. O nome do gancho descreve o ângulo ("prova", "dor", "mito"), não o número do arquivo, para a planilha ser legível meses depois.
