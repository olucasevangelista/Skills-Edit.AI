import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { L, SEGURA, type Cores } from "../../tipos";
import { EASE, pop, prog } from "../../componentes/Movimento";

export type Mensagem = {
  de: "eu" | "outro";
  texto?: string;
  imagem?: string;
  /** instante em que a mensagem aparece */
  tempoS: number;
  /** quanto tempo o "digitando..." aparece antes (só nas mensagens de "outro") */
  digitandoS?: number;
};

export type PropsChat = {
  cores: Cores;
  fonte: string;
  duracaoS: number;
  /** contato fictício (ou o do anunciante): sem nome real de pessoa */
  contato: { nome: string; status?: string };
  mensagens: Mensagem[];
  /** aviso de dramatização, obrigatório quando a conversa é encenada */
  avisoDramatizacao?: string;
  narracao?: string;
  tema?: "claro" | "escuro";
  /** camadas por cima (por exemplo, a legenda) */
  children?: React.ReactNode;
};

const AREA = { y: 454, h: 786 };
const BALAO = { larguraMax: 690, padX: 30, padY: 22, corpo: 46, folga: 16 };

const estimaAltura = (m: Mensagem): number => {
  if (m.imagem) return 360 + BALAO.padY * 2 + BALAO.folga + (m.texto ? 70 : 0);
  const cpl = Math.floor((BALAO.larguraMax - 2 * BALAO.padX) / (BALAO.corpo * 0.54));
  const linhas = Math.max(1, Math.ceil((m.texto ?? "").length / cpl));
  return linhas * BALAO.corpo * 1.3 + BALAO.padY * 2 + BALAO.folga;
};

const Digitando: React.FC<{ frame: number; fundo: string }> = ({ frame, fundo }) => (
  <div style={{ alignSelf: "flex-start", background: fundo, borderRadius: 30, padding: "24px 32px", display: "flex", gap: 10, marginBottom: BALAO.folga }}>
    {[0, 1, 2].map((i) => (
      <div key={i} style={{ width: 16, height: 16, borderRadius: 8, background: "#8A8F98", opacity: 0.45 + 0.55 * Math.max(0, Math.sin(frame * 0.35 - i * 0.9)) }} />
    ))}
  </div>
);

/** 13. Conversa de Chat: balões que surgem em sequência, "digitando...", rolagem e destaque. Interface genérica e dramatização identificada. */
export const Chat: React.FC<PropsChat> = ({ cores, fonte, contato, mensagens, avisoDramatizacao = "Dramatização", narracao, tema = "escuro", children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const escuro = tema === "escuro";
  const fundo = escuro ? "#0F141B" : "#ECE9E2";
  const cabecalho = escuro ? "#161D27" : "#F7F5F0";
  const corTexto = escuro ? "#F2F4F7" : "#111418";
  const recebido = escuro ? "#222B37" : "#FFFFFF";
  const enviado = cores.apoio;
  const visiveis = mensagens.filter((m) => m.tempoS <= t).sort((a, b) => a.tempoS - b.tempoS);
  const ultima = visiveis[visiveis.length - 1];
  const idade = ultima ? (t - ultima.tempoS) * fps : 99;
  const empurrao = ultima ? estimaAltura(ultima) * (1 - prog(idade, 0, 8, EASE.out)) : 0;
  const digitando = mensagens.find((m) => m.de === "outro" && m.digitandoS && t >= m.tempoS - m.digitandoS && t < m.tempoS);
  return (
    <AbsoluteFill style={{ background: fundo, fontFamily: fonte }}>
      {/* cabeçalho genérico */}
      <div style={{ position: "absolute", left: SEGURA.lado, top: 270, width: L - SEGURA.lado - SEGURA.ladoDireito, height: 132, background: cabecalho, borderRadius: 32, display: "flex", alignItems: "center", padding: "0 36px", gap: 24, boxShadow: "0 6px 20px rgba(0,0,0,0.25)" }}>
        <div style={{ width: 84, height: 84, borderRadius: 42, background: cores.destaque, color: "#06210F", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 800, fontSize: 40 }}>{contato.nome.slice(0, 1).toUpperCase()}</div>
        <div>
          <div style={{ color: corTexto, fontWeight: 700, fontSize: 44 }}>{contato.nome}</div>
          {contato.status ? <div style={{ color: escuro ? "#9AA4B2" : "#5B6470", fontSize: 30 }}>{contato.status}</div> : null}
        </div>
      </div>
      {/* conversa: ancorada embaixo; as mensagens antigas sobem quando chega uma nova */}
      <div style={{ position: "absolute", left: 0, top: AREA.y, width: L, height: AREA.h, overflow: "hidden" }}>
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, padding: `0 ${SEGURA.ladoDireito}px 0 ${SEGURA.lado}px`, display: "flex", flexDirection: "column", justifyContent: "flex-end", transform: `translateY(${empurrao}px)` }}>
          {visiveis.map((m, i) => {
            const idadeQ = (t - m.tempoS) * fps;
            const p = Math.max(0, Math.min(1.08, pop(idadeQ, fps, 0, 14, 130)));
            const meu = m.de === "eu";
            const destaque = m === ultima && idadeQ < 18 ? 1 : 0;
            return (
              <div
                key={i}
                style={{
                  alignSelf: meu ? "flex-end" : "flex-start",
                  maxWidth: BALAO.larguraMax,
                  background: meu ? enviado : recebido,
                  color: meu ? "#FFFFFF" : corTexto,
                  borderRadius: 32,
                  borderBottomRightRadius: meu ? 8 : 32,
                  borderBottomLeftRadius: meu ? 32 : 8,
                  padding: `${BALAO.padY}px ${BALAO.padX}px`,
                  marginBottom: BALAO.folga,
                  fontSize: BALAO.corpo,
                  lineHeight: 1.3,
                  fontWeight: 500,
                  transform: `scale(${0.85 + 0.15 * Math.min(1, p)})`,
                  transformOrigin: meu ? "100% 100%" : "0% 100%",
                  opacity: Math.min(1, p * 1.4),
                  boxShadow: destaque ? `0 0 0 4px ${cores.destaque}` : "0 4px 12px rgba(0,0,0,0.22)",
                }}
              >
                {m.imagem ? <Img src={staticFile(m.imagem)} style={{ width: 600, height: 360, objectFit: "cover", borderRadius: 18, display: "block", marginBottom: m.texto ? 14 : 0 }} /> : null}
                {m.texto}
              </div>
            );
          })}
          {digitando ? <Digitando frame={frame} fundo={recebido} /> : null}
        </div>
      </div>
      <div style={{ position: "absolute", left: SEGURA.lado, right: SEGURA.ladoDireito, top: 408, textAlign: "center", color: escuro ? "#8FA0B3" : "#5B6470", fontSize: 28, fontWeight: 600, letterSpacing: 1 }}>{avisoDramatizacao}</div>
      {narracao ? <Audio src={staticFile(narracao)} /> : null}
      {children}
    </AbsoluteFill>
  );
};
