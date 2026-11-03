import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig } from "remotion";
import { A, L, type PropsBase } from "../../tipos";
import { JanelaVideo } from "../../componentes/JanelaVideo";
import { EASE, pop, prog } from "../../componentes/Movimento";
import { Tarja } from "../../componentes/Tarja";
import { Titulo } from "../../componentes/Titulo";

export type PropsDepoimento = PropsBase & {
  /** identificação da pessoa: só com o que ela autorizou */
  identificacao?: { nome: string; descricao?: string };
  /** provas que entram na palavra que ilustram (prints, imagens, resultados reais) */
  inserts?: { src: string; deS: number; ateS: number; legenda?: string }[];
  /** zooms pontuais de ênfase nas frases-chave (com retorno ao neutro) */
  zooms?: { deS: number; ateS: number; escala: number }[];
  /** enquadramento base (1 = sem zoom) */
  zoomBase?: number;
};

const Insert: React.FC<{ src: string; legenda?: string; fonte: string; texto: string }> = ({ src, legenda, fonte, texto }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = Math.max(0, pop(frame, fps, 0, 14, 130));
  return (
    <div style={{ position: "absolute", left: 48, top: 420, width: L - 96, transform: `scale(${0.9 + 0.1 * Math.min(1, p)})`, opacity: Math.min(1, p * 1.5) }}>
      <JanelaVideo src={src} x={0} y={0} w={L - 96} h={520} raio={24} sombra="0 24px 60px rgba(0,0,0,0.55)" fit="cover" muted />
      {legenda ? (
        <div style={{ position: "absolute", left: 0, top: 540, width: L - 96, textAlign: "center", color: texto, fontFamily: fonte, fontWeight: 700, fontSize: 40, textShadow: "0 3px 14px rgba(0,0,0,0.7)" }}>{legenda}</div>
      ) : null}
    </div>
  );
};

/** 07. Depoimento: a pessoa direto para a câmera, legenda com destaque, zooms pontuais e inserts de prova real. */
export const Depoimento: React.FC<PropsDepoimento> = ({
  video,
  takes,
  sobreposicaoS,
  children,
  titulo,
  cores,
  fonte,
  identificacao,
  inserts = [],
  zooms = [],
  zoomBase = 1.04,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const zoom = zooms.reduce((m, z) => {
    const de = z.deS * fps;
    const ate = z.ateS * fps;
    const entra = prog(frame, de, de + 4, EASE.out);
    const sai = prog(frame, ate - 8, ate, EASE.inOut);
    return Math.max(m, zoomBase + (z.escala - zoomBase) * entra * (1 - sai));
  }, zoomBase);
  return (
    <AbsoluteFill style={{ background: cores.fundo }}>
      <JanelaVideo src={video} takes={takes} sobreposicaoS={sobreposicaoS} x={0} y={0} w={L} h={A} escala={zoom} origem="50% 33%" />
      {identificacao ? (
        <Tarja texto={identificacao.descricao ? `${identificacao.nome}, ${identificacao.descricao}` : identificacao.nome} fonte={fonte} fundo="rgba(0,0,0,0.62)" cor={cores.texto} y={290} altura={84} tamanho={38} deS={0.5} ateS={4} />
      ) : null}
      {titulo ? <Titulo texto={titulo.split("\n")} fonte={fonte} cor={cores.texto} y={420} tamanho={60} deS={0.2} ateS={2.6} caixaAlta /> : null}
      {inserts.map((c, i) => (
        <Sequence key={`${c.src}-${i}`} from={Math.round(c.deS * fps)} durationInFrames={Math.max(1, Math.round((c.ateS - c.deS) * fps))} name={`prova ${i + 1}`}>
          <Insert src={c.src} legenda={c.legenda} fonte={fonte} texto={cores.texto} />
        </Sequence>
      ))}
      {children}
    </AbsoluteFill>
  );
};
