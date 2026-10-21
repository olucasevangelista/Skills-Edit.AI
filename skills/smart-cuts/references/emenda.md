# Emenda por sobreposição

Todo corte segue o mesmo desenho, dentro do mesmo corte e entre trechos de lugares diferentes do vídeo.

## O estilo

- **O take seguinte entra colado no começo da voz.** Sem respiro, sem silêncio antes. A palavra nova já começa quando a imagem troca.
- **A frase anterior termina inteira.** Nunca se come a última sílaba para fazer a emenda caber.
- **Imagem e áudio do take seguinte entram juntos, antes de a fala anterior acabar.** Nunca só a imagem, nunca só o áudio. A imagem troca no mesmo instante em que o áudio novo começa; por alguns centésimos de segundo as duas vozes se ouvem juntas.
- No áudio, o trecho anterior desce suavemente durante a sobreposição e o novo entra com um fade de 30 ms, só para evitar estalo.

Os números do padrão (estilo `curto`):

| O quê | Valor |
|---|---|
| Entrada do trecho novo antes do fim do anterior | 0,22 s |
| Voz do anterior e do novo sobrepostas | ~0,1 s |
| Respiro antes da primeira consoante do trecho novo | 25 ms |
| Cauda do trecho anterior depois da última palavra | ~0,1 s (nunca pega o som seguinte) |

## Pausas dentro de um mesmo trecho

Pausa longa dentro de um trecho também é encurtada, com a mesma sobreposição (0,12 s), só que sobre o silêncio: é uma emenda sem estalo, e a imagem não "pula".

| Estilo | Pausa a partir de | Fica com | Para quê |
|---|---|---|---|
| `curto` (padrão) | 0,22 s | 0,08 s | Reels, Shorts, TikTok: ritmo rápido |
| `aula` | 0,55 s | 0,30 s | fala didática, mais natural |
| `suave` | 0,90 s | 0,55 s | entrevista, tom calmo |

Escolha com `--estilo` em `planejar_cortes.py`. Ajustes finos: `--pausa-minima`, `--pausa-final`, `--sobreposicao-emenda`, `--emenda-gap`, `--cauda-final`. Quando a graça é o silêncio (pausa dramática, piada), planeje esse corte à parte, com `--so <id> --estilo suave` (e uma `--pausa-minima` maior que a pausa que deve ficar), para a pausa ficar inteira.

## Onde cai a emenda

- **Sempre em silêncio real**, medido no áudio: abaixo de cerca de −40 dB por pelo menos 60 ms. Uma pausa de 60 ms já serve. Os tempos da transcrição não servem de guia sozinhos, porque escorregam.
- Sem pausa entre o que fica e o que sai (palavras coladas), não dá para cortar sem comer ou trazer palavra: o planejador avisa com `ENTROU` ou `SAIU`. Nesse caso mantenha a frase inteira ou ponha a emenda na pausa real mais próxima (entrar uma palavra custa menos que tirar uma).
- Marque o fim do trecho no **início da última palavra** que fica. O planejador usa o fim dela. Marcar um fim calculado à mão já cortou palavras curtas como "quê?" e números.
- Emenda escolhida à mão: `"emendas": {"0": [38.95, 61.15]}` no `cortes.json` (fim da voz que fica, início da voz que entra, em segundos do original). Use os silêncios de `ler.py --silencio`.

## O que conferir de ouvido

- A costura soa natural: mesma entonação, mesma ideia, nenhuma palavra repetida nem fantasma.
- Não junte duas frases que mudam o sentido do que a pessoa disse. Não tire a palavra que conecta ("então", "só que") se a frase seguinte depende dela.
- Nenhum estalo e nenhuma palavra cortada: `verificar.py` mede os dois.
