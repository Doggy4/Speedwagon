#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import datetime
import inspect

import discord
import random
from discord.ext import commands
from discord.ext import tasks
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

from channels import channels
from ex_parser.authorization.authorizer import Authorizer
from managers.command_manager import CommandManager
from managers.database_manager import LeftMembersDatabaseManager
from managers.log_manager import LogManager
from managers.rank_manager import RankManager
from utils import config_parser, roles, text
from utils.statuses import statuses
from utils.users import LeftUser

AUTHOR_ID = 529874353962352650
GUILD_ID = 549166689506557972


class Speedwagon(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs),
        self.database_manager = None
        self.log_manager = None
        self.authorizer = None
        self.rank_manager = None
        self.slash = SlashCommand(self, sync_commands=True)
        self.start_tasks()

        for name, member in inspect.getmembers(self):
            if isinstance(member, commands.Command):
                if member.parent is None:
                    self.add_command(member)

    @commands.command(name='avatar', aliases=['av', 'ав', 'аватар'])
    async def avatar(ctx, *, user: discord.User = None):
        user = ctx.author if user is None else user
        await ctx.reply(**CommandManager.avatar(ctx, user))

    @avatar.error
    async def avatar_error(ctx, error):
        if isinstance(error, commands.UserNotFound):
            await ctx.reply(**CommandManager.user_does_not_exist())

    @commands.command(name='top', aliases=['топ'])
    async def top(ctx, *, top_type: str = None):
        if not await CommandManager.confirm_channel_access(ctx, ctx.channel.id, 'top'):
            return
        pending_message = await ctx.reply(**CommandManager.pending())
        if top_type == 'online' or top_type == 'онлайн':
            await pending_message.edit(**CommandManager.online())
        elif top_type == 'votes' or top_type == 'голоса':
            await pending_message.edit(**CommandManager.votes())

    @commands.command(name='monitoring', aliases=['online', 'servers', 'server', 'mon', 'players', 'мониторинг', 'онлайн', 'игроки', 'мон', 'сервера', 'сервер', 'серверы'])
    async def monitoring(ctx):
        if not await CommandManager.confirm_channel_access(ctx, ctx.channel.id, 'monitoring'):
            return
        pending_message = await ctx.reply(**CommandManager.pending())
        await pending_message.edit(**CommandManager.monitoring())

    @commands.command(name='player', aliases=['user', 'name', 'username', 'nickname', 'игрок', 'никнейм', 'имя', 'пользователь'])
    async def player(ctx, nickname: str):
        if not await CommandManager.confirm_channel_access(ctx, ctx.channel.id, 'player'):
            return
        pending_message = await ctx.reply(**CommandManager.pending())
        await pending_message.edit(**CommandManager.player(nickname))

    @commands.command(name='clan', aliases=['клан'])
    async def clan(ctx, clan_name: str):
        if not await CommandManager.confirm_channel_access(ctx, ctx.channel.id, 'clan'):
            return
        pending_message = await ctx.reply(**CommandManager.pending())
        await pending_message.edit(**CommandManager.clan(clan_name))

    @commands.command(name='help', aliases=['support', 'bot', 'speedwagon', 'помощь', 'поддержка', 'хелп', 'бот', 'спидвагон'])
    async def help(ctx):
        embed = CommandManager.help(ctx.channel.id, ctx.author.permissions_in(ctx.channel).administrator)
        await ctx.reply(embed=embed[0])

    def start_tasks(self):
        self.random_status_task.start()
        self.confirm_authorization_task.start()
        self.update_rank_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        self.log_manager = LogManager(guild=self.get_guild(GUILD_ID))
        self.authorizer = Authorizer(self.log_manager)
        self.rank_manager = RankManager()
        await self.log_manager.ready()

    # async def on_error(self, event, *args, **kwargs):
    #     await self.log_manager.error(event, args, kwargs)

    async def on_member_join(self, member):
        left_user = LeftMembersDatabaseManager().get_delete_user(member.id)
        if left_user is not None:
            await member.edit(nick=left_user.display_name,
                              roles=list(map(lambda x: self.get_guild(GUILD_ID).get_role(x), left_user.roles_ids)))
        await self.log_manager.member_join(member)

    async def on_member_remove(self, member):
        if not (len(member.roles) == 2 and member.roles[0].id == 549166689506557950 and member.roles[1].id == 559487078191202325):
            LeftMembersDatabaseManager().add_update_user(LeftUser(discord_id=member.id,
                                                                  display_name=member.nick if member.nick is not None else member.display_name,
                                                                  roles_ids=list(map(lambda x: x.id, member.roles))))
        await self.log_manager.member_leave(member)

    async def on_member_update(self, before, after):
        await self.log_manager.member_update(before, after)

    async def on_member_ban(self, guild, user):
        await self.log_manager.member_ban(user)

    async def on_member_unban(self, guild, user):
        await self.log_manager.member_unban(user)

    async def on_message_edit(self, before, after):
        if not (before.author.bot or before.author.id == AUTHOR_ID):
            await self.log_manager.message_edit(before, after)

    # async def on_message(self, message):
    #     if message.channel.id == channels.MUSIC:
    #         await asyncio.sleep(30)
    #         await message.delete()

    async def on_message_delete(self, message):
        if not (message.author.bot or message.author.id == AUTHOR_ID):
            await self.log_manager.message_delete(message)

    async def on_reaction_add(self, reaction, user):
        await self.log_manager.reaction_add(reaction, user)

    async def on_reaction_remove(self, reaction, user):
        await self.log_manager.reaction_remove(reaction, user)

    async def on_raw_reaction_add(self, payload):
        role_id = roles.reactions_roles.get(payload.emoji.id, 0)
        if role_id != 0:
            await payload.member.add_roles(self.get_guild(GUILD_ID).get_role(role_id))
            await payload.member.add_roles(self.get_guild(GUILD_ID).get_role(852124056043651083))

    async def on_raw_reaction_remove(self, payload):
        role_id = roles.reactions_roles.get(payload.emoji.id, 0)
        if role_id != 0:
            role = self.get_guild(GUILD_ID).get_role(role_id)
            member = self.get_guild(GUILD_ID).get_member(payload.user_id)
            if role_id in list(map(lambda x: x.id, member.roles)):
                await member.remove_roles(role)
            if not text.common_member(roles.reactions_roles.values(), list(map(lambda x: x.id, member.roles))):
                await member.remove_roles(self.get_guild(GUILD_ID).get_role(852124056043651083))

    async def on_reaction_clear(self, message, reactions):
        await self.log_manager.reaction_clear(message, reactions)

    async def on_guild_channel_create(self, channel):
        await self.log_manager.guild_channel_create(channel)

    async def on_guild_channel_delete(self, channel):
        await self.log_manager.guild_channel_delete(channel)

    async def on_guild_role_create(self, role):
        await self.log_manager.guild_role_create(role)

    async def on_guild_role_delete(self, role):
        await self.log_manager.guild_role_delete(role)

    async def on_voice_state_update(self, member, before, after):
        await self.log_manager.voice_state_update(member, before, after)

    @tasks.loop(seconds=10)  # random status every 10 seconds
    async def random_status_task(self):
        status = random.choice(statuses)
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Activity(type=status[0], name=status[1]))

    @tasks.loop(minutes=30)  # confirm authorization every 30 minutes
    async def confirm_authorization_task(self):
        await self.authorizer.validate()

    @tasks.loop(minutes=10)  # update rank every minute
    async def update_rank_task(self):
        # if datetime.datetime.now().strftime('%M') == '00':
        # RankManager()
        pass

    @random_status_task.before_loop
    @confirm_authorization_task.before_loop
    @update_rank_task.before_loop
    async def before_task_loop(self):
        await self.wait_until_ready()  # wait until the bot logs in


