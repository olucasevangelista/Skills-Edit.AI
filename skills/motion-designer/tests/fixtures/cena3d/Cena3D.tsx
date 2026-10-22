import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { Ambiente, CameraRig, Luzes, PisoDeSombra, type CamKey } from "../camera3d";
import { prog } from "../movimento";

/** Cena mínima: um cubo sobre um piso de sombra. A câmera orbita da esquerda para a direita e se aproxima. */
export const CHAVES: CamKey[] = [
  { f: 0, az: -40, el: 8, dist: 12, t: [0, 0, 0], fov: 30 },
  { f: 45, az: 0, el: 6, dist: 9, t: [0, 0, 0], fov: 30 },
  { f: 90, az: 40, el: 8, dist: 6, t: [0, 0, 0], fov: 30 },
];

const Cubo: React.FC = () => {
  const f = useCurrentFrame();
  const s = 0.2 + 0.8 * prog(f, 0, 20);
  return (
    <mesh castShadow position={[0, 0, 0]} scale={s}>
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color="#7C8CFF" roughness={0.35} metalness={0.1} />
    </mesh>
  );
};

export const Cena3D: React.FC = () => {
  const { width, height } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: "#0E1220" }}>
      <ThreeCanvas width={width} height={height} shadows dpr={1} gl={{ antialias: true, alpha: true }} camera={{ fov: 30, position: [0, 0, 12] }}>
        <CameraRig keys={CHAVES} shiftPx={110} />
        <Ambiente />
        <Luzes />
        <PisoDeSombra y={-1.2} />
        <Cubo />
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
