from embeds.custom_embed import CustomEmbed, EmbedFooter
from utils import colors

# User rank-card embed
def user_card(image_url):
	return CustomEmbed(title='**Статистика игрока:**', color=colors.yellow, image_url=image_url)

# Top rank-card embed
def top_card(image_url):
	return CustomEmbed(title='**Топ игроков по активности:**', color=colors.yellow, image_url=image_url)

# Level change-card embed
def level_change_card(image_url, isMentioned):
	return CustomEmbed(title='**Обновление уровня:**', color=colors.yellow, image_url=image_url, footer=EmbedFooter(text='\nОтключить упоминания (уведомления) - /notifications | /nots') if isMentioned else EmbedFooter(text='\nВключить упоминания (уведомления) - /notifications | /nots'))

# Rank change-card embed
def rank_change_card(image_url, isMentioned):
	return CustomEmbed(title='**Обновление ранга:**', color=colors.yellow, image_url=image_url, footer=EmbedFooter(text='\nОтключить упоминания (уведомления) - /notifications | /nots') if isMentioned else EmbedFooter(text='\nВключить упоминания (уведомления) - /notifications | /nots'))
