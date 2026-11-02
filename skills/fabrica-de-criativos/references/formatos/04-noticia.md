# 04. Notícia

**Também pedido como:** notícia, flash de notícia, urgente, manchete.

## Assinatura visual

Estética de **notícia rápida de rede social**: o **vídeo em tela cheia**, o **logotipo do veículo no topo** e a **manchete numa caixa branca** (texto preto em caixa alta, fonte condensada e pesada) que **entra da esquerda para a direita**: **primeiro a caixa**, e o **texto logo depois, terminando cerca de 0,5 s depois da caixa**. Informal, mais solta que um telejornal (o formato 11 é o formal). Variação: a tarja de cor viva com texto branco.

## Ideal quando

- O anúncio parte de **um fato, dado ou novidade verdadeiros** do nicho ("saiu", "mudou", "descobriram") e a manchete sustenta o que vem depois.
- Há **imagens ou vídeos de apoio** relacionados.
- Quer-se energia e urgência **reais**.

## Evite quando

- A "notícia" seria **inventada** ou imitaria uma matéria de **veículo real**: isso é enganoso, arrisca a conta e pode ser ilegal como publicidade disfarçada.
- O conteúdo é uma oferta comum sem nenhum fato novo: a manchete forçaria uma urgência que não existe.
- A plataforma ou a lei de publicidade exige a identificação do anúncio e a pessoa não vai colocá-la.

## Composição (1080x1920)

| Elemento | Posição e tamanho |
|---|---|
| **Fundo** | o vídeo ou a imagem em **tela cheia**; um leve escurecido no topo (~30%) para o logotipo ler |
| **Logotipo** | no topo, centralizado (ou à esquerda), em y ≈ 290; ~84 px de altura. O kit traz um veículo **fictício pronto**: **Cidade Hoje**, um "C" vermelho com o nome em caixa alta (`MARCA_NOTICIA` em `kit/marcas.ts`; o nome não foi pesquisado em registro de marcas, troque se quiser). Para usar outro, ponha o **logo do SEU veículo ou perfil** |
| **Manchete** | caixa branca com texto preto em caixa alta, corpo de 56 a 68 px, até **3 linhas**, **x entre 90 e 960**, com a **borda de baixo em y ≈ 1220** (a manchete cresce para cima) |
| **Tarja secundária** | opcional, uma faixa menor de cor escura ou de apoio com a fonte ou o complemento |
| **Legenda** | y ≈ 780, acima da manchete, nunca na base |
| **Rodapé/ticker** (opcional) | uma faixa fina em y ≈ 1200 a 1250, **não** na base |

## Elementos e animações

- **Entrada da manchete (o tempo faz parte do formato):** a caixa branca cresce da esquerda para a direita em ~0,3 s; o texto começa a aparecer quando a caixa ainda está entrando (~0,13 s) e **termina ~0,5 s depois de a caixa terminar**. A revelação do texto é linear, para o olho perceber a varredura. Saída em fade curto.
- **Manchetes que trocam** com o assunto, cada uma com a mesma entrada.
- **Cortes rápidos e transições simples** (corte, deslize curto). Sem vinheta de abertura longa.
- **Identidade própria:** o logotipo e o nome são **os do SEU veículo, perfil ou marca**, sem o logotipo, o nome ou a vinheta de um veículo de imprensa real (por exemplo, portais e telejornais conhecidos): ele é sério, é identificável e imitá-lo é enganoso.

## Cortes e ritmo

- Emenda com **sobreposição** (`cortes.md`); evento novo a cada **~1,5 a 2 s**, é um formato rápido.
- A manchete fica **2 a 4 s** no começo e pode voltar atualizada no meio.

## Texto e legenda

- A manchete **diz só o que o anúncio sustenta**, sem inventar um "fato".
- Legenda palavra a palavra com realce nos números.
- Aviso de **publicidade** quando fizer sentido (e conferido pela pessoa).

## Som

- Voz em primeiro plano; efeito curto na entrada da manchete (um "blip" ou whoosh discreto); música de tensão leve, bem abaixo, opcional.

## Materiais

- **Peça:** o vídeo principal, a **manchete** e os materiais de apoio **reais**.
- **Pode buscar sozinho:** imagens e vídeos de apoio com licença clara, ícones, sons de transição, fonte, música.
- **Nunca invente:** a notícia, a pesquisa, a fonte, o veículo, uma matéria real ou uma citação de autoridade.

## Variações dentro do formato

- Caixa branca com texto preto, ou tarja de cor viva com texto branco; logotipo no centro ou à esquerda.
- Com e sem ticker; mais ou menos imagens de apoio entre as manchetes.
- A manchete (o ângulo do fato) e quantas vezes ela troca.

## Armadilhas e checklist

- [ ] A manchete é **verdadeira** e o anúncio a sustenta.
- [ ] Nenhum logotipo, nome ou vinheta de veículo real; a identidade é própria.
- [ ] Há um aviso de **publicidade** quando necessário, e a pessoa conferiu as políticas atuais.
- [ ] A tarja não cobre o rosto; o texto está dentro das margens.
- [ ] Nada de urgência fabricada ("urgente" só se for).

## Kit

Composição **`Noticia`** (`kit/formatos/noticia`): o logotipo e a manchete animada já prontos, **basta trocar a marca, o vídeo e as manchetes**. Props: `video` (em tela cheia; pode ser uma imagem), `marca` (`{ nome, letra, cor, logo }`, o seu veículo; o `logo` é um arquivo em `public/`), `posicaoMarca`, `manchetes` (lista de `{ texto, deS, ateS }`), e opcionais `baseY`, `caixaS`, `textoAtrasoS`, `textoDurS`, `corCaixa`, `corTexto`, `tamanho`, `escurecer`, `legendas`, `yLegenda`. Sem `logo`, o logotipo é um quadrado com a letra e o nome.

## Apoio

Se a skill `creative-lab` estiver disponível, use a `conformidade.md` e as regras de gancho dela; se a `smart-cuts` estiver disponível, use-a para os cortes.
