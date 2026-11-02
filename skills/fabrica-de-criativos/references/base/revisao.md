# Revisão

Não confie na prévia: confira o que foi renderizado. Estes comandos funcionam; troque os nomes pelos do projeto.

## 1. Quadros de diagnóstico

Um quadro por instante-chave: o primeiro quadro (gancho), cada troca de elemento, a mudança de layout, o CTA e o último quadro.

```
npx remotion still src/index.ts <Composicao> out/f120.png --frame=120 --props=props.json
```

Monte uma folha de contato para ver a sequência de uma vez:

```
ffmpeg -i out/f20.png -i out/f120.png -i out/f200.png -filter_complex "[0:v]scale=360:-1[a];[1:v]scale=360:-1[b];[2:v]scale=360:-1[c];[a][b][c]hstack=inputs=3" folha.png
```

Olhe a folha: o gancho aparece, o formato é reconhecível, nada está vazio ou no lugar errado, o texto cabe e se lê. Inclua quadros **entre** os instantes-chave: é ali que a câmera, os cruzamentos e as transições mostram erros.

## 2. O arquivo exportado

```
python <skill>/scripts/verificar_saida.py out/criativo.mp4 --duracao 30
```

Ele mede: **tamanho** (1080x1920), **taxa de quadros**, **duração**, se há **áudio**, o **volume** (LUFS e pico), **quadros pretos** e **imagem congelada**, e sai com código 1 se algo estiver fora do esperado. Opções: `--lufs` (alvo, padrão −14), `--tamanho 1080x1920`, `--duracao` (esperada).

Compare um quadro do arquivo com o mesmo quadro da prévia: devem ser iguais.

**Se o volume saiu fora do alvo** (o Remotion exporta o áudio como está; um trecho de fala costuma sair perto de −18 LUFS): meça e normalize em duas passadas, sem tocar na imagem.

```
ffmpeg -i criativo.mp4 -vn -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -
ffmpeg -i criativo.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true" -c:a aac -b:a 192k -ar 48000 criativo_14.mp4
```

Troque os `<...>` pelos valores impressos pela primeira. Num teste, um arquivo de −18,9 LUFS saiu com −14,0; a duração cresceu 0,1 s (o AAC acrescenta um pequeno silêncio no começo), então rode o `verificar_saida.py` de novo no arquivo final.

## 3. Medidas por pixel (opcional, para zonas seguras)

Com Python e uma biblioteca de imagem, confira que **não há texto claro** no topo (0 a 270 px), na base (a partir de ~1250 px) e nas laterais (menos de 90 e mais de 990 px). Um **objeto que sai de cena** pode cruzar a margem; texto e rosto parados, não.

## 4. Checklist geral

- [ ] O primeiro quadro tem um assunto e já mostra o formato escolhido.
- [ ] Há um evento visual nos primeiros 1,5 s e nenhuma lacuna acima de ~2,5 s.
- [ ] Cada corte tem emenda com sobreposição, sem palavra cortada e sem estalo.
- [ ] Legenda presente, correta, com realce nos trechos ★, fora da base e sem cobrir a boca.
- [ ] Texto e rosto dentro das zonas seguras; texto com tempo de leitura.
- [ ] Voz limpa e em primeiro plano; música bem abaixo; volume final perto de −14 LUFS.
- [ ] O CTA está claro nos últimos segundos, sem fade que sugira "acabou".
- [ ] Todo material de prova (depoimento, resultado, antes e depois, conversa) é real, autorizado ou está identificado como ilustração ou dramatização.
- [ ] O `MATERIAIS.md` lista o que foi buscado, de onde e com qual licença.
- [ ] O checklist do próprio formato (no fim do arquivo dele) passou.

## 5. O que declarar na entrega

Diga o que foi verificado (quadros, medidas, arquivo) e **o que não foi**. Em geral:

- A **reprodução contínua com som** (você não escuta): peça à pessoa que assista no player.
- O **gosto** da música e do ritmo.
- As **políticas da plataforma** e as **licenças**: são da pessoa.
- Qualquer simplificação que mude o formato (por exemplo, recorte feito por chroma key em vez de segmentação).