class Slash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.command_manager = CommandManager()

    @cog_ext.cog_slash(name='avatar', description='Аватар пользователя', options=[
        create_option(name='user', description='Пользователь, чей аватар необходимо получить', option_type=6,
                      required=False)], guild_ids=[GUILD_ID])
    async def _avatar(self, ctx: SlashContext, user: discord.User = None):
        user = ctx.author if user is None else user
        await ctx.send(**self.command_manager.avatar(ctx, user))

    @cog_ext.cog_slash(name='help', description='Общая информация и доступные команды', guild_ids=[GUILD_ID])
    async def _help(self, ctx: SlashContext):
        embeds = self.command_manager.help(ctx.channel_id, ctx.author.permissions_in(ctx.channel).administrator)
        await ctx.send(embed=embeds[0])
        if len(embeds) > 1:
            await ctx.send(embeds=embeds[1:], hidden=True)

    @cog_ext.cog_slash(name='player', description='Информация об игроке', options=[
        create_option(name='nickname', description='Никнейм игрока', option_type=3, required=True)],
                       guild_ids=[GUILD_ID])
    async def _player(self, ctx: SlashContext, nickname: str):
        if not await self.command_manager.confirm_channel_access(ctx, ctx.channel_id, self._player.name):
            return
        await ctx.defer()
        await ctx.send(**self.command_manager.player(nickname))

    @cog_ext.cog_slash(name='role', description='Информация об игроке', options=[
        create_option(name='nickname', description='Никнейм игрока', option_type=3, required=True)],
                       guild_ids=[GUILD_ID])
    async def _role(self, ctx: SlashContext, nickname: str):
        if not await self.command_manager.confirm_channel_access(ctx, ctx.channel_id, self._player.name):
            return
        await ctx.defer()
        await ctx.send(**self.command_manager.player(nickname))

    @cog_ext.cog_slash(name='clan', description='Информация о клане', options=[
        create_option(name='clan_name', description='Название клана', option_type=3, required=True)],
                       guild_ids=[GUILD_ID])
    async def _clan(self, ctx: SlashContext, clan_name: str):
        if not await self.command_manager.confirm_channel_access(ctx, ctx.channel_id, self._clan.name):
            return
        await ctx.defer()
        await ctx.send(**self.command_manager.clan(clan_name))

    @cog_ext.cog_slash(name='monitoring', description='Мониторинг серверов', guild_ids=[GUILD_ID])
    async def _monitoring(self, ctx):
        if not await self.command_manager.confirm_channel_access(ctx, ctx.channel_id, self._monitoring.name):
            return
        await ctx.defer()
        await ctx.send(**self.command_manager.monitoring())

    @cog_ext.cog_subcommand(base='top', name='online', description='Топ игроков по онлайну', guild_ids=[GUILD_ID])
    async def _top_online(self, ctx: SlashContext):
        if not await self.command_manager.confirm_channel_access(ctx, ctx.channel_id, self._top_online.name):
            return
        await ctx.defer()
        await ctx.send(**self.command_manager.online())

    @cog_ext.cog_subcommand(base='top', name='votes', description='Топ игроков по голосам', guild_ids=[GUILD_ID])
    async def _top_votes(self, ctx: SlashContext):
        if not await self.command_manager.confirm_channel_access(ctx, ctx.channel_id, self._top_votes.name):
            return
        await ctx.defer()
        await ctx.send(**self.command_manager.votes())

    @cog_ext.cog_slash(name='purge', description='Чистка сообщений', options=[
        create_option(name='count', description='Количество сообщений', option_type=4, required=True)],
                       guild_ids=[GUILD_ID])
    async def _purge(self, ctx: SlashContext, count: int):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).manage_messages):
            return
        await ctx.channel.purge(limit=count)
        await self.bot.log_manager.message_purge(ctx.author, ctx.channel_id, count)
        await ctx.send(f'Успешно удалено **{count}** сообщений.', hidden=True)

    @cog_ext.cog_slash(name='link', description='Привязка никнейма к дискорд-аккаунту', options=[
        create_option(name='nickname', description='Игровой никнейм на проекте', option_type=3, required=True),
        create_option(name='member', description='Дискорд-аккаунт на сервере', option_type=6, required=True)],
                       guild_ids=[GUILD_ID], )
    async def _link(self, ctx: SlashContext, nickname: str, member: discord.Member):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).administrator):
            return
        await ctx.send(**self.command_manager.link(self.bot.rank_manager, nickname, member.id))

    @cog_ext.cog_slash(name='kick', description='Кикнуть пользователя с сервера', options=[
        create_option(name='user', description='Пользователь, которого необходимо кикнуть', option_type=6,
                      required=True),
        create_option(name='reason', description='Причина кика', option_type=3, required=False)],
                       guild_ids=[GUILD_ID], )
    async def _kick(self, ctx: SlashContext, user: discord.Member, reason: str = 'Не веди себя плохо :)'):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).kick_members):
            return
        await user.kick(reason=reason)
        await ctx.send(f'Пользователь **{user.display_name}** успешно кикнут по причине `{reason}`.')

    @cog_ext.cog_slash(name='ban', description='Забанить пользователя на сервере', options=[
        create_option(name='user', description='Пользователь, которого необходимо забанить', option_type=6,
                      required=True),
        create_option(name='reason', description='Причина кика', option_type=3, required=False)],
                       guild_ids=[GUILD_ID], )
    async def _ban(self, ctx: SlashContext, user: discord.Member, reason: str = 'Не веди себя плохо :)'):
        if not await self.command_manager.confirm_permission_access(ctx,
                                                                    ctx.author.permissions_in(ctx.channel).ban_members):
            return
        await user.ban(reason=reason)
        await ctx.send(f'Пользователь **{user.display_name}** успешно забанен по причине `{reason}`.')

    @cog_ext.cog_slash(name='recruit', description='Принять новобранца в клан', options=[
        create_option(name='nickname', description='Игровой никнейм на проекте', option_type=3, required=True),
        create_option(name='name', description='Настоящее имя игрока', option_type=3, required=True),
        create_option(name='user', description='Пользователь, которого необходимо принять в клан', option_type=6,
                      required=True),
        create_option(name='term', description='Длительность испытательного срока (в сутках). По умолчанию: 7',
                      option_type=4, required=False),
        create_option(name='mention', description='Оповещение клану. По умолчанию: False', option_type=5,
                      required=False)], guild_ids=[GUILD_ID])
    async def _recruit(self, ctx: SlashContext, nickname: str, name: str, user: discord.Member, term: int = 7,
                       mention: bool = False):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).administrator):
            return
        await ctx.send(
            **await self.command_manager.recruit(ctx, self.bot.rank_manager, nickname, name, user, mention, term))

    @cog_ext.cog_slash(name='say', description='Соообщение от лица бота', options=[
        create_option(name='channel', description='Канал сообщения', option_type=7, required=True),
        create_option(name='text', description='Текст сообщения', option_type=3, required=True),
        create_option(name='reaction', description='Реакция к отправленному сообщению', option_type=3, required=False)],
                       guild_ids=[GUILD_ID])
    async def _say(self, ctx: SlashContext, channel: discord.TextChannel, text: str, reaction: str = None):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).administrator):
            return
        message = await channel.send(text)
        if reaction is not None:
            await message.add_reaction(reaction)
        await ctx.send('✅', hidden=True)

    @cog_ext.cog_subcommand(base='rank', name='top', description='Топ игроков по рангу', guild_ids=[GUILD_ID])
    async def _rank_top(self, ctx: SlashContext):
        if not await self.command_manager.confirm_channel_access(ctx, ctx.channel_id, self._rank_top.base):
            return
        await ctx.send('Бип буп бип')

    @cog_ext.cog_subcommand(base='rank', name='player', description='Ранг пользователя', options=[
        create_option(name='nickname', description='Никнейм игрока на проекте', option_type=3, required=False),
        create_option(name='user', description='Дискорд игрока', option_type=6, required=False)], guild_ids=[GUILD_ID])
    async def _rank_player(self, ctx: SlashContext, nickname: str = None, user: discord.Member = None):
        if not await self.command_manager.confirm_channel_access(ctx, ctx.channel_id, self._rank_player.base):
            return
        await ctx.send('Бип буп бип')

    @cog_ext.cog_subcommand(base='history', subcommand_group='member', name='accept',
                            description='Добавление участника в клан (обновление истории клана)', options=[
            create_option(name='nickname', description='Игровой никнейм на проекте', option_type=3, required=True),
            create_option(name='date',
                          description=f'Дата осуществления. По умолчанию: {datetime.datetime.now().strftime("%d/%m/%Y")}',
                          option_type=3, required=False)], guild_ids=[GUILD_ID])
    async def _history_member_accept(self, ctx: SlashContext, nickname: str,
                                     date: str = datetime.datetime.now().strftime('%d/%m/%Y')):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).administrator):
            return
        await ctx.send(**await self.command_manager.history_member_accept(ctx, nickname, date))

    @cog_ext.cog_subcommand(base='history', subcommand_group='member', name='kick',
                            description='Исключение участника из клана (обновление истории клана)', options=[
            create_option(name='nickname', description='Игровой никнейм на проекте', option_type=3, required=True),
            create_option(name='date',
                          description=f'Дата осуществления. По умолчанию: {datetime.datetime.now().strftime("%d/%m/%Y")}',
                          option_type=3, required=False)], guild_ids=[GUILD_ID])
    async def _history_member_kick(self, ctx: SlashContext, nickname: str,
                                   date: str = datetime.datetime.now().strftime('%d/%m/%Y')):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).administrator):
            return
        await ctx.send(**await self.command_manager.history_member_kick(ctx, nickname, date))

    @cog_ext.cog_subcommand(base='history', subcommand_group='member', name='reserve',
                            description='Перевод участника в резервный состав (обновление истории клана)', options=[
            create_option(name='nickname', description='Игровой никнейм на проекте', option_type=3, required=True),
            create_option(name='date',
                          description=f'Дата осуществления. По умолчанию: {datetime.datetime.now().strftime("%d/%m/%Y")}',
                          option_type=3, required=False)], guild_ids=[GUILD_ID])
    async def _history_member_reserve(self, ctx: SlashContext, nickname: str,
                                      date: str = datetime.datetime.now().strftime('%d/%m/%Y')):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).administrator):
            return
        await ctx.send(**await self.command_manager.history_member_reserve(ctx, nickname, date))

    @cog_ext.cog_subcommand(base='history', subcommand_group='member', name='return',
                            description='Перевод участника в основной состав (обновление истории клана)', options=[
            create_option(name='nickname', description='Игровой никнейм на проекте', option_type=3, required=True),
            create_option(name='date',
                          description=f'Дата осуществления. По умолчанию: {datetime.datetime.now().strftime("%d/%m/%Y")}',
                          option_type=3, required=False)], guild_ids=[GUILD_ID])
    async def _history_member_return(self, ctx: SlashContext, nickname: str,
                                     date: str = datetime.datetime.now().strftime('%d/%m/%Y')):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).administrator):
            return
        await ctx.send(**await self.command_manager.history_member_return(ctx, nickname, date))

    @cog_ext.cog_subcommand(base='history', subcommand_group='member', name='enhance',
                            description='Повышение участника в звании (обновление истории клана)', options=[
            create_option(name='nickname', description='Игровой никнейм на проекте', option_type=3, required=True),
            create_option(name='rank', description='Новое звание участника', option_type=3, required=True,
                          choices=[create_choice(value='Глава клана', name='Лидер (глава)'),
                                   create_choice(value='Офицер клана', name='Офицер')]), create_option(name='date',
                                                                                                       description=f'Дата осуществления. По умолчанию: {datetime.datetime.now().strftime("%d/%m/%Y")}',
                                                                                                       option_type=3,
                                                                                                       required=False)],
                            guild_ids=[GUILD_ID])
    async def _history_member_enhance(self, ctx: SlashContext, nickname: str, rank: str,
                                      date: str = datetime.datetime.now().strftime('%d/%m/%Y')):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).administrator):
            return
        await ctx.send(**await self.command_manager.history_member_enhance(ctx, nickname, rank, date))

    @cog_ext.cog_subcommand(base='history', subcommand_group='member', name='lower',
                            description='Понижение участника в звании (обновление истории клана)', options=[
            create_option(name='nickname', description='Игровой никнейм на проекте', option_type=3, required=True),
            create_option(name='rank', description='Новое звание участника', option_type=3, required=True,
                          choices=[create_choice(value='Участник клана', name='Участник'),
                                   create_choice(value='Офицер клана', name='Офицер')]), create_option(name='date',
                                                                                                       description=f'Дата осуществления. По умолчанию: {datetime.datetime.now().strftime("%d/%m/%Y")}',
                                                                                                       option_type=3,
                                                                                                       required=False)],
                            guild_ids=[GUILD_ID])
    async def _history_member_lower(self, ctx: SlashContext, nickname: str, rank: str,
                                    date: str = datetime.datetime.now().strftime('%d/%m/%Y')):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).administrator):
            return
        await ctx.send(**await self.command_manager.history_member_lower(ctx, nickname, rank, date))

    @cog_ext.cog_subcommand(base='history', subcommand_group='clan', name='alliance',
                            description='Заключение союза с кланом (обновление истории клана)', options=[
            create_option(name='clan', description='Название клана на проекте', option_type=3, required=True),
            create_option(name='date',
                          description=f'Дата осуществления. По умолчанию: {datetime.datetime.now().strftime("%d/%m/%Y")}',
                          option_type=3, required=False)], guild_ids=[GUILD_ID])
    async def _history_clan_alliance(self, ctx: SlashContext, clan: str,
                                     date: str = datetime.datetime.now().strftime('%d/%m/%Y')):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).administrator):
            return
        await ctx.send(**await self.command_manager.history_clan_alliance(ctx, clan, date))

    @cog_ext.cog_subcommand(base='history', subcommand_group='clan', name='terminate_alliance',
                            description='Расторжение союза с кланом (обновление истории клана)', options=[
            create_option(name='clan', description='Название клана на проекте', option_type=3, required=True),
            create_option(name='date',
                          description=f'Дата осуществления. По умолчанию: {datetime.datetime.now().strftime("%d/%m/%Y")}',
                          option_type=3, required=False)], guild_ids=[GUILD_ID])
    async def _history_clan_terminate_alliance(self, ctx: SlashContext, clan: str,
                                               date: str = datetime.datetime.now().strftime('%d/%m/%Y')):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).administrator):
            return
        await ctx.send(**await self.command_manager.history_clan_terminate_alliance(ctx, clan, date))

    @cog_ext.cog_subcommand(base='history', subcommand_group='clan', name='war',
                            description='Объявление войны клану (обновление истории клана)', options=[
            create_option(name='clan', description='Название клана на проекте', option_type=3, required=True),
            create_option(name='date',
                          description=f'Дата осуществления. По умолчанию: {datetime.datetime.now().strftime("%d/%m/%Y")}',
                          option_type=3, required=False)], guild_ids=[GUILD_ID])
    async def _history_clan_war(self, ctx: SlashContext, clan: str,
                                date: str = datetime.datetime.now().strftime('%d/%m/%Y')):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).administrator):
            return
        await ctx.send(**await self.command_manager.history_clan_war(ctx, clan, date))

    @cog_ext.cog_subcommand(base='history', subcommand_group='clan', name='truce',
                            description='Объявление перемирия (после войны) клану (обновление истории клана)', options=[
            create_option(name='clan', description='Название клана на проекте', option_type=3, required=True),
            create_option(name='date',
                          description=f'Дата осуществления. По умолчанию: {datetime.datetime.now().strftime("%d/%m/%Y")}',
                          option_type=3, required=False)], guild_ids=[GUILD_ID])
    async def _history_clan_truce(self, ctx: SlashContext, clan: str,
                                  date: str = datetime.datetime.now().strftime('%d/%m/%Y')):
        if not await self.command_manager.confirm_permission_access(ctx, ctx.author.permissions_in(
                ctx.channel).administrator):
            return
        await ctx.send(**await self.command_manager.history_clan_truce(ctx, clan, date))


if __name__ == '__main__':
    speedwagon = Speedwagon(intents=discord.Intents.all(), command_prefix='/', case_insensitive=True, help_command=None)
    speedwagon.add_cog(Slash(speedwagon))
    speedwagon.run(config_parser.get_section_params('bot').get('token'))
