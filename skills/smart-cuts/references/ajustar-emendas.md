# Ajustar as emendas no planejador

A regra da emenda (o desenho, os valores e o porquê) está em `emenda.md`. Esta página é só o que é específico do `planejar_cortes.py` e do `montar.py`.

## Estilos de pausa

No estilo `curto`, a pausa longa dentro de um trecho **some**: a fala seguinte entra sobre o fim da anterior, como numa emenda de trecho (`emenda.md`). Nos estilos `aula` e `suave`, a pausa que fica é emendada sobre o silêncio (0,12 e 0,15 s). Escolha com `--estilo` em `planejar_cortes.py`:

| Estilo | Pausa a partir de | Fica com | Para quê |
|---|---|---|---|
| `curto` (padrão) | 0,22 s | some | Reels, Shorts, TikTok: ritmo rápido |
| `aula` | 0,55 s | 0,30 s | fala didática, mais natural |
| `suave` | 0,90 s | 0,55 s | entrevista, tom calmo |

Ajustes finos: `--pausa-minima`, `--pausa-final` (negativo = a pausa some e as vozes se sobrepõem), `--sobreposicao-emenda`, `--emenda-gap` (negativo = as vozes se sobrepõem, em s: 0,10 s são 3 quadros), `--cauda-final`. Quando a graça é o silêncio (pausa dramática, piada), planeje esse corte à parte, com `--so <id> --estilo suave` (e uma `--pausa-minima` maior que a pausa que deve ficar), para a pausa ficar inteira.

## Valores do padrão (estilo `curto`; `aula` e `suave` usam voz sobreposta de 0,12 e 0,10 s)

| O quê | Valor |
|---|---|
| Entrada do trecho novo antes do fim do anterior | 0,275 s |
| Voz do anterior e do novo sobrepostas | 0,15 s (4 a 5 quadros) |
| Respiro antes da primeira consoante do trecho novo | 25 ms |
| Cauda do trecho anterior depois da última palavra | ~0,1 s (nunca pega o som seguinte) |

## Onde cai a emenda

- O planejador procura **silêncio real** no áudio (abaixo de cerca de −40 dB por pelo menos 60 ms). Os tempos da transcrição não servem de guia sozinhos, porque escorregam.
- Sem pausa entre o que fica e o que sai (palavras coladas), não dá para cortar sem comer ou trazer palavra: o planejador avisa com `ENTROU` ou `SAIU`. Mantenha a frase inteira ou ponha a emenda na pausa real mais próxima (entrar uma palavra custa menos que tirar uma).
- Marque o fim do trecho no **início da última palavra** que fica. O planejador usa o fim dela. Marcar um fim calculado à mão já cortou palavras curtas como "quê?" e números.
- Emenda escolhida à mão: `"emendas": {"0": [38.95, 61.15]}` no `cortes.json` (fim da voz que fica, início da voz que entra, em segundos do original). Use os silêncios de `ler.py --silencio`.

## O que conferir de ouvido

`verificar.py` mede estalos e palavras cortadas. Fica para o ouvido: a costura soar natural, sem palavra repetida nem fantasma, e sem juntar duas frases que mudam o sentido.
