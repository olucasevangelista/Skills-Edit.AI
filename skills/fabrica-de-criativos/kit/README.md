# Kit Remotion da Fábrica de Criativos

Oito composições prontas e parametrizadas por props, para o agente **trocar os props e renderizar** em vez de escrever o formato do zero. É opcional: se a pessoa prefere montar do zero, ignore esta pasta.

| Composição | Formato | Props específicas (além das comuns) |
|---|---|---|
| `TelaDividida` | 01 | `conteudoSuperior` (lista `{ src, tipo, deS, ateS }`), `proporcao`, `zoomPessoa`, `origemPessoa` |
| `PostSocial` | 03 | `marca`, `texto`, `midia` (1 ou 2), `fundoCartao`, `alturaCartao` |
| `Noticia` | 04 | `marca`, `posicaoMarca`, `manchetes` (`{ texto, deS, ateS }`), `baseY`, `caixaS`, `textoAtrasoS`, `textoDurS`, `corCaixa`, `corTexto`, `tamanho`, `escurecer` |
| `Depoimento` | 07 | `identificacao`, `inserts` (`{ src, deS, ateS, legenda }`), `zooms` (`{ deS, ateS, escala }`), `zoomBase` |
| `React` | 08 | `conteudo`, `pausas`, `ampliacoes` (intervalos `{ deS, ateS }`), `rotuloOrigem`, `volumeConteudo` |
| `Chat` | 13 | `contato`, `mensagens` (`{ de, texto, imagem, tempoS, digitandoS }`), `avisoDramatizacao`, `narracao`, `tema` (a faixa do contato tem a largura da conversa e cantos arredondados; sem `titulo`) |
| `AntesDepois` | 14 | `antes`, `depois`, `modo` (`deslize`, `lado-a-lado`, `sequencia`), `revelarEmS`, `duracaoRevelacaoS`, `rotulos` |
| `Cinema` | 15 | `janela` (padrão quadrada, 984 x 984), `tratamento`, `musica`, `volumeMusica` |

**Props comuns** (`tipos.ts`, `PropsBase`): `video` (arquivo em `public/`), `takes` e `sobreposicaoS` (emendas com sobreposição), `titulo`, `cores`, `fonte`, `duracaoS` e `children` (uma camada por cima, veja abaixo).

## Como usar

1. Num projeto Remotion 4 com `remotion`, `@remotion/cli`, `@remotion/media`, `react` e `typescript` instalados, rode `python <skill>/scripts/instalar_kit.py <pasta do projeto>`. Ele copia o código para `src/fabrica/` e as **fontes e marcas** (`assets/`) para `public/fabrica/` (sem as fontes, o texto cai numa fonte do sistema).
2. Ponha os arquivos de mídia em `public/` (vídeos, imagens, música).
3. Veja `exemplo/props.ts`: ele traz props de exemplo para as oito composições. Copie o do formato escolhido para um JSON e troque os arquivos, os textos e os tempos.
4. Renderize:

```
npx remotion still src/fabrica/index.ts Cinema out/teste.png --frame=60 --props=props.json
npx remotion render src/fabrica/index.ts Cinema out/cinema.mp4 --props=props.json --codec=h264 --image-format=png
```

`--props` é mesclado sobre os `defaultProps` de `Root.tsx`; informe só o que muda. Tamanho 1080x1920, 30 quadros por segundo, e a duração vem de `duracaoS`.

## Trocar a marca (Post de Rede Social e Notícia)

Os dois formatos trazem o layout e a animação prontos, e a **marca é um prop**: `marca: { nome, letra, cor, logo }`. Ponha o **logo do SEU perfil ou veículo** (PNG, de preferência transparente) em `public/` e aponte `logo: "meu-logo.png"`; sem logo, o kit desenha um logotipo simples com a letra e o nome. O kit traz duas marcas prontas em `marcas.ts`: **`MARCA_CHOQUEI`** (o logo e o nome da página; o autor da skill informou que ela tolera o uso, o que **não foi verificado** e não é licença) e **`MARCA_NOTICIA`** (o veículo fictício "Cidade Hoje", sem logo). Não há logotipo de nenhum veículo de imprensa real, de propósito.

## Peças comuns (`componentes/`)

`Marca` (avatar e logotipo), com realce), `Takes` (emenda com sobreposição de imagem e áudio), `JanelaVideo` (vídeo em janela, com recorte, zoom e cantos), `Titulo`, `Tarja` e `Movimento` (curvas de animação; tudo é função do quadro, sem timers nem CSS animation).

## Legenda e outras camadas: ficam por sua conta

O kit **não traz legenda, estilo de legenda nem movimento de câmera**: a skill do Remotion já tem tudo isso, e o estilo certo muda de anúncio para anúncio. Cada composição aceita `children`, que é desenhado **por cima de tudo**; crie uma composição sua que embrulha a do kit e põe a legenda (os componentes de legenda do Remotion, com o `legendas.remotion.json` da transcrição):

```tsx
import { Noticia } from "./fabrica/formatos/noticia/Noticia";
export const MinhaNoticia: React.FC<PropsNoticia> = (props) => (
  <Noticia {...props}>{/* sua legenda aqui, no y indicado no arquivo do formato */}</Noticia>
);
```

As posições seguras da legenda de cada formato estão no arquivo dele em `references/formatos/` (tabela de composição). Em `assets/fontes` vêm só as duas fontes dos layouts (Montserrat no texto, Barlow Condensed na manchete da Notícia).

## Margens

`SEGURA` em `tipos.ts`: topo 270, base 670, lados 90 e direita 120 (1080x1920). Texto e rosto ficam dentro; fundos de mídia podem passar. São pontos de partida conservadores, confirme na plataforma.

## O que foi verificado

Versão testada: Remotion 4.0.535, Windows. `tests/verificar_kit.py <projeto>` copia o kit para o projeto, gera entradas sintéticas e confere: `tsc` e `eslint`; um quadro de cada composição (áreas, cores, janela quadrada do Cinema, cartão do Post, faixa do contato do Chat na largura da conversa e a entrada da manchete: caixa primeiro, texto cerca de 0,5 s depois); pausa e retomada do React; deslize do Antes e Depois; balões do Chat; zoom do Depoimento; margens do texto; formatos distintos entre si; determinismo; a emenda com sobreposição (imagem e áudio entram juntos antes do fim da voz anterior); e o fade final da trilha do Cinema.

Isso prova que a mecânica funciona com mídia sintética. **Não** prova que o resultado é bonito nem que performa como anúncio: confira os quadros com o material real.
