import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { SEGURA } from "../tipos";
import { EASE, prog } from "./Movimento";

type Props = {
  /** uma ou várias linhas */
  texto: string | string[];
  fonte: string;
  cor: string;
  /** topo do bloco, em px (respeite a zona segura: y >= 270) */
  y: number;
  tamanho?: number;
  /** quando aparece e quando sai, em segundos */
  deS?: number;
  ateS?: number;
  peso?: number;
  /** cor da palavra final (realce), se diferente */
  corRealce?: string;
  caixaAlta?: boolean;
  espaco?: number;
  serifada?: boolean;
  /** entrada só em fade, lenta (para formatos calmos) */
  suave?: boolean;
  /** sombra de texto, para ler sobre imagens */
  sombra?: boolean;
};

/** Título com entrada curta (sobe e aparece) e saída em fade. Linha por linha, com pequena defasagem. */
export const Titulo: React.FC<Props> = ({ texto, fonte, cor, y, tamanho = 84, deS = 0.1, ateS, peso = 800, corRealce, caixaAlta = false, espaco = 0.02, serifada = false, suave = false, sombra = true }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const linhas = Array.isArray(texto) ? texto : [texto];
  const ini = Math.round(deS * fps);
  const fim = ateS === undefined ? undefined : Math.round(ateS * fps);
  if (frame < ini || (fim !== undefined && frame > fim + 8)) return null;
  const saida = fim === undefined ? 1 : 1 - prog(frame, fim, fim + 8, EASE.in);
  return (
    <div style={{ position: "absolute", top: y, left: SEGURA.lado, width: width - 2 * SEGURA.lado, textAlign: "center", opacity: saida }}>
      {linhas.map((l, i) => {
        const p = suave ? prog(frame, ini + i * 8, ini + i * 8 + 24, EASE.soft) : prog(frame, ini + i * 5, ini + i * 5 + 14, EASE.out);
        const ultima = i === linhas.length - 1;
        return (
          <div
            key={i}
            style={{
              fontFamily: serifada ? 'Georgia, "Times New Roman", serif' : fonte,
              fontWeight: peso,
              fontSize: tamanho,
              lineHeight: 1.08,
              letterSpacing: -tamanho * espaco,
              textTransform: caixaAlta ? "uppercase" : undefined,
              color: ultima && corRealce ? corRealce : cor,
              opacity: p,
              transform: suave ? undefined : `translateY(${(1 - p) * 36}px)`,
              textShadow: sombra ? "0 4px 18px rgba(0,0,0,0.55)" : undefined,
            }}
          >
            {l}
          </div>
        );
      })}
    </div>
  );
};
