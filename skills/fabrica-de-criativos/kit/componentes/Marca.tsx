import React from "react";
import { Img, staticFile } from "remotion";
import { L, SEGURA } from "../tipos";

/** A marca de quem anuncia: o nome do perfil ou do veículo PRÓPRIO, com o logo (arquivo em public/) ou só a letra e a cor. */
export type Marca = {
  nome: string;
  /** letra do avatar e do logotipo quando não há `logo` (padrão: a primeira letra do nome) */
  letra?: string;
  cor: string;
  /** arquivo de logo em public/ (PNG, de preferência com fundo transparente) */
  logo?: string;
};

/** Avatar redondo do perfil: o logo, ou a letra sobre a cor da marca. */
export const Avatar: React.FC<{ marca: Marca; tamanho: number; fonte: string }> = ({ marca, tamanho, fonte }) =>
  marca.logo ? (
    <Img src={staticFile(marca.logo)} style={{ width: tamanho, height: tamanho, borderRadius: tamanho / 2, objectFit: "cover", display: "block" }} />
  ) : (
    <div
      style={{
        width: tamanho,
        height: tamanho,
        borderRadius: tamanho / 2,
        background: marca.cor,
        color: "#FFFFFF",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: fonte,
        fontWeight: 800,
        fontSize: tamanho * 0.5,
      }}
    >
      {(marca.letra ?? marca.nome).slice(0, 1).toUpperCase()}
    </div>
  );

/** Logotipo para o topo de um vídeo de notícia: o logo, ou um quadrado com a letra ao lado do nome em caixa alta. */
export const Logotipo: React.FC<{ marca: Marca; fonte: string; y: number; posicao?: "centro" | "esq"; altura?: number }> = ({ marca, fonte, y, posicao = "centro", altura = 84 }) => (
  <div
    style={{
      position: "absolute",
      top: y,
      left: posicao === "esq" ? SEGURA.lado : 0,
      width: posicao === "esq" ? undefined : L,
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      gap: 18,
      filter: "drop-shadow(0 4px 14px rgba(0,0,0,0.55))",
    }}
  >
    {marca.logo ? (
      <Img src={staticFile(marca.logo)} style={{ height: altura, maxWidth: 520, objectFit: "contain", display: "block" }} />
    ) : (
      <>
        <div
          style={{
            width: altura,
            height: altura,
            background: marca.cor,
            color: "#FFFFFF",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontFamily: fonte,
            fontWeight: 900,
            fontSize: altura * 0.72,
          }}
        >
          {(marca.letra ?? marca.nome).slice(0, 1).toUpperCase()}
        </div>
        <div style={{ color: "#FFFFFF", fontFamily: fonte, fontWeight: 800, fontSize: altura * 0.58, letterSpacing: altura * 0.07, textTransform: "uppercase" }}>{marca.nome}</div>
      </>
    )}
  </div>
);
