import difflib
import discord

from embeds.custom_embed import CustomEmbed, EmbedField, EmbedFooter
from utils import colors

# -------Member logs
# Member join embed
def member_join(member: discord.Member):
	return CustomEmbed(title='**Участник подключился к серверу**', color=colors.green, thumbnail_url=member.avatar_url, footer=EmbedFooter(text=f'ID: {member.id}'), fields=[EmbedField(name='Пользователь:', value=f'<@!{member.id}> | {member.name}#{member.discriminator}')])

# Member leave embed
def member_leave(member: discord.Member):
	return CustomEmbed(title='**Участник покинул сервер**', color=colors.red, thumbnail_url=member.avatar_url, footer=EmbedFooter(text=f'ID: {member.id}'), fields=[EmbedField(name='Пользователь:', value=f'<@!{member.id}> | {member.name}#{member.discriminator}')])

# Add role to member embed
def member_role_add(member: discord.Member, role: discord.Role):
	return CustomEmbed(title='**Добавление роли пользователю**', color=colors.green, thumbnail_url=member.avatar_url, footer=EmbedFooter(text=f'ID: {member.id}'), fields=[EmbedField(name='Пользователь:', value=f'<@!{member.id}> | {member.name}#{member.discriminator}'), EmbedField(name='Роль:', value='%s' % role.name)])

# Delete role to member embed
def member_role_delete(member: discord.Member, role: discord.Role):
	return CustomEmbed(title='**Снятие роли с пользователя**', color=colors.red, thumbnail_url=member.avatar_url, footer=EmbedFooter(text=f'ID: {member.id}'), fields=[EmbedField(name='Пользователь:', value=f'<@!{member.id}> | {member.name}#{member.discriminator}'), EmbedField(name='Роль:', value='%s' % role.name)])

# Change member's name
def member_name_change(before_member: discord.Member, after_member: discord.Member):
	return CustomEmbed(title='**Изменение никнейма пользователя**', thumbnail_url=before_member.avatar_url, footer=EmbedFooter(text=f'ID: {before_member.id}'), fields=[EmbedField(name='Пользователь:', value=f'<@!{after_member.id}> | {after_member.name}#{after_member.discriminator}'), EmbedField(name='Предыдущий никнейм:', value=f'{before_member.nick}') if before_member.nick is not None else EmbedField(name='Предыдущий никнейм:', value=f'{before_member.display_name}'), EmbedField(name='Конечный никнейм:', value=f'{after_member.nick}') if after_member.nick is not None else EmbedField(name='Конечный никнейм:', value=f'{after_member.display_name}')])

# Ban member embed
def member_ban(user: discord.User):
	return CustomEmbed(title='**Пользователь забанен**', color=colors.red, thumbnail_url=user.avatar_url, footer=EmbedFooter(text=f'ID: {user.id}'), fields=[EmbedField(name='Пользователь:', value=f'<@!{user.id}> | {user.name}#{user.discriminator}')])

# Unban member embed
def member_unban(user: discord.User):
	return CustomEmbed(title='**Пользователь разбанен**', color=colors.green, thumbnail_url=user.avatar_url, footer=EmbedFooter(text=f'ID: {user.id}'), fields=[EmbedField(name='Пользователь:', value=f'<@!{user.id}> | {user.name}#{user.discriminator}')])

# -------Message logs
# Message edit embed
def message_edit(message: discord.Message, before_message_content: str, after_message_content: str):
	member = message.author
	return CustomEmbed(title='**Изменение сообщения**', thumbnail_url=member.avatar_url, footer=EmbedFooter(text=f'ID: {member.id}'), fields=[EmbedField(name='Пользователь:', value=f'<@!{member.id}> | {member.name}#{member.discriminator}'), EmbedField(name='Канал:', value=f'<#{message.channel.id}>'), EmbedField(name='Сообщение:', value=f'[Нажми на меня]({message.jump_url})'), EmbedField(name='Первоначальное сообщение:', value=before_message_content), EmbedField(name='Конечное сообщение:', value=after_message_content), EmbedField(name='Разница:', value=''.join([li for li in difflib.ndiff(before_message_content, after_message_content) if li[0] != ' ']))])

# Message delete embed
def message_delete(message: discord.Message, message_content: str):
	member = message.author
	return CustomEmbed(title='**Удаление сообщения**', color=colors.red, thumbnail_url=member.avatar_url, footer=EmbedFooter(text=f'ID: {member.id}'), fields=[EmbedField(name='Пользователь:', value=f'<@!{member.id}> | {member.name}#{member.discriminator}'), EmbedField(name='Канал:', value=f'<#{message.channel.id}>'), EmbedField(name='Сообщение:', value=message_content)])

# Message purge embed
def message_purge(member: discord.Member, channel_id: int, purged_messages_number: int):
	return CustomEmbed(title='**Чистка сообщений**', color=colors.red, thumbnail_url=member.avatar_url, footer=EmbedFooter(text=f'ID: {member.id}'), fields=[EmbedField(name='Пользователь:', value=f'<@!{member.id}> | {member.name}#{member.discriminator}'), EmbedField(name='Канал:', value=f'<#{channel_id}>'), EmbedField(name='Количество удаленных сообщений:', value=f'{purged_messages_number}')])

