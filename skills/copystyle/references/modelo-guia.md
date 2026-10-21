# Modelo do GUIA-DE-ESTILO.md e do estilos.json

O guia é o que o editor lê antes de CADA vídeo. Ele diz qual formato escolher, com quais números, e o que nunca fazer. Escreva em português do Brasil, frases diretas, tabelas onde houver números. Cite a referência de cada receita (`ref_01`, `ref_03`) para o editor poder abrir a análise. Tamanho típico: 250 a 400 linhas.

## Estrutura

```markdown
# Guia de estilo de {{Nome}} ({{marca}})

Versão N, dd/mm/aaaa. Feito a partir de X vídeos de referência ({{autores}}),
dissecados quadro a quadro (quadros, transcrição e medições de som).
Detalhes em `referencias/<lote>/analise/<slug>/analise.md` e sínteses em `_grupo_*.md`.

## Briefing
(tabela da entrevista, em `entrevista.md`)

## 1. Quem fala e como chamar
Quem aparece, persona dos memes (terceira pessoa, apelidos), o que substitui a marca
e o parceiro das páginas de referência (se a referência é dupla e o criador fala
sozinho: quem faz o papel do segundo? chat, aluno, uma IA, um meme de reação),
o tom do narrador, erros propositais de internet (dose).

## 2. Vocabulário vivo em {{mês ano}}
Pode usar / morto ou datado / emojis que funcionam e quando / regra de segurança
(deboche aponta para coisa ou para o próprio criador, nunca para pessoa, aparência, grupo).
Nomes e termos que o Whisper costuma errar, com a grafia certa.

## 3. Primeira decisão: meme ou sério
Tabela "sinal no trecho -> tom/formato". Regra de desempate (o que o criador mais gosta).
Um vídeo nunca mistura dois sistemas de legenda.

## 4. Formatos MEME (um subtítulo por formato)
Para cada: referências, quando usar, estrutura (tabela momento/o que acontece/números),
parâmetros (fonte, tamanho em % da largura, posição y, cores), música e nível, final.

## 5. Caixa de ferramentas MEME
Tabela efeito | quando | receita com números (punch-in, palavra maldita, meme PIP,
relâmpago + boom, emoji no rosto, máquina de escrever, P&B, flash...). Frequência máxima.

## 6. Legendas MEME (um sistema por vídeo)
Cada sistema com fonte, peso, caixa, tamanho, cor, sombra/contorno, palavras por página,
animação, posição y, e o nome do estilo no `estilos.json`.

## 7. Áudio MEME
Tabela clima | trilha das referências (com a confiança da identificação) | uso. Níveis
(cama X a Y dB abaixo da voz), golpes (corte seco na virada, drop depois do silêncio,
música para na revelação), lista dos efeitos sonoros que existem nas referências (e só eles).

## 8. Formato SÉRIO principal ({{referência favorita}})
8.1 números (palavras por minuto, pausa máxima, eventos por minuto, flashes, nível da trilha);
8.2 modos de tela (% do tempo, quando); 8.3 assinatura (ex.: flash de luz) quadro a quadro;
8.4 legenda séria com tokens; 8.5 estrutura narrativa (gancho, viradas, mecânica, síntese, CTA, em %);
8.6 áudio sério.

## 9. Dialetos sérios alternativos
Tabela comparando (layout, legenda, recurso-assinatura, retórica, áudio) e quando usar cada um.

## 10. Regras de tela 9:16
Zonas de interface do app, faixa segura de texto e rosto, posição de legenda e manchete.

## 11. Checklist de QA de cada vídeo

## 12. Índice das referências
Tabela slug | autor | data | duração | link | análise.

## 13. Preferências do criador
Itens com data, regra e o porquê. Esta seção nunca é apagada numa atualização.

## 14. Mapa para o Remotion
Tabela técnica do guia -> como montar: elemento (texto, vídeo, imagem, overlay, som),
quando entra e sai (em relação a uma palavra), números (tamanho, posição, duração, cor)
e o estilo do `estilos.json`. Para a técnica que você não sabe como fazer, escreva
"sem receita pronta" + a melhor aproximação.
```

## Mapa para o Remotion: exemplo de linhas

