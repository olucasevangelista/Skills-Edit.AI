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

## Como obter o som (pergunte)

1. **Trilha e narração da própria pessoa:** use o mapa de som para posicionar os eventos e montar os arquivos no Remotion (`<Audio>` de `@remotion/media`, um por faixa, com `premountFor`).
2. **Efeitos da biblioteca do Remotion** (whoosh, clique, ding, shutter): estão listados na skill do Remotion. Bom para efeitos; não resolve a trilha.
3. **Síntese por script (opcional):** `kit/audio/sintetizar.py` gera trilha e efeitos a partir do mapa de eventos, sem samples nem música de terceiros.

Se a pessoa não tem trilha e quer algo pronto rápido, ofereça a síntese e avise dos limites.

## Síntese opcional

Precisa de **Python 3.10+ e numpy** (`pip install numpy`). Só quem escolher a síntese instala o numpy.

```
python <skill>/kit/audio/sintetizar.py mapa.json --saida audio
```

Gera `sfx.wav`, `musica.wav` (se o mapa tiver `trilha`) e `mix.wav`, em 48 kHz estéreo, com o mesmo ganho nas três para a proporção entre elas não mudar. O mapa é um JSON com a duração, a semente, a trilha (BPM, acordes, trecho) e os eventos (instante, tipo, ganho, pan). Modelo em `kit/audio/mapa-exemplo.json`. Tipos de evento: `bumbo`, `clique`, `chiado`, `whoosh`, `toque` (nota MIDI) e `acorde` (lista de notas).

No Remotion, ponha os WAV em `public/audio/` e use um `<Audio>` por faixa (`sfx.wav` e `musica.wav`, para ajustar o volume de cada um), ou só o `mix.wav`.

**Limites, para dizer à pessoa:**

- O som é eletrônico e simples, com cara de **trilha conceitual**. Pode ser trocada por uma música de verdade, e é para isso que `musica.wav` e `sfx.wav` saem separados.
- A mistura sai **baixa** (no teste com o mapa de exemplo, −23,8 LUFS). Ajuste o volume na exportação, abaixo.
- Não foi ouvida por pessoa nesta verificação: os testes medem duração, pico, presença de som em cada evento e determinismo. A avaliação de gosto é da pessoa.

## Volume final

Depois de exportar, normalize o volume para o destino. Para feed (Reels, TikTok, Shorts) o alvo é −14 LUFS. **Duas passadas**, porque uma só erra mais:

```
ffmpeg -hide_banner -i peca.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -
ffmpeg -i peca.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true" -c:a aac -b:a 192k -ar 48000 -t <duracao em segundos> peca_final.mp4
```

Os valores `<...>` vêm do JSON impresso pela primeira passada. O `-t` impede o arquivo de crescer uns centésimos. No teste, a mistura sintetizada passou de −23,7 para −14,7 LUFS com este método (uma só passada deu −15,1). Meça depois (`-af ebur128=peak=true`) em vez de supor.
