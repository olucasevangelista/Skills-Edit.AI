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

Instalar a transcrição:

```
npx skills add olucasevangelista/Skills-Edit.AI --skill transcrever-groq -g
```

## Segurança

Skills rodam com as permissões do seu agente. Leia o conteúdo antes de instalar. Nenhuma skill daqui guarda chaves em arquivos do repositório.
