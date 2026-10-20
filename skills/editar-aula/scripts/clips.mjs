// Renderiza SO as janelas com motion de uma composição Remotion transparente (sem o vídeo), um clipe por janela.
// O Remotion abre o Chrome e tira um screenshot por quadro; renderizar só as janelas (e não a aula inteira) é o que
// faz a exportação caber em minutos.
//
// Uso:
//   node <skill>/scripts/clips.mjs janelas.json --projeto <pasta do projeto Remotion> --saida clips
//        [--composicao Motions] [--entrada src/index.ts] [--porta 3100] [--rspack] [--concorrencia 50%]
//
// janelas.json (tempos em segundos do VÍDEO LIMPO):
//   [{"nome": "Titulo da aula", "inicio": 1.0, "duracao": 3.0}, {"nome": "Destaque", "inicio": 95.5, "duracao": 2.2}]
//
// Janelas que se sobrepõem (ou encostam) são unidas num único clipe. Sem isso, um motion que coincide com a janela de
// outro apareceria desenhado duas vezes e a transparência somaria.
// Saída: clips/clipNN.mov (ProRes 4444 com transparência) e clips/manifest.json.
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const args = process.argv.slice(2);
const flag = (nome, padrao) => {
  const i = args.indexOf(nome);
  return i >= 0 ? args[i + 1] : padrao;
};
const arquivoJanelas = args.find((a) => !a.startsWith("--") && a.endsWith(".json"));
if (!arquivoJanelas || !flag("--projeto") || !flag("--saida")) {
  console.error("Uso: node clips.mjs janelas.json --projeto <pasta do projeto Remotion> --saida clips [--composicao Motions] [--porta 3100] [--rspack]");
  process.exit(2);
}
const projeto = path.resolve(flag("--projeto"));
const saida = path.resolve(flag("--saida"));
const composicao = flag("--composicao", "Motions");
const entrada = path.resolve(projeto, flag("--entrada", "src/index.ts"));
const porta = Number(flag("--porta", "3100")); // diferente da porta do Studio (3000), senão o render falha
const concorrencia = flag("--concorrencia", "50%");

if (projeto.includes("!")) {
  console.error("O caminho do projeto tem '!' e isso quebra o bundler. Mova o projeto Remotion para uma pasta sem '!'.");
  process.exit(2);
}
const doProjeto = createRequire(path.join(projeto, "package.json"));
let bundle, renderMedia, selectComposition;
try {
  ({ bundle } = doProjeto("@remotion/bundler"));
  ({ renderMedia, selectComposition } = doProjeto("@remotion/renderer"));
} catch (e) {
  console.error(`Nao encontrei o Remotion em ${projeto}. Confira a pasta do projeto (onde esta o package.json) e rode npm install.`);
  process.exit(2);
}

const janelas = JSON.parse(fs.readFileSync(arquivoJanelas, "utf-8"));
if (!Array.isArray(janelas) || janelas.length === 0) {
  console.error("janelas.json esta vazio.");
  process.exit(2);
}
fs.mkdirSync(saida, { recursive: true });

const t0 = Date.now();
const serveUrl = await bundle({
  entryPoint: entrada,
  rootDir: projeto,
  publicDir: path.join(projeto, "public"),
  rspack: args.includes("--rspack"), // a API Node nao le o remotion.config.ts
});
const comp = await selectComposition({ serveUrl, id: composicao, port: porta });
const fps = comp.fps;
const ultimo = comp.durationInFrames - 1;

// janelas -> intervalos de quadros, unidos quando se sobrepõem ou encostam
const quadros = janelas
  .map((j) => {
    const de = Math.max(0, Math.round(j.inicio * fps));
    const ate = Math.min(ultimo, de + Math.max(1, Math.round(j.duracao * fps)) - 1);
    return { de, ate, nomes: [j.nome ?? "motion"] };
  })
  .sort((a, b) => a.de - b.de);
const unidos = [];
for (const q of quadros) {
  const u = unidos[unidos.length - 1];
  if (u && q.de <= u.ate + 1) {
    u.ate = Math.max(u.ate, q.ate);
    u.nomes.push(...q.nomes);
  } else unidos.push({ ...q });
}
console.log(`${janelas.length} janelas -> ${unidos.length} clipes (projeto empacotado em ${((Date.now() - t0) / 1000).toFixed(0)} s)`);

const manifesto = [];
for (const [i, u] of unidos.entries()) {
  const arquivo = path.join(saida, `clip${String(i).padStart(2, "0")}.mov`);
  const inicio = Date.now();
  await renderMedia({
    composition: comp,
    serveUrl,
    codec: "prores",
    proResProfile: "4444",
    pixelFormat: "yuva444p10le",
    imageFormat: "png", // sem PNG nao ha transparencia
    frameRange: [u.de, u.ate], // intervalo INCLUSIVO
    outputLocation: arquivo,
    port: porta,
    concurrency: concorrencia,
    timeoutInMilliseconds: 180000,
  });
  manifesto.push({ arquivo, inicio: u.de / fps, duracao: (u.ate - u.de + 1) / fps, nomes: u.nomes });
  console.log(`[${i + 1}/${unidos.length}] ${path.basename(arquivo)} (${((u.ate - u.de + 1) / fps).toFixed(1)} s) em ${((Date.now() - inicio) / 1000).toFixed(0)} s`);
}
fs.writeFileSync(path.join(saida, "manifest.json"), JSON.stringify(manifesto, null, 1));
console.log(`pronto: ${manifesto.length} clipes em ${saida} (${((Date.now() - t0) / 1000).toFixed(0)} s no total)`);
