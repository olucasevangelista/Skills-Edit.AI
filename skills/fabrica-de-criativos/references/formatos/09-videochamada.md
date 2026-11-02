# 09. Videochamada

**Também pedido como:** google meet, videochamada, chamada de vídeo, reunião, call.

## Assinatura visual

A conversa dentro de uma **interface de videochamada genérica**: **participantes em quadros separados**, **ícones de microfone, câmera e controles**, **destaque de quem está falando** e alternância de enquadramentos. A assinatura é a **moldura de reunião**: parece uma ligação real acontecendo.

## Ideal quando

- Existe uma **conversa gravada de verdade** entre duas ou mais pessoas (um cliente e o suporte, uma mentoria, uma consultoria, uma entrevista).
- A mensagem é uma **troca** (pergunta e resposta, dúvida e solução).
- Quer-se uma estética de **acesso e proximidade**.

## Evite quando

- A chamada seria **encenada e apresentada como real**: **encenação deve ser indicada** (aviso de dramatização), e os "participantes" não podem ser passados por clientes reais.
- Os participantes **não autorizaram** o uso da imagem no anúncio.
- Existe uma só pessoa: use Depoimento ou Cinema.

## Composição (1080x1920)

| Elemento | Posição e tamanho |
|---|---|
| **Fundo da chamada** | cor escura lisa (ou clara), sem logotipo de aplicativo |
| **2 participantes** | **dois quadros empilhados** de ~984 x ~450, y de ~330 a ~780 e de ~800 a ~1250, cantos de ~20 px |
| **Mais participantes** | grade 2 x 2 de quadros menores, ou **um quadro grande e os outros em miniaturas** |
| **Rótulo de nome** | pílula pequena no canto inferior esquerdo de cada quadro |
| **Indicador de fala** | contorno na **cor de destaque** (3 a 4 px) no quadro de quem fala, que **muda de lugar** com a fala |
| **Ícones** | microfone e câmera discretos em cada quadro; uma barra de controles genéricos (opcional), y ≈ 1180 a 1250 |
| **Legenda** | no encontro dos quadros ou sobre o quadro de quem fala, sem cobrir a boca |

## Elementos e animações

- **Quem fala** ganha o contorno e, em trechos longos, um quadro **maior** (animado em 0,3 s).
- **Entrada na chamada:** os quadros aparecem em sequência (opcional).
- **Alternância de enquadramentos** com zooms discretos no rosto de quem fala.
- **Sem logotipo, cores ou ícones característicos de um aplicativo real.**

## Cortes e ritmo

- Cortes e emendas por **fala**, com **sobreposição** (`cortes.md`); o indicador de quem fala troca no instante da fala.
- Evento novo (troca de quem fala, ampliação, texto, insert) a cada **~2 a 3 s**.

## Texto e legenda

- Legenda palavra a palavra de quem fala, com realce nos ★; **o rótulo do nome** só com o nome que a pessoa autorizou.

## Som

- As falas em primeiro plano, **niveladas entre os participantes** (volumes iguais); ruído de sala reduzido sem alterar o timbre; música opcional bem baixa; um som discreto de entrada na chamada (opcional).

## Materiais

- **Peça:** a **gravação da conversa** (ou os vídeos reais dos participantes), com **autorização** de imagem; os nomes que podem aparecer.
- **Pode buscar sozinho:** ícones, sons discretos, fonte, música.
- **Nunca invente:** participantes, uma conversa que não aconteceu apresentada como real, falas atribuídas a quem não as disse.

## Variações dentro do formato

- Disposição (empilhado, grade, um grande e miniaturas); tema claro ou escuro.
- Com e sem barra de controles; com e sem contorno de quem fala.
- Quanto tempo cada participante fica em destaque.

## Armadilhas e checklist

- [ ] Todos os participantes **autorizaram** a imagem.
- [ ] Se for encenação, há o aviso de **dramatização**.
- [ ] Nenhum logotipo ou identidade de aplicativo real.
- [ ] O indicador acompanha a fala.
- [ ] Os volumes das falas estão equilibrados.

## Kit

Sem kit nesta versão. Monte com `kit/componentes` (`JanelaVideo`, `Legenda`, `Tarja`, `Movimento`).

## Apoio

Se a skill `smart-cuts` estiver disponível, use-a para escolher os trechos da conversa e emendá-los; se a `creative-lab` estiver disponível, use as regras de gancho e de conformidade dela.
