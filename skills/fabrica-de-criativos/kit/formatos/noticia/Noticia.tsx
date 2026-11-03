import React from "react";
import { AbsoluteFill, Easing, useCurrentFrame, useVideoConfig } from "remotion";
import { A, FONTE_MANCHETE, L, SEGURA, type PropsBase } from "../../tipos";
import { JanelaVideo } from "../../componentes/JanelaVideo";
import { Logotipo, type Marca } from "../../componentes/Marca";
import { EASE, prog } from "../../componentes/Movimento";

export type Manchete = { texto: string; deS: number; ateS: number };

export type PropsNoticia = Omit<PropsBase, "titulo"> & {
  /** o logotipo do topo: o SEU veículo, perfil ou marca (nome e logo próprios) */
  marca: Marca;
  posicaoMarca?: "centro" | "esq";
  /** as manchetes, uma de cada vez; devem ser verdadeiras e sustentadas pelo anúncio */
  manchetes: Manchete[];
  /** y da borda de baixo da caixa da manchete (padrão 1220, acima da zona de interface) */
  baseY?: number;
  /** a caixa branca termina de entrar em `caixaS`; o texto começa `textoAtrasoS` depois da caixa e leva `textoDurS` */
  caixaS?: number;
  textoAtrasoS?: number;
  textoDurS?: number;
  corCaixa?: string;
  corTexto?: string;
  tamanho?: number;
  /** escurece o topo para o logotipo ler sobre qualquer imagem (0 a 0,6) */
  escurecer?: number;
  /** fonte da manchete (padrão: Barlow Condensed, condensada e pesada) */
  fonteManchete?: string;
};

type PropsFaixa = { texto: string; fonte: string; deS: number; ateS: number; baseY: number; caixaS: number; textoAtrasoS: number; textoDurS: number; corCaixa: string; corTexto: string; tamanho: number };

/** Uma manchete: a caixa branca entra da esquerda para a direita; o texto entra no mesmo sentido, um pouco depois, e termina meio segundo depois da caixa. */
const Faixa: React.FC<PropsFaixa> = ({ texto, fonte, deS, ateS, baseY, caixaS, textoAtrasoS, textoDurS, corCaixa, corTexto, tamanho }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ini = Math.round(deS * fps);
  const fim = Math.round(ateS * fps);
  if (frame < ini || frame > fim + 6) return null;
  const f = frame - ini;
  const caixa = prog(f, 0, Math.round(caixaS * fps), EASE.out);
  const a = Math.round(textoAtrasoS * fps);
  const letra = prog(f, a, a + Math.round(textoDurS * fps), Easing.linear);  // linear: o texto leva mesmo o tempo dito, sem terminar antes do olho perceber
  const saida = 1 - prog(frame, fim, fim + 5, EASE.in);
  const estilo: React.CSSProperties = {
    fontFamily: fonte,
    fontWeight: 800,
    fontSize: tamanho,
    lineHeight: 1.1,
    textTransform: "uppercase",
    letterSpacing: 0,
    padding: "0.03em 0.26em 0.01em",
    boxDecorationBreak: "clone",
    WebkitBoxDecorationBreak: "clone",
  };
  return (
    <div style={{ position: "absolute", left: SEGURA.lado, bottom: A - baseY, maxWidth: L - SEGURA.lado - SEGURA.ladoDireito, opacity: saida }}>
      <div style={{ position: "relative", display: "inline-block" }}>
        <div style={{ clipPath: `inset(0 ${(1 - caixa) * 100}% 0 0)` }}>
          <span style={{ ...estilo, background: corCaixa, color: "transparent" }}>{texto}</span>
        </div>
        <div style={{ position: "absolute", left: 0, top: 0, clipPath: `inset(0 ${(1 - letra) * 100}% 0 0)` }}>
          <span style={{ ...estilo, color: corTexto }}>{texto}</span>
        </div>
      </div>
    </div>
  );
};

/** 04. Notícia: vídeo em tela cheia, logotipo no topo e a manchete numa caixa branca que entra da esquerda para a direita. */
export const Noticia: React.FC<PropsNoticia> = ({
  video,
  takes,
  sobreposicaoS,
  children,
  fonte,
  marca,
  posicaoMarca = "centro",
  manchetes,
  baseY = 1220,
  caixaS = 0.3,
  textoAtrasoS = 0.13,
  textoDurS = 0.67,
  corCaixa = "#FFFFFF",
  corTexto = "#0B0B0B",
  tamanho = 92,
  fonteManchete = FONTE_MANCHETE,
  escurecer = 0,
}) => {
  return (
  <AbsoluteFill style={{ background: "#000000" }}>
    <JanelaVideo src={video} takes={takes} sobreposicaoS={sobreposicaoS} x={0} y={0} w={L} h={A} origem="50% 40%" />
    <div style={{ position: "absolute", left: 0, top: 0, width: L, height: 620, background: `linear-gradient(rgba(0,0,0,${escurecer}), rgba(0,0,0,0))` }} />
    <Logotipo marca={marca} fonte={fonte} y={SEGURA.topo + 20} posicao={posicaoMarca} />
    {manchetes.map((m, i) => (
      <Faixa key={i} texto={m.texto} fonte={fonteManchete} deS={m.deS} ateS={m.ateS} baseY={baseY} caixaS={caixaS} textoAtrasoS={textoAtrasoS} textoDurS={textoDurS} corCaixa={corCaixa} corTexto={corTexto} tamanho={tamanho} />
    ))}
    {children}
  </AbsoluteFill>
  );
};
