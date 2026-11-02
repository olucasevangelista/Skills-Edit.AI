import React from "react";
import { AbsoluteFill, Freeze, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Video } from "@remotion/media";
import { A, L, SEGURA, type PropsBase } from "../../tipos";
import { cameraDe } from "../../componentes/Camera";
import { JanelaVideo } from "../../componentes/JanelaVideo";
import { Legenda } from "../../componentes/Legenda";
import { EASE, prog } from "../../componentes/Movimento";
import { Tarja } from "../../componentes/Tarja";
import { Titulo } from "../../componentes/Titulo";

export type Intervalo = { deS: number; ateS: number };

export type PropsReact = PropsBase & {
  /** o vídeo comentado (arquivo em public/); `video` é a reação da pessoa */
  conteudo: string;
  /** o conteúdo para (e o áudio dele cala) enquanto a pessoa comenta; depois retoma do mesmo ponto */
  pausas?: Intervalo[];
  /** o conteúdo cresce para ser visto de perto */
  ampliacoes?: Intervalo[];
  rotuloOrigem?: string;
  /** volume do áudio do conteúdo quando ele roda (a voz da pessoa é sempre a mais forte) */
  volumeConteudo?: number;
};

type Segmento = { de: number; dur: number; srcQuadro: number; congelado: boolean };

/** Divide a linha do tempo em trechos que tocam e trechos congelados; cada trecho que toca retoma de onde o anterior parou. */
export const segmentarConteudo = (pausas: Intervalo[], totalQuadros: number, fps: number): Segmento[] => {
  const ordenadas = [...pausas].sort((a, b) => a.deS - b.deS);
  const segs: Segmento[] = [];
  let saida = 0;
  let fonte = 0;
  for (const p of ordenadas) {
    const de = Math.round(p.deS * fps);
    const ate = Math.round(p.ateS * fps);
    if (de > saida) {
      segs.push({ de: saida, dur: de - saida, srcQuadro: fonte, congelado: false });
      fonte += de - saida;
    }
    segs.push({ de, dur: Math.max(1, ate - de), srcQuadro: fonte, congelado: true });
    saida = ate;
  }
  if (totalQuadros > saida) segs.push({ de: saida, dur: totalQuadros - saida, srcQuadro: fonte, congelado: false });
  return segs;
};

const Conteudo: React.FC<{ src: string; pausas: Intervalo[]; volume: number; w: number; h: number; total: number }> = ({ src, pausas, volume, w, h, total }) => {
  const { fps } = useVideoConfig();
  const estilo = { width: w, height: h, objectPosition: "50% 40%" };
  return (
    <>
      {segmentarConteudo(pausas, total, fps).map((s, i) => (
        <Sequence key={i} from={s.de} durationInFrames={s.dur} name={s.congelado ? "conteudo parado" : "conteudo"}>
          {s.congelado ? (
            <Freeze frame={0}>
              <Video src={staticFile(src)} trimBefore={s.srcQuadro} muted objectFit="cover" style={estilo} />
            </Freeze>
          ) : (
            <Video src={staticFile(src)} trimBefore={s.srcQuadro} volume={volume} objectFit="cover" style={estilo} />
          )}
        </Sequence>
      ))}
    </>
  );
};

/** 08. React: o conteúdo comentado em cima (para, cresce e retoma) e a pessoa reagindo embaixo. */
export const React_: React.FC<PropsReact> = ({
  video,
  takes,
  sobreposicaoS,
  legendas,
  titulo,
  cores,
  fonte,
  duracaoS,
  destaques,
  camera,
  conteudo,
  pausas = [],
  ampliacoes = [],
  rotuloOrigem,
  volumeConteudo = 0.45,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const total = Math.round(duracaoS * fps);
  const base = A * 0.5;
  const maisGrande = A * 0.667;
  const amp = ampliacoes.reduce((m, a) => {
    const de = a.deS * fps;
    const ate = a.ateS * fps;
    return Math.max(m, prog(frame, de, de + 10, EASE.inOut) * (1 - prog(frame, ate - 10, ate, EASE.inOut)));
  }, 0);
  const topo = Math.round(base + (maisGrande - base) * amp);
  return (
    <AbsoluteFill style={{ background: cores.fundo }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: L, height: topo, overflow: "hidden", background: "#000" }}>
        <Conteudo src={conteudo} pausas={pausas} volume={volumeConteudo} w={L} h={Math.round(maisGrande)} total={total} />
      </div>
      <JanelaVideo src={video} takes={takes} sobreposicaoS={sobreposicaoS} x={0} y={topo} w={L} h={A - topo} escala={1.1} origem="50% 28%" camera={cameraDe(legendas, destaques, camera)} />
      <div style={{ position: "absolute", left: 0, top: topo - 4, width: L, height: 8, background: cores.destaque, boxShadow: "0 0 24px rgba(0,0,0,0.5)" }} />
      {rotuloOrigem ? <Tarja texto={rotuloOrigem} fonte={fonte} fundo="rgba(0,0,0,0.65)" cor={cores.texto} y={290} altura={64} tamanho={34} x={SEGURA.lado} largura={460} deS={0.2} /> : null}
      {titulo ? <Titulo texto={titulo.split("\n")} fonte={fonte} cor={cores.texto} y={380} tamanho={64} deS={0.2} ateS={2.6} caixaAlta /> : null}
      <div style={{ position: "absolute", left: 0, top: topo - 70, width: L }}>
        <Legenda legendas={legendas} cores={cores} fonte={fonte} y={0} destaques={destaques} />
      </div>
    </AbsoluteFill>
  );
};
