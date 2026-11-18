# Limpar a fala: erros, repetições e silêncios

Quando o material é uma gravação falada (quase sempre), **limpe a fala antes de montar o formato**. O resultado é um `limpo.mp4`: só o que fica, sem silêncio perceptível entre as frases e com as emendas por sobreposição (`emenda.md`). O formato, a legenda e os inserts são montados em cima dele, no Remotion.

**Padrão de qualidade:** entre uma frase e a seguinte quase não sobra pausa: no estilo `curto` ela some e a fala seguinte entra sobre o fim da anterior (`emenda.md`). Um silêncio de meio segundo ou de um segundo que ficou é **defeito**: quebra o ritmo e o espectador sente, mesmo sem saber dizer o que foi. Não entregue assim e **não diga que terminou antes de o verificador passar**.

## A ordem

1. **Inspecione** o arquivo (`fluxo.md`, passo 1).
2. **Transcreva o bruto** com tempo por palavra. Aqui a transcrição serve só para **decidir o que sai**.
3. **Passada 1, escolher o que fica** (julgamento; abaixo).
4. **Passada 2, pausas e emendas** (script; abaixo).
5. **Verifique** (abaixo).
6. **Transcreva o `limpo.mp4`** (não o bruto): as legendas e os inserts já nascem com o tempo certo.
7. **Monte o formato no Remotion** usando o `limpo.mp4` como a fala do vídeo.

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
| `curto` (padrão) | 0,22 s | some (a fala seguinte entra sobre a anterior) | anúncio, ritmo apertado |
| `aula` | 0,55 s | 0,30 s | fala didática, mais natural |
| `suave` | 0,90 s | 0,55 s | depoimento emocional, Cinema, tom calmo |

Emendas: a voz do trecho novo se sobrepõe à anterior por 0,10 a 0,15 s (3 a 5 quadros, conforme o estilo; 0,15 s no `curto`). No `curto`, tirar uma pausa usa essa mesma emenda; nos estilos `aula` e `suave`, a pausa que fica é emendada sobre o silêncio (0,12 s). Ajustes finos: `--pausa-minima`, `--pausa-final` (negativo = a pausa some e as vozes se sobrepõem), `--sobreposicao-emenda`, `--emenda-gap` (negativo = as vozes se sobrepõem, em s: 0,10 s são 3 quadros), `--limiar` (em dB). No `montar.py`: `--lufs` (padrão -14, o de anúncio), `--fps`, `--qualidade maxima`, `--sem-tratamento-audio` (sem o equalizador e o compressor de voz).

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

- **Vários arquivos do mesmo vídeo** (partes gravadas separadas): limpe cada um (`--saida limpeza/p1`, `p2`...) e depois una os arquivos limpos com a emenda abaixo.
- **Emenda entre arquivos diferentes**: a mesma regra de `emenda.md`: imagem e áudio do seguinte entram **juntos**, com a voz dele sobre o fim da voz anterior. Cada `limpo.mp4` traz ~0,25 s de silêncio no começo e ~0,35 s no fim, e é preciso tirá-los na junção; senão sobra quase meio segundo sem fala entre as vozes. Meça no áudio (`silencedetect`) onde a voz do primeiro arquivo termina (`V1`) e onde a do segundo começa (`V2`). Então `T1 = V1 + 0.10` (onde o primeiro termina) e `S2 = V2 - 0.025` (onde o segundo começa), com `d = 0.275` (a voz do segundo fica ~0,15 s, 4 a 5 quadros, sobre a do primeiro):
  ```
  ffmpeg -y -i p1.mp4 -i p2.mp4 -filter_complex "[0:v]fps=30,trim=end=<T1-0.275>,setpts=PTS-STARTPTS[v0];[1:v]fps=30,trim=start=<S2>,setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0[v];[0:a]atrim=end=<T1>,asetpts=PTS-STARTPTS[a0];[1:a]atrim=start=<S2>,asetpts=PTS-STARTPTS[a1];[a0][a1]acrossfade=d=0.275:c1=qsin:c2=nofade[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k junto.mp4
  ```
  (A duração final é `T1 + (duração de p2 - S2) - 0.275`, no vídeo e no áudio.)
- **Já havia legenda do bruto**: o `timeline.json` converte o tempo: `final = final_ini + (t - bruto_ini)` do trecho em que `t` cai. Palavras de trechos removidos somem. Costuma ser mais simples e mais seguro transcrever o `limpo.mp4`.
- **Trocar de enquadramento entre takes dentro do Remotion** (e não só tirar silêncio) é outro uso: `assets/componentes/TakesSobrepostos.tsx` faz a mesma emenda direto na composição. Para tirar erro e silêncio de uma gravação, use os scripts: são medidos e verificados.
- **Só áudio** (sem imagem): o `montar.py` limpa o áudio e grava `limpo.m4a`.
