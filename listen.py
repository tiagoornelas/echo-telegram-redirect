from echo import echo_listen

listen_to = [
    # Mestre Manager
    -1001729121754,
    # Alertas FIFA
    -1001793865102,
    # Debugger Chat
    -1001660066336,
]

channel_name_by_id = {1729121754: "Mestre Manager", 1793865102: "GD", 1660066336: "Debugger"}

# Entradas - Echo Telegram
target_channel = -1001790572391

echo_listen(listen_to, channel_name_by_id, target_channel)
