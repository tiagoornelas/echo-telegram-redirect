from client import client
from telethon.sync import events
from telethon.tl import types
from message import format_gd_groups_messages, get_roi_by_group_and_time

listen_to = [
    # GD 12 min
    -1001727812180,
    # GD 10 min
    -1001658824373,
    # GD 8 min
    -1001552985975,
    # Debugger,
    # -1001660066336
]

# GD FIFA
target_channel = -1001793865102

channel_name_by_id = {1727812180: "⏱️12", 1658824373: "⏱️10", 1552985975: "⏱️8"}

results_link_by_id = {
    1727812180: "https://www.totalcorner.com/league/view/12985",
    1658824373: "https://www.totalcorner.com/league/view/13321",
    1552985975: "https://www.totalcorner.com/league/view/12995",
}


def get_channel_name(event):
    try:
        channel_id = event.message.peer_id.channel_id
        return channel_name_by_id[channel_id]
    except:
        return ""


def format_attention_message(event):
    eight_min = 1552985975
    ten_min = 1658824373
    twelve_min = 1727812180

    channel_name = get_channel_name(event)

    if event.message.peer_id.channel_id == eight_min:
        return f"💎 Atentos 💎\n\n{channel_name}: {get_roi_by_group_and_time(eight_min)}"
    if event.message.peer_id.channel_id == ten_min:
        return f"💎 Atentos 💎\n\n{channel_name}: {get_roi_by_group_and_time(ten_min)}"
    if event.message.peer_id.channel_id == twelve_min:
        return f"💎 Atentos 💎\n\n{channel_name}: {get_roi_by_group_and_time(twelve_min)}"


def format_message(event):
    # Specific logic for attention messages
    if "Atentos" in event.message.message:
        return format_attention_message(event)

    channel_str = get_channel_name(event)
    # Specific logic for tip messages
    if "bet365.com" in event.message.message:
        custom_str = event.message.message.split("💎 Green Diamond 💎")[0]
        result_str = f"ℹ [Resultados]({results_link_by_id[event.message.peer_id.channel_id]})"
        return f"{channel_str}: {custom_str}{result_str}"
    else:
        # Checks for empty messages to avoid ":" after channel name when only images is sent
        if event.message.message != "":
            return f"{channel_str}: {event.message.message}"
        else:
            return channel_str


client.start()
print("🤫 Silence... Echo is listening!")


@client.on(events.NewMessage(chats=listen_to))
async def main(event):
    try:
        message = format_message(event)
        # Sends text only when there is no image
        if event.message.media is None or isinstance(event.message.media, types.MessageMediaWebPage):
            return await client.send_message(entity=target_channel, message=message, link_preview=False)
        # Sends image with caption
        else:
            return await client.send_file(entity=target_channel, file=event.message.media, caption=message)
    except Exception as e:
        print(f"⚠️ Error handled by Echo!\n\n{e}")


client.run_until_disconnected()
