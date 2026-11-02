# 06. Motion Design

**Também pedido como:** motion, motion graphics, vídeo animado, anúncio animado, explicativo animado.

## Assinatura visual

O anúncio **sem pessoa falando**: construído com **textos animados, ícones, formas, imagens e gráficos**, em **2D e, quando faz sentido, 3D**, conduzidos por uma **narração**. O estilo visual é **consistente do começo ao fim** e a imagem **explica** o produto, o benefício, o processo ou o mecanismo.

## Ideal quando

- **Não há uma pessoa para gravar**, ou a pessoa prefere não aparecer.
- O produto é **abstrato** (software, método, processo, serviço) e precisa de uma imagem que o torne visível.
- Há uma **narração** ou um roteiro, e o **mecanismo** ou o passo a passo merece ser mostrado em movimento.

## Evite quando

- O anúncio precisa de **prova humana** (depoimento, rosto, confiança pessoal): prefira Depoimento ou Tela Dividida.
- Não há tempo ou material para construir uma identidade visual coerente: motion improvisado parece amador.
- O pedido é "só decorar com ícones": isso não explica nada.

## Composição (1080x1920)

- **Uma ideia e um objeto herói por cena**; no máximo ~4 elementos secundários.
- **Estrutura em cinco movimentos** (15 a 30 s): **gancho** (a frase e o objeto herói no 1º segundo), **herói em ação**, **uma função por vez**, **convergência** (tudo se reúne) e **assinatura** (nome e frase final, quadro estável).
- **Texto:** uma frase por cena, até 6 a 8 palavras, grande (90 a 125 px a frase principal, 70 a 90 px a de apoio), dentro das margens (topo ~270, laterais ~90, base livre ~670).
- **Cena de 3 a 7 s**; menos de 2 s não deixa o objeto assentar.

## Elementos e animações

- **Tudo é função do quadro:** posição, estado e câmera dependem só do número do quadro (sem CSS animation, timers ou `useFrame` como relógio), para a prévia e o arquivo saírem iguais.
- **Entrada** do objeto em 12 a 18 quadros, com leve overshoot; **repouso** de ~0,6 a 0,8 s antes da próxima ação; **todo movimento termina em repouso**.
- **Continuidade:** quando um objeto dá lugar a outro, use **uma curva de rotação compartilhada** (sem salto) e um brilho curto na troca.
- **Câmera** (em 3D): por chaves, com aproximação lenta nas cenas de apresentação e afastamento na convergência.
- **Técnica em degraus:** 2D (SVG, CSS) para relações planas; 2D com perspectiva para uma leve profundidade; **3D de verdade** só quando o volume ou o ponto de vista fazem parte da explicação (custa ~5 vezes mais código e render mais pesado). Se a pessoa pediu 3D, **entregue 3D** ou diga o que não deu.

## Cortes e ritmo

- A **narração** define o tempo; o evento visual cai **na palavra** que ele ilustra. Evento novo a cada ~2 s; marco grande a cada ~6 a 8 s.
- Se há trilha, os eventos grandes caem **na batida** (a 120 BPM, uma batida a cada 15 quadros a 30 fps).

## Texto e legenda

- Legenda opcional (depende da cena); o texto da cena é **curto e complementa a narração**.
- **Número só com dado real**; sem dado, ilustração qualitativa, identificada.

## Som

- **Narração** em primeiro plano; **trilha** abaixo; **mapa de som** por instante da animação (um efeito por evento grande); fade nos últimos 0,7 s.
- Se a pessoa não tem trilha, **escolha uma** (`materiais.md`) ou sintetize uma simples; avise que a síntese é eletrônica e simples.

## Materiais

- **Peça:** a **narração** (ou o roteiro), a identidade (cores, fonte, logo) e as imagens ou ícones que quer usar.
- **Pode buscar sozinho:** ícones, formas e gráficos gerados por código; fontes; música e efeitos; imagens de apoio com licença clara.
- **Nunca invente:** números, dados, métricas, depoimentos ou logos parecidos com os de uma marca.

## Variações dentro do formato

- Técnica (2D ou 3D); paleta e fonte; ritmo; o objeto herói.
- Com e sem trilha; versão curta e longa.

## Armadilhas e checklist

- [ ] Um objeto herói e uma ideia por cena; nada acumulando.
- [ ] A ação visual corresponde à frase e não sugere uma informação nova.
- [ ] Tudo legível em tamanho de celular e dentro das margens.
- [ ] O arquivo exportado mostra o mesmo da prévia (sem tela vazia).
- [ ] Os números têm base real.

## Kit

Sem kit de formato nesta versão. O `kit/componentes/Movimento.ts` traz as curvas (`prog`, `pop`, `track`, `drift`, `squash`).

## Apoio

Se a skill `motion-designer` estiver disponível, **use-a**: ela traz a lógica do motion explicativo, a estrutura da peça, a direção de arte, a câmera 3D, a direção de áudio e o kit. Se não, siga o resumo acima e a skill do Remotion para criar e exportar.
