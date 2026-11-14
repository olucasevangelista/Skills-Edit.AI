# Tipos de vídeo e o que cada um pede

O tipo do vídeo decide **onde cabe cada coisa**: o que pode ficar por cima da imagem, como tratar as pausas e que ritmo faz sentido. Pergunte; se a pessoa não souber dizer, **olhe o vídeo**.

## Como identificar olhando

Uma folha com um quadro a cada 20 s (ajuste o intervalo ao tamanho do vídeo) e, depois, um quadro em cheio onde houver dúvida:

```
ffmpeg -i bruto.mp4 -vf "fps=1/20,scale=320:-1,tile=6x4" -frames:v 1 folha.png
ffmpeg -ss 125 -i bruto.mp4 -frames:v 1 quadro.png
```

| O que aparece | Tipo |
|---|---|
| O rosto ocupa a tela | Pessoa falando para a câmera |
| Terminal, código, navegador, interface; o rosto pequeno num canto | Gravação de tela com rosto no canto |
| Animações sobre uma narração; pouco ou nenhum rosto | Motion no corpo |
| Muda de um para outro ao longo do vídeo | Mistura: classifique **por trecho** |

Se o vídeo não cabe em nenhum, descreva para si **o que é a imagem e o que o espectador precisa enxergar** e aplique a mesma ideia: nada cobre o que ele precisa ver. Na dúvida, pergunte.

## Pessoa falando para a câmera

O formato mais livre: a imagem é o rosto e o resto é espaço para dar ritmo.

- **Cortes:** limpe à vontade (erros, repetições, pausas). O estilo `curto` costuma servir. Com muitos cortes de salto, alterne o enquadramento entre cortes seguidos (por exemplo 1,0 e ~1,05): o salto some dentro da mudança de zoom.
- **Ritmo:** é aqui que entram, de vez em quando, motion designs, inserts (imagem, print, ícone), texto em destaque e zoom, **de acordo com o estilo da pessoa**.
- **Cuidado:** não cubra os olhos nem a boca. Todo zoom volta ao tamanho normal.

## Gravação de tela com rosto no canto

**A tela é o conteúdo.** O cuidado aqui é máximo.

- **Regra de ouro:** enquanto a pessoa mostra, clica, digita ou aponta algo, **nada é colocado por cima da área da tela**.
- **Motion só quando a fala vira conceito** e a pessoa deixa de mexer na tela. Exemplo: ela explica como funciona a arquitetura de vários servidores, mas na imagem só há o terminal aberto, sem desenhar nada. Aí um motion que mostra a ideia (isso liga naquilo) ajuda a entender, e a narração continua. Se a pessoa **está desenhando na tela**, não entra motion.
- **Pausas com ação na tela não são silêncio morto:** carregando, rodando um comando, digitando. Cortar ali apaga um pedaço da demonstração. Veja `limpeza.md`, seção "Gravação de tela".
- **Como decidir onde um elemento entra:** extraia um quadro do instante e **olhe**. Se há texto, código, menu ou cursor em movimento onde ele entraria, mude a posição ou não use. Em dúvida, pergunte.
- Mantenha o rosto do canto visível o tempo todo.

## Motion no corpo

A imagem é uma animação construída sobre a narração; a **narração é o material bruto**.

- **Limpe a fala antes de animar.** Cortar depois de os motions prontos desencontra tudo. O `montar.py` entrega o vídeo limpo (ou só o áudio limpo, se o arquivo for só áudio).
- **Transcreva o áudio limpo:** os tempos das palavras guiam cada animação.
- O ritmo vem da troca de cenas e de elementos junto com a fala. Criar e exportar é com a skill do Remotion; a lógica visual (o que a animação mostra, na ordem em que a pessoa fala) é sua.
- Se o rosto aparece (na abertura ou no final), ele entra como um dos trechos da mistura.

## Mistura

Muitos vídeos alternam (rosto, depois tela, depois motion). Classifique **por trecho**, aplique a regra de cada um e, na conversa com o usuário, diga qual regra usou em cada parte. Nas passagens de um tipo para outro, use a emenda com sobreposição (`meio-e-ritmo.md`).
