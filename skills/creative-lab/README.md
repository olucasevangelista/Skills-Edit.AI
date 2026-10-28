# creative-lab

Direção para editar **anúncios em vídeo** (Meta Ads, TikTok Ads, Reels e Shorts patrocinados) pensada para reter e mostrar o resultado prometido: gancho com promessa visível, ritmo apertado, inserts, motion e tela dividida, destaque do mecanismo único, uso da página de vendas para entender a copy e **variação de criativos** para teste. Inclui um script que junta vários ganchos a um mesmo corpo de anúncio.

Cuida da edição e do visual, não do roteiro falado. Os motions e as animações são feitos no Remotion (skill do Remotion) e a transcrição vem da skill `transcrever-groq`.

## Instalar

```
npx skills add olucasevangelista/Skills-Edit.AI --skill creative-lab -g
```

Depois, no chat do agente, chame `/creative-lab` e diga o que quer ("edita esse anúncio" ou "faz 5 versões com ganchos diferentes").

## O que precisa

Só o script precisa de **Python 3.10+** (só biblioteca padrão) e **FFmpeg** com `ffprobe` (`winget install Gyan.FFmpeg` no Windows, `brew install ffmpeg` no macOS). O resto é direção em texto.

## Conteúdo

| Arquivo | Para quê |
|---|---|
| `references/anuncio-e-retencao.md` | anatomia do anúncio, ritmo, loops abertos, zoom, emenda com sobreposição, texto e som |
| `references/gancho.md` | padrões de gancho, escolha por tipo de oferta, regras do texto |
| `references/resultado-e-mecanismo.md` | mostrar o resultado e o quanto ajuda; destacar o mecanismo único |
| `references/copy-da-pagina.md` | pedir a página, mapa de copy, como a copy decide a edição |
| `references/variacoes.md` | teste de criativos, matriz, os modos de variação, métricas |
| `references/inserts-texto-e-zonas.md` | inserts, legendas, zonas seguras, logos |
| `references/conformidade.md` | prova honesta, antes e depois, promessas sensíveis |
| `references/verificador.md` | auditoria do anúncio |
| `scripts/variar_ganchos.py` | junta cada gancho ao corpo, com emenda por sobreposição, no mesmo volume, e gera `matriz.csv` |

## O script

```
python scripts/variar_ganchos.py --corpo corpo.mp4 --ganchos g1.mp4 g2.mp4 --saida variantes --prefixo anuncio
```

Gera `anuncio__g1.mp4`, `anuncio__g2.mp4` e `matriz.csv`. O corpo é codificado uma vez e reaproveitado; a imagem e o áudio do corpo entram juntos, antes de a fala do gancho acabar; todas as variantes saem no mesmo volume (−14 LUFS por padrão).

## Estado dos testes

| Item | Situação |
|---|---|
| Testes automáticos do script (11) | Passando no Windows 11, com mídia sintética (cada trecho com um tom e uma cor) |
| Sobreposição | Medida: a imagem e o áudio do corpo entram com ~0,03 s de diferença e ~0,09 s antes de a fala do gancho acabar. Um controle com sobreposição mínima reprova no mesmo teste |
| Volume | As variantes sintéticas ficaram em −13,7 a −13,8 LUFS (alvo −14), com menos de 0,2 dB de diferença entre elas |
| Corpo | O mesmo quadro do corpo é idêntico em todas as variantes; gancho de outra proporção sai no tamanho do corpo; nomes e `matriz.csv` conferidos |
| Mídia real (um vídeo seu de 1080p, 21,8 s de corpo e dois ganchos de 5 s) | 2 variantes em 23 s, as duas em −14,0 LUFS; o corte de imagem caiu em 4,93 s (previsto 4,94 s) e sem estalo (salto 0,087; o limite é 0,35) |
| **Sentido da ponte entre gancho e corpo** | **Não é medido pelo script.** É conferência de quem edita (ler o fim do gancho junto do começo do corpo) |
| **macOS** | **Não testado** |
| **Desempenho de anúncio** | **Nada foi medido.** A skill não afirma que um tipo de gancho converta mais |
| **Políticas das plataformas** | **Não foram conferidas.** `conformidade.md` manda o usuário conferir as vigentes |

Rodar os testes: `python -m unittest discover -s tests` (precisa de FFmpeg).

## Limites que vale conhecer

- **Zonas seguras:** os valores variam entre as fontes (a base vai de ~320 a ~670 px em guias diferentes) e entre as versões dos apps. A skill usa um ponto de partida conservador e manda confirmar na especificação atual da plataforma ou num print da interface.
- **Métricas:** hook rate é calculado pelo anunciante (visualizações de 3 s ÷ impressões). O hold rate tem definições diferentes entre as fontes, então a skill manda escolher uma e usar a mesma em todas as variantes.
- Os números de ritmo (evento a cada ~1 a 1,5 s no começo, no máximo 2,5 s depois) são pontos de partida, não leis. A referência do usuário vence.
- O script **só junta**. Criar cada gancho (texto, tela dividida, motion) é feito no Remotion ou no editor da pessoa. O corpo e os ganchos precisam ter imagem e áudio.
