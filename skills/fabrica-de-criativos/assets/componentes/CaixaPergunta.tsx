/**
 * Caixinha de pergunta (estilo de story): cabeçalho escuro com "Faça uma pergunta" e corpo claro com a pergunta.
 *
 * É uma PEÇA PARA REAPROVEITAR no seu projeto Remotion (copie o arquivo e ajuste o que precisar), não um editor:
 * a composição, os cortes, a legenda e o resto do vídeo continuam sendo seus. Só depende do `remotion`.
 *
 * Dois modos de texto:
 * - "digitado": as palavras aparecem no instante em que são faladas (passe `palavras` com o tempo de cada uma, vindo da
 *   transcrição) ou, sem `palavras`, o texto é digitado de forma uniforme; cursor piscando.
 * - "fixo": o texto já aparece inteiro (o formato mais comum do Instagram).
 *
 * Todo movimento é função do quadro (sem CSS animation nem timers), como o Remotion exige.
 * Use dentro de uma <Sequence>, ou passe `deS`/`ateS` em segundos a partir do começo da composição.
 */
import React from "react";
import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export type PalavraFalada = { /** a palavra como será escrita */ p: string; /** instante em que é falada, em segundos */ s: number };

export type PropsCaixaPergunta = {
  /** o texto da pergunta */
  texto: string;
  modo?: "digitado" | "fixo";
  /** modo digitado: o tempo de cada palavra (da transcrição). Se omitido, digita de forma uniforme */
  palavras?: PalavraFalada[];
  /** modo digitado sem `palavras`: quanto tempo leva para digitar tudo (s) */
  duracaoDigitandoS?: number;
  /** instante em que a caixinha entra (s) */
  deS?: number;
  /** instante em que ela começa a sair (s); se omitido, fica na tela */
  ateS?: number;
  /** texto do cabeçalho */
  titulo?: string;
  /**
   * posição e largura no quadro (padrão para 1080x1920: centrada, topo em 220).
   * Direção: a caixinha fica SEMPRE no alto (é a primeira coisa que a pessoa vê ao escanear o vídeo), sem colar na margem
   * nem correr o risco de ser cortada. Pense no cartão JÁ COM O TEXTO COMPLETO (ele cresce para baixo enquanto digita):
   * o ideal é que a borda de baixo termine antes das sobrancelhas; cobrir até ~70% da testa é tranquilo, e cobrir mais
   * só se não houver espaço. Ajuste `y` olhando um quadro com o texto inteiro.
   */
  x?: number;
  y?: number;
  largura?: number;
  /** escurecimento do vídeo atrás enquanto a caixinha está na tela (0 a 0,5) */
  veu?: number;
  fonte?: string;
  /** cores do cartão (o padrão imita a caixinha do story) */
  corCabecalho?: string;
  corCorpo?: string;
  corTexto?: string;
};

const palavrasUniformes = (texto: string, deS: number, duracao: number): PalavraFalada[] => {
  const ps = texto.split(/\s+/).filter(Boolean);
  return ps.map((p, i) => ({ p, s: deS + (duracao * i) / Math.max(1, ps.length) }));
};

/** O texto digitado até o instante t: cada palavra vai sendo escrita a partir do seu instante. */
const textoAte = (t: number, palavras: PalavraFalada[], fimS: number): string => {
  let saida = "";
  palavras.forEach((w, i) => {
    if (t < w.s) return;
    const fim = i + 1 < palavras.length ? palavras[i + 1].s : fimS;
    const frac = Math.min(1, (t - w.s) / Math.max(0.12, (fim - w.s) * 0.8));
    saida += (saida ? " " : "") + w.p.slice(0, Math.max(1, Math.ceil(w.p.length * frac)));
  });
  return saida;
};

export const CaixaPergunta: React.FC<PropsCaixaPergunta> = ({
  texto,
  modo = "digitado",
  palavras,
  duracaoDigitandoS = 2.4,
  deS = 0.3,
  ateS,
  titulo = "Faça uma pergunta",
  x,
  y = 220,
  largura = 780,
  veu = 0.28,
  fonte = 'system-ui, "Segoe UI", Arial, sans-serif',
  corCabecalho = "#0B0B0E",
  corCorpo = "#FFFFFF",
  corTexto = "#111114",
}) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const t = frame / fps;

  const entra = interpolate(t, [deS, deS + 0.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(1.9)) });
  const sai = ateS === undefined ? 0 : interpolate(t, [ateS, ateS + 0.45], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  if (t < deS - 0.01 || sai >= 1) return null;

  const ps = palavras ?? palavrasUniformes(texto, deS + 0.4, duracaoDigitandoS);
  const fimDigitacao = ps.length ? ps[ps.length - 1].s + 0.5 : deS;
  const escrito = modo === "fixo" ? texto : textoAte(t, ps, fimDigitacao);
  const cursor = modo === "digitado" && Math.floor(t * 2.4) % 2 === 0 && t < fimDigitacao + 0.4;
  const opacidade = Math.min(1, Math.max(0, entra) * 3) * (1 - sai);

  return (
    <>
      {/* véu leve: o vídeo fica um pouco mais escuro atrás da caixinha */}
      <div style={{ position: "absolute", inset: 0, background: `rgba(0,0,0,${veu})`, opacity: Math.min(1, entra * 2) * (1 - sai) }} />
      <div
        style={{
          position: "absolute",
          left: x ?? (width - largura) / 2,
          top: y,
          width: largura,
          opacity: opacidade,
          scale: String((0.7 + 0.3 * Math.max(0, entra)) * (1 - 0.06 * sai)),
          rotate: `${(1 - Math.min(1, entra)) * -3}deg`,
          translate: `0px ${-sai * 60}px`,
          filter: "drop-shadow(0 30px 60px rgba(0,0,0,0.45))",
          fontFamily: fonte,
        }}
      >
        <div style={{ height: 112, borderRadius: "38px 38px 0 0", background: corCabecalho, display: "flex", alignItems: "center", justifyContent: "center", color: "#FFFFFF", fontWeight: 600, fontSize: 38, letterSpacing: "-0.01em" }}>{titulo}</div>
        <div style={{ minHeight: 210, borderRadius: "0 0 38px 38px", background: corCorpo, padding: "40px 46px 54px", textAlign: "center", color: corTexto, fontWeight: 500, fontSize: 46, lineHeight: 1.28, letterSpacing: "-0.015em" }}>
          {escrito}
          {modo === "digitado" ? <span style={{ display: "inline-block", width: 4, height: 50, background: cursor ? corTexto : "transparent", marginLeft: 4, translate: "0px 9px" }} /> : null}
        </div>
      </div>
    </>
  );
};
