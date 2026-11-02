import { PASTA_ASSETS } from "./tipos";
import type { Marca } from "./componentes/Marca";

/**
 * Marcas prontas.
 * - `MARCA_CHOQUEI`: o logo da página Choquei (o arquivo vem em `assets/marcas/choquei.png`). É uma marca de TERCEIRO:
 *   o autor da skill informa que a página tolera esse uso, mas isso não foi verificado nem é uma licença. Quem usar responde por isso.
 * - `MARCA_NOTICIA`: um nome fictício de portal de notícias de cidade, sem logo, para o formato Notícia.
 *   O nome não foi pesquisado em registro de marcas: troque por um nome seu se preferir.
 */
export const MARCA_CHOQUEI: Marca = { nome: "Choquei", cor: "#FFD400", logo: `${PASTA_ASSETS}/marcas/choquei.png` };
export const MARCA_NOTICIA: Marca = { nome: "Cidade Hoje", letra: "C", cor: "#D7263D" };
