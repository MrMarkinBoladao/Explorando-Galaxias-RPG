/*
 * mesa-online-config.js — O projeto do Firebase que guarda a mesa online.
 *
 * Isto NÃO é senha. No Firebase, a configuração do app é pública de propósito: ela vai no
 * site de qualquer um que usa o serviço. Quem protege os dados são as regras do banco
 * (firebase/database.rules.json), que rodam no servidor do Google: só o Mestre lê a parte
 * dele, e cada jogador só lê a própria ficha.
 *
 * Para desligar a mesa online, troque o objeto abaixo por `null`: o site volta a funcionar
 * só no navegador de cada um, como antes. Para trocar de projeto, cole aqui o firebaseConfig
 * de Configurações do projeto > Seus apps (o passo a passo está em site/LEIA-ME.md).
 * Quem já definiu `window.EG_MESA_ONLINE` antes deste arquivo (os testes, com o emulador do
 * Firebase, ou `null` para testar o site sem a mesa) não é sobrescrito.
 */
if (window.EG_MESA_ONLINE === undefined) {
  window.EG_MESA_ONLINE = {
    apiKey: "AIzaSyBSeDRndx340SHY38APvKHowycS7E1r_Is",
    authDomain: "explorando-galaxias-rpg.firebaseapp.com",
    databaseURL: "https://explorando-galaxias-rpg-default-rtdb.firebaseio.com",
    projectId: "explorando-galaxias-rpg",
    storageBucket: "explorando-galaxias-rpg.firebasestorage.app",
    messagingSenderId: "274403955725",
    appId: "1:274403955725:web:7778c1c15438954625f144",
  };
}
