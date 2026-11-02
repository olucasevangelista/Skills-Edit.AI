# 01. Tela Dividida

**Também pedido como:** split screen, tela dividida, vídeo em duas partes.

## Assinatura visual

Duas áreas empilhadas com uma **divisória nítida**: a **pessoa falando embaixo** e a **prova em cima** (tela, resultado, produto, imagem), que **troca no instante em que a fala a cita**. O que o torna reconhecível é a metade de cima que se renova enquanto a metade de baixo, a pessoa, fica constante.

## Ideal quando

- Há **algo concreto para mostrar** enquanto a pessoa fala: uma tela de resultado, uma demonstração, um produto, um print, uma gravação.
- O gancho é "prova primeiro" ou "demonstração".
- App, ferramenta, e-commerce e infoproduto com prova real.

## Evite quando

- Não há **nada para mostrar** em cima: a área de cima vira um buraco ou um texto repetindo a fala.
- A fala é **emocional** e precisa do rosto em tela cheia (prefira Depoimento ou Cinema).
- A prova que existe é **fraca ou genérica**: a metade de cima expõe isso.

## Composição (1080x1920)

| Elemento | Posição e tamanho |
|---|---|
| **Área de cima** (conteúdo) | y de 0 a 960 (50%); pode ir de 45% a 55% da altura, **a mesma em todo o vídeo** |
| **Área de baixo** (pessoa) | y de 960 a 1920 |
| **Divisória** | linha de 6 a 8 px na cor de destaque, ou uma sombra suave de 24 px |
| **Rosto** | centro da cabeça em y ≈ 1100 a 1180, **cabeça inteira**, acima da zona de interface da base (a partir de ~1250) |
| **Legenda** | no **encontro das áreas** (y ≈ 900 a 1020), centralizada; nunca na base |
| **Título de gancho** | no topo da área de cima, y ≥ 270 |

- O vídeo da pessoa ocupa a área de baixo com `objectFit: cover`; um **zoom de 1,1 a 1,25** nessa área ajuda o rosto a ocupar o espaço.
- O conteúdo de cima usa `cover` quando a proporção combina e `contain` com **fundo desfocado** do próprio conteúdo quando não combina.

## Elementos e animações

- **Troca do conteúdo de cima** na palavra que ilustra: entrada de 0,2 s (deslize curto ou fade), **um conteúdo por vez**, cada um por 1,5 a 3 s.
- **Destaque dentro do conteúdo** (círculo ou seta em um botão, número em foco), para guiar o olho.
- Entrada do título com `pop` leve; sai antes do próximo texto.

## Cortes e ritmo

- Emendas da pessoa com **sobreposição** (`cortes.md`); a área de cima **não reinicia** a cada emenda, ela segue a fala.
- Evento novo em cima a cada **~1,5 a 2,5 s**; a área de cima parada por mais de ~3 s é lacuna.
- Em jump cuts, alterne o enquadramento da pessoa (1,0 e ~1,07).

## Texto e legenda

- Legenda palavra a palavra no encontro das áreas, com realce nos ★.
- Texto de ênfase sobre a área de cima (não sobre o rosto), curto, no máximo 6 palavras.

## Som

- Voz em primeiro plano; efeito curto (clique, whoosh) só nas trocas **grandes** de conteúdo; música opcional bem abaixo da voz.

## Materiais

- **Peça:** o vídeo da pessoa; as imagens, prints, gravações de tela ou vídeos do que ela cita.
- **Pode buscar sozinho:** b-roll ilustrativo, ícones, mockups de celular ou computador, logos de marcas citadas (identificação editorial), música e efeitos.
- **Nunca invente:** resultados, prints de clientes, números, telas de painel de vendas que não existem.

## Variações dentro do formato

- Proporção 50/50, 45/55 ou 55/45; pessoa embaixo ou em cima (uma por teste).
- Tipo do conteúdo de cima: gravação de tela, produto, texto grande, comparação.
- Estilo da divisória; velocidade das trocas; com e sem destaque.

## Armadilhas e checklist

- [ ] Rosto inteiro, no painel de baixo, acima da zona de interface.
- [ ] A divisória fica sempre no mesmo lugar.
- [ ] Cada conteúdo de cima entra na palavra que ilustra (±0,1 s) e tem relação direta com a fala.
- [ ] Nenhuma área de cima parada por mais de ~3 s.
- [ ] A legenda não cobre a boca nem vai para a base.
- [ ] O conteúdo mostrado é real.

## Kit

Composição **`TelaDividida`** (`kit/formatos/tela-dividida`). Props: `video`, `legendas`, `titulo`, `cores`, `fonte`, `duracaoS`, mais `conteudoSuperior` (lista de `{ src, tipo: "imagem" | "video", deS, ateS }`), `proporcao` (padrão 0.5) e `zoomPessoa` (padrão 1.12).

## Apoio

Se a skill `creative-lab` estiver disponível, use as regras de gancho e de retenção dela para decidir o que entra em cima; se a skill `smart-cuts` estiver disponível, use-a para escolher e emendar os trechos da pessoa.
