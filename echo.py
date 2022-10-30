from client import client
from telethon.sync import events
from message import format_gd_groups_messages


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
        return ""


def echo_listen(from_chats, channel_names_by_id, to_chat):
    client.start()
    print("🤫 Silence... Echo is listening!")

    @client.on(events.NewMessage(chats=from_chats))
    async def main(event):
        try:
            channel_name = get_channel_name(channel_names_by_id, event)
            message = f"{channel_name}: {event.message.message}"

            if message != "":
                await client.send_message(entity=to_chat, message=message, link_preview=False)
        except Exception as e:
            print(f"⚠️ Error handled by Echo!\n\n{e}")

        try:
            if hasattr(event.message, "media"):
                await client.send_message(entity=to_chat, file=event.message.media)
        except:
            print(f"📝 No image sent! Only text echoed!")

    client.run_until_disconnected()
