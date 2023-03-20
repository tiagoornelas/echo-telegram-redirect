require("dotenv").config();
const TeleBot = require("telebot");
const inquirer = require("inquirer");
const wa = require("@open-wa/wa-automate");
const MongoClient = require("mongodb").MongoClient;

const MONGO_DB = "data";
const MONGO_URL = process.env.MONGO_URL;
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_RECIPIENT_CHAT_ID = process.env.TELEGRAM_RECIPIENT_CHAT_ID;

const mongoConnection = () => {
  return MongoClient.connect(MONGO_URL, {
    useNewUrlParser: true,
    useUnifiedTopology: true
  })
    .then(conn => conn.db(MONGO_DB))
    .catch(err => {
      console.error(err);
      process.exit(1);
    });
};

const logSentMessage = (message, chatSettings) =>
  mongoConnection().then(db =>
    db.collection("messages").insertOne({
      from_app: "Whatsapp",
      to_app: "Telegram",
      from: chatSettings.sourceChat,
      to: TELEGRAM_RECIPIENT_CHAT_ID,
      bot_token: TELEGRAM_BOT_TOKEN,
      message: message.text,
      datetime: new Date()
    })
  );

const logError = error =>
  mongoConnection().then(db =>
    db.collection("errors").insertOne({
      from_app: "Whatsapp",
      to_app: "Telegram",
      error: error,
      datetime: new Date()
    })
  );

const telegramBot = new TeleBot(TELEGRAM_BOT_TOKEN);
telegramBot.start();

wa.create({
  sessionId: "ECHO_TEL",
  multiDevice: true,
  authTimeout: 60,
  blockCrashLogs: true,
  disableSpins: true,
  headless: true,
  hostNotificationLang: "PT_BR",
  logConsole: false,
  popup: true,
  qrTimeout: 0
}).then(waClient => start(waClient));

function logAppInitialization(chatSettings) {
  console.log("Echo Sentinel running...");
  console.log("Listening to Whatsapp chat:");
  console.log(`-> ${chatSettings.sourceChat}`);
}

async function start(waClient) {
  try {
    const chats = await waClient.getAllChats();

    const whatsappChats = {
      array: [],
      dict: {}
    };

    chats.forEach(chat => {
      whatsappChats.array.push(chat.formattedTitle);
      whatsappChats.dict[chat.formattedTitle] = chat.id;
    });

    inquirer
      .prompt([
        {
          type: "list",
          message: "Select source chats",
          name: "source",
          choices: whatsappChats.array
        }
      ])
      .then(answers => {
        const chatSettings = {
          sourceChat: whatsappChats.dict[answers.source],
          sourceChatTitle: whatsappChats.array.find(chat => chat.id === whatsappChats.dict[answers.source])
        };

        logAppInitialization(chatSettings);

        waClient.onMessage(async message => {
          if (message.chatId === chatSettings.sourceChat) {
            if (message.mimetype && message.mimetype.includes("image")) {
              logSentMessage(message, chatSettings);
              const mediaData = await wa.decryptMedia(message);
              telegramBot.sendPhoto(TELEGRAM_RECIPIENT_CHAT_ID, mediaData, { caption: message.text });
            } else if (message.text) {
              logSentMessage(message, chatSettings);
              telegramBot.sendMessage(TELEGRAM_RECIPIENT_CHAT_ID, message.text);
            }
          }
        });
      })
      .catch(err => {
        logError(err);
      });
  } catch (err) {
    logError(err);
  }
}
