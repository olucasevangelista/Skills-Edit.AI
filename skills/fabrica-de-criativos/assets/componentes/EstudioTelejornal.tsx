/**
 * Cenário e título de telejornal, para o formato 11: um estúdio ilustrado (degradê, feixes de luz e globos de linhas girando
 * devagar) e o título de bancada ("NOTÍCIA" cromado sobre uma placa "URGENTE").
 *
 * São PEÇAS PARA REAPROVEITAR no seu projeto Remotion (copie e ajuste), não um editor: o apresentador, a faixa do meio, os
 * cartões, a legenda e a composição são seus. Só dependem do `remotion`. Tudo é função do quadro.
 *
 * As cores padrão (azul e vermelho) são as do exemplo do autor, não uma regra: troque pelas do tema ou da marca. Os globos e os
 * feixes são decoração; use `globos={[]}` ou `feixes={false}` para tirar. O texto do título e a fonte são seus (use uma fonte
 * condensada e pesada, já carregada). Mantenha a identidade própria: nada de nome, logotipo ou vinheta de canal real.
 */
import React from "react";
import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export type Globo = {
  /** posição do canto superior esquerdo e diâmetro, em px */
  x: number;
  y: number;
  d: number;
  /** opacidade das linhas (0 a 1) */
  opacidade: number;
  /** velocidade de giro (radianos por segundo; negativo gira ao contrário) */
  giro: number;
};

export type PropsEstudio = {
  /** degradê radial do centro para a borda */
  cores?: [string, string, string];
  corLinhas?: string;
  /** cor dos feixes de luz (com transparência) */
  corFeixe?: string;
  feixes?: boolean;
  globos?: Globo[];
};

/** Os dois globos do exemplo (1080x1920): um no alto à direita e outro embaixo à esquerda, atrás do apresentador. */
export const GLOBOS_PADRAO: Globo[] = [
  { x: 560, y: 40, d: 760, opacidade: 0.28, giro: 0.25 },
  { x: -260, y: 1130, d: 1000, opacidade: 0.2, giro: -0.2 },
];

const GloboDeLinhas: React.FC<{ g: Globo; t: number; cor: string }> = ({ g, t, cor }) => {
  const r = g.d / 2;
  const giro = t * g.giro;
  return (
    <svg width={g.d} height={g.d} viewBox={`${-r} ${-r} ${g.d} ${g.d}`} style={{ position: "absolute", left: g.x, top: g.y, opacity: g.opacidade }}>
      <g fill="none" stroke={cor} strokeWidth={2.2}>
        <circle r={r - 2} />
        {/* meridianos: a largura de cada elipse acompanha o giro */}
        {[0.25, 0.5, 0.75, 1].map((k) => (
          <ellipse key={`m${k}`} rx={(r - 2) * Math.abs(Math.cos((k * Math.PI) / 2 + giro)) + 1} ry={r - 2} />
        ))}
        {/* paralelos */}
        {[-0.66, -0.33, 0, 0.33, 0.66].map((k) => (
          <ellipse key={`p${k}`} cy={k * r} rx={Math.sqrt(1 - k * k) * (r - 2)} ry={Math.sqrt(1 - k * k) * (r - 2) * 0.16} />
        ))}
      </g>
    </svg>
  );
};

export const EstudioTelejornal: React.FC<PropsEstudio> = ({
  cores = ["#1337A8", "#0A1E5A", "#050B26"],
  corLinhas = "#9FC2FF",
  corFeixe = "rgba(160,200,255,0.16)",
  feixes = true,
  globos = GLOBOS_PADRAO,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  return (
    <>
      <div style={{ position: "absolute", inset: 0, background: `radial-gradient(100% 60% at 50% 30%, ${cores[0]} 0%, ${cores[1]} 45%, ${cores[2]} 100%)` }} />
      {feixes
        ? [-200, 150, 520, 840].map((x, i) => (
            <div
              key={x}
              style={{ position: "absolute", left: x + 30 * Math.sin(t * 0.6 + i), top: -200, width: 150 + i * 30, height: 2400, background: `linear-gradient(90deg, transparent, ${corFeixe}, transparent)`, transform: "rotate(24deg)" }}
            />
          ))
        : null}
      {globos.map((g, i) => (
        <GloboDeLinhas key={i} g={g} t={t} cor={corLinhas} />
      ))}
    </>
  );
};

const Cromado: React.FC<{ children: React.ReactNode; tamanho: number; fonte: string }> = ({ children, tamanho, fonte }) => (
  <div
    style={{
      fontFamily: fonte,
      fontWeight: 800,
      fontSize: tamanho,
      fontStyle: "italic",
      letterSpacing: "0.02em",
      lineHeight: 1,
      background: "linear-gradient(180deg, #FFFFFF 0%, #C9D3E6 45%, #8C98B3 55%, #E8EEF8 100%)",
      WebkitBackgroundClip: "text",
      backgroundClip: "text",
      color: "transparent",
      filter: "drop-shadow(0 4px 6px rgba(0,0,0,0.55))",
    }}
  >
    {children}
  </div>
);

export type PropsTituloBancada = {
  linha1?: string;
  linha2?: string;
  /** y do topo do título (padrão 280) */
  y?: number;
  fonte?: string;
  /** instante em que o título entra (s) */
  deS?: number;
  /** cor da placa */
  corPlaca?: string;
};

/** Título de bancada: uma linha cromada em cima e, embaixo, a palavra principal sobre uma placa. Entra com um pop curto. */
export const TituloBancada: React.FC<PropsTituloBancada> = ({ linha1 = "NOTÍCIA", linha2 = "URGENTE", y = 280, fonte = '"Arial Narrow", Arial, sans-serif', deS = 0.05, corPlaca = "#C0121F" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const e = interpolate(t, [deS, deS + 0.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(1.7)) });
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, display: "flex", flexDirection: "column", alignItems: "center", opacity: Math.min(1, e * 1.4), scale: String(0.8 + 0.2 * e) }}>
      <Cromado tamanho={76} fonte={fonte}>{linha1}</Cromado>
      <div style={{ marginTop: 4, padding: "4px 56px 8px", borderRadius: 14, background: corPlaca, border: "5px solid #D8DFEE", boxShadow: "0 10px 30px rgba(0,0,0,0.55), inset 0 3px 0 rgba(255,255,255,0.35)" }}>
        <Cromado tamanho={120} fonte={fonte}>{linha2}</Cromado>
      </div>
    </div>
  );
};
