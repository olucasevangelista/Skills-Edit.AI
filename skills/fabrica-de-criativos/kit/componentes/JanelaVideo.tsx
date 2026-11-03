import React from "react";
import { Img, staticFile, useVideoConfig } from "remotion";
import { Video } from "@remotion/media";
import type { Take } from "../tipos";
import { Takes } from "./Takes";

const EH_IMAGEM = /\.(png|jpe?g|webp|gif|avif|svg)$/i;

type Props = {
  /** arquivo em public/ (vídeo ou imagem) */
  src?: string;
  /** em vez de `src`: uma sequência de trechos com emenda por sobreposição */
  takes?: Take[];
  sobreposicaoS?: number;
  x: number;
  y: number;
  w: number;
  h: number;
  raio?: number;
  fit?: "cover" | "contain";
  /** zoom aplicado dentro da janela (1 = sem zoom) */
  escala?: number;
  /** ponto do enquadramento (CSS object-position e transform-origin), por exemplo "50% 30%" */
  origem?: string;
  volume?: number;
  muted?: boolean;
  /** quadros a pular no início do vídeo */
  trimBefore?: number;
  filtro?: string;
  sombra?: string;
  /** cor de fundo atrás da mídia (útil com fit "contain") */
  fundo?: string;
};

/** Uma janela retangular (com cantos arredondados) que mostra um vídeo, uma imagem ou uma sequência de takes. */
export const JanelaVideo: React.FC<Props> = ({
  src,
  takes,
  sobreposicaoS,
  x,
  y,
  w,
  h,
  raio = 0,
  fit = "cover",
  escala = 1,
  origem = "50% 35%",
  volume = 1,
  muted = false,
  trimBefore = 0,
  filtro,
  sombra,
  fundo,
}) => {
  const { fps } = useVideoConfig();
  const estilo: React.CSSProperties = {
    width: "100%",
    height: "100%",
    objectFit: fit,
    objectPosition: origem,
  };
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h, borderRadius: raio, overflow: "hidden", boxShadow: sombra, background: fundo }}>
      <div style={{ position: "absolute", inset: 0, transform: `scale(${escala})`, transformOrigin: origem, filter: filtro }}>
        {takes ? (
          <Takes takes={takes} fps={fps} sobreposicaoS={sobreposicaoS} objectFit={fit} volume={muted ? 0 : volume} origem={origem} />
        ) : src && EH_IMAGEM.test(src) ? (
          <Img src={staticFile(src)} style={estilo} />
        ) : src ? (
          <Video src={staticFile(src)} trimBefore={trimBefore} objectFit={fit} style={estilo} volume={muted ? 0 : volume} />
        ) : null}
      </div>
    </div>
  );
};
