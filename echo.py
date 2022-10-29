from client import client
from telethon.sync import events
from message import format_gd_groups_messages

def echo_list_chats():
    client.start()
    print("🔍 Echo is looking for your chats...")
    for dialog in client.iter_dialogs():
            print(f"ID: {dialog.id} Name: {dialog.name}")


def echo_listen(from_chats, gd_chat, to_chat):
    client.start()
    print("🤫 Silence... Echo is listening!")
    @client.on(events.NewMessage(chats=from_chats))
    async def main(event):
        try:
            message = format_gd_groups_messages(event, gd_chat)
            if message != "":
                await client.send_message(entity=to_chat, message=message, link_preview=False)
        except Exception as e:
            print(f"⚠️ Error handled by Echo!\n\n{e}")

    client.run_until_disconnected()
