import { continueRender, delayRender, staticFile } from "remotion";
import { PASTA_ASSETS } from "../tipos";

const pedidas = new Set<string>();

const carregar = (familia: string, arquivo: string, peso: string) => {
  if (typeof document === "undefined" || pedidas.has(familia + peso)) return;
  pedidas.add(familia + peso);
  const espera = delayRender(`fonte ${familia} ${peso}`);
  new FontFace(familia, `url(${staticFile(`${PASTA_ASSETS}/fontes/${arquivo}`)}) format("woff2")`, { weight: peso })
    .load()
    .then((f) => document.fonts.add(f))
    .catch((e) => console.error(`Fonte ${familia} não carregou (rode o instalador do kit para copiar public/${PASTA_ASSETS}/fontes):`, e))
    .finally(() => continueRender(espera));
};

/** Carrega as fontes do kit (Montserrat para texto e legenda; Barlow Condensed para manchetes). Chame uma vez, no Root. */
export const carregarFontes = () => {
  carregar("Montserrat", "Montserrat-VF.woff2", "100 900");
  carregar("Barlow Condensed", "BarlowCondensed-Bold.woff2", "700");
  carregar("Barlow Condensed", "BarlowCondensed-ExtraBold.woff2", "800");
};
