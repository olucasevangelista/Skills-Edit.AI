# 11. Telejornal

**Também pedido como:** jornal nacional, telejornal, noticiário, âncora, estúdio de jornal.

## Assinatura visual

Estética de **telejornal tradicional, mais formal e estruturada que a Notícia (formato 04)**: um **cenário inspirado em estúdio jornalístico**, o **apresentador enquadrado como âncora**, uma **vinheta de abertura**, **tarjas** com manchetes e **painéis** com imagens de apoio. O ritmo é de apresentação, não de rede social.

## Ideal quando

- O anúncio quer **autoridade e seriedade** sobre um fato, um relatório de uma oferta ou uma novidade **verdadeiros**.
- Há um **apresentador** (a pessoa do anúncio ou um ator identificado como encenação) e um **roteiro** em tom de matéria.
- Há **imagens de apoio** reais para os painéis.

## Evite quando

- O anúncio **simularia ter sido transmitido ou endossado por um telejornal real**: isso é enganoso e pode ser ilegal como publicidade disfarçada. A identidade deve ser **própria**.
- A "matéria" seria uma notícia **inventada**.
- A plataforma ou a lei exige a identificação do anúncio e a pessoa não vai colocá-la.

## Composição (1080x1920)

| Elemento | Posição e tamanho |
|---|---|
| **Cenário** | estúdio **genérico** gerado por código: fundo escuro com painéis de luz e uma tela ao fundo (sem a estética identificável de um canal real) |
| **Apresentador** | enquadrado na altura do peito, **cabeça inteira em y ≈ 600 a 900**, centralizado ou levemente deslocado |
| **Vinheta de abertura** | 2 a 3 s, **com nome de programa próprio ou do anunciante**, em movimento de câmera e luz |
| **Tarja de manchete** | y ≈ 1000 a 1160, com o título e uma linha de apoio, **acima da base** |
| **Painel de apoio** | uma janela ao lado ou atrás da pessoa (imagens, vídeo, gráfico), y ≈ 330 a ~800 |
| **Legenda** | y ≈ 1170 a 1240, discreta |

## Elementos e animações

- **Vinheta própria** (curta); **tarjas** que entram com deslize e saem com o assunto; **painéis** que trocam na palavra.
- **Relógio, nome da "edição" ou ticker** são opcionais e **inventados ou do anunciante**.
- **Transições** de apresentação (corte, deslize, fusão) sem efeitos de rede social.

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
- [ ] A tarja fica acima da base e o rosto está inteiro.
- [ ] O ritmo é formal sem lacunas.

## Kit

Sem kit nesta versão. Monte com `kit/componentes` (`Tarja`, `Titulo`, `JanelaVideo`, `Legenda`, `Movimento`).

## Apoio

Se a skill `creative-lab` estiver disponível, use a `conformidade.md` dela; se a `motion-designer` estiver disponível, use-a para a vinheta e para os gráficos animados.
