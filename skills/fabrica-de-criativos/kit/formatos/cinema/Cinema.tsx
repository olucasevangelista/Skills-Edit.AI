import React from "react";
import { AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { A, L, LIMITE_BASE, type PropsBase } from "../../tipos";
import { JanelaVideo } from "../../componentes/JanelaVideo";
import { Legenda } from "../../componentes/Legenda";
import { EASE, prog } from "../../componentes/Movimento";
import { Titulo } from "../../componentes/Titulo";

export type PropsCinema = PropsBase & {
  /** a janela do vídeo (padrão 984 x 554, raio 28) */
  janela?: { largura: number; altura: number; raio: number };
  /** tratamento de cor, igual em todo o vídeo */
  tratamento?: { saturacao: number; contraste: number; granulacao?: boolean };
  /** trilha (arquivo em public/) e o volume dela */
  musica?: string;
  volumeMusica?: number;
  /** mostra a legenda (discreta) abaixo da janela */
  legendaAbaixo?: boolean;
};

const GRANULACAO = `url("data:image/svg+xml;utf8,${encodeURIComponent(
  "<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>",
)}")`;

/** 15. Cinema: fundo preto, janela do vídeo com cantos arredondados, título editorial no topo, tratamento de cor e trilha. */
export const Cinema: React.FC<PropsCinema> = ({
  video,
  takes,
  sobreposicaoS,
  legendas,
  titulo,
  cores,
  fonte,
  duracaoS,
  destaques,
  camera,
  janela = { largura: 984, altura: 554, raio: 28 },
  tratamento = { saturacao: 0.9, contraste: 1.08, granulacao: false },
  musica,
  volumeMusica = 0.22,
  legendaAbaixo = false,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const x = (L - janela.largura) / 2;
  const reservaLegenda = legendaAbaixo ? 110 : 0; // a janela sobe para a legenda ficar acima da zona de interface da base
  const y = Math.max(360, Math.min((A - janela.altura) / 2, LIMITE_BASE - janela.altura - reservaLegenda));
  const total = duracaoS * fps;
  const escala = 1 + 0.06 * prog(frame, 0, total, EASE.soft); // zoom muito suave ao longo do vídeo
  const aparece = prog(frame, 0, 18, EASE.soft);
  return (
    <AbsoluteFill style={{ background: "#000000" }}>
      {titulo ? <Titulo texto={titulo.split("\n")} fonte={fonte} cor={cores.texto} y={300} tamanho={72} peso={600} deS={0.3} serifada suave espaco={0.01} /> : null}
      <div style={{ opacity: aparece, transform: `scale(${0.96 + 0.04 * aparece})` }}>
        <JanelaVideo
          src={video}
          takes={takes}
          sobreposicaoS={sobreposicaoS}
          x={x}
          y={y}
          w={janela.largura}
          h={janela.altura}
          raio={janela.raio}
          escala={escala}
          camera={{ push: camera?.push ?? 0.04, punches: camera?.punches ?? [] }}
          filtro={`saturate(${tratamento.saturacao}) contrast(${tratamento.contraste})`}
          sombra="0 30px 80px rgba(0,0,0,0.6)"
        />
        {tratamento.granulacao ? (
          <div
            style={{
              position: "absolute",
              left: x,
              top: y,
              width: janela.largura,
              height: janela.altura,
              borderRadius: janela.raio,
              backgroundImage: GRANULACAO,
              backgroundPosition: `${(frame * 37) % 220}px ${(frame * 53) % 220}px`,
              opacity: 0.08,
              mixBlendMode: "overlay",
              pointerEvents: "none",
            }}
          />
        ) : null}
      </div>
      {legendaAbaixo ? <Legenda legendas={legendas} cores={cores} fonte={fonte} y={y + janela.altura + 44} tamanho={52} destaques={destaques} discreta larguraMax={880} /> : null}
      {musica ? (
        <Audio
          src={staticFile(musica)}
          volume={(f) => {
            const fadeFinal = Math.min(1, Math.max(0, (total - f) / (0.7 * fps)));
            const fadeInicial = Math.min(1, f / (0.5 * fps));
            return volumeMusica * fadeFinal * fadeInicial;
          }}
        />
      ) : null}
    </AbsoluteFill>
  );
};
