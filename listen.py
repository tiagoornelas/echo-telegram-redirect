from echo import echo_listen

listen_to = [
  # Mestre Manager
  -1001729121754,
  # Luan FIFA
  -1001858291401,
  # Alertas FIFA
  -1001793865102,
  # Debugger Chat
  -1001660066336
]

# Alertas FIFA
gd_channel_id = 1793865102

# Entradas - Echo Telegram
target_channel = -1001790572391

echo_listen(listen_to, gd_channel_id, target_channel)
