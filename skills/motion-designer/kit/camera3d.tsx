/**
 * Câmera 3D dirigida por chaves, mais ambiente e luzes básicas (opcional, só para peças em 3D de verdade).
 * Precisa de: three, @react-three/fiber e @remotion/three. O setup do <ThreeCanvas> está na skill do Remotion.
 * A câmera depende só do frame (sem useFrame), então a prévia e o render mostram a mesma coisa.
 *
 * Uso dentro de <ThreeCanvas>:
 *   <CameraRig keys={CAMERA} />
 *   <Ambiente />
 *   <Luzes />
 */
import React, { useMemo } from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";
import { RoomEnvironment } from "three/examples/jsm/environments/RoomEnvironment.js";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { drift, rad, track, type Vec3 } from "./movimento";

/** Uma chave de câmera em coordenadas esféricas ao redor de um alvo. */
export type CamKey = {
  f: number; // quadro
  az: number; // azimute em graus (0 = de frente, positivo = para a direita)
  el: number; // elevação em graus
  dist: number; // distância do alvo
  t: Vec3; // alvo (para onde a câmera olha)
  fov: number; // campo de visão vertical em graus
  roll?: number; // inclinação em graus
};

/** Estado da câmera num quadro: interpola cada campo das chaves e acrescenta uma tremida mínima no alvo. */
export const camState = (f: number, keys: CamKey[]) => {
  const k = (sel: (c: CamKey) => number) => track(f, keys.map((c) => ({ f: c.f, v: sel(c) })));
  const az = rad(k((c) => c.az));
  const el = rad(k((c) => c.el));
  const dist = k((c) => c.dist);
  const t: Vec3 = [
    k((c) => c.t[0]) + drift(f, 0.011, 0.3) * 0.025,
    k((c) => c.t[1]) + drift(f, 0.013, 1.1) * 0.025,
    k((c) => c.t[2]),
  ];
  const position: Vec3 = [
    t[0] + dist * Math.sin(az) * Math.cos(el),
    t[1] + dist * Math.sin(el),
    t[2] + dist * Math.cos(az) * Math.cos(el),
  ];
  return { position, target: t, fov: k((c) => c.fov), roll: rad(k((c) => c.roll ?? 0)) };
};

/**
 * Câmera guiada pelas chaves. `shiftPx` desloca a lente para subir o assunto até a zona segura
 * (positivo = o assunto sobe), sem mexer na composição.
 */
export const CameraRig: React.FC<{ keys: CamKey[]; shiftPx?: number }> = ({ keys, shiftPx = 0 }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const camera = useThree((s) => s.camera) as THREE.PerspectiveCamera;
  const st = camState(frame, keys);
  camera.up.set(Math.sin(st.roll), Math.cos(st.roll), 0);
  camera.position.set(...st.position);
  camera.fov = st.fov;
  camera.near = 0.08;
  camera.far = 120;
  camera.lookAt(...st.target);
  camera.setViewOffset(width, height, 0, shiftPx, width, height);
  camera.updateProjectionMatrix();
  return null;
};

/** Reflexos suaves de estúdio (ambiente por imagem) e mapeamento de tom neutro, que preserva as cores da paleta. */
export const Ambiente: React.FC<{ intensidade?: number }> = ({ intensidade = 0.85 }) => {
  const gl = useThree((s) => s.gl);
  const scene = useThree((s) => s.scene);
  const env = useMemo(() => {
    const pm = new THREE.PMREMGenerator(gl);
    const rt = pm.fromScene(new RoomEnvironment(), 0.035);
    pm.dispose();
    return rt.texture;
  }, [gl]);
  gl.toneMapping = THREE.NeutralToneMapping;
  gl.toneMappingExposure = 1.0;
  scene.environmentIntensity = intensidade;
  return <primitive object={env} attach="environment" />;
};

/** Uma luz principal com sombra, mais duas luzes de contorno coloridas. Passe as cores da paleta. */
export const Luzes: React.FC<{ cor?: string; contornoA?: string; contornoB?: string }> = ({
  cor = "#FFFFFF",
  contornoA = "#8AA4FF",
  contornoB = "#FFB38A",
}) => {
  const frame = useCurrentFrame();
  const sway = drift(frame, 0.012, 0.4);
  return (
    <>
      <directionalLight
        position={[3.4 + sway * 0.8, 5.4, 10]}
        intensity={2.3}
        color={cor}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-left={-11}
        shadow-camera-right={11}
        shadow-camera-top={11}
        shadow-camera-bottom={-11}
        shadow-camera-near={1}
        shadow-camera-far={45}
        shadow-bias={-0.0004}
        shadow-normalBias={0.02}
      />
      <pointLight position={[-7, 1.5, 6]} intensity={70} color={contornoA} decay={2} />
      <pointLight position={[6, 3.5, -4]} intensity={90} color={contornoB} decay={2} />
    </>
  );
};

/** Piso invisível que só recebe sombra suave (efeito de estúdio). Coloque abaixo do objeto. */
export const PisoDeSombra: React.FC<{ y?: number; opacidade?: number; cor?: string }> = ({
  y = -2.3,
  opacidade = 0.16,
  cor = "#10131c",
}) => (
  <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, y, 0]} receiveShadow>
    <planeGeometry args={[90, 90]} />
    <shadowMaterial transparent opacity={opacidade} color={cor} />
  </mesh>
);
