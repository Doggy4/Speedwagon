import discord

from channels import channels
from embeds import log
from embeds.command import welcome
from images.image_processors import welcome_card

class LogManager(object):
	def __init__(self, guild: discord.Guild):
		self.guild = guild

		self.MAX_MESSAGE_LENGTH = 1020
		self.OPTIMAL_MESSAGE_LENGTH = 1000

	async def error(self, event, *args, **kwargs):
		await self.guild.get_channel(channels.SYSTEM_LOGS).send(embed=log.error(event, args, kwargs))

	async def ready(self):
		await self.guild.get_channel(channels.SYSTEM_LOGS).send(embed=log.ready())

	async def member_join(self, member: discord.Member):
		from utils.structures import WelcomeStructure
		await self.guild.get_channel(channels.WELCOME).send(content=f'<@!{member.id}>', embed=welcome(WelcomeStructure(thumbnail=member.avatar_url, image_url=welcome_card(nickname=member.nick if member.nick is not None else member.display_name, avatar=member.avatar_url, member_number=self.guild.member_count - 1), name=member.display_name, members_count=self.guild.member_count - 1)))
		await self.guild.get_channel(channels.JOIN_LEAVE_LOGS).send(embed=log.member_join(member))

	async def member_leave(self, member: discord.Member):
		await self.guild.get_channel(channels.JOIN_LEAVE_LOGS).send(embed=log.member_leave(member))

	async def member_update(self, before_member: discord.Member, after_member: discord.Member):
		if after_member.roles != before_member.roles:
			difference = set(after_member.roles) - set(before_member.roles)
			if len(difference) > 0:
				await self.guild.get_channel(channels.MEMBER_LOGS).send(embed=log.member_role_add(member=before_member, role=difference.pop()))
			else:
				await self.guild.get_channel(channels.MEMBER_LOGS).send(embed=log.member_role_delete(member=before_member, role=(set(before_member.roles) - set(after_member.roles)).pop()))

		if before_member.nick != after_member.nick:
			await self.guild.get_channel(channels.MEMBER_LOGS).send(embed=log.member_name_change(before_member=before_member, after_member=after_member))

	async def member_ban(self, user: discord.User):
		await self.guild.get_channel(channels.BAN_LOGS).send(embed=log.member_ban(user))

	async def member_unban(self, user: discord.User):
		await self.guild.get_channel(channels.BAN_LOGS).send(embed=log.member_unban(user))

	async def message_delete(self, message: discord.Message):
		if len(message.content) > 0:
			await self.guild.get_channel(channels.MESSAGE_LOGS).send(embed=log.message_delete(message, message_content=message.content[:self.MAX_MESSAGE_LENGTH]))

	async def message_edit(self, before_message: discord.Message, after_message: discord.Message):
		if before_message.content != after_message.content:
			await self.guild.get_channel(channels.MESSAGE_LOGS).send(embed=log.message_edit(before_message, before_message_content=before_message.content[:self.MAX_MESSAGE_LENGTH], after_message_content=after_message.content[:self.MAX_MESSAGE_LENGTH]))

	async def message_purge(self, member: discord.Member, channel_id: int, purged_messages_number: int):
		await self.guild.get_channel(channels.MESSAGE_LOGS).send(embed=log.message_purge(member, channel_id, purged_messages_number))

	async def reaction_add(self, reaction: discord.Reaction, user: discord.User):
		await self.guild.get_channel(channels.REACTION_LOGS).send(embed=log.reaction_add(user=user, reaction=reaction))

	async def reaction_remove(self, reaction: discord.Reaction, user: discord.User):
		await self.guild.get_channel(channels.REACTION_LOGS).send(embed=log.reaction_remove(user=user, reaction=reaction))

	async def reaction_clear(self, message: discord.Message, reactions: [discord.Reaction]):
		await self.guild.get_channel(channels.REACTION_LOGS).send(embed=log.reaction_clear(message=message, reactions=reactions))

	async def guild_channel_delete(self, channel: discord.abc.GuildChannel):
		if isinstance(channel, discord.TextChannel):
			await self.guild.get_channel(channels.CHANNEL_LOGS).send(embed=log.text_channel_delete(channel=channel))
		elif isinstance(channel, discord.VoiceChannel):
			await self.guild.get_channel(channels.CHANNEL_LOGS).send(embed=log.voice_channel_delete(channel=channel))
		elif isinstance(channel, discord.CategoryChannel):
			await self.guild.get_channel(channels.CHANNEL_LOGS).send(embed=log.category_channel_delete(channel=channel))

	async def guild_channel_create(self, channel: discord.abc.GuildChannel):
		if isinstance(channel, discord.TextChannel):
			await self.guild.get_channel(channels.CHANNEL_LOGS).send(embed=log.text_channel_create(channel=channel))
		elif isinstance(channel, discord.VoiceChannel):
			await self.guild.get_channel(channels.CHANNEL_LOGS).send(embed=log.voice_channel_create(channel=channel))
		elif isinstance(channel, discord.CategoryChannel):
			await self.guild.get_channel(channels.CHANNEL_LOGS).send(embed=log.category_channel_create(channel=channel))

	async def guild_role_create(self, role: discord.Role):
		await self.guild.get_channel(channels.ROLE_LOGS).send(embed=log.role_create(role=role))

	async def guild_role_delete(self, role: discord.Role):
		await self.guild.get_channel(channels.ROLE_LOGS).send(embed=log.role_delete(role=role))

	async def voice_state_update(self, member: discord.Member, before_voice_state: discord.VoiceState, after_voice_state: discord.VoiceState):
		from utils.text import voice_state_to_string
		await self.guild.get_channel(channels.VOICE_LOGS).send(embed=log.voice_state_update(member=member, state=voice_state_to_string(before_voice_state=before_voice_state, after_voice_state=after_voice_state)))

	async def session_confirm_progress(self):
		await self.guild.get_channel(channels.PARSER_LOGS).send(embed=log.session_confirm_progress())

	async def session_confirm_success(self):
		await self.guild.get_channel(channels.PARSER_LOGS).send(embed=log.session_confirm_success())

	async def session_confirm_failed(self):
		await self.guild.get_channel(channels.PARSER_LOGS).send(embed=log.session_confirm_failed())

	async def session_confirm_blocked(self):
		await self.guild.get_channel(channels.PARSER_LOGS).send(embed=log.session_confirm_blocked())
