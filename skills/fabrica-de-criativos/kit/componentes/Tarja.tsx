import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { L, SEGURA } from "../tipos";
import { EASE, prog } from "./Movimento";

type Props = {
  texto: string;
  fonte: string;
  /** cor da faixa e do texto */
  fundo: string;
  cor: string;
  y: number;
  altura?: number;
  tamanho?: number;
  x?: number;
  largura?: number;
  deS?: number;
  ateS?: number;
  caixaAlta?: boolean;
};

/** Faixa de texto (manchete, identificação, rótulo) que entra deslizando da lateral e sai em fade. */
export const Tarja: React.FC<Props> = ({ texto, fonte, fundo, cor, y, altura = 120, tamanho = 56, x = SEGURA.lado, largura = L - SEGURA.lado - SEGURA.ladoDireito, deS = 0.3, ateS, caixaAlta = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ini = Math.round(deS * fps);
  const fim = ateS === undefined ? undefined : Math.round(ateS * fps);
  if (frame < ini || (fim !== undefined && frame > fim + 8)) return null;
  const p = prog(frame, ini, ini + 9, EASE.out);
  const saida = fim === undefined ? 1 : 1 - prog(frame, fim, fim + 8, EASE.in);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: largura,
        height: altura,
        background: fundo,
        color: cor,
        display: "flex",
        alignItems: "center",
        padding: "0 32px",
        borderRadius: 14,
        fontFamily: fonte,
        fontWeight: 800,
        fontSize: tamanho,
        lineHeight: 1.05,
        textTransform: caixaAlta ? "uppercase" : undefined,
        transform: `translateX(${(1 - p) * -largura * 0.4}px)`,
        opacity: p * saida,
        boxShadow: "0 12px 30px rgba(0,0,0,0.35)",
      }}
    >
      {texto}
    </div>
  );
};
