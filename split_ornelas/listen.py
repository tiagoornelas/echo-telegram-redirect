from echo import echo_listen

listen_to = [
    # SBP - Staho
    -1001247444492,
    # SBP - Basil
    -1001657959018,
    # SBP
    -1001397538920,
    -1001303952700,
    # Ornelas Bot
    2022773493,
    # Debugger Chat
    -1001660066336,
]

channel_name_by_id = {
    2022773493: "Ornelas Bot",
    1247444492: "SBP - Staho",
    1657959018: "SBP - Basil",
    1397538920: "SBP - Resultados",
    1303952700: "SBP - Anúncios",
    1660066336: "Debugger"
}

# Entradas - Echo Telegram
ornelas_source_channel_id = 2022773493

default_target_channel = -1001790572391
ornelas_target_channel = -1001684445367

echo_listen(listen_to, channel_name_by_id, default_target_channel, ornelas_source_channel_id, ornelas_target_channel)
