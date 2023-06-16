import os
import datetime
import inquirer
from telethon.tl import types
from dotenv import load_dotenv
from telethon.sync import events
from telethon.sync import TelegramClient
from pymongo import MongoClient


def log_app_initialization(chat_settings):
    print("Echo Sentinel running...")
    print("Listening to Telegram chats:")
    for chat in chat_settings['source_chats_titles']:
        print(f"-> {chat}")
    print("Sending to chat:")
    print(f"<- {chat_settings['recipient_chat_title']}")
    if chat_settings['should_sanitize']:
        print("Tip Manager's messages sanitizer is enabled")


def log_sent_message(message, chat_settings):
    print(f"{datetime.datetime.utcnow()} - {message}")
    db.messages.insert_one({
        'from_app': 'Telegram',
        'to_app': 'Telegram',
        'from': chat_settings['source_chats_titles'],
        'to': chat_settings['recipient_chat_title'],
        'message': message,
        'datetime': datetime.datetime.utcnow()
    })

def log_error(message, chat_settings, error):
    print(f"{datetime.datetime.utcnow()} - ERROR: {error}")
    db.errors.insert_one({
        'from_app': 'Telegram',
        'to_app': 'Telegram',
        'from': chat_settings['source_chats_titles'],
        'to': chat_settings['recipient_chat_title'],
        'message': message,
        'error': error,
        'datetime': datetime.datetime.utcnow()
    })

def sanitize_tipmanager_messages(message):
    if "Poxa, que pena" in message:
        return ""
    message = f"{message.replace('tipmanager', 'dataapi')}"
    message = f"{message.split('———')[0]}"
    if 'https://bot.' in message:
        links = f"[Battle 8'](https://www.bet365.com/#/AC/B1/C1/D1002/E47578773/G938/) | [Adriatic 10'](https://www.bet365.com/#/AC/B1/C1/D1002/E90158949/G938/) | [GT 12'](https://www.bet365.com/#/AC/B1/C1/D1002/E71755872/G938/)"
        message = f"{message.split('https://bot.')[0]}{links}"
    return message

def prompt_for_chat_settings(client):
    chats = client.iter_dialogs()
    chat_dict = {}
    for chat in chats:
        chat_dict[chat.title] = chat.id
    chat_choices = [chat.title for chat in chats]

    questions = [
        inquirer.Checkbox('source', message='Select source chats', choices=chat_choices),
        inquirer.List('recipient', message='Select recipient chat', choices=chat_choices),
        inquirer.Confirm('should_sanitize', message="Do you want to sanitize Tip Manager's messages?", default=False)
    ]

    answers = inquirer.prompt(questions)
    should_sanitize = answers['should_sanitize']

    source_chats_titles = answers['source']
    recipient_chat_title = answers['recipient']

    source_chats = []
    for chat in source_chats_titles:
        source_chats.append(chat_dict[chat])

    recipient_chat = chat_dict[recipient_chat_title]

    return {
        'source_chats': source_chats,
        'source_chats_titles': source_chats_titles,
        'recipient_chat': recipient_chat,
        'recipient_chat_title': recipient_chat_title,
        'should_sanitize': should_sanitize
    }

load_dotenv()

MONGO_URL = os.environ.get('MONGO_URL')

mongo = MongoClient(MONGO_URL)
db = mongo['data']

TELEGRAM_API_ID = os.environ.get('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.environ.get('TELEGRAM_API_HASH')

client = TelegramClient('EchoTel', api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)

client.start()
chat_settings = prompt_for_chat_settings(client)
log_app_initialization(chat_settings)

@client.on(events.NewMessage(chats=chat_settings['source_chats']))
async def main(event):
    try:
        message = event.message.message
        if chat_settings['should_sanitize'] == True:
            message = sanitize_tipmanager_messages(message)
        
        log_sent_message(message, chat_settings)
        if event.message.media is None or isinstance(event.message.media, types.MessageMediaWebPage):
            await client.send_message(entity=chat_settings['recipient_chat'], message=message, link_preview=False)
        else:
            return await client.send_file(entity=chat_settings['recipient_chat'], file=event.message.media, caption=message)
    except Exception as e:
        log_error(event.message.message, chat_settings, e)

client.run_until_disconnected()
