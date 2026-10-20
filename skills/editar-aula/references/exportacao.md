# Exportação rápida de motions

Renderizar a aula inteira no Remotion é lento: ele abre o Chrome, tira uma captura por quadro (até em quadro vazio) e ainda decodifica o vídeo dentro do Chrome a cada quadro. Quando os motions só **colocam coisas por cima** do vídeo, dá para renderizar **só os segundos em que existem** e deixar o FFmpeg fazer a codificação do vídeo uma única vez.

## Quando usar

- **Use** para motions que só adicionam pixels: cartelas de título, destaques de texto, listas, cards e telas cheias com fundo opaco.
- **Não use** para motions que transformam o vídeo: punch-in ou zoom, corte, tela dividida com o rosto reposicionado, efeito de cor no rosto. Esses precisam do vídeo dentro da composição: renderize direto com o Remotion (skill do Remotion).

## Medido por um agente em testes reais (valores do relatório do usuário)

| | Render direto | Só as janelas com motion + FFmpeg |
|---|---|---|
| Aula | 9:23, 17 motions | 7:28, 12 motions |
| Tempo | ~33 min estimados (cancelado em ~35%) | ~7,5 min (Remotion 2 min 10 s + FFmpeg 5 min) |

Ressalvas: as aulas eram diferentes e a qualidade foi comparada **só visualmente** (quadros sobre cada motion), sem medida objetiva. Não use esses números como promessa de tempo.

## O fluxo

1. **Vídeo limpo:** `aula_limpa.mp4` (e `timeline.json`) do `montar.py`, ou o vídeo que o usuário já tem limpo.
2. **Projeto Remotion com duas composições** que usam o mesmo componente de motions:
   - `Aula`: a prévia no Studio, com `<Video src={staticFile('aula_limpa.mp4')} />` e os motions por cima.
   - `Motions`: **só os motions**, fundo transparente, e **a mesma duração, taxa de quadros e tamanho do vídeo limpo**. É esta que vai para o render.
   - Escreva cada motion como `<Sequence from={Math.round(T * fps)} durationInFrames={Math.round(D * fps)}>`, com `T` e `D` em segundos do vídeo limpo e `fps` vindo de `useVideoConfig()`.
3. **`janelas.json`:** a lista dos motions com nome, início e duração (você já sabe, porque foi quem os planejou).
   ```json
   [{"nome": "Titulo da aula", "inicio": 1.0, "duracao": 3.0},
    {"nome": "Destaque", "inicio": 95.5, "duracao": 2.2}]
   ```
4. **Clipes:** `node <skill>/scripts/clips.mjs janelas.json --projeto <pasta do projeto Remotion> --saida clips`. Cada janela vira um clipe ProRes 4444 com transparência; **janelas que se sobrepõem são unidas** num clipe só (senão o motion apareceria desenhado duas vezes).
5. **Colar e exportar:** `python <skill>/scripts/colar.py trabalho/aula_limpa.mp4 clips/manifest.json --saida aula_final.mp4 --folha`. O vídeo é codificado uma vez com os clipes por cima, e o áudio é copiado sem recodificar. `--folha` gera `folha_motions.png`, um quadro no meio de cada motion.
6. **Conferir:** duração igual à do vídeo limpo e a folha de conferência: cada motion apareceu, no tempo certo, legível e sem cobrir rosto, mãos ou o conteúdo da tela.

Qualidade: `colar.py` codifica em libx264 com CRF 14 (`--qualidade maxima` usa o preset `slow`, mais lento).

## Pegadinhas

| Problema | Solução |
|---|---|
| "not a valid Remotion project" ao renderizar | A porta está ocupada pelo Studio (3000). O script usa a 3100 (`--porta`) |
| Erro do bundler com caminho estranho | Um `!` no caminho do projeto quebra o bundler. Mova o projeto Remotion para uma pasta sem `!` (vídeos e saídas podem ficar onde estão) |
| O projeto usa Rspack e o bundler reclama | Acrescente `--rspack` (a API do Node não lê o `remotion.config.ts`) |
| 404 do vídeo na prévia | Use `staticFile('arquivo.mp4')` no `<Video>` |
| `interpolate` quebra | O intervalo de entrada precisa ser estritamente crescente; inverta a saída, não a entrada |
| Um render falho parece "concluído" | Não esconda o código de saída com `| tail`; confira o código ao final |

## Se houver motion que transforma o vídeo

Misture os dois caminhos só se for simples: nesse caso, prefira o render direto de toda a aula (mais lento) em vez de tentar juntar métodos.
