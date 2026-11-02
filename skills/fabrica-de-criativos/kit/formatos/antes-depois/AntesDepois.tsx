import React from "react";
import { AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { L, type PropsBase } from "../../tipos";
import { JanelaVideo } from "../../componentes/JanelaVideo";
import { Legenda } from "../../componentes/Legenda";
import { EASE, prog } from "../../componentes/Movimento";
import { Titulo } from "../../componentes/Titulo";

export type PropsAntesDepois = Omit<PropsBase, "video"> & {
  video?: string;
  /** as duas situações (imagem ou vídeo em public/): reais, e com o mesmo enquadramento */
  antes: string;
  depois: string;
  modo?: "deslize" | "lado-a-lado" | "sequencia";
  rotulos?: { antes: string; depois: string };
  /** instante em que a revelação começa e quanto ela dura */
  revelarEmS?: number;
  duracaoRevelacaoS?: number;
  /** narração em áudio (opcional) */
  narracao?: string;
};

const MIDIA = { x: 0, y: 330, w: L, h: 1260 };

const Rotulo: React.FC<{ texto: string; lado: "esq" | "dir"; cores: PropsBase["cores"]; fonte: string; opacidade: number; xBase?: number }> = ({ texto, lado, cores, fonte, opacidade, xBase = 0 }) => (
  <div
    style={{
      position: "absolute",
      top: MIDIA.y + 28,
      [lado === "esq" ? "left" : "right"]: xBase + (lado === "esq" ? 70 : 100),
      padding: "10px 26px",
      borderRadius: 999,
      background: "rgba(0,0,0,0.7)",
      color: cores.texto,
      fontFamily: fonte,
      fontWeight: 800,
      fontSize: 44,
      letterSpacing: 2,
      opacity: opacidade,
    }}
  >
    {texto}
  </div>
);

/** 14. Antes e Depois: duas situações reais no mesmo enquadramento, com divisória que desliza e rótulos nítidos. */
export const AntesDepois: React.FC<PropsAntesDepois> = ({
  legendas,
  titulo,
  cores,
  fonte,
  destaques,
  antes,
  depois,
  modo = "deslize",
  rotulos = { antes: "ANTES", depois: "DEPOIS" },
  revelarEmS = 2,
  duracaoRevelacaoS = 1.6,
  narracao,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ini = revelarEmS * fps;
  const pct = modo === "lado-a-lado" ? 50 : modo === "sequencia" ? (frame >= ini ? 100 : 0) : prog(frame, ini, ini + duracaoRevelacaoS * fps, EASE.inOut) * 100;
  const emMovimento = modo === "deslize" && pct > 0 && pct < 100;
  const xDiv = (pct / 100) * L;
  return (
    <AbsoluteFill style={{ background: cores.fundo }}>
      {modo === "lado-a-lado" ? (
        <>
          <JanelaVideo src={antes} x={0} y={MIDIA.y} w={L / 2 - 4} h={MIDIA.h} muted />
          <JanelaVideo src={depois} x={L / 2 + 4} y={MIDIA.y} w={L / 2 - 4} h={MIDIA.h} muted />
          <Rotulo texto={rotulos.antes} lado="esq" cores={cores} fonte={fonte} opacidade={1} />
          <Rotulo texto={rotulos.depois} lado="dir" cores={cores} fonte={fonte} opacidade={1} />
        </>
      ) : (
        <>
          <JanelaVideo src={antes} {...MIDIA} muted />
          <div style={{ position: "absolute", left: MIDIA.x, top: MIDIA.y, width: MIDIA.w, height: MIDIA.h, clipPath: `inset(0 ${100 - pct}% 0 0)` }}>
            <JanelaVideo src={depois} x={0} y={0} w={MIDIA.w} h={MIDIA.h} muted />
          </div>
          {emMovimento ? (
            <>
              <div style={{ position: "absolute", left: xDiv - 4, top: MIDIA.y, width: 8, height: MIDIA.h, background: cores.texto, boxShadow: "0 0 18px rgba(0,0,0,0.6)" }} />
              <div style={{ position: "absolute", left: xDiv - 36, top: MIDIA.y + MIDIA.h / 2 - 36, width: 72, height: 72, borderRadius: 36, background: cores.texto, boxShadow: "0 8px 22px rgba(0,0,0,0.5)" }} />
            </>
          ) : null}
          <Rotulo texto={rotulos.antes} lado="esq" cores={cores} fonte={fonte} opacidade={pct < 60 ? 1 : 0} />
          <Rotulo texto={rotulos.depois} lado="dir" cores={cores} fonte={fonte} opacidade={pct > 40 ? 1 : 0} />
        </>
      )}
      {titulo ? <Titulo texto={titulo.split("\n")} fonte={fonte} cor={cores.texto} y={285} tamanho={60} deS={0.1} caixaAlta /> : null}
      <Legenda legendas={legendas} cores={cores} fonte={fonte} y={1090} destaques={destaques} />
      {narracao ? <Audio src={staticFile(narracao)} /> : null}
    </AbsoluteFill>
  );
};
