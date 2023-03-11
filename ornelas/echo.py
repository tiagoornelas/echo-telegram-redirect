from client import client
from telethon.tl import types
from telethon.sync import events


def echo_list_chats():
    client.start()
    print("🔍 Echo is looking for your chats...")
    for dialog in client.iter_dialogs():
        print(f"ID: {dialog.id} Name: {dialog.name}")


def echo_listen(from_chats, channel_names_by_id, to_chat):
    client.start()
    print("🤫 Silence... Echo is listening!")

    @client.on(events.NewMessage(chats=from_chats))
    async def main(event):
        try:
            message = event.message.message

            # Splits Tip Managers default footer
            # Sanitizes any messages to avoid leaking Tip Manager data sourcing
            if "tipmanager" in message:
                message = f"{message.replace('tipmanager', 'dataapi')}"
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
