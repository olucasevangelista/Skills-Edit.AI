# Limpar a fala: erros, repetições e silêncios

Quando o material é uma gravação falada (quase sempre), **limpe a fala antes de montar o anúncio**. O resultado é um `limpo.mp4`: só o que fica, sem silêncio perceptível entre as frases e com as emendas por sobreposição (`anuncio-e-retencao.md`, seção 5). Os inserts, a legenda, o motion e a tela dividida são feitos em cima dele, no Remotion ou no editor da pessoa.

**Padrão de qualidade:** entre uma frase e a seguinte sobra no máximo **~0,1 s** (estilo `curto`). Um silêncio de meio segundo ou de um segundo que ficou é **defeito**: quebra o ritmo e o espectador sente, mesmo sem saber dizer o que foi. Não entregue assim e **não diga que terminou antes de o verificador passar**.

## A ordem

1. **Inspecione** o arquivo (tamanho, taxa de quadros, duração, se tem áudio: `ffprobe`).
2. **Transcreva o bruto** com tempo por palavra. Aqui a transcrição serve só para **decidir o que sai**.
3. **Passada 1, escolher o que fica** (julgamento; abaixo).
4. **Passada 2, pausas e emendas** (script; abaixo).
5. **Verifique** (abaixo).
6. **Transcreva o `limpo.mp4`** (não o bruto): as legendas e os inserts já nascem com o tempo certo.
7. **Monte o anúncio** (inserts, texto, zoom, motion) usando o `limpo.mp4` como a fala do vídeo.

## Passada 1: escolher o que fica

Quem grava erra e repete a mesma frase quatro, cinco, seis vezes. É preciso **escolher a melhor tentativa e remover as outras**, antes de mexer nas pausas.

```
python <skill>/scripts/achar_repeticoes.py transcricao.json
```

Lista as tentativas que começam igual, os recomeços no meio da frase e imprime a sugestão `--remover`. **É uma ajuda, não uma decisão:** ele não ouve o áudio.

- **Leia as tentativas como texto.** Fique com a **última tentativa completa e sem tropeço**. O final dela não pode estar cortado, e ela tem de encaixar na frase anterior que fica. Se a última é mais curta que uma anterior, desconfie.
- **Em dúvida, pergunte.** Mostre as tentativas com os tempos ("a certa é a de 17 s ou a de 24 s?"). Perguntar custa menos que refazer.
- **Você não ouve a entonação nem a fluidez.** Se a escolha dependia disso, diga na entrega que a escuta final é da pessoa.
- **O Whisper esconde retakes** quando transcreve o arquivo inteiro: junta tentativas e omite frases repetidas. Se o texto parece curto para o tempo, **transcreva cada trecho mantido sozinho** (com 0,1 s de folga nas pontas) e leia em sequência como texto corrido: palavra repetida, frase pela metade e retake escondido aparecem aí.
- Também saem: comentários fora da fala ("peraí", "deixa eu refazer"), o começo antes da fala e o fim depois dela. Hesitação curta e natural fica.
- **Não junte duas frases que mudam o sentido** do que a pessoa disse, e não tire a palavra que conecta ("então", "só que") se a frase seguinte depende dela.

O resultado é uma lista de intervalos do bruto: `--remover "a-b,c-d"` (segundos ou mm:ss). Os tempos da transcrição escorregam 0,2 a 0,5 s; por isso o script **alinha cada pedido aos limites reais da fala** (tolerância de 1,5 s) e mostra "pedido" e "alinhado" no plano: confira. Se avisar que **não conseguiu alinhar** (o erro está no meio de uma fala contínua, sem pausa nas bordas), ajuste os tempos olhando o volume ou use `--sem-alinhar` (corta exatamente onde você disse).

## Passada 2: pausas e emendas

```
python <skill>/scripts/planejar_cortes.py bruto.mp4 --saida limpeza --estilo curto --remover "0.3-12.6,18-26.8"
python <skill>/scripts/montar.py limpeza/cortes.json --saida limpeza
```

O planejador mede o **volume do áudio** (não os tempos da transcrição) para achar a fala e as pausas, e grava `cortes.json` e `plano_cortes.md`. O `montar.py` corta e emenda imagem e áudio com a **sobreposição** e grava `limpo.mp4` e `timeline.json` (o mapa de tempo bruto para final). Rode o `montar.py` **sozinho**: se outro processo pesado de vídeo estiver rodando junto (o recorte de fundo, por exemplo), a codificação pode falhar.

| Estilo | Pausa a partir de | Fica com | Para quê |
|---|---|---|---|
| `curto` (padrão) | 0,22 s | 0,08 s | anúncio, ritmo apertado |
| `aula` | 0,55 s | 0,30 s | fala didática, mais natural |
| `suave` | 0,90 s | 0,55 s | depoimento emocional, tom calmo |

