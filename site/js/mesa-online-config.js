/*
 * mesa-online-config.js — O projeto do Firebase que guarda a mesa online.
 *
 * Isto NÃO é senha. No Firebase, a configuração do app é pública de propósito: ela vai no
 * site de qualquer um que usa o serviço. Quem protege os dados são as regras do banco
 * (firebase/database.rules.json), que rodam no servidor do Google: só o Mestre lê a parte
 * dele, e cada jogador só lê a própria ficha.
 *
 * Enquanto estiver `null`, a mesa online fica desligada e o site funciona como sempre.
 * Para ligar, siga "Mesa online" em site/LEIA-ME.md e troque o `null` pelo que o Firebase
 * mostrar em Configurações do projeto > Seus apps, assim:
 *
 *   window.EG_MESA_ONLINE = window.EG_MESA_ONLINE || {
 *     apiKey: "...", authDomain: "....firebaseapp.com",
 *     databaseURL: "https://...firebaseio.com", projectId: "...", appId: "...",
 *   };
 */
window.EG_MESA_ONLINE = window.EG_MESA_ONLINE || null;
