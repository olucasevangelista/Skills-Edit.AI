# Solução de problemas

Comece por `python configurar.py status`: ele diz o que está faltando, sem mostrar a chave.

## Python

- Precisa de **Python 3.10 ou mais novo**. Confira com `python --version` (macOS: `python3 --version`).
- Windows: instale em python.org (marque "Add Python to PATH") ou `winget install Python.Python.3.13`.
- macOS: o Python que vem com as ferramentas da Apple pode ser antigo. Instale em python.org ou com `brew install python`. No macOS use `python3` nos comandos.

## FFmpeg

A transcrição usa `ffmpeg` e `ffprobe` para extrair o áudio.
- Windows: `winget install Gyan.FFmpeg`, depois feche e abra o terminal.
- macOS: `brew install ffmpeg` (Homebrew em https://brew.sh).
- `python configurar.py ambiente` mostra o que falta.

## Cofre de credenciais

`status` retorna código 2 e uma mensagem quando o cofre tem problema.

**Bloqueado / acesso negado**
- macOS: abra "Acesso às Chaves", desbloqueie o chaveiro "login". Quando o macOS perguntar se o Python pode usar a chave, digite a senha do Mac e escolha **"Sempre Permitir"**. Se aparecer o pedido a cada uso, é porque foi escolhido "Permitir" em vez de "Sempre Permitir".
- Windows: o Gerenciador de Credenciais é por conta de usuário. Use o terminal normal da sua conta (evite sessões remotas ou contas de serviço).

**Cofre indisponível (sem backend)**
- Acontece em conexões SSH, contêineres, servidores e alguns Linux sem ambiente gráfico.
- Alternativa suportada: defina a variável de ambiente `GROQ_API_KEY` na sessão que vai rodar a transcrição. Prefira defini-la só para o processo (por exemplo, no gerenciador de segredos do servidor) em vez de gravá-la em arquivos.

**"O componente keyring não está instalado"**
- Rode `python configurar.py setup` (ou `ambiente`), que cria o ambiente próprio e instala as bibliotecas.

## Ambiente próprio (venv)

- Fica em uma pasta do usuário, fora dos projetos: Windows `%LOCALAPPDATA%\transcrever-groq\venv`, macOS `~/Library/Application Support/transcrever-groq/venv`.
- Para recriar do zero: `python configurar.py ambiente --forcar`.
- Para mudar de lugar: defina `TRANSCREVER_GROQ_HOME`.

## Chave

- "A Groq recusou essa chave": gere outra em console.groq.com/keys e rode `configurar.py update`.
- Colou a chave por engano em chat, e-mail ou arquivo: revogue-a no painel da Groq e crie outra.
- A chave nunca é gravada em arquivo por esta skill. Se existir `GROQ_API_KEY` no ambiente e também uma chave no cofre, **o cofre vale**; `status` mostra qual está em uso.
