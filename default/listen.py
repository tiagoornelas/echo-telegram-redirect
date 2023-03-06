from echo import echo_listen

listen_to = [
    # Mestre Manager
    -1001729121754,
    # Debugger Chat
    -1001660066336,
]

channel_name_by_id = {2022773493: "Ornelas Bot", 1729121754: "Mestre Manager", 1793865102: "GD", 1660066336: "Debugger"}

# Entradas - Echo Telegram
ornelas_source_channel_id = 2022773493

default_target_channel = -1001790572391
ornelas_target_channel = -1001790572391

echo_listen(listen_to, channel_name_by_id, default_target_channel, ornelas_source_channel_id, ornelas_target_channel)
