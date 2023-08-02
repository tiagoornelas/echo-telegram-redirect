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

def get_player_names(message):
    player_names_split_array = message.split(" vs ")
    first_part_player_names_array = player_names_split_array[0].split(" ")
    player_names = first_part_player_names_array[-1] + " vs " + player_names_split_array[1].split(" " or "\n(")[0]
    return player_names

def get_odd(message):
    return message.split("@")[1].split("\n")[0]

def get_tip_line(message):
    if "PRE-LIVE" in message:
        if "Over" in message or "Under" in message:
            line_array = message.split(" @")[0].split(" ")[-3:]
            line = f"{line_array[0]} {line_array[2]}".replace("\n\n", "")
            return line
        else:
            return message.split(" @")[0].split("\n\n")[-1]
    else:
        return message.split(" @")[0].replace("Jogador - ", "")

def sanitize_timezone_string(message):
    return message.replace("(America/Sao_Paulo)", "")

def get_match_time(message):
    if "cio: " in message:
        splitted_message = message.split("cio: ")[1].split("\n")[0]
        without_timezone_message = sanitize_timezone_string(splitted_message)
        return without_timezone_message
    else:
        return "Live"
    
def get_strategy(message):
    return message.split("gia: ")[1].split("\n\n")[0]

def sanitize_tipmanager_messages(message):
    if "Poxa, que pena" in message:
        return ""
    match_time = get_match_time(message)
    player_names = get_player_names(message)
    line = get_tip_line(message)
    odd = get_odd(message)
    strategy = get_strategy(message)
    message = f"{match_time} - {player_names} - {line} @{odd}\n\n{strategy}"
    return message

def check_edited_message_equality(original, edited):
    return original.split("@")[0] == edited.split("@")[0]

def sanitize_tipmanager_messages_with_results(message):
    match_time = get_match_time(message)
    player_names = get_player_names(message)
    line = get_tip_line(message)
    odd = get_odd(message)
    strategy = get_strategy(message)
    result = message.split("Resultado: ")[1].replace("\n", " ")
    message = f"{match_time} - {player_names} - {line} @{odd}\n\n{strategy}\n\n{result}"
    return message

def check_edited_message_equality(original, edited):
    return original.split("@")[0] == edited.split("@")[0]

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

TELEGRAM_API_ID = os.environ.get('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.environ.get('TELEGRAM_API_HASH')

client = TelegramClient('EchoTel', api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)

client.start()
chat_settings = prompt_for_chat_settings(client)
log_app_initialization(chat_settings)

@client.on(events.NewMessage(chats=chat_settings['source_chats']))
async def handle_new_message(event):
    message = event.message.message
    if chat_settings['should_sanitize'] == True:
        message = sanitize_tipmanager_messages(message)
    
    print(message, chat_settings)
    try:
        message = event.message.message
        if chat_settings['should_sanitize'] == True:
            message = sanitize_tipmanager_messages(message)
        
        print(message, chat_settings)
        if event.message.media is None or isinstance(event.message.media, types.MessageMediaWebPage):
            await client.send_message(entity=chat_settings['recipient_chat'], message=message, link_preview=False)
        else:
            return await client.send_file(entity=chat_settings['recipient_chat'], file=event.message.media, caption=message)
    except Exception as e:
        print(event.message.message, chat_settings, e)

@client.on(events.MessageEdited(chats=chat_settings['source_chats']))
async def handle_message_edit(event):
    if chat_settings['should_sanitize'] == True:
        if "Resultado" in event.message.message:
            sanitized_edited_message = sanitize_tipmanager_messages(event.message.message)
            async for message in client.iter_messages(chat_settings['recipient_chat']):
                found_message = check_edited_message_equality(message.message, sanitized_edited_message)
                if found_message:
                    sanitized_found_message = sanitize_tipmanager_messages_with_results(event.message.message)
                    await client.edit_message(chat_settings['recipient_chat'], message.id, sanitized_found_message)
                    break

client.run_until_disconnected()
