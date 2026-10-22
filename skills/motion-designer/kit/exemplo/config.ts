/**
 * Tudo que costuma ser editado fica aqui: formato, tempos, textos, cores e a fala.
 * O resto do exemplo só lê este arquivo. Peça fictícia (marca "Trilha", só geometria), 12 s em 9:16.
 */
export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;
export const DURATION = 360; // 12 s

/** Cores da peça (sobre fundo escuro; o destaque é a única cor quente/viva). */
export const PALETA = {
  fundo: "#0E1220",
  fundoClaro: "#161C30",
  tinta: "#F4F6FF",
  suave: "#98A2C3",
  apoio: "#7C8CFF",
  destaque: "#3DDC97",
} as const;

/** Margens seguras para Reels e Stories (px em 1080x1920). Texto importante fica dentro delas. */
export const SAFE = { topo: 270, base: 360, lado: 90 } as const;

export const FONTE = 'Inter, "Segoe UI", system-ui, sans-serif';

export const TEXTOS = {
  gancho: ["Seu pedido", "em três passos."],
  explicacao: "Cada etapa muda o pacote.",
  fecho: "Tudo em um só fluxo.",
  marca: "Trilha",
  aviso: "Peça de exemplo, marca fictícia",
} as const;

/** Início e fim de cada cena, em segundos. */
export const CENAS = {
  gancho: { de: 0, ate: 3 },
  processo: { de: 3, ate: 9 },
  fecho: { de: 9, ate: 12 },
} as const;

/**
 * A fala (ou o roteiro) com o instante em que cada etapa é dita. O movimento é ancorado nestes
 * instantes: o pacote chega à estação um pouco ANTES da palavra e muda de estado NA palavra.
 * Em uma peça real, estes tempos vêm da transcrição da narração.
 */
export const ETAPAS = [
  { palavra: "separa", t: 3.9, y: 760 },
  { palavra: "embala", t: 5.5, y: 1060 },
  { palavra: "envia", t: 7.1, y: 1360 },
] as const;

/** Quadros de antecedência com que o pacote chega antes da palavra. */
export const ANTECEDENCIA = 12;
