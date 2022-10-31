from client import client
from telethon.sync import events
from gd.message import format_gd_groups_messages, get_roi_by_group_and_time

listen_to = [
    # GD 12 min
    -1001727812180,
    # GD 10 min
    -1001658824373,
    # GD 8 min
    -1001552985975,
]

# Alertas FIFA
target_channel = -1001793865102

channel_name_by_id = {1727812180: "⏱️ 12 min", 1658824373: "⏱️ 10 min", 1552985975: "⏱️ 8 min"}


def get_channel_name(event):
    try:
        channel_id = event.message.peer_id.channel_id
        return f"{channel_name_by_id[channel_id]}\n\n"
    except:
        return ""


def format_message(event):
    # Return nothing for empty messages (such as images)
    if event.message.message == "":
        return

    # Avoid any checks when attention message
    if "Atentos" in event.message.message:
        return event.message.message

    # Avoid messages without tips
    if "bet365.com" in event.message.message:
        channel_str = get_channel_name(event)
        custom_str = event.message.message.split("💎 Green Diamond 💎")[0]
        return f"{channel_str}{custom_str}"
    else:
        return ""

def format_gd_groups_messages(message):
    eight_min = "⏱️ 8 min"
    ten_min = "⏱️ 10 min"
    twelve_min = "⏱️ 12 min"

    if eight_min in message:
        message_header = f"{eight_min} {get_roi_by_group_and_time(eight_min)}"
        return message.replace(eight_min, message_header)
    if ten_min in message:
        return message.replace(ten_min, get_roi_by_group_and_time(ten_min))
    if twelve_min in message:
        return message.replace(twelve_min, get_roi_by_group_and_time(twelve_min))

client.start()
print("🤫 Silence... Echo is listening!")


@client.on(events.NewMessage(chats=listen_to))
async def main(event):
    try:
        message = format_message(event)
        message_with_roi = format_gd_groups_messages(message, channel_name_by_id[event.message.peer_id.channel_id])
        if message != "":
            await client.send_message(entity=target_channel, message=message_with_roi, link_preview=False)
    except Exception as e:
        print(f"⚠️ Error handled by Echo!\n\n{e}")


client.run_until_disconnected()
