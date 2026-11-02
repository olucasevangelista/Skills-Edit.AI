/** Tipos e constantes compartilhados pelas composições do kit. */

/** Uma palavra da legenda, no formato do `legendas.remotion.json` gerado pela transcrição (mesmo formato `Caption` do Remotion). */
export type Caption = {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs: number | null;
  confidence: number | null;
};

export type Cores = {
  fundo: string;
  texto: string;
  destaque: string;
  apoio: string;
};

/** Um trecho de um vídeo-fonte, em segundos. Vários trechos viram uma sequência com emenda por sobreposição. */
export type Take = { src: string; deS: number; ateS: number };

/** Zoom rápido de ênfase (punch-in): entra em ~5 quadros e volta ao normal. */
export type Punch = { deS: number; ateS: number; escala: number };

/** Movimento de câmera sobre o vídeo da pessoa: um avanço lento e punch-ins nas palavras de destaque. */
export type CameraProps = {
  /** quanto o vídeo cresce ao longo do trecho (0,05 = 5%); padrão 0,05; 0 desliga */
  push?: number;
  /** punch-ins; se omitido, saem automaticamente nas palavras de `destaques` */
  punches?: Punch[];
};

/** Props que todas as composições aceitam. */
export type PropsBase = {
  /** vídeo principal (nome do arquivo em public/) */
  video?: string;
  /** emendas: se houver, substitui `video` por uma sequência de trechos com sobreposição de imagem e áudio */
  takes?: Take[];
  /** sobreposição das emendas, em segundos (0,1 a 0,25) */
  sobreposicaoS?: number;
  legendas: Caption[];
  titulo?: string;
  cores: Cores;
  /** família de fonte já carregada no projeto */
  fonte: string;
  duracaoS: number;
  /** palavras que recebem o realce na legenda (minúsculas, sem pontuação) */
  destaques?: string[];
  /** movimento de câmera sobre o vídeo da pessoa (padrão: avanço lento e punch-ins nos destaques) */
  camera?: CameraProps;
};

export const L = 1080;
export const A = 1920;
export const FPS = 30;

/** Zonas seguras (pontos de partida conservadores; confirme na plataforma): texto e rosto ficam dentro. */
export const SEGURA = { topo: 270, base: 670, lado: 90, ladoDireito: 120 } as const;
/** Linha (y) a partir da qual começa a zona de interface da base. */
export const LIMITE_BASE = A - SEGURA.base;

export const CORES_PADRAO: Cores = {
  fundo: "#0E1220",
  texto: "#FFFFFF",
  destaque: "#3DDC97",
  apoio: "#7C8CFF",
};

/** Fontes do kit: carregadas de `public/fabrica/fontes/` (veja `componentes/Fontes.ts`); as seguintes são o plano B do sistema. */
export const FONTE_PADRAO = 'Montserrat, "Segoe UI", system-ui, sans-serif';
export const FONTE_MANCHETE = '"Barlow Condensed", "Arial Narrow", "Segoe UI", sans-serif';

/** Pasta (dentro de `public/`) onde o instalador copia fontes e marcas. */
export const PASTA_ASSETS = "fabrica";
