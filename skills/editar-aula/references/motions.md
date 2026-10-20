# Motions de aula

Os motions existem para **ajudar o aluno a entender e se orientar**, não para enfeitar. Em aula, menos é mais.

## Tipos e orçamento

| Tipo | Quando | Duração | Quantidade |
|---|---|---|---|
| **Título da aula** | Começo da aula | 2 a 3 s | 1 |
| **Título de seção** | Troca de assunto | 2 a 2,5 s | 1 por seção (3 a 8 em 20 min) |
| **Destaque de termo ou frase-chave** | Na palavra dita; termo novo, definição, número | 1,5 a 2,5 s | no máximo 1 a cada ~60 a 90 s |
| **Lista** | A pessoa enumera 3 ou mais itens | cada item entra quando é dito | só quando houver enumeração |
| **Motion explicativo** | Ideia abstrata ou densa (processo, comparação, estrutura) | 4 a 8 s | no máximo 1 a cada 3 a 5 min |

- Deixe **pelo menos ~20 s** entre dois motions, salvo título de seção seguido de destaque.
- Não coloque motion por cima da abertura se a pessoa está dizendo algo importante nos primeiros segundos: o título pode entrar um pouco depois ou ao lado.
- A quantidade que o usuário pedir vence o orçamento. Ele é só um padrão para não poluir.

## Como escolher o que destacar

- **Termo-chave:** a palavra nova da aula, a definição, o nome de uma ferramenta, um número. Texto de até 5 palavras, escrito como o aluno vai buscar depois.
- **Motion explicativo:** pergunte "isso dá para entender só falando?". Se a explicação depende de ver relações (A leva a B, três camadas, antes e depois), um diagrama simples ajuda. Se é só uma definição, o destaque basta.
- Diagramas simples: poucos elementos, texto grande, uma ideia por motion e animação que acompanha a ordem em que a pessoa fala.

## Como criar sem perder tempo

Crie cada tipo de motion **uma vez** e **duplique ajustando** texto e tempo, em vez de começar do zero a cada um. Guarde cores e fontes da identidade em um único lugar e use em todos. Só os motions explicativos pedem criação própria, e são poucos. Se o usuário forneceu pouca densidade visual (só quer títulos), mantenha tudo simples.

## Onde criar e exportar

No **Remotion**: use o vídeo limpo como base da composição e coloque os motions por cima, na mesma composição. A skill do Remotion explica como montar e exportar. Use o mesmo tamanho e a mesma taxa de quadros do vídeo limpo (estão em `timeline.json`, se você usou os scripts).

## De onde tirar os tempos

O melhor jeito é **transcrever o vídeo já limpo**: os tempos de palavra são os do vídeo final. O motion entra **na palavra que ele ilustra** (±0,1 s) e sai depois do tempo de leitura (0,4 s + 0,3 s por palavra, mínimo 1,5 s).

## Conferir antes de entregar

Veja um quadro no meio de cada motion: legível, dentro da imagem, **sem cobrir o conteúdo** (`formatos.md`) e com a identidade certa.

## Capítulos

Com as seções decididas, gere `capitulos.txt` com o tempo **no vídeo limpo**:

```
00:00 Abertura
02:15 O que é um agente
07:40 Como ele roda 24 horas
```
