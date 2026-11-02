# 12. Tutorial de Tela

**Também pedido como:** tutorial de tela, screen recording, demonstração de tela, gravação de tela dinâmica.

## Assinatura visual

Uma **gravação de tela** transformada em demonstração **dinâmica e fácil de seguir**: **zooms nos pontos relevantes**, **destaques em botões, campos e menus**, **setas e indicadores de clique** e, opcionalmente, a tela **dentro de um mockup** de celular ou computador. A assinatura é o **olhar guiado**: a câmera vai até onde a ação acontece.

## Ideal quando

- O produto é **software, app ou ferramenta** e o anúncio **mostra o fluxo** (do clique ao resultado).
- Há uma **narração** (ou a pessoa fala enquanto grava) explicando cada passo.
- O resultado **aparece na tela** (um relatório pronto, um envio, um painel).

## Evite quando

- A tela é **confusa ou cheia de dados sensíveis** (nomes, e-mails, valores de clientes): **esconda ou desfoque** o que for pessoal.
- A demonstração é longa demais para o anúncio: encurte para o fluxo essencial.
- Não há como mostrar o resultado na tela.

## Composição (1080x1920)

| Elemento | Posição e tamanho |
|---|---|
| **Gravação de tela** | em um mockup de celular ou computador, **ou** em uma janela de ~984 de largura (cantos arredondados), centralizada, y ≈ 400 a ~1240 |
| **Zoom** | escala **1,6 a 2,4** com o centro na região de interesse; **a região inteira cabe** no quadro |
| **Destaque** | anel, retângulo ou realce em torno do botão ou campo; cor de destaque, 4 a 6 px |
| **Indicador de clique** | círculo que se expande onde o clique acontece (0,3 a 0,4 s) |
| **Seta** | aponta para o elemento citado, entra na palavra |
| **Legenda e texto explicativo** | acima do mockup (y ≈ 280 a 380) ou logo abaixo (y ≈ 1260 a 1320), nunca na base |

## Como posicionar os zooms

O Remotion **não detecta o cursor**: **você** posiciona os zooms.

1. Gere folhas de contato da gravação (`ffmpeg -i tela.mp4 -vf "fps=2,scale=400:-2,tile=6x4" folha_%02d.jpg`) e **olhe** onde está cada ação (clique, menu, campo).
2. Cruze com a **fala** (a transcrição com tempo) para saber **em que instante** cada elemento é citado.
3. Marque, para cada ação: **instante, centro do zoom (x, y em fração do quadro) e escala**.
4. Anime o zoom com uma **curva por chaves** (entrada suave em ~0,4 s, **repouso** na ação, volta ao quadro cheio quando muda de contexto). **Todo zoom volta ao neutro.**
5. Confira os quadros: a região certa está no centro, o texto fica legível, nada importante saiu da tela.

## Elementos e animações

- **Câmera que acompanha a ação**: o zoom se move de um ponto de interesse ao seguinte em vez de cortar.
- **Indicador de clique** no instante em que a ação acontece; **realce** do campo preenchido.
- **Mockup** (celular ou computador) desenhado por código, **genérico**.

## Cortes e ritmo

- **Corte as esperas** (carregamentos, pausas) com **aceleração** ou salto, e diga isso na tela se a espera existe de verdade ("acelerado").
- Evento novo (zoom, destaque, seta, texto) a cada **~1,5 a 2,5 s**.
- Se há a pessoa falando em cima, emenda com **sobreposição** (`cortes.md`).

## Texto e legenda

- **Texto explicativo** curto por passo ("1. conecta a conta"), no instante em que o passo acontece, **com o mesmo termo da fala**.
- Legenda palavra a palavra se há narração.

## Som

- Narração em primeiro plano; **cliques sutis** nos indicadores (opcional); música bem baixa ou nenhuma.

## Materiais

- **Peça:** a **gravação de tela** e a **narração**, se houver; as informações a esconder.
- **Pode buscar sozinho:** mockups genéricos (por código), ícones, sons de clique, fonte, música.
- **Nunca invente:** um resultado na tela que o produto não gera, números de painéis, dados de clientes.

## Variações dentro do formato

- Com e sem mockup (celular, computador, nenhum); escala do zoom.
- Tipo de destaque (anel, retângulo, seta); com e sem indicador de clique.
- Velocidade (acelerar ou não as esperas).

## Armadilhas e checklist

- [ ] Dados pessoais e sensíveis estão **ocultos**.
- [ ] Os zooms centralizam a região certa e **voltam** ao quadro cheio.
- [ ] O texto na tela é legível em tamanho de celular.
- [ ] A aceleração das esperas está indicada.
- [ ] O resultado final está **visível** pelo tempo de ser lido.

## Kit

Sem kit nesta versão. Use `kit/componentes` (`Legenda`, `Movimento` para a curva `track`, `JanelaVideo`).

## Apoio

Se a skill `motion-designer` estiver disponível, use-a para as setas e destaques animados; se a `creative-lab` estiver disponível, use as regras de resultado e de mecanismo dela.
