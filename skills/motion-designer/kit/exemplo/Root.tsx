import React from "react";
import { Composition } from "remotion";
import { Exemplo } from "./Exemplo";
import { DURATION, FPS, HEIGHT, WIDTH } from "./config";

export const RemotionRoot: React.FC = () => (
  <Composition id="Exemplo" component={Exemplo} durationInFrames={DURATION} fps={FPS} width={WIDTH} height={HEIGHT} />
);
