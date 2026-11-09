/**
 * Emenda com sobreposição (o corte do estilo do autor): o próximo take entra colado no começo da voz e começa ainda durante
 * o finalzinho do anterior. A IMAGEM nova e o ÁUDIO novo entram no mesmo instante; o áudio do take anterior desce ao longo
 * da sobreposição e o do novo entra com um fade curto. Nunca corte seco só de áudio ou só de imagem.
 *
 * É uma PEÇA PARA REAPROVEITAR no seu projeto Remotion (copie e ajuste), não um editor: o enquadramento, o que vai por cima
 * e o resto da composição são seus. Depende de `remotion` e `@remotion/media`.
 *
 * Cada take é um trecho de um arquivo em `public/` (`deS` e `ateS` em segundos DENTRO do arquivo). Use `duracaoDosTakes` para
 * saber a duração total da sequência (cada emenda "come" a sobreposição).
 */
import React from "react";
import { Sequence, staticFile } from "remotion";
import { Video } from "@remotion/media";

export type Take = { src: string; deS: number; ateS: number };

const q = (s: number, fps: number) => Math.round(s * fps);

/** Duração total (s) de uma lista de takes com sobreposição. */
export const duracaoDosTakes = (takes: Take[], sobreposicaoS: number): number =>
  takes.reduce((t, k) => t + (k.ateS - k.deS), 0) - sobreposicaoS * Math.max(0, takes.length - 1);

type Props = {
  takes: Take[];
  fps: number;
  /** sobreposição da emenda, em segundos (0,1 a 0,25; padrão 0,18) */
  sobreposicaoS?: number;
  objectFit?: "cover" | "contain";
  volume?: number;
  /** ponto de ancoragem do enquadramento (CSS object-position) */
  origem?: string;
};

export const TakesSobrepostos: React.FC<Props> = ({ takes, fps, sobreposicaoS = 0.18, objectFit = "cover", volume = 1, origem = "50% 35%" }) => {
  const sob = q(sobreposicaoS, fps);
  let inicio = 0;
  return (
    <>
      {takes.map((t, i) => {
        const dur = q(t.ateS - t.deS, fps);
        const de = inicio;
        inicio += dur - sob;
        const ultimo = i === takes.length - 1;
        const primeiro = i === 0;
        return (
          <Sequence key={`${t.src}-${i}`} from={de} durationInFrames={dur} name={`take ${i + 1}`}>
            <Video
              src={staticFile(t.src)}
              trimBefore={q(t.deS, fps)}
              objectFit={objectFit}
              style={{ width: "100%", height: "100%", objectPosition: origem }}
              volume={(f) => {
                const sobe = primeiro ? 1 : Math.min(1, f + 1); // fade de entrada de ~1 quadro
                const desce = ultimo ? 1 : Math.min(1, Math.max(0, (dur - f) / Math.max(1, sob)));
                return volume * sobe * desce;
              }}
            />
          </Sequence>
        );
      })}
    </>
  );
};
