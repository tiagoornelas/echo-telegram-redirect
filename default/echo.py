from client import client
from telethon.tl import types
from telethon.sync import events


def echo_list_chats():
    client.start()
    print("🔍 Echo is looking for your chats...")
    for dialog in client.iter_dialogs():
        print(f"ID: {dialog.id} Name: {dialog.name}")


def get_channel_name(channel_names_by_id, event):
    try:
        channel_id = event.message.peer_id.channel_id
        return channel_names_by_id[channel_id]
    except:
        print(event.message)
        chat_id = event.message.chat_id
        try:
            return channel_names_by_id[chat_id]
        except:
            return ""


def echo_listen(from_chats, channel_names_by_id, to_chat):
    client.start()
    print("🤫 Silence... Echo is listening!")

    @client.on(events.NewMessage(chats=from_chats))
    async def main(event):
        try:
            channel_name = get_channel_name(channel_names_by_id, event)
            message = f"{channel_name}: {event.message.message}"

            if "tipmanager.net" in message:
                message = f"{message.split('———')[0]}"
            # Sends text only when there is no image
            if event.message.media is None or isinstance(event.message.media, types.MessageMediaWebPage):
                await client.send_message(entity=to_chat, message=message, link_preview=False)
            # Sends image with caption
            else:
                return await client.send_file(entity=to_chat, file=event.message.media, caption=message)
        except Exception as e:
            print(f"⚠️ Error handled by Echo!\n\n{e}")

    client.run_until_disconnected()
