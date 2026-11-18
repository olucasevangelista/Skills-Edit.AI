# Áudio

O som decide se o motion parece pronto. Em toda peça existe a **direção de áudio** (abaixo). Como o som é obtido é uma escolha da pessoa.

## Direção de áudio (sempre)

**Mapa de som.** Uma tabela de cada instante da animação com o que toca, escrita antes do código:

| Tempo | Movimento | Som |
|---|---|---|
| 0,0 s | entrada do gancho | batida inicial e um toque agudo |
| 3,9 s | etapa 1 | clique |
| 7,9 s | objeto sai de cena | whoosh curto |
| 9,7 s | marca assenta | acorde |
| fim | encerramento | resolução e fade nos últimos 0,7 s |

**Grade de batidas.** Se há trilha, os eventos grandes caem na batida. A 120 BPM uma batida dura 0,5 s, ou **15 quadros a 30 fps** (60 quadros a 120 BPM por compasso de 4). Calcule os instantes em quadros e coloque no `config.ts`.

**Mistura.**

- A **voz** (narração ou fala) sempre em primeiro plano. Trilha bem abaixo dela, em torno de 20 dB. Sem voz, a trilha pode ocupar mais espaço.
- **Efeitos sonoros curtos** nos eventos grandes, em volume baixo. Som em todo evento pequeno cansa.
- **Fade** nos últimos 0,5 a 0,7 s da trilha; o corte seco no final da peça parece erro.
- O som e a imagem terminam juntos: nada de música depois do último quadro.

## Som por evento (peça inteira)

Num motion explicativo dentro de um vídeo com pessoa, o som costuma ser só a locução e, no máximo, um efeito aqui e ali: o mapa de som acima basta. Numa **peça inteira** (anúncio, conteúdo, vinheta feitos só de motion), o som tem dezenas de momentos, e os instantes digitados à mão ficam errados na primeira vez que a animação muda de ritmo. Por isso o som **lê os mesmos instantes que a animação**.

1. O `config.ts` exporta `EVENTOS`: nomes de momentos e o instante de cada um em segundos, **um por linha, com número literal** (`"etapa.separa": 3.9,`). A animação usa esses instantes (`sec(EVENTOS["etapa.separa"], fps)`), e as cenas derivadas deles. Inclua também os momentos derivados: cada passo de uma sequência, cada pouso, cada pulso, cada palavra que entra.
2. O mapa de som aponta para o **nome** do evento (`"evento": "etapa.separa"`), com um `"deslocamento"` em segundos só para um ajuste fino. Nunca escreva um instante à mão. Mudou um tempo? A animação e o som se movem juntos.
3. Peça ao `sintetizar.py` que leia a lista do projeto e encaixe cada som no quadro: `python <skill>/kit/audio/sintetizar.py mapa.json --saida audio --eventos config.ts --fps 30`. Ele imprime cada evento com o instante e o quadro, e para com o erro claro se um nome não existir.
4. Se os sons vêm de uma biblioteca da pessoa e entram no Remotion, o ponto forte de um arquivo quase nunca está no primeiro instante. Meça: `python <skill>/kit/audio/ataque.py sons/*.wav`. O arquivo deve **começar `ponto` segundos antes do evento**, para o ponto certo cair nele:
   - **pico** para batidas, pops, cliques e whooshes (o momento mais forte cai no evento);
   - **início** para camas e sons longos;
   - **fim** para um riser que deve terminar na revelação.
5. **Confira o resultado medindo**, não supondo: cada som cai no quadro do seu evento, no máximo um quadro de erro. Um desvio maior é defeito de montagem.

Como o som lê a mesma lista, ele não precisa esperar a imagem travar para ser posicionado, mas o **nível final** só se acerta com a imagem pronta (veja "Volume final").

### Direção de som para peça inteira

Pontos de partida, como o resto desta skill:

