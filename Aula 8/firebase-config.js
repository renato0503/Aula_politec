/* =====================================================================
   Configuração do Firebase compartilhada pela fase de ideação.
   Usado pelo formulário (Aula 8/formulario-ideacao.html), pelo hub
   (Aula 8/index.html) e pela página de cada app (Aula 8/app.html).

   O projeto esta no plano Spark: usa apenas o Firestore. Os arquivos
   enviados pela turma sao gravados como documentos na colecao
   `ideacao_arquivos`, com o conteudo em base64. O limite do Firestore e
   de 1 MiB por documento, entao cada arquivo aceito tem no maximo 600 KB.

   O modulo tenta carregar o SDK pela CDN em varias versoes, para nao
   quebrar quando o Google publicar uma nova. Se nenhuma carregar, o
   formulario continua funcionando offline: ele salva no navegador e
   exporta o arquivo .json, e o envio ao Firestore fica desligado.
   ===================================================================== */

export const firebaseConfig = {
  apiKey: "AIzaSyBmMTIdsrY7sfzgmzzz_5wcaDa0p8kIgVg",
  authDomain: "aulapolitec.firebaseapp.com",
  projectId: "aulapolitec",
  storageBucket: "aulapolitec.firebasestorage.app",
  messagingSenderId: "197369546553",
  appId: "1:197369546553:web:6a791877082d82c9690ae8",
  measurementId: "G-2V4EMHX17Y"
};

const VERSOES = ["11.10.0", "12.0.0", "11.6.0", "10.12.5"];
const BASE = "https://www.gstatic.com/firebasejs";

let modulos = null;
let erro = "";

async function carregar(v) {
  const [appMod, fs, auth] = await Promise.all([
    import(`${BASE}/${v}/firebase-app.js`),
    import(`${BASE}/${v}/firebase-firestore.js`),
    import(`${BASE}/${v}/firebase-auth.js`)
  ]);
  const app = appMod.initializeApp(firebaseConfig);
  return {
    app: app,
    fs: fs,
    auth: auth,
    db: fs.getFirestore(app),
    versao: v
  };
}

export async function iniciarFirebase() {
  if (modulos) return modulos;
  if (erro) throw new Error(erro);
  for (const v of VERSOES) {
    try {
      modulos = await carregar(v);
      window.__firebaseErro = "";
      return modulos;
    } catch (e) {
      erro = e.message || String(e);
    }
  }
  window.__firebaseErro = erro;
  throw new Error("Não foi possível carregar o SDK do Firebase: " + erro);
}

export function firebaseDisponivel() {
  return !!modulos;
}

export const COLECAO = "ideacao";
export const COLECAO_ARQUIVOS = "ideacao_arquivos";
export const LIMITE_ARQUIVO = 600 * 1024; /* Firestore aceita 1 MiB por documento; o base64 pesa 33% */
