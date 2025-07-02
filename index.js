
import makeWASocket, { useMultiFileAuthState, DisconnectReason } from '@whiskeysockets/baileys'; import qrcode from 'qrcode-terminal'; import express from 'express'; import dotenv from 'dotenv'; import fs from 'fs'; import { Configuration, OpenAIApi } from 'openai';

// Load env dotenv.config();

const app = express(); const PORT = process.env.PORT || 3000;

// Initialize OpenRouter/OpenAI API const configuration = new Configuration({ apiKey: process.env.OPENROUTER_API_KEY }); const openai = new OpenAIApi(configuration);

let sock;

// Serve connection page app.get('/', (req, res) => { res.send(<html> <body style="font-family: sans-serif; text-align: center;"> <h1>Connect your WhatsApp to <strong>Adam_D'H7</strong></h1> <div id="qr"></div> <script> const evtSource = new EventSource('/events'); evtSource.onmessage = e => { if (e.data.startsWith('QR:')) { document.getElementById('qr').innerHTML = '<img src="' + e.data.split('QR:')[1] + '"/>'; } else if (e.data.startsWith('CODE:')) { document.getElementById('qr').innerHTML = '<h2>Your link code: ' + e.data.split('CODE:')[1] + '</h2>'; } }; </script> </body> </html>); });

// SSE for QR and code app.get('/events', (req, res) => { res.set({ 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' }); sock.ev.on('connection.update', update => { const { qr, connection } = update; if (qr) { qrcode.generate(qr, { small: true }, qrString => { const imgData = 'data:image/png;base64,' + require('qrcode').toDataURL(qr); res.write(data: QR:${imgData}\n\n); }); } if (connection === 'open') { // generate 8-digit code const code = Math.floor(10000000 + Math.random() * 90000000).toString(); res.write(data: CODE:${code}\n\n); } }); });

// Start express app.listen(PORT, () => { console.log(Server running on http://localhost:${PORT}); });

// Initialize WhatsApp connection async function startSock() { const { state, saveCreds } = await useMultiFileAuthState(process.env.SESSION_FILE); sock = makeWASocket({ auth: state, printQRInTerminal: false });

sock.ev.on('creds.update', saveCreds);

sock.ev.on('messages.upsert', async ({ messages }) => { const msg = messages[0]; if (!msg.message || msg.key.fromMe) return;

const text = msg.message.conversation || msg.message.extendedTextMessage?.text;
const chatId = msg.key.remoteJid;

// Send typing indicator
await sock.presenceSubscribe(chatId);
sock.sendPresenceUpdate('composing', chatId);

// Query OpenRouter
const response = await openai.createChatCompletion({
  model: 'gpt-3.5-turbo',
  messages: [{ role: 'system', content: "You are Adam_D'H7, temperamental like Snober but helpful." },
             { role: 'user', content: text }]
});
const reply = response.data.choices[0].message.content;

// Send reply
await sock.sendMessage(chatId, { text: reply });
sock.sendPresenceUpdate('paused', chatId);

});

sock.ev.on('connection.update', update => { const { connection, lastDisconnect } = update; if (connection === 'close') { const reason = lastDisconnect.error?.output?.statusCode; console.log('Disconnected', reason); startSock(); } }); }

startSock();