- **Combine o som com o significado:** peças de um logo que se encaixam são cliques tonais; um cartão que abre é um deslize com aparecimento; um objeto que encolhe até um ícone é uma sucção mecânica; pulsos de áudio são batidas graves e suaves; a revelação final é um riser que termina nela, mais uma onda e uma batida grave.
- **Whoosh só para movimento** (um movimento de câmera, um deslize). Um corte ou uma transformação de forma leva um pop, um tique ou uma batida suave, não um whoosh.
- **Não repita o mesmo som igual.** Varie o tom e o nível de um efeito que se repete (um clique por etapa, subindo um pouco de tom a cada vez dá a sensação de progresso).
- **Camadas:** 2 a 4 **camas** ambientes (um pad tonal numa só tonalidade, uma camada de ar filtrada, uma textura baixa), com fade e um aumento suave na revelação; whooshes discretos (de −26 a −33 dB) sob cada movimento; as batidas e os pops por cima; um segundo riser e uma nota grave sob a revelação final.
- **Níveis:** uma faixa só de efeitos em torno de −20 LUFS, com picos abaixo de −2 dBFS, deixa espaço para a música. Sem locução, a música fica de 8 a 10 dB abaixo dos efeitos para os detalhes ainda aparecerem. Confira também o desenho de onda: não deve haver buracos mortos.
- **Música com a duração exata** e batidas que casem com algo rítmico da imagem (pulsos a cada 0,62 s pedem ~97 BPM). Se for pedir uma música, descreva o estilo, o BPM, a estrutura (entrada, crescimento, queda, saída) e corte uma seção para a queda cair na revelação.
- **Locução:** cerca de 2,2 palavras por segundo deixa espaço para respirar (10 s são de 18 a 22 palavras, com os últimos 2 s para o fecho). Uma linha curta por cena, só o que é verdade e que a pessoa pode sustentar. Depois da gravação real, ajuste os tempos do `EVENTOS` à fala.

## Como obter o som (pergunte)

1. **Trilha e narração da própria pessoa:** use o mapa de som para posicionar os eventos e montar os arquivos no Remotion (`<Audio>` de `@remotion/media`, um por faixa, com `premountFor`).
2. **Efeitos da biblioteca do Remotion** (whoosh, clique, ding, shutter): estão listados na skill do Remotion. Bom para efeitos; não resolve a trilha.
3. **Síntese por script (opcional):** `kit/audio/sintetizar.py` gera trilha e efeitos a partir do mapa de eventos, sem samples nem música de terceiros. Em peça inteira, os eventos podem apontar para nomes do `config.ts` (seção acima).

Se a pessoa não tem trilha e quer algo pronto rápido, ofereça a síntese e avise dos limites.

## Síntese opcional

Precisa de **Python 3.10+ e numpy** (`pip install numpy`). Só quem escolher a síntese instala o numpy.

```
python <skill>/kit/audio/sintetizar.py mapa.json --saida audio
```

Gera `sfx.wav`, `musica.wav` (se o mapa tiver `trilha`) e `mix.wav`, em 48 kHz estéreo, com o mesmo ganho nas três para a proporção entre elas não mudar. O mapa é um JSON com a duração, a semente, a trilha (BPM, acordes, trecho) e os eventos (instante **ou nome do evento**, tipo, ganho, pan). Modelos em `kit/audio/mapa-exemplo.json` (instantes em segundos) e `kit/audio/mapa-eventos-exemplo.json` (por nome, com `--eventos config.ts`). Tipos de evento: `bumbo`, `clique`, `chiado`, `whoosh`, `toque` (nota MIDI) e `acorde` (lista de notas).

No Remotion, ponha os WAV em `public/audio/` e use um `<Audio>` por faixa (`sfx.wav` e `musica.wav`, para ajustar o volume de cada um), ou só o `mix.wav`.

**Limites, para dizer à pessoa:**

- O som é eletrônico e simples, com cara de **trilha conceitual**. Pode ser trocada por uma música de verdade, e é para isso que `musica.wav` e `sfx.wav` saem separados.
- A mistura sai **baixa** (no teste com o mapa de exemplo, −23,8 LUFS). Ajuste o volume na exportação, abaixo.
- Os testes medem duração, pico, presença de som em cada evento e determinismo; a avaliação de gosto é da pessoa.

## Volume final

Depois de exportar, normalize o volume para o destino. Para feed (Reels, TikTok, Shorts) o alvo é −14 LUFS. **Duas passadas**, porque uma só erra mais:

```
ffmpeg -hide_banner -i peca.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -
ffmpeg -i peca.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true" -c:a aac -b:a 192k -ar 48000 -t <duracao em segundos> peca_final.mp4
```

Os valores `<...>` vêm do JSON impresso pela primeira passada. O `-t` impede o arquivo de crescer uns centésimos. No teste, a mistura sintetizada passou de −23,7 para −14,7 LUFS com este método (uma só passada deu −15,1). Meça depois (`-af ebur128=peak=true`) em vez de supor.
