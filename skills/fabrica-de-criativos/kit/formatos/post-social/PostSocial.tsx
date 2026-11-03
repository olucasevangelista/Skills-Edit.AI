import React from "react";
import { AbsoluteFill } from "remotion";
import { A, L, SEGURA, type PropsBase } from "../../tipos";
import { JanelaVideo } from "../../componentes/JanelaVideo";
import { Avatar, type Marca } from "../../componentes/Marca";

export type Midia = {
  /** arquivo em public/ (vídeo ou imagem) */
  src: string;
  /** só uma mídia toca o áudio; se nenhuma estiver marcada, é a primeira */
  audio?: boolean;
  /** ponto do enquadramento (CSS object-position), por exemplo "50% 30%" */
  origem?: string;
  escala?: number;
  fit?: "cover" | "contain";
};

export type PropsPostSocial = Omit<PropsBase, "video" | "takes" | "sobreposicaoS" | "titulo"> & {
  /** o perfil do post: o SEU perfil ou marca (nome e logo próprios) */
  marca: Marca;
  /** a frase de impacto do post, até ~4 linhas; use o que o vídeo sustenta */
  texto: string;
  /** uma mídia (tela cheia), duas lado a lado, ou vídeo e imagem */
  midia: Midia[];
  fundoCartao?: "claro" | "escuro";
  /** altura do cartão em px; se omitida, é calculada pelo tamanho do texto */
  alturaCartao?: number;
};

const CORPO = 46;
const LINHA = Math.round(CORPO * 1.3);
const LARGURA_TEXTO = L - SEGURA.lado - SEGURA.ladoDireito;
const AVATAR = 92;

/** Estimativa conservadora da altura do cartão: o topo respeita a zona segura e o texto ocupa até onde for preciso. */
export const alturaDoCartao = (texto: string): number => {
  const porLinha = Math.floor(LARGURA_TEXTO / (CORPO * 0.56));
  const linhas = Math.min(5, Math.max(1, Math.ceil(texto.length / porLinha)));
  return SEGURA.topo + 20 + AVATAR + 26 + linhas * LINHA + 34;
};

/** 03. Post de Rede Social: cartão do perfil com a frase de impacto em cima; a mídia (um vídeo, dois vídeos ou vídeo e imagem) embaixo. */
export const PostSocial: React.FC<PropsPostSocial> = ({ marca, texto, midia, fundoCartao = "claro", alturaCartao, fonte, children }) => {
  const claro = fundoCartao === "claro";
  const altura = alturaCartao ?? alturaDoCartao(texto);
  const itens = midia.slice(0, 2);
  const comAudio = itens.some((m) => m.audio) ? itens.findIndex((m) => m.audio) : 0;
  const largura = itens.length === 2 ? (L - 6) / 2 : L;
  return (
    <AbsoluteFill style={{ background: "#000000", fontFamily: fonte }}>
      {itens.map((m, i) => (
        <JanelaVideo key={i} src={m.src} x={i * (largura + 6)} y={altura} w={largura} h={A - altura} origem={m.origem ?? "50% 40%"} escala={m.escala} fit={m.fit} muted={i !== comAudio} />
      ))}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: L,
          height: altura,
          background: claro ? "#FFFFFF" : "#15191F",
          boxShadow: "0 6px 24px rgba(0,0,0,0.35)",
        }}
      >
        <div style={{ position: "absolute", left: SEGURA.lado, top: SEGURA.topo + 20, display: "flex", alignItems: "center", gap: 24 }}>
          <Avatar marca={marca} tamanho={AVATAR} fonte={fonte} />
          <div style={{ color: claro ? "#0F1419" : "#F2F4F7", fontWeight: 800, fontSize: 46, letterSpacing: 0.5, textTransform: "uppercase" }}>{marca.nome}</div>
        </div>
        <div
          style={{
            position: "absolute",
            left: SEGURA.lado,
            top: SEGURA.topo + 20 + AVATAR + 26,
            width: LARGURA_TEXTO,
            color: claro ? "#0F1419" : "#F2F4F7",
            fontSize: CORPO,
            lineHeight: `${LINHA}px`,
            fontWeight: 500,
          }}
        >
          {texto}
        </div>
      </div>
      {children}
    </AbsoluteFill>
  );
};
