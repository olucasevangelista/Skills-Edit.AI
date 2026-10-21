# copystyle

Direção e um script de medição para estudar vídeos de referência de edição (Reels, TikToks, Shorts) quadro a quadro e montar o **guia de estilo** de um criador: formatos meme e sério, legendas com fonte, tamanho e posição, gancho, inserts, ritmo, música e efeitos com níveis, zonas do 9:16 e checklist de QA. Junto saem os estilos visuais em tokens (`estilos.json`) e a lista de assets que faltam.

O guia serve para qualquer editor, humano ou agente. A montagem do vídeo é feita com a skill do Remotion, e a transcrição das referências vem da skill `transcrever-groq`.

## O que precisa

**Python 3.10+** (só biblioteca padrão) e **FFmpeg** com `ffprobe` (`winget install Gyan.FFmpeg` no Windows, `brew install ffmpeg` no macOS). Nada mais é instalado.

## Script

| Comando | Para quê |
|---|---|
| `analisar.py analisar <videos> --saida <pasta>` | por vídeo: duração, tamanho, fps, cortes de cena por minuto, volume e picos de som, folhas de contato 6x3 com o tempo em cada quadro |
| `analisar.py quadro <video> <t>` | um quadro em resolução cheia, para medir fonte, tamanho e posição |
| `analisar.py quadro <video> <t> --rajada 1.5 --fps 10` | uma rajada de quadros, para ver a animação de uma legenda ou de um insert |

## Estado dos testes

| Item | Situação |
|---|---|
| Testes automáticos (5) | Passando no Windows 11, com vídeo sintético |
| Vídeo real (um Short vertical 1080x1920 a 60 fps de 14,6 s) | Folhas de contato com o tempo escrito em cada quadro, `meta.json` e `sons.json` conferidos |
| **macOS** | **Não testado.** O tempo escrito nas folhas usa uma fonte do sistema; se nenhuma for achada, a folha sai sem o número e o nome do arquivo diz o intervalo |
| Fluxo completo da skill (entrevista, agentes que dissecam, escrita do guia) | **Não testado de ponta a ponta**: é direção para o agente, sem script que o execute |

Rodar os testes: `python -m unittest discover -s tests` (precisa de FFmpeg).

## Limites que vale conhecer

- Os cortes de cena vêm da mudança de brilho entre quadros: zoom e jump cut leve não aparecem, e dois planos de luminância parecida podem passar batido. Confira nas folhas.
- Os picos de volume (`transientes`) são pistas, não identificação: podem ser efeito sonoro, batida de música ou início de fala. A skill não identifica músicas; quando não há como saber o nome, o guia registra "não identificada" e a pendência vai para o criador.
