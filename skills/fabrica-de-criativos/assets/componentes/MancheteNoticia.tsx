/**
 * Manchete de notícia: uma caixa branca com o texto em caixa alta (e, se quiser, uma etiqueta pequena acima, como "URGENTE").
 *
 * É uma PEÇA PARA REAPROVEITAR no seu projeto Remotion (copie e ajuste), não um editor: o vídeo por baixo, as etiquetas do topo,
 * a legenda e o resto são seus. Só depende do `remotion`. Tudo é função do quadro.
 *
 * Duas entradas:
 * - "revelacao": a caixa branca é revelada da esquerda para a direita e o texto vem logo depois, terminando cerca de 0,5 s
 *   depois da caixa (`caixaS`, `textoAtrasoS` e `textoDurS` ajustam os tempos).
 * - "deslize": a faixa inteira desliza da esquerda (e sai para a esquerda).
 * As manchetes trocam conforme a fala: passe uma lista com `deS`/`ateS` em segundos.
 *
 * Use uma fonte condensada e pesada, já carregada no projeto, em `fonte` (o desenho da fonte é sua escolha).
 * Mantenha a borda de baixo da caixa (`baseY`) acima da zona de interface da base (~1250 em 1080x1920).
 * A caixa fica dentro das margens de segurança (x de 90 a 960); a etiqueta fica colada no canto de cima da caixa.
 */
import React from "react";
import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export type Manchete = { texto: string; deS: number; ateS: number };

export type PropsMancheteNoticia = {
  manchetes: Manchete[];
  modo?: "revelacao" | "deslize";
  /** y da borda de baixo da caixa (a manchete cresce para cima) */
  baseY?: number;
  /** posição da caixa: o padrão (90) deixa uma margem de segurança da borda; 0 encosta na borda esquerda */
  x?: number;
  /** largura máxima da caixa (padrão 870: de x = 90 até a margem direita de 120 px em 1080) */
  larguraMax?: number;
  /** recuo do texto dentro da caixa, em px (padrão 36) */
  recuoX?: number;
  /** "bloco" (padrão): um retângulo branco único, como no exemplo; "linhas": cada linha tem a sua caixa, do tamanho do texto */
  forma?: "bloco" | "linhas";
  fonte: string;
  tamanho?: number;
  corCaixa?: string;
  corTexto?: string;
  /** etiqueta pequena acima da caixa ("URGENTE"); omita para não ter */
  etiqueta?: string;
  corEtiqueta?: string;
  caixaS?: number;
  textoAtrasoS?: number;
  textoDurS?: number;
};

const limita = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

type PropsUma = Required<Pick<PropsMancheteNoticia, "modo" | "baseY" | "x" | "larguraMax" | "recuoX" | "forma" | "fonte" | "tamanho" | "corCaixa" | "corTexto" | "corEtiqueta" | "caixaS" | "textoAtrasoS" | "textoDurS">> &
  Manchete & { etiqueta?: string };

const Uma: React.FC<PropsUma> = ({ texto, deS, ateS, modo, baseY, x, larguraMax, recuoX, forma, fonte, tamanho, corCaixa, corTexto, etiqueta, corEtiqueta, caixaS, textoAtrasoS, textoDurS }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = frame / fps;
  if (t < deS - 0.01 || t > ateS + 0.4) return null;
  const f = t - deS;
  const sai = interpolate(t, [ateS, ateS + 0.3], [0, 1], { ...limita, easing: Easing.in(Easing.cubic) });
  const estilo: React.CSSProperties = {
    fontFamily: fonte,
    fontWeight: 800,
    fontSize: tamanho,
    lineHeight: 1.1,
    textTransform: "uppercase",
    padding: `0.03em ${recuoX}px 0.01em`,
    boxDecorationBreak: "clone",
    WebkitBoxDecorationBreak: "clone",
    ...(forma === "bloco" ? { display: "block", width: larguraMax, boxSizing: "border-box", padding: `14px ${recuoX}px 16px` } : {}),
  };
  const caixa = interpolate(f, [0, caixaS], [0, 1], { ...limita, easing: Easing.out(Easing.cubic) });
  const letra = interpolate(f, [textoAtrasoS, textoAtrasoS + textoDurS], [0, 1], { ...limita, easing: Easing.linear });
  const deslize = interpolate(f, [0, 0.5], [0, 1], { ...limita, easing: Easing.out(Easing.cubic) });
  const translate = modo === "deslize" ? `${(1 - deslize) * -width + sai * -width}px 0px` : "0px 0px";
  return (
    <div style={{ position: "absolute", left: x, bottom: height - baseY, maxWidth: larguraMax, translate, opacity: modo === "revelacao" ? 1 - sai : 1 }}>
      {etiqueta ? (
        <div style={{ display: "inline-block", padding: "6px 30px", background: corEtiqueta, color: "#fff", fontFamily: fonte, fontWeight: 800, fontSize: tamanho * 0.55, letterSpacing: "0.12em" }}>{etiqueta}</div>
      ) : null}
      {modo === "deslize" ? (
        <div style={{ display: "block" }}>
          <span style={{ ...estilo, background: corCaixa, color: corTexto }}>{texto}</span>
        </div>
      ) : (
        <div style={{ position: "relative", display: "inline-block" }}>
          {/* a caixa (texto invisível) e o texto (sem caixa) têm o mesmo desenho, então se alinham; cada um é revelado no seu tempo */}
          <div style={{ clipPath: `inset(0 ${(1 - caixa) * 100}% 0 0)` }}>
            <span style={{ ...estilo, background: corCaixa, color: "transparent" }}>{texto}</span>
          </div>
          <div style={{ position: "absolute", left: 0, top: 0, clipPath: `inset(0 ${(1 - letra) * 100}% 0 0)` }}>
            <span style={{ ...estilo, color: corTexto }}>{texto}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export const MancheteNoticia: React.FC<PropsMancheteNoticia> = ({
  manchetes,
  modo = "revelacao",
  baseY = 1220,
  x = 90,
  larguraMax = 870,
  recuoX = 36,
  forma = "bloco",
  fonte,
  tamanho = 72,
  corCaixa = "#FFFFFF",
  corTexto = "#0B0B0B",
  etiqueta,
  corEtiqueta = "#D7263D",
  caixaS = 0.3,
  textoAtrasoS = 0.13,
  textoDurS = 0.67,
}) => (
  <>
    {manchetes.map((m, i) => (
      <Uma key={i} {...m} modo={modo} baseY={baseY} x={x} larguraMax={larguraMax} recuoX={recuoX} forma={forma} fonte={fonte} tamanho={tamanho} corCaixa={corCaixa} corTexto={corTexto} etiqueta={etiqueta} corEtiqueta={corEtiqueta} caixaS={caixaS} textoAtrasoS={textoAtrasoS} textoDurS={textoDurS} />
    ))}
  </>
);
