from echo import echo_listen

listen_to = [
    # Ornelas Bot
    2022773493,
    # Debugger Chat
    -1001660066336,
]

channel_name_by_id = {2022773493: "Ornelas Bot", 1660066336: "Debugger"}

# Entradas - Echo Telegram
target_channel = -1001790572391

echo_listen(listen_to, channel_name_by_id, target_channel)
