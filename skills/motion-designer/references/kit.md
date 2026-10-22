# Kit (opcional)

Um kit pequeno em `<skill>/kit/`, para poupar trabalho. **Nada é obrigatório**: o agente pergunta se a pessoa quer usar o kit e, se ela preferir, escreve tudo do zero. O agente **copia** o que precisar para o projeto Remotion; a skill não é importada em tempo de execução.

| Arquivo | O que é | Dependências |
|---|---|---|
| `kit/movimento.ts` | curvas, entradas, curva por chaves, drift, squash | `remotion` |
| `kit/camera3d.tsx` | câmera por chaves, ambiente, luzes, piso de sombra | `three`, `@react-three/fiber`, `@remotion/three` |
| `kit/exemplo/` | uma peça completa de 12 s em 9:16, 2D, com marca fictícia | `remotion` e `kit/movimento.ts` |
| `kit/audio/sintetizar.py` | síntese de trilha e efeitos a partir de um mapa | Python 3.10+ e `numpy` |

## `movimento.ts`

Copie para `src/` do projeto e importe: `import { EASE, prog, pop, track, drift, squash, sec } from "./movimento"`.

| Função | Para quê |
|---|---|
| `prog(frame, de, ate, curva?)` | progresso de 0 a 1 entre dois quadros, com curva (`EASE.out`, `EASE.inOut`, `EASE.in`) |
| `pop(frame, fps, inicio, amortecimento?, rigidez?)` | entrada com leve overshoot |
| `track(frame, chaves)` | curva suave por chaves `{ f, v }` (câmera, rotação, posição com paradas) |
| `drift(frame, velocidade, fase?)` | flutuação suave de -1 a 1 |
| `squash(frame, quadro, quantidade?)` | escala `[x, y]` de um impacto |
| `sec(segundos, fps)` | segundos para quadros |
| `lerp`, `lerp3`, `rad`, `clamp01` | auxiliares |

O `fps` entra como parâmetro: o kit não depende de constantes do projeto.

## `camera3d.tsx`

Precisa dos pacotes de 3D. Versões em que foi testado: Remotion 4.0.535, `three` 0.186.1, `@react-three/fiber` 9.8.2 e `@remotion/three` 4.0.535. O setup do `<ThreeCanvas>` está na skill do Remotion. Dentro dele:

```tsx
<CameraRig keys={CHAVES} shiftPx={110} />
<Ambiente />
<Luzes cor="#FFFFFF" contornoA="#8AA4FF" contornoB="#FFB38A" />
<PisoDeSombra y={-1.2} />
```

`CHAVES` é uma lista de `CamKey` (`f`, `az`, `el`, `dist`, `t`, `fov`). `shiftPx` positivo **sobe** o assunto no quadro. O kit importa `./movimento`, então copie os dois arquivos juntos.

Para renderizar quadros 3D use `--gl=angle`.

## `exemplo/`

Uma peça fictícia (marca "Trilha", só geometria) com três cenas:

1. **Gancho:** duas linhas de texto e um objeto que assenta.
2. **Processo:** um pacote percorre três estações e muda de estado em cada uma (preenche, ganha fita, ganha seta de envio), chegando antes da palavra e mudando **na** palavra.
3. **Fecho:** as estações convergem para um ponto, a marca assenta e a frase final fica estável.

Estrutura: `config.ts` (formato, cores, textos, tempos e a fala), `Exemplo.tsx` (as cenas, só lendo do `config.ts`), `Root.tsx` e `index.ts`. Para abrir: copie `kit/movimento.ts` e a pasta `kit/exemplo/` para `src/` (mantendo a pasta `exemplo` ao lado de `movimento.ts`) e rode `npx remotion studio src/exemplo/index.ts`.

Use como **modelo de estrutura**, não como arte final: troque textos, cores, objetos e tempos pelos da peça.

Observação sobre a zona segura: todo o texto fica dentro das margens; o pacote **sai** pela base da tela ao ser "enviado", o que é intencional (objeto saindo de cena).

## `audio/sintetizar.py`

Veja `audio.md` (como usar, mapa de eventos, limites). O `mapa-exemplo.json` casa com os tempos do `exemplo/`.

## Estado verificado

Tipos e lint passam; o exemplo renderiza (360 quadros, 12 s, 1080x1920), com o mesmo quadro idêntico em duas renderizações; a câmera 3D foi renderizada em uma cena mínima e seguiu as chaves; a síntese passa nos testes de duração, pico, eventos e determinismo. Detalhes e limites no `README.md`.
