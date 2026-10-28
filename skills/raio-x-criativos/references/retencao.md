# Raio-X da retenção (o corpo do criativo)

Depois do gancho, o que faz a pessoa **continuar**? O raio-x lista o que, no corpo do vídeo, pode estar segurando a atenção, e **onde** ela pode estar escapando. Tudo como hipótese, com evidência por segundo.

Material: a transcrição, o **mapa de ritmo** (`analisar.py mapa`), as folhas de contato do vídeo inteiro e a janela do final.

## 1. O que pode estar segurando a pessoa

Para cada item, procure a **evidência** no vídeo e anote o instante:

| Mecanismo | Como reconhecer (evidência) |
|---|---|
| **Promessa feita cedo e segurada até a revelação** | no começo se promete algo ("vou te mostrar...", "o terceiro passo...") e a resolução só vem mais tarde; anote o instante da promessa e o da revelação |
| **Storytelling** | há personagem, um conflito, uma virada e uma resolução; a fala conta uma história em vez de listar argumentos |
| **Novos ganchos ao longo do vídeo (re-ganchos)** | em vários pontos, algo novo é prometido ou perguntado ("mas tem um detalhe", "e aqui vem o melhor"), ou há um evento visual forte de **tipo diferente**; anote cada instante |
| **Escalada** | cada trecho aumenta a aposta (um resultado maior, uma prova mais forte, uma virada) |
| **Progresso marcado** | "são 3 passos": a pessoa sabe onde está e quanto falta |
| **Prova distribuída** | provas aparecem ao longo do vídeo, não todas no fim |
| **Ritmo visual** | cortes, inserts, texto novo, mudança de enquadramento, tela dividida (o mapa mostra quando) |
| **Conteúdo interessante por si** | uma informação, um segredo ou uma demonstração que vale ver; descreva o que é |
| **Humor ou surpresa** | momentos que quebram o tom e prendem |
| **Variação de formato** | passa de pessoa falando para gravação de tela, para depoimento, para animação |
| **Música e som** | **só se o usuário contou ou há indício** (um volume que sobe nos marcos, picos coincidindo com eventos): você não escuta |
| **Legenda e ênfase em texto** | palavras-chave destacadas ajudam a acompanhar sem som |

## 2. Como ler o mapa de ritmo

O mapa traz **medidas**, não notas. Use-as para **achar onde olhar** e para **dar número** às hipóteses:

- **Cortes por minuto e maior trecho sem corte** (`maior_trecho_sem_corte`): mostram se o vídeo é movimentado ou se há um trecho longo parado. **Lembre:** o detector não pega zoom nem jump cut leve; confirme nas folhas antes de afirmar "trecho parado".
- **Cortes nos 3 e 5 primeiros segundos**: o quanto o começo se mexe.
- **Palavras por minuto e pausas de fala:** o ritmo da fala. **Não existe valor "certo"**: compare com os outros criativos da mesma conta e com o tipo de conteúdo (uma história pede outro ritmo que uma lista).
- **A tabela por janela de tempo:** cada linha tem cortes, palavras, volume e o trecho falado. Preencha a coluna "função" (o que aquela janela faz: promessa, prova, mecanismo, re-gancho, CTA...). As janelas **sem corte, sem palavra e com pouco som** são as candidatas a **queda de atenção**.
- **Volume dos primeiros 3 s, do meio e dos últimos 5 s:** mostra se o vídeo termina com a mesma energia que começou.
- **"Som" na tabela** é o quanto da janela tem som acima do limiar (voz, música ou efeito): com música contínua, o silêncio não aparece. As **pausas de fala** vêm da transcrição.

## 3. Onde a atenção pode cair (hipótese de queda)

Aponte, **com o instante**, os trechos com:

- **Muito tempo sem nenhum evento** (sem corte de cena, sem texto novo, sem insert, sem mudança de enquadramento), conferido nas folhas.
- **Uma pausa grande** na fala sem nada acontecendo na tela.
- **Explicação sem prova ou sem imagem**, um bloco falado longo no mesmo enquadramento.
- **Uma promessa que ninguém segura**: o começo promete algo e o corpo não volta a ela.
- **Mudança de assunto sem re-gancho**: troca de parte (problema, solução, oferta) sem nada novo para renovar o interesse.
- **Queda de energia perto do fim**: volume e cortes caem antes do CTA.

Sem dados de retenção, isso é **hipótese de onde poderia cair**. Com dados (hold rate, a curva de retenção que o usuário tiver), cruze: se ele disser "a queda é no segundo 14", veja o que acontece ali.

## 4. Perguntas que fecham a análise da retenção

- O que o criativo promete cedo, e **em que segundo** entrega?
- Quantos **re-ganchos** existem e em que instantes? Estão espaçados?
- Há uma **história** ou uma lista de argumentos?
- Qual é o **maior intervalo sem evento**, e o que a fala diz ali?
- O criativo **mantém a energia** até o CTA?
