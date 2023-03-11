from echo import echo_listen

listen_to = [
    # Ornelas Bot (Tip Manager)
    2022773493,
    # Debugger Chat
    -1001660066336,
]

channel_name_by_id = {2022773493: "Ornelas Bot", 1660066336: "Debugger"}

# Entradas - Ornelas Bot Channel
target_channel = -1001684445367

echo_listen(listen_to, channel_name_by_id, target_channel)
