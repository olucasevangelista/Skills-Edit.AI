# Peça inteira em motion

Um vídeo feito só de objetos animados (comercial conceitual, vinheta, vídeo de produto). Não há pessoa falando: quem conduz são o objeto herói, o texto curto de cada cena e o som.

## Estrutura

Cinco movimentos, em qualquer duração de 15 a 30 s:

| # | Movimento | O que acontece | 18 s | 30 s |
|---|---|---|---|---|
| 1 | **Gancho** | Uma frase curta e o objeto herói aparecem no primeiro segundo; a pessoa entende de que se trata | 0 a 3 s | 0 a 5 s |
| 2 | **Herói em ação** | O objeto principal se revela e se move; uma ideia clara (em peças curtas, isto é parte do gancho) | no gancho | 5 a 11 s |
| 3 | **Uma função por vez** | Cada benefício ou etapa tem a sua cena, com um objeto e uma frase | 3 a 8 s | 11 a 18 s |
| 4 | **Convergência** | Tudo o que apareceu se reúne em um só arranjo (os objetos se juntam, a câmera se afasta) | 8 a 13 s | 18 a 25 s |
| 5 | **Assinatura** | Nome ou marca e uma frase final, em um quadro estável | 13 a 18 s | 25 a 30 s |

Os tempos são pontos de partida: ajuste ao conteúdo. O que não muda é a ordem e a regra de um objeto e uma ideia por cena.

## Regras de cada cena

- **Um objeto herói e uma ideia por cena.** No máximo quatro elementos secundários, todos a serviço dele.
- **Texto:** uma frase por cena, no máximo 6 a 8 palavras, grande (cerca de 90 a 125 px num quadro de 1080 de largura para a frase principal; 70 a 90 px para a de apoio). Escreva o texto a partir da mensagem, não da lista de recursos.
- **Duração de cada cena:** de 3 a 7 s. Uma cena de menos de 2 s não deixa o objeto assentar.
- **Entrada e repouso:** o objeto entra (12 a 18 quadros), assenta e fica estável por tempo suficiente para ser percebido e lido, antes da próxima ação.
- **Zona segura (9:16):** topo 270 px, base 360 px, laterais 90 px. Texto e o objeto principal ficam dentro; objetos podem cruzar a margem ao entrar e sair de cena.
- **Encerramento estável:** a peça termina em um quadro parado, com a assinatura, por 2 a 3 s. Não termine em fade para preto.

## Peça sobre uma marca real

Veja as regras de marca em `direcao-de-arte.md`. Em resumo: tokens de cor consultados na fonte oficial, fonte livre no lugar da proprietária, nenhum logo ou arquivo da marca reaproveitado, e o aviso "conceito independente, não oficial" dentro da peça e na documentação.

## Documento de direção (`DIRECAO.md`)

Escreva antes do código e peça a aprovação da pessoa. Modelo:

```markdown
# Título da peça

Duração, formato, taxa de quadros. Conceito não oficial, se for o caso.

| Tempo | Direção |
|---|---|
| 0 a 3 s | Fundo escuro. Frase em branco. Objeto herói entra e assenta. |
| 3 a 8 s | Quatro cenas curtas, uma função por vez. Um objeto principal em cada. |
| 8 a 13 s | Os objetos convergem. Câmera afasta. Duas frases, uma de cada vez. |
| 13 a 18 s | Cor de fundo da marca ocupa o quadro. Nome e frase final, estáveis. |

Paleta (3 cores e 1 de destaque). Fonte (livre, com a licença). Zona segura.
Mapa de som por instante (veja audio.md).
Textos, exatamente como vão aparecer.
```

## `config.ts` único

Formato, duração, textos, cores, tempos de cada cena e, no 3D, as chaves de câmera ficam em um arquivo só. Quem quiser mudar uma frase ou um tempo edita ali, e o resto da peça acompanha. O kit traz um exemplo (`references/kit.md`).

## Cenas isoladas no Studio

Além da composição completa, registre cada cena como uma composição separada (por exemplo numa pasta "Cenas"). Assim a pessoa abre e ajusta uma cena sem percorrer a peça inteira.
