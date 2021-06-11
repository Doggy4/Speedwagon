from channels import channels
from embeds.custom_embed import CustomEmbed, EmbedAuthor, EmbedField, EmbedFooter
from utils import images, colors
from utils import structures

# Avatar embed
def avatar(image_url, author_avatar, name, discriminator):
	return CustomEmbed(title='**Аватар**', image_url=image_url, author=EmbedAuthor(name=f'{name}#{discriminator}', icon_url=author_avatar))

# Monitoring embed
def monitoring(data: structures.MonitoringStructure):
	embed = CustomEmbed(title='**Мониторинг серверов**', author=EmbedAuthor(name='Excalibur-Craft Data', icon_url=images.EX_CRAFT_LOGO), thumbnail_url=images.MONITORING_THUMBNAIL, fields=[EmbedField(name='**Общий онлайн**', value=f'{data.total_online} игроков')])
	for server in data.servers:
		embed.add_field(name=f'**{server.name}**', value=f'{server.online} игроков')

	return embed

# Votes embed
def votes(data: structures.VoteStructure):
	embed = CustomEmbed(title='**Топ по количеству голосов**', author=EmbedAuthor(name='Excalibur-Craft Data', icon_url=images.EX_CRAFT_LOGO), thumbnail_url=images.VOTE_THUMBNAIL, color=0xffb136)
	for _player in data.players:
		embed.add_field(name=f'**{_player.place} место**', value=_player.nickname)

	return embed

# Online embed
def online(data: structures.OnlineStructure):
	embed = CustomEmbed(title='**Топ по количеству голосов**', author=EmbedAuthor(name='Excalibur-Craft Data', icon_url=images.EX_CRAFT_LOGO), thumbnail_url=images.ONLINE_THUMBNAIL, color=0xdbdbdb)
	for _player in data.players:
		embed.add_field(name=f'**{_player.nickname}**', value=_player.online)

	return embed

# Player embed
def player(data: structures.PlayerStructure):
	return CustomEmbed(title=f'**Информация об игроке {data.nickname}**', author=EmbedAuthor(name='Excalibur-Craft Data', icon_url=images.EX_CRAFT_LOGO), thumbnail_url=data.thumbnail, image_url=data.image_url, fields=[EmbedField(name='**Дата регистрации:**', value=data.registration_date), EmbedField(name='**Часов в игре за месяц:**', value=f'{data.monthly_online}'), EmbedField(name='**Часов в игре за все время:**', value=f'{data.all_time_online}'), EmbedField(name='**Статус в игре:**', value=data.status), EmbedField(name='**Клан:**', value=f'{data.clan}\n\n**Скин и плащ**', inline=False) if data.has_cape else EmbedField(name='**Клан:**', value=f'{data.clan}\n\n**Скин**')])

# Clan embed
def clan(data: structures.ClanStructure):
	return CustomEmbed(title=f'**Информация о клане {data.name}**', author=EmbedAuthor(name='Excalibur-Craft Data', icon_url=images.EX_CRAFT_LOGO), thumbnail_url=data.thumbnail, fields=[EmbedField(name="**Девиз клана:**", value=data.motto), EmbedField(name="**Место в топе:**", value=f'{data.top_place}'), EmbedField(name="**Место в рейтинге:**", value=f'{data.rating_place}'), EmbedField(name="**Голосов:**", value=f'{data.votes}'), EmbedField(name="**Опыт:**", value=f'{data.experience}'), EmbedField(name="**Игроков:**", value=f'{data.players}'), EmbedField(name="**Средний онлайн за всё время:**", value=f'{data.all_time_online}'), EmbedField(name="**Средний онлайн за месяц:**", value=f'{data.monthly_online}')])

# Welcome embed
def welcome(data: structures.WelcomeStructure):
	return CustomEmbed(title=f'**Добро пожаловать на Discord-сервер официального клана [BestLife]**', author=EmbedAuthor(name='BestLife Official Clan', icon_url='https://i.ibb.co/YfvrWVZ/image.png'), color=colors.darkseagreen, thumbnail_url=data.thumbnail, image_url=data.image_url, footer=EmbedFooter(text='\nНадеемся, Вы останетесь надолго!', icon_url='https://cdn.discordapp.com/emojis/586502453424553985.png?v=1'),
					   fields=[EmbedField(name=f'**Мои поздравления, {data.name}!**', value=f'Вы {data.members_count}-й участник сервера!'), EmbedField(name='**Общение с другими участниками сервера: **', value=f'<#{channels.COMMUNITY}>'), EmbedField(name='**Speedwagon (клановый бот): **', value=f'<#{channels.SPEEDWAGON}>'), EmbedField(name='**Дискорд конференции официальных кланов:**', value=f'<#{channels.OFFICIAL_CLANS}>'), EmbedField(name='**Ссылка на набор в клан:**', value='[Нажми на меня](https://forum.excalibur-craft.ru/forum/125-BestLife/)'), EmbedField(name='**Бессрочное приглашение на наш сервер:**', value='[Нажми на меня](https://discord.gg/ER5Vfmx)')])

# Meme embed
def meme(url: str):
	return CustomEmbed(title='**Meme**', image_url=url, color=colors.whitesmoke)
