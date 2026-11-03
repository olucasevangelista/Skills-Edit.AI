/**
 * Props de exemplo de cada composição. Servem de MODELO: troque os arquivos (em public/), os textos, as cores e os tempos.
 * Os nomes de arquivo abaixo são os que o verificador do kit gera para testar.
 */
import { CORES_PADRAO, FONTE_PADRAO } from "../tipos";
import { MARCA_CHOQUEI, MARCA_NOTICIA } from "../marcas";
import type { PropsAntesDepois } from "../formatos/antes-depois/AntesDepois";
import type { PropsChat } from "../formatos/chat/Chat";
import type { PropsCinema } from "../formatos/cinema/Cinema";
import type { PropsDepoimento } from "../formatos/depoimento/Depoimento";
import type { PropsNoticia } from "../formatos/noticia/Noticia";
import type { PropsPostSocial } from "../formatos/post-social/PostSocial";
import type { PropsReact } from "../formatos/react/React";
import type { PropsTelaDividida } from "../formatos/tela-dividida/TelaDividida";

const BASE = { cores: CORES_PADRAO, fonte: FONTE_PADRAO, duracaoS: 8 };

export const propsTelaDividida: PropsTelaDividida = {
  ...BASE,
  video: "pessoa.mp4",
  titulo: "SEU RESULTADO\nEM MINUTOS",
  conteudoSuperior: [
    { src: "conteudo1.png", tipo: "imagem", deS: 0.2, ateS: 3.2 },
    { src: "conteudo2.png", tipo: "imagem", deS: 3.2, ateS: 6 },
    { src: "conteudo3.mp4", tipo: "video", deS: 6, ateS: 8 },
  ],
};

export const propsCinema: PropsCinema = {
  ...BASE,
  duracaoS: 6,
  video: "pessoa.mp4",
  titulo: "Nem tudo se resolve\nde um dia para o outro",
  musica: "musica.wav",
};

export const propsReact: PropsReact = {
  ...BASE,
  video: "reacao.mp4",
  conteudo: "conteudo3.mp4",
  titulo: "OLHA O QUE\nELES DISSERAM",
  rotuloOrigem: "vídeo original",
  pausas: [{ deS: 2, ateS: 3.5 }],
  ampliacoes: [{ deS: 4.5, ateS: 6 }],
};

export const propsAntesDepois: PropsAntesDepois = {
  ...BASE,
  antes: "antes.png",
  depois: "depois.png",
  titulo: "A DIFERENÇA\nÉ VISÍVEL",
  modo: "deslize",
  revelarEmS: 2,
  duracaoRevelacaoS: 2,
};

export const propsChat: PropsChat = {
  cores: CORES_PADRAO,
  fonte: FONTE_PADRAO,
  duracaoS: 9,
  contato: { nome: "Atendimento", status: "online" },
  avisoDramatizacao: "Dramatização",
  mensagens: [
    { de: "outro", texto: "Oi! Vi que você tem uma dúvida sobre o plano.", tempoS: 0.6 },
    { de: "eu", texto: "Tenho sim: quanto tempo leva para começar?", tempoS: 2.4 },
    { de: "outro", texto: "Em poucos minutos. Quer que eu mostre o passo a passo?", tempoS: 4.4, digitandoS: 1.2 },
    { de: "eu", texto: "Quero!", tempoS: 6.4 },
  ],
};

export const propsDepoimento: PropsDepoimento = {
  ...BASE,
  video: "pessoa.mp4",
  titulo: "ELE CONTA\nO QUE MUDOU",
  identificacao: { nome: "Nome autorizado", descricao: "cliente" },
  inserts: [{ src: "prova.png", deS: 3, ateS: 5, legenda: "resultado real, autorizado" }],
  zooms: [{ deS: 1.5, ateS: 2.6, escala: 1.16 }],
};

/** A marca é a Choquei pronta do kit; troque por um perfil seu quando quiser. O texto deve ser uma frase que o vídeo sustenta. */
export const propsPostSocial: PropsPostSocial = {
  ...BASE,
  marca: MARCA_CHOQUEI,
  texto: "ATENÇÃO! Escreva aqui a frase de impacto do post, em até quatro linhas, com o que o vídeo mostra de verdade.",
  midia: [{ src: "pessoa.mp4", audio: true }, { src: "reacao.mp4" }],
};

/** A marca é o veículo fictício "Cidade Hoje"; as manchetes devem ser fatos verdadeiros que o anúncio sustenta. */
export const propsNoticia: PropsNoticia = {
  ...BASE,
  video: "pessoa.mp4",
  marca: MARCA_NOTICIA,
  manchetes: [
    { texto: "Escreva aqui a manchete verdadeira do seu anúncio", deS: 0.5, ateS: 4 },
    { texto: "Segunda manchete, se o vídeo pedir", deS: 5, ateS: 7.5 },
  ],
};