| Técnica (referência) | Elemento | Quando | Números |
|---|---|---|---|
| Meme em tela cheia na palavra-gatilho (`ref_02`) | imagem ou vídeo curto | entra 0 a 0,3 s antes da palavra; sai em 1,5 a 2,5 s | tela cheia, legenda some enquanto está no ar |
| Punch-in de ênfase (`ref_01`, `ref_04`) | escala do vídeo | na palavra mais forte da frase | 1,00 para 1,07 em 0,15 s; volta no próximo corte |
| Palavra gigante na virada (`ref_02`) | texto | na palavra do punchline | 14% da largura da tela, centro em y=0,45, cor de destaque |
| Estalo de câmera na revelação (`ref_03`) | efeito sonoro | junto do quadro de revelação | nível ~6 dB abaixo da voz |

Itens que costumam não ter receita pronta no Remotion e merecem uma nota de aproximação: título atrás do sujeito (precisa de máscara de segmentação), troca de fonte por quadro, câmera lenta com interpolação, shake, transição whip ou glitch própria, vídeo de terceiro com áudio original alternando.

## estilos.json

```json
{
  "fontes": [
    {"family": "Archivo", "arquivo": "fontes/Archivo-900.ttf", "weight": "900", "style": "normal"}
  ],
  "legendas": {
    "amarela-karaoke": {
      "fonte": "Archivo", "peso": 900, "tamanho": 68, "caixa": "alta",
      "cor": "#FFFFFF", "cor_ativa": "#F4ED1D",
      "contorno": 5, "cor_contorno": "#000000", "sombra": "0 6px 14px rgba(0,0,0,0.55)",
      "y": 0.72, "largura_max": 900, "animacao": "karaoke",
      "agrupamento": "meme", "max_palavras": 3
    },
    "serifada-frase": {
      "fonte": "Merriweather", "peso": 700, "tamanho": 46, "caixa": "normal",
      "cor": "#FFFFFF", "sombra": "2px 2px 4px rgba(0,0,0,0.6)", "y": 0.70,
      "animacao": "nenhuma", "agrupamento": "frase", "max_palavras": 7, "max_caracteres": 44
    }
  },
  "ganchos": {
    "tarja-azul": {
      "fonte": "Archivo", "peso": 900, "tamanho": 60, "caixa": "alta", "cor": "#FFFFFF",
      "fundo": "#1E5BFF", "raio": 22, "padding": "18px 34px", "y": 0.30,
      "animacao": "pop", "largura_max": 950, "capa_na_faixa": true
    }
  }
}
```

Tokens de legenda: `fonte`, `peso`, `tamanho` (px num quadro de 1080 de largura; 6% da largura = 65 px), `cor`, `cor_ativa` (karaokê), `caixa` (alta, baixa, normal), `y` (centro, fração da altura), `largura_max`, `sombra` (CSS), `contorno` (px) e `cor_contorno`, `fundo` (tarja) com `padding` e `raio`, `animacao` (nenhuma, fade, pop, acumula, karaoke), `entrelinha`, `espacamento_letras`, `escala_x` (1,06 = mais larga), `italico`. Agrupamento das palavras: `agrupamento` (`curto` = 1 a 3 palavras, grudando as curtas; `frase`; `meme` = até `max_palavras`, quebra em pontuação; `palavra` = uma por vez), `max_palavras`, `max_caracteres`, `sem_pontuacao`.

Tokens de gancho: `fonte`, `peso`, `tamanho`, `cor`, `fundo` (pílula ou tarja; ausente = texto solto), `raio`, `padding`, `y`, `caixa`, `contorno`, `cor_contorno`, `sombra`, `animacao` (pop, fade, seco, maquina), `largura_max`, `capa_na_faixa`.

Quem monta o vídeo no Remotion lê estes tokens como especificação: cada nome acima descreve o comportamento esperado.

Medindo na referência: tamanho em px = (altura da maiúscula medida / largura do quadro) x 1080 / 0,72 (a maiúscula ocupa ~72% do corpo da fonte). Posição y = centro do bloco / altura do quadro. Depois confirme comparando um quadro de teste com o quadro real da referência.
