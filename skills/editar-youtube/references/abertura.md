# A abertura: os primeiros 5 a 10 segundos

Quem decide ficar ou sair decide aqui. Esses segundos precisam ser **muito dinâmicos e atraentes**, e **bonitos e bem feitos**: é o trecho mais caro do vídeo, então gaste tempo nele. A partir daí, cada parte do vídeo alimenta a vontade de continuar.

**Não há regra de formato.** A abertura depende do tipo de vídeo e do estilo da pessoa. O que não muda é o que ela precisa fazer.

## O que a abertura faz

1. **Diz o que a pessoa vai ver ou aprender:** a promessa, em poucas palavras e sem enrolar.
2. **Às vezes mostra o que vem:** o que ela vai fazer, o resultado, a tela funcionando.
3. **Abre uma curiosidade que só se resolve no final.** O espectador pensa "que legal... e como eu faço isso?" e fica para descobrir.

O que ela **não** faz: resumir o vídeo nem entregar o final. Se o vídeo ensina a editar vídeos com uma ferramenta, a abertura mostra o que será possível e deixa o "como" para o decorrer. Cada trecho seguinte alimenta mais a vontade de ver o resto.

## Caçar o momento-gancho no próprio vídeo

Antes de pensar em animação, **procure o melhor instante do vídeo** e traga um pedaço dele para o começo.

1. Leia a transcrição limpa inteira e marque os candidatos: o resultado pronto, a tela mostrando o que foi feito, um antes e depois, a frase mais forte, o momento da revelação.
2. **Num vídeo de demonstração em tela,** procure no meio (ou mais adiante) um **print**: o quadro em que a tela mostra o resultado. Procure na fala por "print", "olha aqui", "ficou assim", "resultado". Atenção: a transcrição pode escrever **"link" onde a pessoa disse "print"**; leia o contexto e confira no quadro.
3. Extraia o quadro do instante e **olhe**: `ffmpeg -ss 312 -i limpo.mp4 -frames:v 1 print.png`. Se serve, ele entra no começo como prévia do que vem.
4. Posicione sem entregar o final: a prévia mostra *o quê*, e o *como* continua adiante.

## Maneiras de abrir (exemplos, não regras)

Escolha pelo assunto e pelo estilo da pessoa. **Escolha uma e execute com capricho**, em vez de empilhar cinco ideias.

- **Reduzir a pessoa** para uma janela menor e desenhar, com motion, algo que ilustra a promessa ao lado.
- **Recortar a pessoa do fundo** (`scripts/recortar_pessoa.py`, num trecho curto) e colocar **atrás** dela elementos que façam sentido com o assunto: imagens, ícones, texto, objetos animados.
- **Texto em destaque,** grande, com a promessa, entrando na palavra dita.
- **Imagens ou prints aparecendo** na hora em que a pessoa os cita.
- **O print do meio do vídeo** como prévia do resultado.
- **Tela dividida:** a pessoa de um lado e o resultado do outro.
- **Começar no meio da ação** e voltar ao início.

Os elementos (animações, cores, fontes, o desenho dos objetos) **são da pessoa**: monte-os no Remotion com a identidade dela. Se for uma linguagem visual nova para ela, **mostre um quadro ou um trecho curto e peça a opinião** antes de seguir.

## Depois da abertura: manter a curiosidade

A abertura abre a pergunta; o resto do vídeo a mantém viva até a resposta.

- Dê **pequenas promessas e revelações parciais** ao longo do vídeo ("daqui a pouco eu mostro como", "e o resultado final fica assim"), **de acordo com o que a pessoa já fala**. Não invente promessas que o vídeo não cumpre.
- **Resolva no final** o que a abertura prometeu.
- Evite repetir no meio o que a abertura já mostrou, a não ser que seja a hora de pagar a promessa.

## Os cortes da abertura

A abertura é um **momento-chave**: faça a emenda com sobreposição bem feita em cada corte (imagem e áudio do take seguinte entram juntos, antes de a fala anterior acabar) e combine com a mudança visual, para o corte parecer intencional e dinâmico.

## Conferir

Veja só os primeiros 10 s, sem contexto:

- Dá para entender o que o vídeo promete?
- Dá vontade de continuar? Ficou alguma pergunta no ar?
- Entregou o final por engano?
- Está bonita, legível e com a identidade da pessoa? Texto com tempo de leitura (0,4 s + 0,3 s por palavra, mínimo 1 s)?
- Nenhum elemento cobre o rosto, as mãos ou o que importa na tela?
