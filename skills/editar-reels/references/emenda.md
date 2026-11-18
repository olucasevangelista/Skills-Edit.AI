# Emenda por sobreposição

A regra de todo corte entre takes de fala, em qualquer ferramenta de edição. **Imagem e áudio do take seguinte entram juntos, antes de a imagem e o áudio do take anterior acabarem.**

## O desenho

```
                  entra o take 2             acaba o take 1
                                 │         │
imagem 2                         ┌─────────── V  take 2 ────────────┐
imagem 1    ┌───────── V  take 1 ──────────┐
áudio 1     ┌───────── A  take 1 ──────────┐
áudio 2                          ┌─────────── A  take 2 ────────────┐
                                 └─────────┘
                                 sobreposição
```

Quatro faixas, duas de imagem e duas de áudio. O que o desenho diz:

- **O take 2 entra por inteiro de uma vez:** a imagem e o áudio dele começam no mesmo instante, e esse instante cai **antes** do fim do take 1.
- **A imagem do take 2 fica por cima.** A imagem troca num corte seco, no instante em que o áudio novo entra. Sem dissolve, sem fade.
- **O áudio do take 2 já começa falando.** Não há silêncio nem respiro no início dele: o corte é rente à primeira palavra, então a voz nova está presente desde o primeiro instante da sobreposição.
- **O áudio do take 1 vai até o fim**, e a voz nova entra enquanto ele ainda termina a última palavra: por um instante curto, as duas vozes se ouvem juntas, de propósito. Em nenhum ponto da sobreposição fica sem fala.
- **O take 1 termina inteiro.** A última sílaba nunca é cortada para a emenda caber.

Por que assim: não se espera a pessoa terminar para mostrar a próxima ideia, e o vídeo nunca tem respiro entre uma frase e a outra. O espectador sente energia e continuidade, e não percebe a emenda.

Isto **não é um L-cut nem um J-cut**: nesses, a imagem e o áudio entram em momentos diferentes. Aqui entram juntos.

## Valores de partida

| O quê | Valor |
|---|---|
| **Voz do take 2 sobreposta à voz do take 1** | **3 a 6 quadros** (0,1 a 0,2 s a 30 fps). O take 2 já está falando enquanto o take 1 termina a última palavra |
| Folga antes da primeira consoante do take 2 | 20 a 30 ms, só para não comê-la. É o único trecho do take 2 sem voz, e dura menos de um quadro |
| Cauda do take 1 depois da última palavra | ~0,1 s, sem pegar o som seguinte |
| Fade do áudio | take 1 desce suavemente durante a sobreposição; take 2 entra com 10 a 30 ms, só para evitar estalo |

Referência de unidades a 30 fps: 1 quadro = 0,033 s; 3 quadros = 0,10 s; 4 = 0,13 s; 5 = 0,17 s; 6 = 0,20 s. Trabalhe em quadros: é o que o editor mostra e o que o olho percebe.

**Escolha dentro da faixa pelo material.** Última palavra seca ou com consoante curta: 3 quadros. Palavra que termina aberta ou com decaimento longo: 5 ou 6. Se as duas vozes ficam **embaralhadas** (não dá para entender nenhuma), reduza. Se o efeito não se percebe (o corte não dá dinamismo), aumente. Os valores são pontos de partida: ajuste ao ritmo da fala.

## Em cada junção

1. **Deixe o take 1 terminar de falar.** Corte-o só depois da última palavra e do decaimento natural dela.
2. **Corte o início do take 2 rente à fala:** sem respiro, sem inspiração, sem ruído de sala antes. Comece no instante em que a voz começa.
3. **Posicione o take 2** para que a primeira palavra dele comece durante o finalzinho do take 1 (a sobreposição acima).
4. **Imagem e áudio do take 2 começam no mesmo quadro.** Confira que a soma das duas vozes não estoura o volume.

Montando à mão em qualquer editor: ponha os takes alternando entre as duas faixas de imagem e as duas de áudio (take 1 na faixa de baixo, take 2 na de cima, take 3 na de baixo de novo...), com a sobreposição entre cada par.

## Onde cai a emenda

- **Em silêncio real, medido no áudio**, e não pelo tempo da transcrição, que escorrega 0,2 a 0,5 s em arquivos longos. Um silêncio de 60 ms abaixo de cerca de −40 dB já serve: `ffmpeg -i video.mp4 -af silencedetect=noise=-40dB:d=0.06 -f null -`.
- **Nenhuma palavra cortada.** Marque o fim do trecho no início da última palavra que fica e confira transcrevendo o resultado.
- **Sem pausa entre o que fica e o que sai** (palavras coladas): mantenha a frase inteira ou mova a emenda para a pausa real mais próxima. Entrar uma palavra a mais custa menos que tirar uma.
- **Não use `silenceremove` do FFmpeg para isso:** ele corta seco, sem a sobreposição, e come o começo das palavras.

## Pausas dentro do mesmo take

Tirar uma pausa de dentro de um take segue **a mesma regra de uma troca de take**: a fala seguinte entra, com imagem e áudio juntos, sobre o finalzinho da fala anterior, com voz na sobreposição (3 a 6 quadros) e sem nenhum espaço sem fala. A pausa **some**, e quem assiste sente a fala emendada, sem respiro.

A exceção é a pausa que é para ficar. Aí não há o que sobrepor: a emenda cai dentro do silêncio que sobra (com uns 0,12 s de sobreposição, só para não estalar e a imagem não "pular"). Quanto de pausa fica depende do tom:

| Tom | Pausa a partir de | O que acontece |
|---|---|---|
| Ritmo rápido (Reels, anúncio, pessoa falando para a câmera) | 0,22 s | a pausa some: a fala seguinte entra sobre o final da anterior, com voz na sobreposição |
| Didático, natural (aula, tutorial, gravação de tela) | 0,55 s | fica com 0,30 s, e a emenda cai nesse silêncio |
| Calmo (entrevista, depoimento emocional) | 0,90 s | fica com 0,55 s, e a emenda cai nesse silêncio |

**Um silêncio de meio segundo a um segundo que sobrou é defeito** (quebra o ritmo), exceto quando a pausa é o efeito: frase de impacto, piada, suspense antes de uma revelação. Aí mantenha-a inteira, sem emenda dentro dela.

## Onde vale

- **Em todo corte de fala:** dentro do mesmo take, entre trechos de partes diferentes do vídeo e entre arquivos diferentes.
- **Com mais cuidado nos momentos-chave** (abertura, virada, revelação, troca de seção), combinando o corte com uma mudança visual: zoom, troca de plano, elemento novo.
- **Troca de câmera para tela ou motion com a narração contínua:** o áudio já é contínuo, então só a imagem troca, na palavra que a motiva.

## Conferir de ouvido

- A costura soa natural: mesma entonação, mesma ideia, nenhuma palavra repetida nem fantasma.
- Não junte duas frases que mudam o sentido do que a pessoa disse. Não tire a palavra que conecta ("então", "só que") se a frase seguinte depende dela.
- Nenhum estalo, nenhuma palavra cortada e nenhuma imagem entrando antes ou depois do áudio.
- Não é o padrão: o áudio cortando seco (mesmo com a imagem entrando antes), a imagem entrando depois do áudio, nem o take seguinte começando com respiro e pausa.