# -------Guild Channel logs
# Text channel create embed
def text_channel_create(channel: discord.TextChannel):
	return CustomEmbed(title='**Создание текстового канала**', color=colors.green, fields=[EmbedField(name='Канал:', value=f'<#{channel.id}>'), EmbedField(name='Название:', value=channel.name)])

# Text channel delete embed
def text_channel_delete(channel: discord.TextChannel):
	return CustomEmbed(title='**Удаление текстового канала**', color=colors.red, fields=[EmbedField(name='Канал:', value=f'<#{channel.id}>'), EmbedField(name='Название:', value=channel.name)])

# Voice channel create embed
def voice_channel_create(channel: discord.VoiceChannel):
	return CustomEmbed(title='**Создание голосового канала**', color=colors.green, fields=[EmbedField(name='Название:', value=channel.name), EmbedField(name='ID:', value=f'{channel.id}')])

# Voice channel delete embed
def voice_channel_delete(channel: discord.VoiceChannel):
	return CustomEmbed(title='**Удаление голосового канала**', color=colors.red, fields=[EmbedField(name='Название:', value=channel.name), EmbedField(name='ID:', value=f'{channel.id}')])

# Category channel create embed
def category_channel_create(channel: discord.CategoryChannel):
	return CustomEmbed(title='**Создание категории**', color=colors.green, fields=[EmbedField(name='Название:', value=channel.name), EmbedField(name='ID:', value=f'{channel.id}')])

# Category channel delete embed
def category_channel_delete(channel: discord.CategoryChannel):
	return CustomEmbed(title='**Удаление категории**', color=colors.red, fields=[EmbedField(name='Название:', value=channel.name), EmbedField(name='ID:', value=f'{channel.id}')])

# -------Role logs
# Role create embed
def role_create(role: discord.Role):
	return CustomEmbed(title='**Создание роли**', color=colors.green, footer=EmbedFooter(text=f'ID: {role.id}'), fields=[EmbedField(name='Название роли:', value=role.name)])

# Role delete embed
def role_delete(role: discord.Role):
	return CustomEmbed(title='**Удаление роли**', color=colors.red, footer=EmbedFooter(text=f'ID: {role.id}'), fields=[EmbedField(name='Название роли:', value=role.name)])

# -------Voice logs
# Voice state update embed
def voice_state_update(member: discord.Member, state: str):
	return CustomEmbed(title='**Обновление голосового статуса**', thumbnail_url=member.avatar_url, fields=[EmbedField(name='Пользователь:', value=f'<@!{member.id}> | {member.name}#{member.discriminator}'), EmbedField(name='Статус:', value=state)])

# -------Reaction logs
# Reaction add embed
def reaction_add(user: discord.User, reaction: discord.Reaction):
	return CustomEmbed(title='**Добавление реакции к сообщению**', color=colors.green, thumbnail_url=user.avatar_url, fields=[EmbedField(name='Пользователь:', value=f'<@!{user.id}> | {user.name}#{user.discriminator}'), EmbedField(name='Канал:', value=f'<#{reaction.message.channel.id}>'), EmbedField(name='Сообщение:', value=f'[Нажми на меня]({reaction.message.jump_url})'), EmbedField(name='Реакция:', value=reaction.emoji)])

# Reaction delete embed
def reaction_remove(user: discord.User, reaction: discord.Reaction):
	return CustomEmbed(title='**Удаление реакции с сообщения**', color=colors.red, thumbnail_url=user.avatar_url, fields=[EmbedField(name='Пользователь:', value=f'<@!{user.id}> | {user.name}#{user.discriminator}'), EmbedField(name='Канал:', value=f'<#{reaction.message.channel.id}>'), EmbedField(name='Сообщение:', value=f'[Нажми на меня]({reaction.message.jump_url})'), EmbedField(name='Реакция:', value=reaction.emoji)])

# Reaction clear embed
def reaction_clear(message: discord.Message, reactions: [discord.Reaction]):
	return CustomEmbed(title='**Очистка реакций с сообщения**', color=colors.red, fields=[EmbedField(name='Канал:', value=f'<#{message.channel.id}>'), EmbedField(name='Сообщение:', value=f'[Нажми на меня]({message.jump_url})'), EmbedField(name='Количество реакций:', value=f'{len(reactions)}'), EmbedField(name='Реакции:', value=''.join([str(reaction.emoji) for reaction in reactions]))])

# -------System logs
def error(event, *args, **kwargs):
	return CustomEmbed(title='**Event raised an uncaught exception**', fields=[EmbedField(name='Event:', value=event), EmbedField(name='Args:', value=f'{args}'), EmbedField(name='Kwargs:', value=f'{kwargs}')], color=colors.red)

def ready():
	return CustomEmbed(title='**Connection completed successfully**', color=colors.green)

def session_confirm_progress():
	return CustomEmbed(title='**Session initialization in progress**', color=colors.yellow)

def session_confirm_success():
	return CustomEmbed(title='**Session initialization completed successfully**', color=colors.green)

def session_confirm_failed():
	return CustomEmbed(title='**Session initialization failed**', color=colors.red)

def session_confirm_blocked():
	return CustomEmbed(title='**Session initialization blocked**', description='A second attempt to initialize and authorize the session will be made after 30 minutes.', color=colors.red)
