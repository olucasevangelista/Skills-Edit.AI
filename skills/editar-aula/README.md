# editar-aula

Direção para o agente editar aulas gravadas com padrão e qualidade: o que limpar, como dividir em seções com capítulos e onde colocar títulos, destaques e motions explicativos, sem cobrir o que o aluno precisa ver. Inclui scripts opcionais de limpeza (cortar pausas e erros) e uma exportação rápida dos motions.

Os motions são criados com a skill do Remotion.

## Instalar

```
npx skills add olucasevangelista/Skills-Edit.AI --skill editar-aula -g
```

Depois, no chat do agente, chame `/editar-aula` e diga o que quer ("edita essa aula").

## Scripts (opcionais)

Precisam de **Python 3.10+** (só biblioteca padrão) e **FFmpeg** com `ffprobe` (`winget install Gyan.FFmpeg` no Windows, `brew install ffmpeg` no macOS).

| Script | Para quê |
|---|---|
| `diagnosticar.py` | formato, volume, fala e avisos do arquivo bruto |
| `planejar_cortes.py` | acha as pausas pelo volume, remove os erros indicados e calcula as emendas |
| `montar.py` | aplica os cortes e normaliza o volume em -16 LUFS |
| `verificar.py` | mede duração, sincronia, volume, pausas que sobraram e estalos |
| `clips.mjs` | renderiza só as janelas com motion de uma composição Remotion transparente (precisa de Node.js e de um projeto Remotion) |
| `colar.py` | cola esses clipes sobre o vídeo limpo e exporta o final, com uma folha de conferência |

## Estado dos testes

| Item | Situação |
|---|---|
| Testes automáticos dos scripts (24) | Passando no Windows 11 |
| Aula real (bruto de 3m54 com takes repetidos) | Limpa em ~2 min e verificada: -16,0 LUFS, 0 estalos em 15 emendas, duração igual ao plano |
| Vídeo sintético de 10 min com 300 cortes | Pronto em ~2 min, -16,0 LUFS, 0 estalos em 40 emendas |
| Exportação rápida: projeto Remotion de teste, janelas que se sobrepõem unidas, motions conferidos por pixel (11 de 11 pontos) | Verificada no Windows. O ganho de tempo (~33 min para ~7,5 min) vem do relatório de um teste do usuário, não de medição minha |
| **macOS** | **Não testado** |
| Aulas de várias horas | Não testadas |

Rodar os testes: `python -m unittest discover -s tests` (precisa de FFmpeg).
