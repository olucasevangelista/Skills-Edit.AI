import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig } from "remotion";
import { drift, EASE, lerp, pop, prog, sec, squash, track } from "../movimento";
import { ANTECEDENCIA, CENAS, ETAPAS, FONTE, HEIGHT, PALETA, SAFE, TEXTOS, WIDTH } from "./config";

const CX = WIDTH / 2;

const Fundo: React.FC = () => {
  const f = useCurrentFrame();
  // um único foco de luz, longe do texto, que se move devagar
  const gx = 50 + Math.sin(f / 90) * 12;
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse 70% 38% at ${gx}% 78%, rgba(124,140,255,0.22) 0%, rgba(124,140,255,0) 70%), linear-gradient(180deg, ${PALETA.fundo} 0%, ${PALETA.fundoClaro} 100%)`,
      }}
    />
  );
};

/** Texto que sobe e aparece, linha a linha. `delay` em quadros. */
const Linha: React.FC<{ texto: string; y: number; tamanho: number; atraso: number; cor?: string }> = ({
  texto,
  y,
  tamanho,
  atraso,
  cor = PALETA.tinta,
}) => {
  const f = useCurrentFrame();
  const p = prog(f, atraso, atraso + 14, EASE.out);
  return (
    <div
      style={{
        position: "absolute",
        left: SAFE.lado,
        right: SAFE.lado,
        top: y,
        textAlign: "center",
        fontFamily: FONTE,
        fontWeight: 700,
        fontSize: tamanho,
        letterSpacing: -tamanho * 0.03,
        lineHeight: 1.08,
        color: cor,
        opacity: p,
        transform: `translateY(${(1 - p) * 40}px)`,
      }}
    >
      {texto}
    </div>
  );
};

/* --------------------------------------------------------------- cena 1: gancho */

const Gancho: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = Math.max(0.0001, pop(f, fps, 6, 12, 120));
  return (
    <AbsoluteFill>
      <Linha texto={TEXTOS.gancho[0]} y={SAFE.topo + 40} tamanho={120} atraso={4} />
      <Linha texto={TEXTOS.gancho[1]} y={SAFE.topo + 180} tamanho={120} atraso={11} cor={PALETA.destaque} />
      <div
        style={{
          position: "absolute",
          left: CX - 90,
          top: 1000 + drift(f, 0.05, 1) * 8,
          width: 180,
          height: 180,
          borderRadius: 44,
          background: PALETA.apoio,
          transform: `scale(${s})`,
          boxShadow: "0 30px 70px rgba(0,0,0,0.4)",
        }}
      />
    </AbsoluteFill>
  );
};

/* ------------------------------------------------- cena 2: processo (A vira B) */

const TAM = 150; // lado do pacote
const FIM_FICA = 22; // quadros parado em cada estação (intervalo estável para perceber o resultado)

/** Posição vertical do pacote: chega de cima, para em cada estação antes da palavra e segue depois. */
const pacoteY = (f: number, fps: number) => {
  const chaves = [{ f: 0, v: 560 }];
  for (const e of ETAPAS) {
    const chegada = sec(e.t, fps) - ANTECEDENCIA;
    chaves.push({ f: chegada, v: e.y }, { f: chegada + FIM_FICA, v: e.y });
  }
  chaves.push({ f: sec(CENAS.processo.ate, fps) - 8, v: 1700 });
  return track(f, chaves);
};

/** Estado do pacote (0 a 1 em cada etapa), que muda NA palavra. */
const estado = (f: number, fps: number, i: number) =>
  prog(f, sec(ETAPAS[i].t, fps), sec(ETAPAS[i].t, fps) + 10, EASE.out);

const Pacote: React.FC<{ f: number; fps: number }> = ({ f, fps }) => {
  const y = pacoteY(f, fps);
  const [a, b, c] = [estado(f, fps, 0), estado(f, fps, 1), estado(f, fps, 2)];
  const [sx, sy] = squash(f, sec(ETAPAS[1].t, fps), 0.12);
  return (
    <div
      style={{
        position: "absolute",
        left: CX - TAM / 2,
        top: y - TAM / 2,
        width: TAM,
        height: TAM,
        borderRadius: 36,
        border: `6px solid ${PALETA.suave}`,
        background: `rgba(124,140,255,${a})`,
        transform: `scale(${sx}, ${sy}) translateX(${c * 0}px)`,
        boxShadow: `0 ${24 + c * 10}px ${50 + c * 30}px rgba(${c > 0.5 ? "61,220,151" : "0,0,0"},${0.25 + c * 0.2})`,
      }}
    >
      {/* fita da embalagem: aparece na segunda etapa */}
      <div style={{ position: "absolute", left: "50%", top: 0, bottom: 0, width: 26, marginLeft: -13, background: PALETA.tinta, opacity: b, transform: `scaleY(${b})` }} />
      {/* seta de envio: aparece na terceira etapa */}
      <svg viewBox="0 0 100 100" style={{ position: "absolute", inset: 22, opacity: c }}>
        <path d="M18 50h58M52 26l26 24-26 24" stroke={PALETA.destaque} strokeWidth="11" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      </svg>
    </div>
  );
};

const Processo: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t0 = sec(CENAS.processo.de, fps);
  const fl = f + t0; // quadro absoluto: os tempos da fala são da peça inteira
  return (
    <AbsoluteFill>
      <Linha texto={TEXTOS.explicacao} y={SAFE.topo + 40} tamanho={78} atraso={4} />
      {/* trilho */}
      <div style={{ position: "absolute", left: CX - 3, top: ETAPAS[0].y, height: ETAPAS[2].y - ETAPAS[0].y, width: 6, borderRadius: 3, background: PALETA.suave, opacity: 0.35 * prog(f, 4, 24) }} />
      {ETAPAS.map((e, i) => {
        const feito = estado(fl, fps, i);
        return (
          <React.Fragment key={e.palavra}>
            <div style={{ position: "absolute", left: CX - 22, top: e.y - 22, width: 44, height: 44, borderRadius: 22, border: `5px solid ${feito > 0.5 ? PALETA.destaque : PALETA.suave}`, background: PALETA.fundo, opacity: prog(f, 4 + i * 4, 22 + i * 4) }} />
            <div style={{ position: "absolute", left: CX + 130, top: e.y - 26, fontFamily: FONTE, fontWeight: 600, fontSize: 52, color: feito > 0.5 ? PALETA.tinta : PALETA.suave, opacity: prog(f, 8 + i * 4, 26 + i * 4) }}>
              {e.palavra}
            </div>
          </React.Fragment>
        );
      })}
      <Pacote f={fl} fps={fps} />
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------ cena 3: convergência e assinatura */

const Fecho: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const conv = prog(f, 0, 26, EASE.inOut);
  const marca = pop(f, fps, 22, 14, 110);
  return (
    <AbsoluteFill>
      {ETAPAS.map((e, i) => (
        <div
          key={e.palavra}
          style={{
            position: "absolute",
            left: CX - 22,
            top: lerp(e.y, 1010, conv) - 22,
            width: 44,
            height: 44,
            borderRadius: 22,
            border: `5px solid ${PALETA.destaque}`,
            background: PALETA.fundo,
            opacity: i === 0 || conv < 1 ? 1 - prog(f, 22, 30) : 0,
          }}
        />
      ))}
      <div
        style={{
          position: "absolute",
          left: CX - 110,
          top: 1010 - 110,
          width: 220,
          height: 220,
          borderRadius: 60,
          background: PALETA.destaque,
          transform: `scale(${Math.max(0.0001, marca)})`,
          boxShadow: "0 30px 80px rgba(61,220,151,0.35)",
        }}
      />
      <Linha texto={TEXTOS.marca} y={1210} tamanho={110} atraso={30} />
      <Linha texto={TEXTOS.fecho} y={1360} tamanho={64} atraso={38} cor={PALETA.suave} />
      <div style={{ position: "absolute", left: SAFE.lado, right: SAFE.lado, top: HEIGHT - SAFE.base - 60, textAlign: "center", fontFamily: FONTE, fontSize: 30, color: PALETA.suave, opacity: 0.7 * prog(f, 50, 66) }}>
        {TEXTOS.aviso}
      </div>
    </AbsoluteFill>
  );
};

export const Exemplo: React.FC = () => {
  const { fps } = useVideoConfig();
  const c = (cena: { de: number; ate: number }) => ({ from: sec(cena.de, fps), durationInFrames: sec(cena.ate - cena.de, fps) });
  return (
    <AbsoluteFill>
      <Fundo />
      <Sequence name="1 Gancho" premountFor={fps} {...c(CENAS.gancho)}>
        <Gancho />
      </Sequence>
      <Sequence name="2 Processo" premountFor={fps} {...c(CENAS.processo)}>
        <Processo />
      </Sequence>
      <Sequence name="3 Fecho" premountFor={fps} {...c(CENAS.fecho)}>
        <Fecho />
      </Sequence>
    </AbsoluteFill>
  );
};
