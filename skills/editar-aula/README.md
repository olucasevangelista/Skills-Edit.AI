# editar-aula

Direção para o agente editar aulas gravadas com padrão e qualidade: o que limpar, como dividir em seções com capítulos e onde colocar títulos, destaques e motions explicativos, sem cobrir o que o aluno precisa ver. Inclui scripts opcionais de limpeza (cortar pausas e erros).

Os motions são criados com a skill do Remotion.

## Instalar

```
npx skills add olucasevangelista/Skills-Edit.AI --skill editar-aula -g
```

Depois, no chat do agente, chame `/editar-aula` e diga o que quer ("edita essa aula").

## Scripts de limpeza (opcionais)

Precisam de **Python 3.10+** (só biblioteca padrão) e **FFmpeg** com `ffprobe` (`winget install Gyan.FFmpeg` no Windows, `brew install ffmpeg` no macOS).

| Script | Para quê |
|---|---|
| `diagnosticar.py` | formato, volume, fala e avisos do arquivo bruto |
| `planejar_cortes.py` | acha as pausas pelo volume, remove os erros indicados e calcula as emendas |
| `montar.py` | aplica os cortes e normaliza o volume em -16 LUFS |
| `verificar.py` | mede duração, sincronia, volume, pausas que sobraram e estalos |

## Estado dos testes

| Item | Situação |
|---|---|
| Testes automáticos dos scripts (19) | Passando no Windows 11 |
| Aula real (bruto de 3m54 com takes repetidos) | Limpa em ~2 min e verificada: -16,0 LUFS, 0 estalos em 15 emendas, duração igual ao plano |
| Vídeo sintético de 10 min com 300 cortes | Pronto em ~2 min, -16,0 LUFS, 0 estalos em 40 emendas |
| **macOS** | **Não testado** |
| Aulas de várias horas | Não testadas |

Rodar os testes: `python -m unittest discover -s tests` (precisa de FFmpeg).
