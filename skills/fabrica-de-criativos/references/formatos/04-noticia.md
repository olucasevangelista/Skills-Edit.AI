# 04. Notícia

**Também pedido como:** notícia, flash de notícia, urgente, manchete.

## Assinatura visual

Estética de **notícia rápida de rede social**: o **vídeo da pessoa em tela cheia**, **etiquetas no topo** (plantão, nome do veículo, aviso de publicidade) e a **manchete numa caixa branca** (texto preto, caixa alta, fonte condensada e pesada) com uma etiqueta pequena ("urgente") acima. Informal, mais solta que um telejornal (o formato 11 é o formal).

## Ideal quando

- O anúncio parte de **um fato, dado ou novidade verdadeiros** do nicho ("saiu", "mudou", "descobriram") e a manchete sustenta o que vem depois.
- Há **imagens ou vídeos de apoio** relacionados.
- Quer-se energia e urgência **reais**.

## Evite quando

- A "notícia" seria **inventada** ou imitaria uma matéria de **veículo real**: isso é enganoso, arrisca a conta e pode ser ilegal como publicidade disfarçada.
- O conteúdo é uma oferta comum sem nenhum fato novo: a manchete forçaria uma urgência que não existe.
- A plataforma ou a lei de publicidade exige a identificação do anúncio e a pessoa não vai colocá-la.

## Composição (pontos de partida, 1080x1920)

| Elemento | Como pensar (no exemplo do autor) |
|---|---|
| **Vídeo** | tela cheia, **levantado ~100 a 130 px** para a manchete cair no **peito**, não no rosto |
| **Legibilidade** | degradê escuro em cima (~380 px) e embaixo (~760 px) da imagem, para as etiquetas e a manchete lerem em qualquer fundo |
| **Etiqueta de plantão** | canto superior **esquerdo** (x ≈ 70, y ≈ 290): uma etiqueta vermelha com um ponto que pisca (~1 vez por segundo) e a palavra "plantão" |
| **Nome do veículo e publicidade** | canto superior **direito**: o nome do veículo numa caixa branca (texto na cor da marca) e, logo abaixo, o aviso **"publicidade"** pequeno, com borda |
| **Manchete** | uma **caixa branca com margem de segurança da borda** (**x de 90 a 960**), com o texto preto em caixa alta, condensado e pesado, 2 a 3 linhas, recuado ~36 px dentro da caixa; a borda de baixo fica **acima de y ≈ 1250**. O texto pode ficar um pouco menor (~64 a 76 px) por causa da margem; isso não é problema |
| **Etiqueta "urgente"** | **colada no canto superior esquerdo da caixa**, em uma cor viva da marca, em caixa alta com letras espaçadas |
| **Legenda** | **este formato costuma dispensar legenda**: menos informação, mais leitura da manchete |
| **Rodapé/ticker** (opcional) | faixa fina em y ≈ 1200 a 1250, não na base |

**Margem de segurança:** o exemplo do autor tem a caixa colada na borda esquerda da tela, mas **a decisão é deixar uma margem**, porque é mais seguro com a interface das plataformas, mesmo que o texto fique um pouco menor. Uma caixa encostada na borda só se a pessoa pedir.

**Nome do veículo:** use um nome **fictício e próprio**, por exemplo o **nome do anunciante + "News"** ("[Marca] News"). **Nunca** o nome, o logotipo ou a vinheta de um veículo de imprensa real: veículos conhecidos são sérios e identificáveis, e imitá-los é enganoso.

## Elementos e animações

- **Entrada da manchete (duas opções):** (a) a faixa inteira desliza da esquerda em ~0,5 s e sai para a esquerda; (b) a caixa branca é revelada da esquerda para a direita e o texto vem logo depois, terminando cerca de 0,5 s depois da caixa.
- **A manchete troca conforme a fala**, a cada 3 a 6 s, dizendo só o que o vídeo sustenta.
- **Cortes rápidos e transições simples** (corte, deslize curto). Sem vinheta de abertura longa.
- Sem efeitos sonoros obrigatórios; um "blip" discreto na entrada da manchete é opcional.

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

- Caixa branca com texto preto, ou tarja de cor viva com texto branco; etiquetas no topo à esquerda, à direita ou centradas.
- Com e sem ticker; com e sem legenda; imagens de apoio entre as manchetes.
- A manchete (o ângulo do fato) e quantas vezes ela troca.

## Armadilhas e checklist

- [ ] A manchete é **verdadeira** e o anúncio a sustenta.
- [ ] Nenhum logotipo, nome ou vinheta de veículo de imprensa real; o nome é fictício e próprio ("[Marca] News").
- [ ] Há um aviso de **publicidade** quando necessário, e a pessoa conferiu as políticas atuais.
- [ ] A tarja não cobre o rosto; o texto está dentro das margens.
- [ ] Nada de urgência fabricada ("urgente" só se for).

## Estruturas e exemplos

**Código para reaproveitar:** `assets/componentes/MancheteNoticia.tsx` é a manchete (caixa branca, texto em caixa alta, etiqueta opcional) como componente do Remotion, com as duas entradas (revelação da esquerda para a direita e deslize) e a caixa como um retângulo único encostado na borda esquerda, como no exemplo (a prop `x` a recua para as margens; `forma: "linhas"` dá uma caixa por linha). **Copie e ajuste**; é uma peça, não um editor: o vídeo, as etiquetas do topo, a legenda e o resto continuam sendo seus. Testado: compila e a caixa entra antes do texto, que termina ~0,5 s depois.

Quadro de demonstração: `references/exemplos/04-noticia.jpg` (manchete em caixa branca, etiquetas no topo, sem legenda). Mistura bem com tela cheia: use a manchete como gancho e passe para outro modo, ou deixe a faixa voltar nos pontos de virada.

## Apoio

Se a skill `creative-lab` estiver disponível, use a `conformidade.md` e as regras de gancho dela; se a `smart-cuts` estiver disponível, use-a para os cortes.
