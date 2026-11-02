import React from "react";
import { Composition } from "remotion";
import { A, FPS, L } from "./tipos";
import { carregarFontes } from "./componentes/Fontes";
import { propsAntesDepois, propsChat, propsCinema, propsDepoimento, propsNoticia, propsPostSocial, propsReact, propsTelaDividida } from "./exemplo/props";
import { AntesDepois } from "./formatos/antes-depois/AntesDepois";
import { Chat } from "./formatos/chat/Chat";
import { Cinema } from "./formatos/cinema/Cinema";
import { Depoimento } from "./formatos/depoimento/Depoimento";
import { Noticia } from "./formatos/noticia/Noticia";
import { PostSocial } from "./formatos/post-social/PostSocial";
import { React_ } from "./formatos/react/React";
import { TelaDividida } from "./formatos/tela-dividida/TelaDividida";

carregarFontes();

/** A duração de cada composição vem do prop `duracaoS`: troque o prop (ou o arquivo de props) e o vídeo muda de tamanho. */
const meta = ({ props }: { props: { duracaoS: number } }) => ({ durationInFrames: Math.max(1, Math.round(props.duracaoS * FPS)) });

export const Raiz: React.FC = () => (
  <>
    <Composition id="TelaDividida" component={TelaDividida} width={L} height={A} fps={FPS} durationInFrames={FPS * 8} defaultProps={propsTelaDividida} calculateMetadata={meta} />
    <Composition id="Cinema" component={Cinema} width={L} height={A} fps={FPS} durationInFrames={FPS * 6} defaultProps={propsCinema} calculateMetadata={meta} />
    <Composition id="React" component={React_} width={L} height={A} fps={FPS} durationInFrames={FPS * 8} defaultProps={propsReact} calculateMetadata={meta} />
    <Composition id="AntesDepois" component={AntesDepois} width={L} height={A} fps={FPS} durationInFrames={FPS * 8} defaultProps={propsAntesDepois} calculateMetadata={meta} />
    <Composition id="Chat" component={Chat} width={L} height={A} fps={FPS} durationInFrames={FPS * 9} defaultProps={propsChat} calculateMetadata={meta} />
    <Composition id="Depoimento" component={Depoimento} width={L} height={A} fps={FPS} durationInFrames={FPS * 8} defaultProps={propsDepoimento} calculateMetadata={meta} />
    <Composition id="PostSocial" component={PostSocial} width={L} height={A} fps={FPS} durationInFrames={FPS * 8} defaultProps={propsPostSocial} calculateMetadata={meta} />
    <Composition id="Noticia" component={Noticia} width={L} height={A} fps={FPS} durationInFrames={FPS * 8} defaultProps={propsNoticia} calculateMetadata={meta} />
  </>
);
