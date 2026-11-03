# Fábrica de Criativos

Uma skill para o agente editar criativos de anúncio em vídeo em **15 formatos**, a partir do mesmo material, e fazer **variações** (o mesmo vídeo em vários formatos, ou o mesmo formato com ganchos e visuais diferentes). Foco em **edição e variação**, não em copy.

Os 15 formatos: Tela Dividida, Fundo Verde (recorte), Post de Rede Social, Notícia, Professor, Motion Design, Depoimento, React, Videochamada, Corte de Podcast, Telejornal, Tutorial de Tela, Conversa de Chat, Antes e Depois e Cinema.

## Instalar

```
npx skills add olucasevangelista/Skills-Edit.AI --skill fabrica-de-criativos -g
```

(vale depois que a skill for publicada no repositório)

## Como é feita

- `SKILL.md`: roteador. Pergunta o essencial, mostra os 15 formatos (quando é ideal, quando evitar, material mínimo) e sugere um quando a pessoa não sabe qual quer.
- `references/formatos/`: um arquivo por formato, todos no mesmo modelo (assinatura visual, composição com números, animações, cortes, texto, som, materiais, variações, checklist, kit, apoio). **Atualizar um formato é editar um arquivo**; um 16º formato é um arquivo novo e uma linha no índice.
- `references/base/`: o que é comum aos 15 (emenda com sobreposição, legenda e zonas seguras, materiais, honestidade, variações, revisão).
- `kit/`: composições Remotion prontas (Tela Dividida, Post de Rede Social, Notícia, Depoimento, React, Chat, Antes e Depois, Cinema) e componentes comuns. Opcional.
- `scripts/`: `instalar_kit.py` (instala o kit, as fontes e as marcas num projeto Remotion), `verificar_saida.py` (mede o arquivo final) e `recortar_pessoa.py` (recorta a pessoa de qualquer fundo).
- `kit/assets/`: fontes (Montserrat e Barlow Condensed, licença OFL) e marcas prontas (logo da Choquei).

**Materiais:** cada formato diz o que pedir, mas o agente tem liberdade de buscar sozinho o que couber (música, imagens e vídeos de apoio com licença clara) e registra a origem e a licença em `MATERIAIS.md`. Nunca inventa depoimento, resultado, antes e depois, notícia ou conversa real.

**Outras skills:** usa `transcrever-groq`, `smart-cuts`, `motion-designer`, `creative-lab`, `copystyle`, `raio-x-criativos` e a skill do Remotion quando estão instaladas; sem elas, segue o procedimento embutido, sem comentar a ausência.

## O que foi testado (e o que não foi)

**Testado por script nesta máquina (Windows):**

- `tests/validar_formatos.py` (16 testes): os 15 arquivos seguem o modelo, o índice do `SKILL.md` bate com os arquivos, nenhuma marca real é nome de formato, nenhum texto revela a ausência de uma skill, os caminhos citados existem, o frontmatter é válido, sem segredos.
- `tests/test_verificar_saida.py` (11 testes, com vídeo sintético): tamanho, taxa de quadros, duração, áudio, volume, quadro preto e imagem congelada, com controles negativos.
- `tests/verificar_kit.py` (57 verificações, Remotion 4.0.535): `tsc` e `eslint`; um quadro de cada composição conferido por medida (áreas, cores, janela do Cinema, cartão do Post de Rede Social, entrada da manchete da Notícia com a caixa antes do texto, troca da marca pelo logo da pessoa, janela quadrada do Cinema, faixa do contato do Chat na largura da conversa); pausa e retomada do React; deslize do Antes e Depois; balões do Chat; zoom do Depoimento; margens do texto; formatos distintos entre si; determinismo; a emenda com sobreposição (imagem e áudio do take novo entram juntos, antes de a voz anterior acabar); fade final da trilha do Cinema. Na primeira rodada (com 6 formatos), 9 verificações falharam: 4 apontaram texto dentro da margem lateral (React, Antes e Depois, Chat e Depoimento) e 5 eram erros da própria medida; depois de corrigir a medida, uma quinta (a legenda da Tela Dividida, 6 px além da margem direita) apareceu. Tudo corrigido.
- **Mídia real:** um trecho de 12 s de um vídeo real (nessa época o kit ainda tinha legenda; ela foi removida depois), renderizado em Tela Dividida, Cinema e Depoimento; os três passam no `verificar_saida.py` e os quadros foram revisados.
- **Recorte:** o comando de `chromakey` do FFmpeg tirou o fundo de um vídeo verde sintético; o WebM com alfa funciona no `<Video>` do Remotion (o ProRes não, sem registro extra). O `recortar_pessoa.py` foi rodado em 3 s de vídeo real: a máscara ficou estável, o corpo saiu limpo, a cadeira ficou com contorno difuso e há um halo suave na borda.
- **Volume:** a normalização em duas passadas levou um arquivo de −18,9 para −14,0 LUFS.

**Não testado ou limitado:**

- O kit cobre **8 dos 15 formatos**; os outros 7 são direção em texto (e o agente monta com os componentes).
- Nenhum formato foi testado com um agente de IA seguindo a skill do início ao fim.
- **Fundo Verde** e **Professor** dependem do recorte; o recorte por modelo é lento em CPU (cerca de 0,8 s por quadro) e foi testado só num trecho curto de câmera parada. O recorte do HyperFrames não foi testado. **Tutorial de Tela**: o zoom depende de o agente localizar o cursor olhando os quadros; não foi testado com uma gravação de tela real.
- macOS e Linux não foram testados.
- Os números de composição, ritmo e zona segura são **pontos de partida**; nenhum foi medido em desempenho de anúncio.
- **As políticas atuais das plataformas não foram conferidas.** Os formatos de notícia, telejornal, depoimento e antes e depois mandam a pessoa conferir as regras e identificar dramatização e publicidade.
