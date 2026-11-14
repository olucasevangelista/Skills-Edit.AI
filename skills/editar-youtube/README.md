# editar-youtube

Direção para o agente editar **vídeos longos de YouTube**: identificar o tipo de vídeo (pessoa falando, gravação de tela com rosto no canto, motion no corpo ou uma mistura), limpar a fala, abrir com um gancho forte, manter a curiosidade até o fim e lembrar a pessoa de seguir nos momentos certos. A skill **não entrega elementos prontos**: a estética é da pessoa, e quem cria os elementos é o agente, no Remotion.

A limpeza da fala usa cortes medidos no áudio, emenda por sobreposição de imagem e áudio, verificação e a escolha do melhor take entre as repetições.

## Instalar

```
npx skills add olucasevangelista/Skills-Edit.AI --skill editar-youtube -g
```

Depois, no chat do agente, chame `/editar-youtube` e diga o que quer ("edita esse vídeo do canal").

## O que tem dentro

| Arquivo | Para quê |
|---|---|
| `references/tipos-de-video.md` | como identificar o tipo (olhando quadros) e o que cada um pede |
| `references/abertura.md` | os primeiros 5 a 10 segundos: promessa sem entregar o final, como achar o momento-gancho no meio do vídeo, maneiras de abrir |
| `references/meio-e-ritmo.md` | o meio por tipo de vídeo, momentos-chave e a emenda com sobreposição |
| `references/chamadas-para-seguir.md` | onde lembrar de seguir ou inscrever-se (cedo, perto do fim e no final) |
| `references/limpeza.md` | da gravação bruta ao `limpo.mp4`: melhor take, erros, silêncios, emendas, gravação de tela, verificação |
| `references/exportacao.md` | exportação rápida dos elementos que só colocam coisas por cima, e quando não usar |

## Scripts (opcionais)

Precisam de **Python 3.10+** (só biblioteca padrão, exceto o recorte) e **FFmpeg** com `ffprobe` (`winget install Gyan.FFmpeg` no Windows, `brew install ffmpeg` no macOS).

| Script | Para quê |
|---|---|
| `diagnosticar.py` | formato, volume, fala e avisos do arquivo bruto |
| `achar_repeticoes.py` | aponta takes repetidos na transcrição e sugere o `--remover` |
| `planejar_cortes.py` | acha as pausas pelo volume (o limiar acompanha o ruído de sala), remove os erros indicados e calcula as emendas |
| `montar.py` | aplica os cortes, emenda com sobreposição e normaliza o volume (padrão -14 LUFS) |
| `verificar_cortes.py` | mede duração, sincronia, volume, pausas que sobraram e estalos |
| `recortar_pessoa.py` | recorta a pessoa de qualquer fundo (RVM) e grava a posição da cabeça; precisa de PyTorch |
| `clips.mjs` | renderiza só as janelas com elemento de uma composição Remotion transparente (precisa de Node.js e de um projeto Remotion) |
| `colar.py` | cola esses clipes sobre o vídeo limpo e exporta o final, com uma folha de conferência |

## Estado dos testes

| Item | Situação |
|---|---|
| Limpeza da fala (`tests/test_cortes.py`, 17 testes) | Passando no Windows 11, com áudio sintético em duas condições de ruído e controles negativos (o verificador reprova um arquivo que ficou com pausas; o detector de repetições não agrupa takes diferentes) |
| Exportação rápida (`tests/test_colar.py`, 5 testes) | Passando |
| A própria skill (`tests/test_skill.py`) | Frontmatter válido, referências existentes, nenhuma outra skill citada, scripts de corte em dia com a versão corrigida mantida no repositório |
| **Nenhum vídeo de YouTube real foi editado seguindo esta skill** | **Não testado de ponta a ponta.** A direção sobre abertura, meio e chamadas para seguir vem do que o autor pediu; é direção para o agente, sem script que a execute |
| Limpeza em gravação humana com ruído real | Não testada. O detector de repetições nunca viu retakes reais |
| Gravação de tela: o passo de conferir se a tela mudou durante uma pausa | Descrito, **não testado** |
| `recortar_pessoa.py` | Testado em 3 s de vídeo real com GPU; em CPU não medido |
| macOS | Não testado |

Os números (posições das chamadas para seguir, ritmo, duração de texto) são **pontos de partida**; nenhum foi medido em desempenho de vídeo.

Rodar os testes: `python -m unittest discover -s tests` (precisa de FFmpeg).
