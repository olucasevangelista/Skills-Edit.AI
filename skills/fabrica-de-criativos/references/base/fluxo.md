# Fluxo: do material ao arquivo final

O mesmo caminho vale para os 15 formatos. O que muda de um formato para outro está no arquivo de `references/formatos/`.

## 1. Receber e inspecionar o material

- Liste o que chegou (vídeos, imagens, áudios, roteiro, gravação de tela) e **leia as propriedades** de cada vídeo: tamanho, taxa de quadros, duração, se tem áudio.
  `ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,width,height,r_frame_rate -of default=nw=1 arquivo.mp4`
- Vídeo de celular em pé gravado deitado, taxa de quadros variável e vídeo HDR aparecem nas propriedades: avise se isso afeta o resultado.
- O **original nunca é alterado**. Trabalhe em uma pasta do projeto (`public/` do Remotion) com cópias ou caminhos.

## 2. Transcrever (se há fala)

Você precisa da **fala com o tempo de cada palavra** para legenda, cortes e inserts.

- Se a skill `transcrever-groq` estiver disponível, use-a. Ela gera o `transcricao.json` e o `legendas.remotion.json` (a lista de legendas no formato do Remotion).
- Se não, use outro meio de transcrição com tempo por palavra que você tenha, ou o **roteiro** que a pessoa mandou, com os tempos marcados pelas pausas do áudio. Sem tempo por palavra, faça a legenda **por frase**.
- O Whisper erra palavras e às vezes omite frases repetidas. A legenda que já está queimada no vídeo, se houver, é a verdade.

## 3. Escolher o formato e planejar

- Se a pessoa não sabe o formato, use a tabela do `SKILL.md` (ideal quando, evite quando) e **recomende um**, com o motivo em uma linha.
- Marque a fala em três níveis: **★ chave** (promessa, número, virada, prova, oferta), **normal** e **baixa**. Isso decide onde vão zoom, texto e insert.
- Monte a **tabela de eventos**: `Início (s) | Evento | Fala`, uma linha curta por evento. O arquivo do formato diz quais eventos existem nele.
- Cheque as **lacunas**: em anúncio, nenhum trecho passa de ~2,5 s sem um evento novo (nos primeiros 5 s, ~1 a 1,5 s). Veja `legenda-e-zonas.md` e o arquivo do formato.

## 4. Montar o projeto

- Crie ou use o projeto Remotion da pessoa (a skill do Remotion explica como). Materiais em `public/`.
- **Se a pessoa quiser usar o kit** (`kit/`), copie `componentes/` e a composição do formato escolhido para `src/`, troque os **props** (`video`, `legendas`, `titulo`, cores, fonte, duração e os específicos do formato) e ajuste. Se preferir, monte do zero seguindo o arquivo do formato.
- Tudo configurável fica num `config.ts` (formato, tempos, textos, cores). As cenas só leem dele, e a pessoa ajusta depois sem refazer.
- **Cortes e emendas:** `cortes.md`.
- **Legenda, texto e zonas seguras:** `legenda-e-zonas.md`.
- **Materiais que faltam:** `materiais.md`.

## 5. Prévia e render

- Mostre uma **prévia** (quadros nos instantes-chave ou o Studio) antes do render final, e só exporte o arquivo final quando a pessoa pedir ou quando o pedido já for "faz tudo".
- Padrão de exportação: **1080x1920, 30 fps, H.264, yuv420p, áudio AAC**. Exemplo de comando:
  `npx remotion render src/index.ts <Composicao> out/criativo.mp4 --props=props.json --codec=h264 --crf=18 --pixel-format=yuv420p --image-format=png --concurrency=2`
  (`--image-format=png` preserva o texto nítido; `--props` troca os props sem editar o código, o que facilita as variações.)
- Em peças 3D, use `--gl=angle`.
- Não esconda o código de saída de um render com falha (`| tail`): confira ao final.

## 6. Verificar e entregar

- Rode `scripts/verificar_saida.py` no arquivo final e a revisão de `revisao.md` (quadros nos instantes-chave, zonas seguras, checklist do formato).
- Entregue: o arquivo, o `MATERIAIS.md` (o que foi buscado, de onde, a licença), o que ficou pendente e o que você **não** conseguiu verificar (por exemplo, a reprodução com som).
- Formato da mensagem: curto. Suposições em até 5 linhas, o plano em tabela e a verificação em até 3 linhas.
