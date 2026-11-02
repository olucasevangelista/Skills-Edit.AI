import { EASE, prog } from "./Movimento";
import type { Caption, CameraProps, Punch } from "../tipos";

const limpa = (t: string) => t.trim().toLowerCase().replace(/[.,!?;:"'()]/g, "");

/** Escala da câmera no quadro: avanço lento (linear) vezes o maior punch-in ativo. */
export const escalaCamera = (frame: number, fps: number, totalQuadros: number, cam?: CameraProps): number => {
  if (!cam) return 1;
  const lento = 1 + (cam.push ?? 0) * prog(frame, 0, Math.max(1, totalQuadros), (t) => t);
  const punch = (cam.punches ?? []).reduce((m, z) => {
    const de = z.deS * fps;
    const ate = z.ateS * fps;
    const forca = prog(frame, de, de + 5, EASE.out) * (1 - prog(frame, ate - 8, ate, EASE.inOut));
    return Math.max(m, 1 + (z.escala - 1) * forca);
  }, 1);
  return lento * punch;
};

/** Punch-ins nos instantes das palavras de `destaques`, com um intervalo mínimo entre eles para não cansar. */
export const punchesDasPalavras = (legendas: Caption[], destaques: string[] = [], escala = 1.07, duracaoS = 0.9, intervaloMinS = 2.4): Punch[] => {
  const alvo = destaques.map(limpa);
  const punches: Punch[] = [];
  let ultimo = -99;
  for (const w of legendas) {
    if (!alvo.includes(limpa(w.text))) continue;
    const t = w.startMs / 1000;
    if (t - ultimo < intervaloMinS) continue;
    punches.push({ deS: t, ateS: t + duracaoS, escala });
    ultimo = t;
  }
  return punches;
};

/** A câmera padrão dos formatos: avanço lento de 5% e punch-ins nas palavras de destaque (o que a pessoa passar em `camera` vale mais). */
export const cameraDe = (legendas: Caption[], destaques?: string[], camera?: CameraProps): CameraProps => ({
  push: camera?.push ?? 0.05,
  punches: camera?.punches ?? punchesDasPalavras(legendas, destaques),
});
