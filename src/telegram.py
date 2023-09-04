import os
import datetime
import asyncio
import random
import inquirer
from telethon.tl import types
from dotenv import load_dotenv
from telethon.sync import events
from telethon.sync import TelegramClient


def log_app_initialization(chat_settings):
    print("Echo Sentinel running...")
    print("Listening to Telegram chats:")
    for chat in chat_settings['source_chats_titles']:
        print(f"-> {chat}")
    print("Sending to chat:")
    print(f"<- {chat_settings['recipient_chat_title']}")
    if chat_settings['should_sanitize']:
        print("Tip Manager's messages sanitizer is enabled")


def log_sent_message(message):
    print(f"{datetime.datetime.utcnow()} - {message}")

def log_error(error):
    print(f"{datetime.datetime.utcnow()} - ERROR: {error}")

def should_block_strategy_by_black_list(message):
    black_list = ["Next Goal"]
    
    try:
        splitted_message = message.split("Estrat")[1].split("gia: ")[1].split("\n")[0]
    except IndexError:
        return False
    
    if any(item in splitted_message for item in black_list):
        return True
    else:
        return False


def get_player_names(message):
    player_names_split_array = message.split(" vs ")
    first_part_player_names_array = player_names_split_array[0].split(" ")
    player_names = first_part_player_names_array[-1] + " vs " + player_names_split_array[1].split(" " or "\n(")[0]
    return player_names

def get_match_time(message):
    return message.split("cio: ")[1].split("\n")[0]

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
        splited_string = message.split("cio: ")[1].split("\n")[0]
        without_timezone_message = sanitize_timezone_string(splited_string)
        return f"às {without_timezone_message}"
    else:
        return "ao-vivo!"

def sanitize_tipmanager_messages(message):
    should_block = should_block_strategy_by_black_list(message)
    if "Poxa, que pena" in message or should_block == True:
        return ""

    match_time = get_match_time(message)
    player_names = get_player_names(message)
    line = get_tip_line(message)
    odd = get_odd(message)
    links = f"[Battle 8'](https://www.bet365.com/#/AC/B1/C1/D1002/E47578773/G938/) | [Adriatic 10'](https://www.bet365.com/#/AC/B1/C1/D1002/E90158949/G938/) | [GT 12'](https://www.bet365.com/#/AC/B1/C1/D1002/E71755872/G938/)"
    message = f"{player_names} {match_time}\n\n{line} @{odd}\n\n{links}"
    return message

def check_edited_message_equality(original, edited):
    return original.split("@")[0] == edited.split("@")[0]

def sanitize_tipmanager_messages_with_results(message):
    match_time = get_match_time(message)
    player_names = get_player_names(message)
    line = get_tip_line(message)
    odd = get_odd(message)
    result = message.split("Resultado")[1].replace("\n", " ")
    message = f"{player_names} {match_time}\n\n{line} @{odd}\n\nPlacar{result}"
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
        inquirer.Confirm('should_sanitize', message="Do you want to sanitize Tip Manager's messages?", default=False),
        inquirer.Confirm('should_send_delayed', message="Do you want to send the same message for another chat with delay?", default=False)
    ]

    answers = inquirer.prompt(questions)
    should_sanitize = answers['should_sanitize']
    should_send_delayed = answers['should_send_delayed']

    source_chats_titles = answers['source']
    recipient_chat_title = answers['recipient']

    source_chats = []
    for chat in source_chats_titles:
        source_chats.append(chat_dict[chat])

    recipient_chat = chat_dict[recipient_chat_title]

    delayed_recipient_chat = None
    delayed_recipient_chat_title = None
    delayed_recipient_delay_time = None

    if should_send_delayed :
        delayed_questions = [
            inquirer.List('delayed_recipient', message='Select delayed recipient chat', choices=chat_choices),
            inquirer.Text('delay_time', message='Type the time in seconds for the delay'),
            inquirer.Text('delay_chance', message='Type the chance on percentage for the message be sent for the delayed chat'),
            inquirer.Text('vip_link', message='Paste the VIP hire link')
        ]
        delayed_answers = answers = inquirer.prompt(delayed_questions)
        delayed_recipient_chat_title = delayed_answers['delayed_recipient']
        delayed_recipient_delay_time = int(delayed_answers['delay_time'])
        delayed_recipient_delay_chance = int(delayed_answers['delay_chance']) * 0.01
        delayed_recipient_vip_link = delayed_answers['vip_link']
        delayed_recipient_chat = chat_dict[delayed_recipient_chat_title]

    return {
        'source_chats': source_chats,
        'source_chats_titles': source_chats_titles,
        'recipient_chat': recipient_chat,
        'recipient_chat_title': recipient_chat_title,
        'should_sanitize': should_sanitize,
        'should_send_delayed': should_send_delayed,
        'delayed_recipient_chat': delayed_recipient_chat,
        'delayed_recipient_chat_title': delayed_recipient_chat_title,
        'delayed_recipient_delay_time': delayed_recipient_delay_time,
        'delayed_recipient_delay_chance': delayed_recipient_delay_chance,
        'delayed_recipient_vip_link': delayed_recipient_vip_link
    }

async def send_delayed_message(message, chat_settings):
    random_number = random.random()
    should_send_delayed_message = random_number >= chat_settings['delayed_recipient_delay_chance']
    if should_send_delayed_message:
        delayed_additional_message = message + '\n\nEsta mensagem foi enviada com ' + str(chat_settings['delayed_recipient_delay_time']) + ' segundos de atraso.\n\n[Assine o VIP](' + chat_settings['delayed_recipient_vip_link'] + ') para receber em tempo real.'
        await asyncio.sleep(chat_settings['delayed_recipient_delay_time'])
        await client.send_message(entity=chat_settings['delayed_recipient_chat'], message=delayed_additional_message, link_preview=False)

load_dotenv()

TELEGRAM_API_ID = os.environ.get('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.environ.get('TELEGRAM_API_HASH')

client = TelegramClient('EchoTel', api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)

client.start()
chat_settings = prompt_for_chat_settings(client)
log_app_initialization(chat_settings)

@client.on(events.NewMessage(chats=chat_settings['source_chats']))
async def handle_new_message(event):
    try:
        message = event.message.message
        if chat_settings['should_sanitize'] == True:
            message = sanitize_tipmanager_messages(message)
        
        log_sent_message(message)
        if event.message.media is None or isinstance(event.message.media, types.MessageMediaWebPage):
            await client.send_message(entity=chat_settings['recipient_chat'], message=message, link_preview=False)
            if chat_settings['should_send_delayed']:
                await send_delayed_message(message, chat_settings)
        else:
            return await client.send_file(entity=chat_settings['recipient_chat'], file=event.message.media, caption=message)
    except Exception as e:
        log_error(e)

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
            
            async for message in client.iter_messages(chat_settings['delayed_recipient_chat'], limit=10):
                found_message = check_edited_message_equality(message.message, sanitized_edited_message)
                if found_message:
                    sanitized_found_message = sanitize_tipmanager_messages_with_results(event.message.message)
                    await client.edit_message(chat_settings['delayed_recipient_chat'], message.id, sanitized_found_message)
                    break

client.run_until_disconnected()
