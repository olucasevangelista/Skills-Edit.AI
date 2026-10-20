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
- Cortes entre takes: veja a seção seguinte (sobreposição), que é o padrão desta skill.
- **Efeito sonoro** curto na entrada de eventos grandes, em volume baixo: a voz sempre em primeiro plano. Evite som em todo evento pequeno.
- Se houver música, ela fica bem abaixo da voz.

## Cortes entre takes: sobreposição (padrão)

O corte **não é seco e a fala não é picotada**. O próximo take entra **colado no começo da fala**, sem respiro nem silêncio antes, e **começa ainda durante o finalzinho do take anterior**: a imagem e o áudio novos aparecem juntos enquanto a última sílaba da frase anterior termina. Na timeline, os dois clipes se sobrepõem por cerca de 0,1 a 0,25 s (3 a 8 quadros a 30 fps). A frase anterior termina inteira, a próxima já está falando, e o vídeo nunca fica parado nem tem pausa entre uma ideia e outra. É fala direta, sem respiro.

Aqui as vozes **se sobrepõem de propósito**, só por esse instante curto.

Como fazer, em cada junção:

1. **Deixe o take anterior terminar de falar.** Corte-o só depois da última palavra e do decaimento natural dela, nunca no meio da última sílaba.
2. **Corte o início do próximo take rente à fala:** sem respiro, sem inspiração, sem ruído de sala antes. Comece no instante em que a voz começa, com no máximo ~20 a 30 ms de folga, só para não comer a consoante.
3. **Posicione o próximo take** para que a primeira palavra dele comece durante o finalzinho da última palavra do anterior (sobreposição de ~0,1 a 0,25 s).
4. **Áudio:** o do take anterior desce suavemente ao longo da sobreposição; o do novo entra com um fade bem curto (10 a 30 ms, só para evitar estalo), para a primeira palavra bater com força. Confira que a soma das duas vozes não estoura o volume.
5. **Imagem:** corta no mesmo instante em que o áudio novo entra (ou dissolve em 2 a 4 quadros).
6. **Ajuste a sobreposição ao material:** se a última palavra do take anterior termina seca, use o mínimo (~0,1 s) para ela não se misturar demais com a primeira palavra nova; se tem decaimento longo, pode chegar a ~0,25 s. As duas vozes devem soar encadeadas, não embaralhadas.
7. **Vale para todo corte do vídeo**, inclusive onde as pausas dentro de um mesmo take são encurtadas.

Os valores são pontos de partida: ajuste ao ritmo da fala e à referência do usuário. Não é o padrão: o áudio cortando seco (mesmo com a imagem entrando antes), nem o próximo take começando com respiro e pausa.
