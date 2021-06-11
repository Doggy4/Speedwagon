import discord
from datetime import datetime

from utils import colors
from utils import images

class EmbedAuthor(object):
	def __init__(self, name: str = None, url: str = None, icon_url: str = None):
		self.url = url
		self.name = name
		self.icon_url = icon_url

class EmbedField(object):
	def __init__(self, name: str = None, value: str = None, inline: bool = False):
		self.name = name
		self.value = value
		self.inline = inline

class EmbedFooter(object):
	def __init__(self, text: str = None, icon_url: str = None):
		self.text = text
		self.icon_url = icon_url

class CustomEmbed(discord.Embed):
	def __init__(self, timestamp=datetime.utcnow(), color=colors.yellow, image_url: str = None, thumbnail_url: str = None, author: EmbedAuthor = EmbedAuthor(name='Speedwagon', icon_url=images.SPEEDWAGON_AVATAR_IMAGE), fields: [EmbedField] = None, footer: EmbedFooter = None, **kwargs):
		super().__init__(**{k:v for k, v in kwargs.items() if v is not None})
		self.set_author(**{k:v for k, v in author.__dict__.items() if v is not None})
		self.timestamp = timestamp
		self.color = color
		if image_url is not None:
			self.set_image(url=image_url)
		if thumbnail_url is not None:
			self.set_thumbnail(url=thumbnail_url)
		if footer is not None:
			self.set_footer(**{k:v for k, v in footer.__dict__.items() if v is not None})
		if fields is not None:
			for field in fields:
				self.add_field(name=field.name, value=field.value, inline=field.inline)
