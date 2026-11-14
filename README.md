# Skills Edit.AI

Skills para agentes de IA (Claude Code, Codex e outros) do treinamento Edit.AI: edição de vídeo com inteligência artificial.

## Como instalar

Você precisa do [Node.js](https://nodejs.org) instalado (ele traz o comando `npx`). Se não tiver, peça ao seu agente: *"instale o Node.js para mim"*.

Instalar uma skill (para todos os seus projetos):

```
npx skills add olucasevangelista/Skills-Edit.AI --skill NOME-DA-SKILL -g
```

O comando pergunta em quais agentes você quer instalar. Para escolher direto, acrescente `-a claude-code -a codex`.

Outros comandos:

| Quero | Comando |
|---|---|
| Ver todas as skills disponíveis | `npx skills add olucasevangelista/Skills-Edit.AI --list` |
| Instalar todas de uma vez | `npx skills add olucasevangelista/Skills-Edit.AI --skill '*' -g` |
| Atualizar as instaladas | `npx skills update` |
| Remover uma skill | `npx skills remove NOME-DA-SKILL -g` |

Também funciona pedir ao próprio agente: *"instale a skill rodando este comando: ..."*. Depois de instalada, chame a skill no chat com `/` e o nome dela.

## Skills disponíveis

| Skill | O que faz |
|---|---|
| [`transcrever-groq`](skills/transcrever-groq) | Transcreve vídeo e áudio com a Groq (Whisper) e gera texto, legendas SRT e JSON com o tempo de cada palavra. Na primeira vez o agente pede a sua chave da Groq e guarda no cofre do computador; depois nunca mais pede. |
| [`editar-reels`](skills/editar-reels) | Guia de edição de Reels, TikTok e Shorts para retenção: gancho com o assunto em destaque no primeiro segundo, uma novidade visual a cada 2 a 3 s, zoom com ênfase, inserts e cortes com sobreposição na fala. Funciona com qualquer ferramenta de edição. |
| [`editar-aula`](skills/editar-aula) | Direção para editar aulas gravadas (câmera, tela com rosto, slides ou só áudio): o que limpar, como dividir em seções com capítulos e onde colocar títulos, destaques e motions sem cobrir o que o aluno precisa ver. Inclui scripts opcionais para cortar pausas e erros. |
| [`motion-designer`](skills/motion-designer) | Direção para criar motion design no Remotion: motions explicativos que mostram um processo ou uma relação sincronizados com a fala, e peças inteiras só de objetos animados em 2D ou 3D (comerciais conceituais, vinhetas, vídeos de produto). Inclui um kit opcional de código e uma síntese opcional de trilha e efeitos sonoros. |
| [`creative-lab`](skills/creative-lab) | Direção para editar anúncios em vídeo com foco em retenção: gancho com promessa visível, ritmo apertado, resultado e mecanismo único em destaque, uso da página de vendas como direção e teste de criativos. Inclui um script que junta vários ganchos a um mesmo corpo de anúncio, com emenda por sobreposição e no mesmo volume, e scripts para limpar a fala do bruto (silêncios, erros e takes repetidos). |
| [`editar-youtube`](skills/editar-youtube) | Direção para editar vídeos longos de YouTube (pessoa falando, tela com rosto no canto, motion no corpo ou mistura): identifica o tipo de vídeo, limpa a fala com emenda por sobreposição (silêncios, erros e takes repetidos), planeja uma abertura forte que instiga sem entregar o final, o meio conforme o estilo da pessoa e as chamadas para seguir no começo e perto do fim. Não entrega elementos prontos: a estética é sua. Inclui scripts de limpeza. |
| [`fabrica-de-criativos`](skills/fabrica-de-criativos) | Guia para o agente editar criativos de anúncio em vídeo no Remotion em 16 formatos (tela dividida, fundo verde, post de rede social, notícia, professor, motion design, depoimento, react, videochamada, corte de podcast, telejornal, tutorial de tela, conversa de chat, antes e depois, cinema e caixinha de pergunta), misturando formatos e adaptando à marca de quem anuncia. Traz direção, estruturas possíveis e exemplos reais de cada formato, algumas peças de código para reaproveitar no Remotion (caixinha de pergunta, manchete de notícia, cenário de telejornal e emenda com sobreposição) e scripts de apoio para limpar a fala (silêncios, erros e takes repetidos), recortar a pessoa e medir o arquivo final. Não traz template que edite por você. |

Instalar a transcrição:

```
npx skills add olucasevangelista/Skills-Edit.AI --skill transcrever-groq -g
```

Instalar o guia de edição de Reels:

```
npx skills add olucasevangelista/Skills-Edit.AI --skill editar-reels -g
```

Instalar a direção de edição de aulas:

```
npx skills add olucasevangelista/Skills-Edit.AI --skill editar-aula -g
```

Instalar o motion design:

```
npx skills add olucasevangelista/Skills-Edit.AI --skill motion-designer -g
```

Instalar a edição de anúncios:

```
npx skills add olucasevangelista/Skills-Edit.AI --skill creative-lab -g
```

Instalar a edição de vídeos de YouTube:

```
npx skills add olucasevangelista/Skills-Edit.AI --skill editar-youtube -g
```

Instalar a fábrica de criativos:

```
npx skills add olucasevangelista/Skills-Edit.AI --skill fabrica-de-criativos -g
```

## Segurança

Skills rodam com as permissões do seu agente. Leia o conteúdo antes de instalar. Nenhuma skill daqui guarda chaves em arquivos do repositório.
