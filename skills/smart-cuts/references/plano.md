# Formato dos arquivos

## `cortes.json` (você escreve)

```json
{
  "video": "aula.mp4",
  "transcricao": "transcricoes/aula/transcricao.json",
  "cortes": [
    {
      "id": "aula_planilha",
      "estilo": "serio",
      "gancho": "PAREI DE USAR PLANILHA EM UMA SEMANA",
      "porque": "resultado concreto com número, arco fechado",
      "trechos": [[12.40, 38.90], [61.20, 70.10]],
      "rosto": {"cx": 960, "cy": 420, "h": 300}
    },
    {
      "id": "aula_bordao",
      "estilo": "meme",
      "gancho": "FULANO DESCOBRIU O ÓBVIO",
      "trechos": [[210.0, 224.5]],
      "bordas": {"inicio": 209.92, "fim": 225.40}
    }
  ]
}
```

Os caminhos de `video` e `transcricao` contam a partir da pasta do `cortes.json`.

- **`trechos`:** cada um é `[início da primeira palavra mantida, início da última palavra mantida]`, em segundos do arquivo original (copie de `ler.py`). O que fica **entre** dois trechos sai (loop, devaneio, repetição). Trechos em ordem; podem estar em outra ordem se a fala continuar fazendo sentido.
- **`estilo`:** `serio` ou `meme`. Não afeta a emenda; vai para o plano para quem faz a legenda e o gancho.
- **`gancho`:** texto curto da manchete (CAIXA ALTA, até ~8 palavras).
- **`id`:** curto, minúsculo, sem espaço. Vira o nome do arquivo.
- **Opcionais:** `porque` (uma linha), `bordas` (instante do original em que a voz do primeiro trecho começa e a do último termina, medidos com `ler.py --silencio`), `emendas` (a emenda `k` é a que liga o trecho `k` ao `k+1`, contando de 0; escolhida à mão como `{"0": [fim da voz que fica, início da voz que entra]}`, também em segundos do original; só se a automática ficou ruim).
- **Livres:** qualquer outro campo (`rosto`, `layout`, `insercoes`, `musica`...) é copiado para o `plano.json` sem mudança. Use para passar ao Remotion o que você decidiu.

### Mais de um vídeo no mesmo corte

```json
{
  "fontes": {"a": {"video": "live1.mp4", "transcricao": "t/live1/transcricao.json"},
             "b": {"video": "live2.mp4", "transcricao": "t/live2/transcricao.json"}},
  "cortes": [{"id": "live_evolucao", "estilo": "serio", "gancho": "MUDEI DE OPINIÃO",
              "trechos": [[300.0, 330.5, "a"], [88.0, 120.0, "b"]]}]
}
```

O terceiro item do trecho é a fonte; sem ele vale a primeira. O corte usa o tamanho e a taxa de quadros da primeira fonte.

## `plano_cortes.json` e `plano_cortes.md` (`planejar_cortes.py`)

O `.md` é para ler: texto final de cada corte, tipo e tempo de cada emenda e os avisos. O `.json` é entrada do `montar.py`: segmentos do original com a sobreposição de cada um. **Não edite à mão**; ajuste o `cortes.json` e planeje de novo.

## `plano.json` (`montar.py`, o que a skill entrega)

Um item por corte:

| Campo | O que é |
|---|---|
| `id`, `estilo`, `gancho`, `porque` | como no `cortes.json` |
| `arquivo` | o mp4 do corte (na mesma pasta) |
| `duracao`, `fps`, `largura`, `altura` | do mp4 final |
| `texto` | o texto final do corte |
| `palavras` | `{palavra, ini, fim}` em segundos **do corte**, estimadas a partir do tempo da transcrição do original. Para legenda, transcreva o mp4 do corte e use esses tempos |
| `emendas` | `{t, tipo, sobreposicao}`: onde ocorre cada emenda no corte (`emenda` entre trechos, `pausa` pausa encurtada) |
| outros | tudo o que você pôs no `cortes.json` (`rosto`, `layout`, ...) |
