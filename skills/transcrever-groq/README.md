# transcrever-groq

Transcreve vídeo ou áudio com a Groq (Whisper) e entrega texto, legendas `.srt` e um JSON com o tempo de cada palavra. Você configura a chave da Groq **uma única vez**; ela fica guardada no cofre do seu computador (Gerenciador de Credenciais do Windows ou Keychain do macOS) e funciona em qualquer pasta ou projeto. Não precisa de arquivo `.env`.

Serve para uso direto no terminal e para agentes como Claude Code e Codex.

## O que você precisa

1. **Python 3.10 ou mais novo** ([python.org](https://www.python.org/downloads/)).
2. **FFmpeg** (o `configurar.py ambiente` diz o comando para o seu sistema).
3. Uma **chave da Groq**, criada em [console.groq.com/keys](https://console.groq.com/keys).

## Primeira vez (uma vez só)

**Pelo agente (o jeito mais simples).** Instale a skill (veja "Usar como skill de agente" abaixo), abra o chat e chame `/transcrever-groq`. O agente confere o computador, instala o que faltar (pedindo sua permissão), pede a sua chave da Groq no chat e guarda no cofre do computador. Você só cola a chave. Nas próximas vezes ele não pede mais, em nenhum projeto.

**Sozinho, no terminal (opcional).** Abra o PowerShell ou o Terminal e rode, na pasta desta skill:

```
python scripts/configurar.py setup          # Windows
python3 scripts/configurar.py setup         # macOS
```

O assistente confere o sistema, cria um ambiente Python próprio (numa pasta sua, fora dos projetos), pede a chave **sem mostrar o que você cola**, confere com a Groq e só então guarda no cofre.

Em ambos os casos a chave nunca vai para argumento de comando, arquivo ou log. Pelo agente, ela é enviada ao programa pela entrada padrão (`configurar.py setup --stdin`). Observação: se você cola a chave no chat, ela fica no histórico daquela conversa. Dá para revogá-la quando quiser em console.groq.com/keys; se preferir, crie uma chave só para esta skill.

## Usar

```
python scripts/transcrever.py "C:\videos\aula.mp4" --saida "C:\projeto\transcricoes"
```

Ele cria `transcricoes/aula/` com `transcricao.txt`, `legendas.srt`, `transcricao.json` e `legendas.remotion.json`. `--saida` é obrigatório.

Opções úteis: `--nome`, `--contexto "nomes e termos técnicos"`, `--inicio` e `--fim` (segundos, `MM:SS` ou `HH:MM:SS`), `--idioma` (padrão `pt`), `--refazer`. Veja `python scripts/transcrever.py --help` e [references/saidas.md](references/saidas.md).

## Gerenciar a chave

| Quero | Comando |
|---|---|
| Ver se está configurada (sem revelar) | `python scripts/configurar.py status` |
| Trocar a chave | `python scripts/configurar.py update` (o agente usa `update --stdin`) |
| Apagar a chave | `python scripts/configurar.py remove` |
| Preparar ou consertar o ambiente | `python scripts/configurar.py ambiente` |

Também dá para usar a variável de ambiente `GROQ_API_KEY` (útil em servidores). Se ela e o cofre existirem ao mesmo tempo, vale o cofre.

## Problemas

Veja [references/solucao-de-problemas.md](references/solucao-de-problemas.md) (cofre bloqueado ou indisponível, Python antigo, FFmpeg).

## Instalar como skill de agente

Com o Node.js instalado, um comando instala a skill para os agentes que você escolher (Claude Code, Codex e outros):

```
npx skills add olucasevangelista/Skills-Edit.AI --skill transcrever-groq -g
```

Sem `-a`, o comando pergunta em quais agentes instalar. Para já escolher: `-a claude-code -a codex`. Depois, no chat do agente, chame `/transcrever-groq`. O próprio agente faz a configuração (`setup --stdin`) quando você enviar a chave no chat. Para atualizar: `npx skills update`. Para remover: `npx skills remove transcrever-groq -g`.

## Estado dos testes

| Item | Situação |
|---|---|
| Windows 11, Python 3.13, Gerenciador de Credenciais real (gravar, ler, trocar e apagar) | Testado |
| Testes automáticos (39): cofre simulado, erros do cofre, chave ausente, pastas diferentes, regressão da transcrição | Passando |
| Saída idêntica à do script original para a mesma resposta da Groq | Verificado |
| Configuração pelo agente (`setup --stdin`) em ambiente novo, com cofre real do Windows (chave de teste; gravar, trocar, apagar) | Testado |
| Validação de uma chave **real** na Groq e uma transcrição real com a chave guardada | Ainda não feito: falta uma chave real |
| **macOS (Keychain)** | **Não testado.** O código usa a mesma biblioteca (`keyring`), mas nenhum teste foi feito em um Mac. |

Para validar no macOS, rode na pasta da skill: `python3 scripts/configurar.py ambiente`, `python3 scripts/configurar.py setup`, `python3 scripts/configurar.py status` e, com o Python do ambiente criado, `RUN_REAL_KEYRING=1 python -m unittest discover -s tests -v`. O macOS pode pedir permissão para o Python acessar o Keychain; escolha "Sempre Permitir".
