import discord


def voice_state_to_string(before_voice_state: discord.VoiceState, after_voice_state: discord.VoiceState):
    global state, channel_name
    if after_voice_state.channel is not None:
        channel_name = after_voice_state.channel.name
    if before_voice_state.deaf and not after_voice_state.deaf:
        state = f'Серверно разглушен\n(Канал: `%{channel_name}`)'
    elif not before_voice_state.deaf and after_voice_state.deaf:
        state = f'Серверно заглушен\n(Канал: `{channel_name}`)'
    elif before_voice_state.mute and not after_voice_state.mute:
        state = f'Серверно размучен\n(Канал: `{channel_name}`)'
    elif not before_voice_state.mute and after_voice_state.mute:
        state = f'Серверно замучен\n(Канал: `{channel_name}`)'
    elif before_voice_state.self_deaf and not after_voice_state.self_deaf:
        state = f'Разглушен\n(Канал: `{channel_name}`)'
    elif not before_voice_state.self_deaf and after_voice_state.self_deaf:
        state = f'Заглушен\n(Канал: `{channel_name}`)'
    elif before_voice_state.self_mute and not after_voice_state.self_mute:
        state = f'Размучен\n(Канал: `{channel_name}`)'
    elif not before_voice_state.self_mute and after_voice_state.self_mute:
        state = f'Замучен\n(Канал: `{channel_name}`)'
    elif before_voice_state.self_stream and not after_voice_state.self_stream:
        state = f'Завершил стрим\n(Канал: `{channel_name}`)'
    elif not before_voice_state.self_stream and after_voice_state.self_stream:
        state = f'Начал стрим\n(Канал: `{channel_name}`)'
    elif before_voice_state.self_video and not after_voice_state.self_video:
        state = f'Завершил видео\n(Канал: `{channel_name}`)'
    elif not before_voice_state.self_video and after_voice_state.self_video:
        state = f'Начал видео\n(Канал: `{channel_name}`)'
    elif before_voice_state.channel is None and after_voice_state.channel is not None:
        state = f'Подключен к каналу `{channel_name}`'
    elif before_voice_state.channel is not None and after_voice_state.channel is None:
        state = f'Отключен от канала `{channel_name}`'
    elif before_voice_state.channel is not None and after_voice_state.channel is not None:
        state = f'Перемещен с канала `{before_voice_state.channel.name}` на канал `{channel_name}`'

    return state


def int_try_parse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if len(a_set.intersection(b_set)) > 0:
        return True
    return False
