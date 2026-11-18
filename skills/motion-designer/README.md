# motion-designer

Direção para criar motion design e motion graphics no Remotion, de dois jeitos: **motions explicativos** (um processo, uma relação ou uma comparação, sincronizados com a fala) e **peças inteiras** feitas só de objetos animados em 2D ou 3D (comerciais conceituais, vinhetas, vídeos de produto). Cobre a lógica visual, a estrutura da peça, a direção de arte, o movimento e a câmera, a direção de áudio e a revisão por quadros.

Traz um **kit opcional** (movimento, câmera 3D, uma peça de exemplo) e uma **síntese opcional** de trilha e efeitos sonoros. Nada disso é obrigatório: o agente pergunta como a pessoa prefere seguir. Os motions são criados e exportados com a skill do Remotion.

## Instalar

```
npx skills add olucasevangelista/Skills-Edit.AI --skill motion-designer -g
```

Depois, no chat do agente, chame `/motion-designer` e diga o que quer ("faz um motion explicando isso" ou "faz um vídeo só de motion").

## O que precisa

- **Remotion** (testado com 4.0.535), Node.js e FFmpeg com `ffprobe`.
- Para o 3D: `three`, `@react-three/fiber` e `@remotion/three` (testado com three 0.186.1 e @react-three/fiber 9.8.2).
- Para a síntese de áudio e a medida de ataque (opcional): **Python 3.10+**, `numpy` e FFmpeg.
- Para a folha numerada do storyboard (opcional): **Pillow**.

## Conteúdo

| Pasta | O que tem |
|---|---|
| `references/` | direção em texto: explicativo, peça inteira, direção de arte, movimento, técnica, áudio, revisão, problemas conhecidos, kit |
| `kit/movimento.ts` | curvas, entradas, curva por chaves, drift, squash |
| `kit/camera3d.tsx` | câmera por chaves, ambiente, luzes, piso de sombra |
| `kit/exemplo/` | peça completa de 12 s em 9:16, 2D, com marca fictícia, para usar como modelo de estrutura |
| `kit/audio/` | `sintetizar.py` (com eventos por nome), `ataque.py` e mapas de exemplo |
| `kit/folha_de_quadros.py` | folha numerada do storyboard |
| `tests/` | testes da síntese e um verificador do kit contra um projeto Remotion |

## Estado dos testes

| Item | Situação |
|---|---|
| Tipos (`tsc`) e lint (`eslint`) do kit e do exemplo | Passando, num projeto limpo com as dependências acima |
| Render do exemplo | 5 quadros e o vídeo completo (360 quadros, 12,000 s, 1080x1920, H.264); a sequência de quadros foi olhada: o pacote chega antes da palavra, muda de estado na palavra e as estações convergem |
| Determinismo | O mesmo quadro renderizado duas vezes sai idêntico (hash igual), nos quadros 20 e 200 |
| Zona segura | Nenhum texto no topo, na base ou nas laterais nos quadros conferidos; só o pacote cruza a base, ao sair de cena |
| Câmera 3D | Renderizada numa cena mínima (um cubo): segue as chaves (de longe e de lado para perto e de frente) e `shiftPx` positivo sobe o assunto. Um erro de sinal que existia no kit foi achado e corrigido nesta verificação |
| Síntese de áudio | 7 testes: duração exata, pico abaixo de −1 dBFS, cada evento audível no instante certo (controle: no instante errado, 0 de 6 passam), trilha com fade, mesma semente gera o mesmo áudio, erro claro para tipo desconhecido |
| Volume da síntese | A mistura de exemplo sai em **−23,8 LUFS**, baixa para feed; com a normalização em duas passadas descrita em `references/audio.md` ficou em −14,7 LUFS |
| Verificador do kit (`tests/verificar_kit.py`) | 11 de 11 verificações passam; com o erro de sinal reintroduzido de propósito, ele falha (10 de 11) |

Verificar o kit contra um projeto Remotion: `python tests/verificar_kit.py <pasta do projeto>`. Testes da síntese: `python -m unittest discover -s tests` (precisa de numpy; sem ele, são pulados).

## Limites que vale conhecer

- O render do 3D foi verificado com `--gl=angle`. Em outra máquina, rode o verificador antes de multiplicar as cenas.
- O kit e o exemplo são um **ponto de partida**: o exemplo mostra a estrutura (um `config.ts`, cenas que só leem dele, tempos ancorados na fala), não uma arte final.
- A trilha sintetizada é eletrônica e simples (trilha conceitual). Pode ser trocada por uma música de verdade, e por isso os arquivos saem separados.
- Peças sobre marcas reais devem seguir as regras de `references/direcao-de-arte.md` (sem logo, símbolo ou fonte da marca; aviso de conceito não oficial).
