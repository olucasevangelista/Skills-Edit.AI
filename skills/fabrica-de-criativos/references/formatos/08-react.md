# 08. React

**Também pedido como:** react, reação, vídeo reagindo a outro vídeo.

## Assinatura visual

**Dois vídeos empilhados**: o **conteúdo comentado em cima** e a **pessoa reagindo embaixo**. A assinatura é a **sincronia**: o conteúdo **pausa** quando a pessoa comenta, **amplia** quando precisa ser visto de perto e **volta** a rodar. Parece uma conversa entre a pessoa e o que ela está vendo.

## Ideal quando

- A pessoa vai **comentar, rebater ou explicar** um trecho de vídeo, uma publicação, uma notícia ou uma tela.
- O argumento é "olha o que estão dizendo e olha a verdade" (mito, erro comum, comparação).
- Há **material de terceiros que a pessoa tem direito de usar** ou conteúdo próprio.

## Evite quando

- O conteúdo comentado é de **terceiro sem autorização**: usar o vídeo de outra pessoa em **anúncio pago** pode exigir permissão e licença, e "estou só comentando" não garante nada. Peça à pessoa que confirme os direitos.
- Não há um conteúdo para reagir: a área de cima fica vazia.
- A reação seria **desonesta** (cortar a fala do outro para mudar o sentido).

## Composição (1080x1920)

| Elemento | Posição e tamanho |
|---|---|
| **Conteúdo comentado** (cima) | y de 0 a 960 (50%); passa a **~65 a 70%** (0 a ~1280) enquanto está **ampliado** |
| **Pessoa reagindo** (baixo) | y de 960 a 1920; cabeça inteira, centro em y ≈ 1100 a 1180 |
| **Divisória** | linha de 6 a 8 px; a transição de tamanho dura 0,3 a 0,4 s com curva `inOut` |
| **Legenda** | no encontro das áreas, só da **pessoa que reage** (a do conteúdo, se houver, fica pequena e dentro da área de cima) |
| **Rótulo de origem** | uma etiqueta pequena na área de cima ("vídeo original", "fonte: ..."), dentro da zona segura |

## Elementos e animações

- **Pausa do conteúdo** (`Freeze`): quando a pessoa comenta, o conteúdo para no quadro; ao terminar o comentário, retoma **do mesmo ponto**.
- **Ampliação temporária** do conteúdo quando há um detalhe a ver (texto pequeno, uma expressão); depois volta a 50%.
- **Destaque** no conteúdo (círculo, seta, zoom) na palavra que a pessoa diz.
- Reações curtas (um olhar, uma risada) podem ganhar um **punch-in** discreto no painel de baixo.

## Cortes e ritmo

- Cortes que **preservam o contexto**: não corte a fala do conteúdo no meio do que ela quer dizer, nem a reação antes do comentário terminar.
- A pessoa de baixo é emendada com **sobreposição** (`cortes.md`); o conteúdo de cima segue o seu próprio tempo, com as pausas e retomadas.
- Evento novo (ampliação, destaque, texto) a cada **~2 a 3 s**; as pausas e retomadas contam como eventos.

## Texto e legenda

- Legenda palavra a palavra da **pessoa**, com realce nos ★.
- Texto de apoio só para **dados de origem** ou uma correção curta ("na verdade: ..."); curto, em cima ou no encontro, nunca sobre o rosto.

## Som

- Quando o conteúdo roda, o seu áudio vai a **~40 a 50% do volume da voz da pessoa**; quando a pessoa fala, o do conteúdo **cai para um fio** ou **silencia** (a voz da pessoa é sempre a mais forte).
- Efeito curto nas pausas e ampliações (opcional). Sem música por cima de dois áudios competindo.

## Materiais

- **Peça:** o conteúdo comentado (o vídeo, a publicação, a tela) e a gravação da reação.
- **Pode buscar sozinho:** ícones, setas, efeitos, música, a fonte e o nome do conteúdo para o rótulo (**se a pessoa disser qual é**).
- **Nunca invente:** um conteúdo que não existe, um comentário atribuído a alguém real, ou a fala de um terceiro.

## Variações dentro do formato

- Quantas pausas, e se o conteúdo amplia ou não.
- Tamanho da área do conteúdo (50% ou 60%); pessoa em cima ou embaixo.
- Com e sem destaque; com e sem rótulo de origem.

## Armadilhas e checklist

- [ ] Os **direitos do conteúdo comentado** foram confirmados pela pessoa.
- [ ] O conteúdo retoma do mesmo ponto depois de uma pausa.
- [ ] A voz da pessoa está sempre acima do áudio do conteúdo.
- [ ] A legenda não cobre o conteúdo nem a boca.
- [ ] O sentido do conteúdo original **não foi alterado** pelos cortes.

## Estruturas e exemplos

Sem quadro de exemplo ainda. Estrutura por descrição: o conteúdo comentado ocupa uma parte da tela e **para** (e cala) quando a pessoa comenta, retomando do mesmo ponto; a pessoa reage na outra parte; o conteúdo pode **crescer** quando precisa ser visto de perto. Se a pessoa mandar uma referência, adicione um quadro em `references/exemplos/`.

## Apoio

Se a skill `smart-cuts` estiver disponível, use-a para limpar a gravação da reação; se a `creative-lab` estiver disponível, use as regras de gancho dela para a abertura.
