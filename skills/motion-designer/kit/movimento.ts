/**
 * Kit de movimento (opcional). Copie este arquivo para o projeto Remotion e importe dele.
 * Tudo aqui é função pura do frame: o mesmo frame dá sempre o mesmo resultado, em qualquer ordem de renderização.
 * Nada de CSS animation, transition, timers ou useFrame como relógio.
 */
import { Easing, interpolate, spring } from "remotion";

export type Vec3 = [number, number, number];
export type Key<T> = { f: number; v: T };

export const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const lerp3 = (a: readonly number[], b: readonly number[], t: number): Vec3 => [
  lerp(a[0], b[0], t),
  lerp(a[1], b[1], t),
  lerp(a[2], b[2], t),
];
export const rad = (deg: number) => (deg * Math.PI) / 180;

/** Segundos para quadros (arredondado). */
export const sec = (s: number, fps: number) => Math.round(s * fps);

/** Curvas de aceleração. `out` freia no fim (entradas), `in` acelera (saídas), `inOut` é a padrão. */
export const EASE = {
  inOut: Easing.bezier(0.65, 0, 0.35, 1),
  out: Easing.bezier(0.16, 1, 0.3, 1),
  in: Easing.bezier(0.55, 0, 0.9, 0.4),
  soft: Easing.bezier(0.45, 0, 0.2, 1),
};

/** Progresso de 0 a 1 entre dois quadros, com curva. Fica em 0 antes e em 1 depois. */
export const prog = (
  frame: number,
  from: number,
  to: number,
  easing: (t: number) => number = EASE.inOut,
) =>
  interpolate(frame, [from, to], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing,
  });

/** Entrada com leve overshoot (mola amortecida): sai de 0, passa um pouco de 1 e assenta em 1. */
export const pop = (frame: number, fps: number, start: number, damping = 13, stiffness = 110) =>
  spring({ frame: frame - start, fps, config: { damping, stiffness, mass: 0.9 } });

/**
 * Curva suave por chaves (cúbica monótona, PCHIP): velocidade contínua entre as chaves, sem overshoot,
 * parada suave nas pontas. Serve para câmera, rotação e posição de objetos que não podem "tremer".
 * As chaves precisam estar em ordem crescente de `f`.
 */
export function track(frame: number, keys: Key<number>[]): number {
  const n = keys.length;
  if (n === 0) throw new Error("track: precisa de pelo menos uma chave");
  if (frame <= keys[0].f) return keys[0].v;
  if (frame >= keys[n - 1].f) return keys[n - 1].v;
  let i = 0;
  while (frame > keys[i + 1].f) i++;
  const k0 = keys[i];
  const k1 = keys[i + 1];
  const h = k1.f - k0.f;
  const t = (frame - k0.f) / h;
  const slope = (a: Key<number>, b: Key<number>) => (b.v - a.v) / (b.f - a.f);
  const tangent = (idx: number) => {
    if (idx <= 0 || idx >= n - 1) return 0;
    const sPrev = slope(keys[idx - 1], keys[idx]);
    const sNext = slope(keys[idx], keys[idx + 1]);
    if (sPrev * sNext <= 0) return 0;
    return (2 * sPrev * sNext) / (sPrev + sNext);
  };
  const m0 = tangent(i);
  const m1 = tangent(i + 1);
  const t2 = t * t;
  const t3 = t2 * t;
  return (
    (2 * t3 - 3 * t2 + 1) * k0.v +
    (t3 - 2 * t2 + t) * h * m0 +
    (-2 * t3 + 3 * t2) * k1.v +
    (t3 - t2) * h * m1
  );
}

/** Flutuação suave e determinística (-1 a 1), para dar vida a um objeto parado. Use amplitude pequena. */
export const drift = (frame: number, speed: number, phase = 0) =>
  Math.sin(frame * speed + phase) * 0.6 + Math.sin(frame * speed * 0.47 + phase * 1.7) * 0.4;

/**
 * Impacto de squash e stretch: devolve a escala [x, y] de um objeto que "bate" no quadro `at`.
 * Achata no eixo y e alarga no x, e assenta em 1 em cerca de meio segundo.
 */
export const squash = (frame: number, at: number, amount = 0.07): [number, number] => {
  if (frame < at) return [1, 1];
  const t = frame - at;
  const bump = Math.exp(-t / 7) * Math.sin(t * 0.85);
  return [1 + amount * 0.5 * bump, 1 - amount * bump];
};
