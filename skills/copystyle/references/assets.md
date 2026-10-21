# Assets: o que o guia precisa, como conseguir, como pedir

Regra: providencie sozinho tudo que for gratuito e de boa qualidade; peça ao criador só o que é pago, pessoal ou que você não achou. Guarde tudo organizado em `copystyle/<nome>/assets/` (`musica/`, `sfx/`, `pack/`, `fontes/`, `marca/`) e registre em `ASSETS-PENDENTES.md` o que ainda falta.

## Música (`assets/musica/`)

- Fontes da lista: as trilhas que o criador citou, as que o guia recomenda e as que o criador identificou nas referências. Sem identificação segura, escreva "trilha não identificada" com o clima e deixe na lista de pendências para o criador dizer o nome.
- Baixe pelo YouTube em áudio de boa qualidade, de preferência o canal oficial ou "Topic": `yt-dlp -f 251 -o "assets/musica/%(title)s.%(ext)s" "<url>"`. Se der 403, atualize o yt-dlp (`uvx yt-dlp@latest ...`).
- Confira a qualidade: música abafada é percebida. Olhe o espectro (`ffmpeg -i musica.opus -lavfi showspectrumpic=s=1024x512 espectro.png`) e ouça um trecho; uma faixa de boa qualidade chega perto de 19 a 20 kHz; se o espectro some bem antes disso, é uma versão abafada e vale procurar outra.
- Normalize em −14 LUFS para o volume ficar previsível: `ffmpeg -i musica.opus -af loudnorm=I=-14:TP=-1.5:LRA=11 musica_norm.wav`.
- Anote para cada faixa um `uso` e um `clima` escritos para o editor ("épico, virada, número grande", "cama calma de explicação", "nostalgia, história antiga"), e os instantes do drop. Se o criador deu a paleta, ela é a primeira opção.
- Direitos: pergunte se ele publica com o áudio do arquivo ou troca pelo áudio do app na hora de postar (Instagram e TikTok têm catálogo próprio). Registre a resposta nas preferências do guia.

## Efeitos sonoros (`assets/sfx/`)

- Pack comprado: peça a pasta e use os arquivos que as referências realmente usam. Corte o silêncio inicial e normalize o pico. Nomes que o guia usa: `boom_sub`, `boom_long`, `ding`, `shutter`, `whoosh`, `riser`, `pop`, `record_scratch`.
- Sem pack: bibliotecas gratuitas com download direto (procure com WebSearch; se o site exige clicar, use o navegador do usuário pela skill de Chrome). Efeito gerado por IA ou sintetizado costuma soar mal; na dúvida, mantenha o item pendente.
- Só providencie os tipos que as referências usam de verdade (o guia lista).

## Pack visual (`assets/pack/`): flashes, light leaks, transições, ícones animados, energias

- Dois tipos de arquivo: vídeo com fundo preto para somar por cima (luz, flash, energia; modo `screen`) e vídeo com transparência real (ícone animado, figurinha; modo `alpha`, ProRes 4444 `.mov` ou WebM VP9 com alfa).
- Anote para cada item a categoria, o modo e em qual estilo de vídeo ele entra.

## Fontes (`assets/fontes/`)

- Google Fonts: baixe os pesos usados (por exemplo 400, 700 e 900) e registre no `estilos.json`. No Remotion também dá para carregar direto pela biblioteca de Google Fonts (skill do Remotion).
- Fonte paga ou própria: peça o arquivo (`.ttf` ou `.otf`); enquanto não chega, use a Google Font mais parecida e anote a pendência.

## Marca (`assets/marca/`)

Logo (PNG transparente), foto de perfil, caricatura ou avatar se o guia usa no final, cores da marca. Sempre do criador (peça).

## ASSETS-PENDENTES.md (modelo)

```markdown
# Assets pendentes de {{Nome}} (atualizado dd/mm/aaaa)

O que já está pronto: N músicas, N efeitos, N itens de pack, fontes X e Y.

Falta você mandar (coloque o arquivo em qualquer pasta e me diga o caminho, ou
arraste para a conversa):
- [ ] Logo em PNG com fundo transparente: aparece no fechamento sério (guia, seção 8.5).
- [ ] Pack de transições e efeitos que você usa (pasta inteira): flash de capítulo e efeitos sonoros.
- [ ] Fonte "Nome da Fonte" (.ttf): legenda dos memes (guia 6.1). Por enquanto uso Montserrat 900.
- [ ] Música "X - Y": não achei em boa qualidade; se tiver o arquivo, mande.
```

Cada item com: o que é, onde aparece no guia, o substituto provisório.
