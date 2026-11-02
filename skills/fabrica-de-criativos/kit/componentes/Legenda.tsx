import React, { useMemo } from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import type { Caption, Cores } from "../tipos";
import { EASE, prog } from "./Movimento";

type Pagina = { palavras: Caption[]; iniMs: number; fimMs: number };

const limpa = (t: string) => t.trim().toLowerCase().replace(/[.,!?;:"'()]/g, "");

/** Agrupa as palavras em páginas de até `max` palavras, quebrando em pontuação final e em pausas. */
export const paginar = (legendas: Caption[], max = 4, pausaMs = 500): Pagina[] => {
  const paginas: Pagina[] = [];
  let atual: Caption[] = [];
  const fecha = () => {
    if (atual.length) {
      paginas.push({ palavras: atual, iniMs: atual[0].startMs, fimMs: atual[atual.length - 1].endMs });
      atual = [];
    }
  };
  legendas.forEach((w, i) => {
    const anterior = legendas[i - 1];
    if (anterior && w.startMs - anterior.endMs > pausaMs) fecha();
    atual.push(w);
    if (atual.length >= max || /[.!?]$/.test(w.text.trim())) fecha();
  });
  fecha();
  return paginas;
};

type Props = {
  legendas: Caption[];
  cores: Cores;
  fonte: string;
  /** topo do bloco da legenda, em px */
  y: number;
  /** corpo do texto, em px (num quadro de 1080 de largura) */
  tamanho?: number;
  maxPalavras?: number;
  larguraMax?: number;
  destaques?: string[];
  /** desloca o tempo (ms), quando a legenda está dentro de uma Sequence que não começa em 0 */
  deslocamentoMs?: number;
  /** estilo discreto (sem caixa alta nem contorno): para formatos calmos */
  discreta?: boolean;
};

/**
 * Legenda palavra a palavra: mostra a página atual (até 3 palavras), a palavra dita ganha cor e um pulso curto,
 * e as palavras de `destaques` ficam na cor de destaque. Contorno fino e sombra suave, sem engordar a letra.
 */
export const Legenda: React.FC<Props> = ({ legendas, cores, fonte, y, tamanho = 64, maxPalavras = 3, larguraMax = 840, destaques = [], deslocamentoMs = 0, discreta = false }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const paginas = useMemo(() => paginar(legendas, maxPalavras), [legendas, maxPalavras]);
  const t = (frame / fps) * 1000 + deslocamentoMs;
  const idx = paginas.findIndex((p, i) => t >= p.iniMs && t < Math.max(p.fimMs + 250, paginas[i + 1]?.iniMs ?? 0));
  if (idx < 0) return null;
  const pag = paginas[idx];
  if (t > pag.fimMs + 250) return null;
  const idadeQuadros = ((t - pag.iniMs) / 1000) * fps;
  const entrada = prog(idadeQuadros, 0, 5, EASE.out);
  const saida = 1 - prog(((t - pag.fimMs) / 1000) * fps, 2, 7, EASE.in);
  const destaquesLimpos = destaques.map(limpa);
  const contorno = Math.max(2, Math.round(tamanho * 0.055));
  return (
    <div
      style={{
        position: "absolute",
        top: y,
        left: (width - larguraMax) / 2,
        width: larguraMax,
        textAlign: "center",
        fontFamily: fonte,
        fontWeight: discreta ? 600 : 800,
        fontSize: tamanho,
        lineHeight: 1.14,
        letterSpacing: discreta ? 0 : -tamanho * 0.01,
        textTransform: discreta ? undefined : "uppercase",
        textShadow: discreta ? "0 2px 12px rgba(0,0,0,0.75)" : "0 5px 18px rgba(0,0,0,0.55)",
        transform: `translateY(${(1 - entrada) * 14}px)`,
        opacity: Math.min(entrada, saida),
      }}
    >
      {pag.palavras.map((w, i) => {
        const ativa = t >= w.startMs && t < w.endMs;
        const marcada = destaquesLimpos.includes(limpa(w.text));
        const idadePalavra = ((t - w.startMs) / 1000) * fps;
        const pulso = ativa ? 1.04 + 0.1 * (1 - prog(idadePalavra, 0, 6, EASE.out)) : 1;
        return (
          <span
            key={`${w.startMs}-${i}`}
            style={{
              color: ativa || marcada ? cores.destaque : cores.texto,
              WebkitTextStroke: discreta ? undefined : `${contorno}px rgba(0,0,0,0.92)`,
              paintOrder: "stroke fill",
              display: "inline-block",
              marginRight: tamanho * 0.24,
              transform: `scale(${pulso})`,
            }}
          >
            {w.text.trim()}
          </span>
        );
      })}
    </div>
  );
};
