# 11. Telejornal

**Também pedido como:** jornal nacional, telejornal, noticiário, âncora, estúdio de jornal.

## Assinatura visual

Estética de **telejornal**, mais formal e estruturada que a Notícia (formato 04): um **estúdio ilustrado** (degradê com **globos de linhas** translúcidos e feixes de luz), um **título de bancada** ("notícia" em letras cromadas e "urgente" numa placa) com o aviso de **publicidade**, uma **faixa do meio** que mostra, em imagens e gráficos, o que está sendo dito, e o **apresentador grande embaixo**. O ritmo é de apresentação, não de rede social.

## Ideal quando

- O anúncio quer **autoridade e seriedade** sobre um fato, um relatório de uma oferta ou uma novidade **verdadeiros**.
- Há um **apresentador** (a pessoa do anúncio ou um ator identificado como encenação) e um **roteiro** em tom de matéria.
- Há **imagens de apoio** reais para os painéis.

## Evite quando

- O anúncio **simularia ter sido transmitido ou endossado por um telejornal real**: isso é enganoso e pode ser ilegal como publicidade disfarçada. A identidade deve ser **própria**.
- A "matéria" seria uma notícia **inventada**.
- A plataforma ou a lei exige a identificação do anúncio e a pessoa não vai colocá-la.

## Composição (pontos de partida, 1080x1920)

Medidas do exemplo do autor; ajuste ao seu criativo.

| Elemento | Como pensar |
|---|---|
| **Cenário** | **gerado por código** e genérico: um degradê (a cor é da marca ou do tema), **dois globos de linhas grandes e translúcidos** girando devagar (um no alto à direita, outro embaixo à esquerda, de modo que o apresentador fique na frente) e **feixes de luz diagonais** que oscilam um pouco |
| **Título** | no topo, centralizado (y ≈ 280 a 500): "NOTÍCIA" em letras cromadas e itálicas (~76 px) e "URGENTE" (~120 px) numa **placa vermelha** com borda clara; entra com um pop curto (~0,5 s) e **fica o vídeo todo** |
| **Aviso** | "PUBLICIDADE", pequeno e com borda, à direita do título |
| **Faixa do meio** | y ≈ 545 a 1015 (~470 px): fundo escurecido com **linhas finas em cima e embaixo**; no canto superior esquerdo um **rótulo da seção** (uma pílula, por exemplo "GESTORES DE TRÁFEGO"); dentro, **o que a fala descreve**: cartões ou miniaturas que surgem em sequência, um diagrama que se constrói, pontos de interrogação. Troca a cada cena (~2 a 6 s) |
| **Apresentador** | **grande, na metade de baixo**: cabeça em y ≈ 1010 a 1350. No exemplo ele é **recortado do fundo** e fica sobre o cenário; sem recorte, uma janela larga embaixo também serve |
| **Legenda** | abaixo da faixa, sobre o apresentador, **acima da zona de interface da base** (confira: nos quadros do exemplo ela ficou mais baixa) |
| **Vinheta de abertura** | **opcional**: o exemplo não tem; o título de bancada já faz esse papel |

## Elementos e animações

- **Cenário vivo, mas discreto:** os globos giram devagar (meridianos que se estreitam e alargam com o giro) e os feixes de luz oscilam. Tudo é função do tempo.
- **Título** com pop curto; **cartões** da faixa do meio entram com escala e fade, um de cada vez, **na palavra** que os cita; um **diagrama** pode se desenhar (um nó, linhas saindo dele, caixas com texto).
- **Rótulo da seção** muda a cada cena.
- **Sem efeitos sonoros**: só a voz do apresentador. Transições de apresentação (corte, fusão), sem efeitos de rede social.
- **Relógio, ticker ou nome da edição** são opcionais e **inventados ou do anunciante**.

## Cortes e ritmo

- Ritmo **mais calmo** que o da Notícia, mas sem lacuna: evento novo (tarja, painel, zoom) a cada **~2,5 s**.
- Emendas com **sobreposição** (`cortes.md`); a abertura e o fecho têm tempo de respiro.

## Texto e legenda

- Manchetes **verdadeiras e sustentadas pelo anúncio**; tom formal.
- Legenda palavra a palavra discreta.
- **Aviso de publicidade** quando fizer sentido (e conferido pela pessoa).

## Som

- Voz do apresentador em primeiro plano; **vinheta sonora própria** curta; música de apresentação **bem abaixo** da voz ou nenhuma.

## Materiais

- **Peça:** o vídeo do apresentador, o **roteiro**, as imagens de apoio **reais**, o **nome do programa** que quer usar.
- **Pode buscar sozinho:** o cenário (gerado por código), vinheta e sons próprios, fontes, imagens de apoio com licença clara.
- **Nunca invente:** a transmissão, o endosso, a reportagem, pesquisas e números, nem use o **nome, o logotipo ou a vinheta de um programa ou veículo real**.

## Variações dentro do formato

- Com e sem vinheta; tom do cenário; posição do painel de apoio.
- Duração da abertura; quantidade de tarjas.
- O ângulo da manchete.

## Armadilhas e checklist

- [ ] A identidade é **própria**; nada de nome, logotipo ou vinheta de veículo real.
- [ ] A "matéria" é **verdadeira** e o anúncio a sustenta.
- [ ] Há um aviso de publicidade quando necessário, e a pessoa conferiu as **políticas atuais**.
- [ ] O título e a faixa do meio ficam acima da base; o rosto está inteiro.
- [ ] O ritmo é formal sem lacunas.

## Estruturas e exemplos

**Código para reaproveitar:** `assets/componentes/EstudioTelejornal.tsx` traz o **cenário** (degradê, feixes de luz e dois globos de linhas girando) e o **título de bancada** (linha cromada sobre uma placa) como componentes do Remotion. **Copie e ajuste**: são peças, não um editor; o apresentador, a faixa do meio, os cartões, a legenda e a composição são seus. As cores padrão (azul e vermelho) são as do exemplo do autor e **trocam por props**; os globos e os feixes podem sair. Testado: compila, o degradê aparece, o cenário se mexe e o título renderiza.

Quadro de demonstração: `references/exemplos/11-telejornal.jpg`. É a estrutura descrita acima (estúdio ilustrado com globos, título "notícia urgente" com aviso de publicidade, faixa do meio com imagens e um diagrama que se constrói, apresentador grande embaixo, legenda). **As cores (o azul), o globo e o desenho dos cartões são escolhas do autor**: adapte ao tema e à marca. A "matéria" diz só o que a fala diz, sem número, pesquisa ou fonte inventados, e a identidade é própria. Combina bem com a **pessoa recortada** (formato 02) para ficar na frente do cenário.

## Apoio

Se a skill `creative-lab` estiver disponível, use a `conformidade.md` dela; se a `motion-designer` estiver disponível, use-a para a vinheta e para os gráficos animados.
