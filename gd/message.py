import datetime
import pytz


def get_now_timerange():
    tz_BR = pytz.timezone("America/Sao_Paulo")
    now = datetime.datetime.now(tz_BR).time()

    if now < datetime.datetime(2001, 1, 1, 6, 0, 0).time():
        return "daybreak"
    if now < datetime.datetime(2001, 1, 1, 12, 0, 0).time():
        return "morning"
    if now < datetime.datetime(2001, 1, 1, 18, 0, 0).time():
        return "afternoon"
    return "evening"


def get_roi_by_group_and_time(group_string):
    data = {
        1552985975: {"daybreak": "+3,52% ⛔", "morning": "+1,60% ⛔", "afternoon": "+6,13% ✅", "evening": "+10,70% ⭐"},
        1658824373: {"daybreak": "+4,80% ⛔", "morning": "+4,52% ⛔", "afternoon": "+8,02% ✅", "evening": "+12,09% ⭐"},
        1727812180: {"daybreak": "+11,70% ⭐", "morning": "+8,87% ✅", "afternoon": "+1,32% ⛔", "evening": "+5,30% ✅"},
    }

    current_timerange = get_now_timerange()
    return data[group_string][current_timerange]


def format_gd_groups_messages(event, gd_group_id):
    eight_min = "⏱️ 8 min"
    ten_min = "⏱️ 10 min"
    twelve_min = "⏱️ 12 min"

    if event.message.peer_id.channel_id == gd_group_id:
        if eight_min in event.message.message:
            message_header = f"{eight_min} {get_roi_by_group_and_time(eight_min)}"
            return event.message.message.replace(eight_min, message_header)
        if ten_min in event.message.message:
            return event.message.message.replace(ten_min, get_roi_by_group_and_time(ten_min))
        if twelve_min in event.message.message:
            return event.message.message.replace(twelve_min, get_roi_by_group_and_time(twelve_min))
    else:
        return event.message.message
