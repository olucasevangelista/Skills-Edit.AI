# Ritmo, zoom e hierarquia de ênfase

## Regra do ritmo

- **Nunca mais que 3 segundos sem um evento visual novo. O ideal é um a cada ~2 s.**
- Um **evento** é uma mudança perceptível em menos de ~0,3 s. Conta como evento: insert (imagem, gráfico, logo, screenshot, ícone), texto novo entrando, mudança de zoom (punch-in ou saída do zoom), corte de câmera, tela dividida ou tela cheia entrando ou saindo, elemento que cruza a tela.
- **Não conta:** um zoom lento e contínuo sozinho (é ambiente), a legenda palavra a palavra sozinha (é a fala, não novidade), um fundo animado discreto.
- **Misture tamanhos.** Eventos grandes (tela dividida, tela cheia de gráfico, texto gigante) a cada ~8 a 10 s como marcos, e eventos pequenos (zoom, ícone, texto curto) nos intervalos. Só eventos grandes cansam; só pequenos viram papel de parede.
- **Varie o tipo.** Não repita o mesmo tipo de evento três vezes seguidas.
- **Exceção legítima:** uma frase de impacto dita com pausa pode ser o próprio evento por até ~3 s. Use pouco, e só com um zoom ou respiro intencional.

## Hierarquia de relevância (decide a ênfase)

Marque cada trecho da fala em três níveis e aplique ênfase proporcional:

| Nível | Quando | Tratamento (ponto de partida) |
|---|---|---|
| ★ **Chave** | Ideia central, número, promessa, virada | Zoom de ênfase (cerca de 1,12 a 1,2 sobre o enquadramento base), texto grande com cor de destaque, insert ilustrando, efeito sonoro curto |
| **Normal** | Explicação que sustenta | Enquadramento base (1,0 a 1,06), legenda normal, insert ocasional |
| **Baixa** | Transição, ressalva, contexto, "então", "tá" | **Tirar o zoom** (voltar a ~1,0), texto pequeno ou nenhum, sem insert |

O contraste entre níveis é o que cria o peso. Se mais de uns 30% do vídeo estiver marcado como chave, a marcação está generosa demais e a ênfase vai se anular: reveja.

## Zoom na prática

- **Punch-in** (salto de 1,0 para ~1,15 em 2 a 4 quadros): para palavras-chave e viradas. **Push** (empurrar devagar, ~1,0 para ~1,1 em 3 a 5 s): para manter vida em trechos longos sem evento.
- **Sempre há um caminho de volta.** Depois de uma frase chave, retorne ao neutro com suavização. Zoom que só aumenta aperta o enquadramento a cada frase e corta a cabeça da pessoa.
- **Esconder cortes secos:** quando há jump cuts, alterne o enquadramento entre cortes consecutivos (por exemplo 1,0 e ~1,05). O salto de imagem desaparece dentro da mudança de zoom.
- **Enquadramento:** olhos no terço superior do quadro; se a pessoa se mexe bastante, deixe o recorte acompanhar o rosto.
- **Tela dividida:** o zoom dentro do painel da pessoa pode ser maior para o rosto ocupar bem o espaço.

## Texto na tela: tempo e leitura

- Tempo mínimo em tela: **~0,4 s + 0,3 s por palavra**, nunca menos de 1 s. Texto que sai antes de ser lido é pior que nenhum texto.
- Um texto novo não deve entrar enquanto o anterior ainda está sendo lido, a menos que o antigo já esteja saindo.

## Sincronia e som

- O evento entra **no início da palavra que ele ilustra** (tolerância de ±0,1 s). Insert atrasado parece erro; ligeiramente adiantado (cerca de 0,1 s) parece intencional.
- Cortes entre takes: veja `emenda.md` (sobreposição), que é o padrão desta skill.
- **Efeito sonoro** curto na entrada de eventos grandes, em volume baixo: a voz sempre em primeiro plano. Evite som em todo evento pequeno.
- Se houver música, ela fica bem abaixo da voz.

## Cortes entre takes: sobreposição (padrão)

Em todo corte, imagem e áudio do take seguinte entram **juntos**, antes de o take anterior acabar. O desenho, os valores e o passo a passo de cada junção estão em `emenda.md`.

## Silêncios e takes repetidos

No Reels a pausa entre uma frase e a seguinte **some**: a fala seguinte entra sobre o fim da anterior, com voz na sobreposição (`emenda.md`). Um silêncio de **meio segundo a um segundo que sobrou** quebra o ritmo e o espectador sente: é defeito, não "respiro natural". Tirar os silêncios e entregar assim não termina o trabalho.

**Ordem:** primeiro escolha o que fica (takes repetidos), depois encurte as pausas e emende; só então legende e coloque os inserts, com os tempos do vídeo já limpo.

1. **Takes repetidos.** Quem grava erra e repete a frase várias vezes. Leia a transcrição com tempo por palavra e ache as tentativas que **começam igual**. Fique com a **última completa e sem tropeço** (o final dela não pode estar cortado e ela tem de encaixar na frase anterior). Em dúvida, **mostre as tentativas com os tempos e pergunte** qual é a certa. Você não ouve a entonação: se a escolha dependia disso, diga. O Whisper às vezes junta ou omite repetições: se o texto parece curto para o tempo, transcreva o trecho mantido sozinho e leia.
2. **Pausas.** Meça no **áudio**, não pela transcrição (os tempos dela escorregam 0,2 a 0,5 s). Com FFmpeg: `ffmpeg -i video.mp4 -af silencedetect=noise=-40dB:d=0.06 -f null -`. **O limiar tem de ficar acima do ruído da sala e abaixo da voz.** Se a sala tem ruído de fundo, o ruído passa de -40 dB e o detector não acha pausa nenhuma: confira com as pausas que a transcrição mostra entre palavras (mais de 0,25 s) e **suba o limiar** (-35, -30 dB) até o detector achá-las. Pausa acima de ~0,25 s some, e a fala seguinte entra sobre o fim da anterior (`emenda.md`). Onde a pausa é o efeito (frase de impacto, piada), mantenha.
3. **Não use `silenceremove` do FFmpeg para isso:** ele corta seco, sem a sobreposição, e come o começo das palavras.
4. **Confira o resultado medindo:** rode o mesmo `silencedetect` no vídeo cortado. Nenhuma pausa acima de ~0,35 s pode sobrar (fora as de efeito), e nenhuma palavra pode ter sido cortada: transcreva o vídeo limpo e leia em sequência.

A régua: pausa curta, melhor tentativa, emenda com sobreposição, tudo medido.
