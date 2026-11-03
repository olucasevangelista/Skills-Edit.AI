import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig } from "remotion";
import { A, L, type PropsBase } from "../../tipos";
import { JanelaVideo } from "../../componentes/JanelaVideo";
import { EASE, prog } from "../../componentes/Movimento";
import { Titulo } from "../../componentes/Titulo";

export type ConteudoSuperior = { src: string; tipo?: "imagem" | "video"; deS: number; ateS: number };

export type PropsTelaDividida = PropsBase & {
  /** o que aparece na área de cima, e quando (entra na palavra que ilustra) */
  conteudoSuperior: ConteudoSuperior[];
  /** fração da altura para a área de cima (padrão 0.5) */
  proporcao?: number;
  /** zoom da pessoa na área de baixo (padrão 1.12) */
  zoomPessoa?: number;
  /** ponto do enquadramento da pessoa (CSS object-position) */
  origemPessoa?: string;
};

const Entrada: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const p = prog(frame, 0, 7, EASE.out);
  return <AbsoluteFill style={{ opacity: p, transform: `translateY(${(1 - p) * 28}px)` }}>{children}</AbsoluteFill>;
};

/** 01. Tela Dividida: a prova em cima (troca na palavra que a cita), a pessoa embaixo, divisória nítida. */
export const TelaDividida: React.FC<PropsTelaDividida> = ({
  video,
  takes,
  sobreposicaoS,
  children,
  titulo,
  cores,
  fonte,
  conteudoSuperior,
  proporcao = 0.5,
  zoomPessoa = 1.12,
  origemPessoa = "50% 28%",
}) => {
  const { fps } = useVideoConfig();
  const topo = Math.round(A * proporcao);
  return (
    <AbsoluteFill style={{ background: cores.fundo }}>
      {/* área de cima: fundo neutro e o conteúdo da vez */}
      <div style={{ position: "absolute", left: 0, top: 0, width: L, height: topo, background: cores.apoio, opacity: 0.18 }} />
      <div style={{ position: "absolute", left: 0, top: 0, width: L, height: topo, overflow: "hidden" }}>
        {conteudoSuperior.map((c, i) => (
          <Sequence key={`${c.src}-${i}`} from={Math.round(c.deS * fps)} durationInFrames={Math.max(1, Math.round((c.ateS - c.deS) * fps))} name={`conteudo ${i + 1}`}>
            <Entrada>
              <JanelaVideo src={c.src} x={0} y={0} w={L} h={topo} fit="cover" origem="50% 40%" muted />
            </Entrada>
          </Sequence>
        ))}
      </div>
      {/* área de baixo: a pessoa */}
      <JanelaVideo src={video} takes={takes} sobreposicaoS={sobreposicaoS} x={0} y={topo} w={L} h={A - topo} escala={zoomPessoa} origem={origemPessoa} />
      {/* divisória */}
      <div style={{ position: "absolute", left: 0, top: topo - 4, width: L, height: 8, background: cores.destaque, boxShadow: "0 0 24px rgba(0,0,0,0.5)" }} />
      {titulo ? <Titulo texto={titulo.split("\n")} fonte={fonte} cor={cores.texto} y={300} tamanho={76} deS={0.15} ateS={2.8} caixaAlta /> : null}
      {children}
    </AbsoluteFill>
  );
};
