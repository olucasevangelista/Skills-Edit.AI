# Variações de criativo

A promessa do produto é produzir **muitas versões em minutos**. Esta skill produz versões bem feitas e **comparáveis**; ela **não promete** que um formato ou um gancho converta mais: quem diz isso é o teste.

## Regra de ouro: uma variável por vez

Mude **uma** coisa e mantenha o resto idêntico. Se o formato, o gancho e o CTA mudam juntos, o teste não diz qual deles fez a diferença.

| Eixo | O que varia | O que fica igual |
|---|---|---|
| **Formato** | o mesmo material em outro dos 15 formatos | a fala, a oferta, o CTA, a duração |
| **Ângulo do gancho** | dor, desejo, prova, curiosidade, mecanismo, mito, objeção, autoridade | o corpo, o CTA, o formato |
| **Tratamento visual do gancho** | prova primeiro, tela dividida, demonstração, texto em destaque, motion | a fala, o corpo, o CTA |
| **Edição** | ritmo (mais ou menos eventos), estilo da legenda, com ou sem música | a fala e a estrutura |
| **CTA** | o texto e o momento | todo o resto |
| **Duração** | versão curta e longa | gancho e CTA |

## Modo 1: o mesmo material em vários formatos

A pessoa manda **um material** e pede, por exemplo, "faz em 4 formatos".

1. **Escolha formatos de assinatura visual diferente** que o material permita (por exemplo, tela dividida, cinema, depoimento e react), em vez de 4 versões parecidas. Use as colunas "ideal quando" e "material mínimo" do `SKILL.md`.
2. **Mantenha a fala e o corte-base iguais** entre as versões; só o formato muda.
3. **Mesmo volume** em todas (referência −14 LUFS), mesma legenda de conteúdo.
4. **Renderize em lote** trocando só os props: uma composição, vários arquivos de props.
   `npx remotion render src/index.ts TelaDividida out/anuncio__tela-dividida.mp4 --props=props_tela.json`
   (um comando por versão; o mesmo para as outras composições).

## Modo 2: um corpo e vários ganchos

O **corpo** é fixo; cada **gancho** é um clipe separado (texto e visual, falado ou não).

1. **Defina os ganchos** com ângulos distintos (uma tabela: tipo, ângulo que testa, o que se fala, o que aparece nos 3 primeiros segundos, material). Uma primeira rodada com **3 a 5 ângulos diferentes** ensina mais que 10 do mesmo.
2. **Cheque a ponte:** leia as últimas palavras do gancho junto com as primeiras do corpo. Se a frase continua com sentido, siga; se quebra, avise e proponha outro fim para o gancho ou outro começo para o corpo.
3. **Junte** cada gancho ao corpo com a **emenda com sobreposição** (`cortes.md`): a imagem e o áudio do corpo entram juntos, antes de a fala do gancho acabar.
4. Se a skill `creative-lab` estiver disponível, use o `variar_ganchos.py` dela para juntar vários ganchos a um corpo (ela normaliza o volume e gera a matriz do teste). Se não, monte cada variante no Remotion com `Sequence`s e normalize o volume de todas para o mesmo alvo.

## Modo 3: variar a edição

Ritmo, legenda, música, duração: **uma coisa por vez**, e anote na matriz o que mudou e o que ficou igual.

## Matriz do teste

Uma tabela por rodada:

| Variante | Formato | Gancho (tipo e ângulo) | O que muda | O que não muda | Data de entrada | Hook rate | Hold rate | CTR | Observações |
|---|---|---|---|---|---|---|---|---|---|

- **Hook rate** = visualizações de 3 s ÷ impressões. Diz se o começo **parou o scroll**.
- **Hold rate** tem **definições diferentes** entre as fontes (por exemplo ThruPlays ÷ visualizações de 3 s, ou visualizações de 15 s ÷ visualizações de 3 s). **Escolha uma e use a mesma em todas as variantes.** Nenhum dos dois é uma coluna nativa das plataformas.
- Compare as variantes **sob as mesmas condições** (público, período, verba parecida) e espere impressões suficientes antes de concluir; esta skill não define esse número.

## Nome dos arquivos

`<anuncio>__<formato>__<gancho>.mp4`, em minúsculas e sem espaço, para a planilha ser legível meses depois. O nome descreve o **formato e o ângulo** ("tela-dividida", "prova"), não o número do arquivo.