Emendas: **0,12 s** de sobreposição ao encurtar uma pausa e **0,22 s** ao remover um erro, com as vozes ainda se sobrepondo ~0,1 s. Ajustes finos: `--pausa-minima`, `--pausa-final`, `--sobreposicao-emenda`, `--emenda-gap`, `--limiar` (em dB). No `montar.py`: `--lufs` (padrão -14, o de anúncio), `--fps`, `--qualidade maxima`, `--sem-tratamento-audio` (sem o equalizador e o compressor de voz).

**Leia o `plano_cortes.md` antes de montar**: a economia de tempo, o limiar e os **avisos**:

- *Áudio com muito ruído de fundo* ou *o arquivo inteiro foi tratado como fala contínua*: o ruído pode estar sendo lido como fala, e as pausas não são achadas. Repita com `--limiar` mais alto (comece por -30) e releia o plano.
- *Sobreposição reduzida em trecho curto*: uma palavra solta entre duas pausas. A pausa foi cortada mesmo assim, com emenda mais curta.
- *Trecho curtíssimo… a pausa ficou como no original*: ali sobrou uma pausa. Remova esse trecho com `--remover` ou aceite, e diga.

**Quando a graça é o silêncio** (pausa dramática, piada, depoimento emocional), planeje esse trecho à parte com `--estilo suave` e uma `--pausa-minima` maior que a pausa que deve ficar.

## Verificar

```
python <skill>/scripts/verificar_cortes.py limpeza/limpo.mp4 --timeline limpeza/timeline.json
```

Mede, sem confiar no plano: duração contra o previsto, vídeo e áudio com a mesma duração, volume (-14 LUFS) e pico, **pausas que sobraram** (acima da pausa mínima do estilo + 0,15 s) e **estalo** nas emendas. Sai com código 1 se algo estiver fora. **Se reprovar, corrija** (estilo, `--limiar`, `--remover`), monte de novo e verifique de novo.

Além disso: olhe quadros logo antes e depois de algumas emendas e **transcreva o `limpo.mp4`**: a leitura corrida mostra palavra repetida, frase pela metade ou sentido trocado. O que o script **não** pega: respiração e estalo de boca, entonação, se a ideia ficou natural. Isso é de ouvido: diga na entrega que a escuta final é da pessoa.

## Casos

- **Corpo e gancho**: limpe o corpo antes de usar o `variar_ganchos.py` (`variacoes.md`); ele já emenda o gancho ao corpo com a mesma sobreposição.
- **Vários arquivos do mesmo vídeo** (partes gravadas separadas): limpe cada um (`--saida limpeza/p1`, `p2`...) e depois una os arquivos limpos com a emenda abaixo.
- **Emenda entre arquivos diferentes**: imagem e áudio do seguinte entram **juntos**, 0,13 s antes de a fala anterior acabar. A versão em que a imagem entra depois do áudio fica estranha. Com `D1` = duração do primeiro arquivo:
  ```
  ffmpeg -y -i p1.mp4 -i p2.mp4 -filter_complex "[0:v]fps=30,trim=end=<D1-0.13>,setpts=PTS-STARTPTS[v0];[1:v]fps=30,setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0[v];[0:a][1:a]acrossfade=d=0.13:c1=tri:c2=tri[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k junto.mp4
  ```
  (Duração testada: a soma das duas menos 0,13 s, no vídeo e no áudio.)
- **Já havia legenda do bruto**: o `timeline.json` converte o tempo: `final = final_ini + (t - bruto_ini)` do trecho em que `t` cai. Palavras de trechos removidos somem. Costuma ser mais simples e mais seguro transcrever o `limpo.mp4`.
- **Só áudio** (sem imagem): o `montar.py` limpa o áudio e grava `limpo.m4a`.

## O que foi testado (e o que não)

- O planejador, o montador e o verificador passaram em testes com áudio sintético (tom com ruído de sala em dois níveis, pausas de 0,6 a 1,1 s) e em gravação de voz gerada por síntese de fala, com **controles negativos**: um arquivo que ficou com pausas é reprovado pelo verificador. O núcleo (medir o volume, achar a fala, emendar com sobreposição) já foi usado em vídeos reais de aula e de criativo.
- **Não foi testado em gravação humana com ruído real** neste ajuste. O limiar se adapta ao piso de ruído medido no próprio áudio, mas sala muito ruidosa (ruído quase no nível da fala) pode exigir `--limiar` à mão.
- O detector de repetições foi testado com transcrições sintéticas e uma transcrição real **sem** retakes (não inventou nenhum). **Não foi validado em transcrições reais com retakes**: trate a sugestão como pista e confirme lendo.
