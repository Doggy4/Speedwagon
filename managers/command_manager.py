import discord
from discord_slash import SlashContext

from embeds.command import *
from embeds.help import *
from embeds.static import *
from ex_parser import parsers
from managers.rank_manager import RankManager

class CommandManager(object):
    _commands = {channels.SPEEDWAGON: ['player', 'clan', 'monitoring', 'online', 'votes'], channels.BOT_TESTING: ['player', 'clan', 'monitoring', 'top', 'online', 'votes', 'rank'], channels.RANK: ['help', 'rank']}

    @staticmethod
    def _command_does_not_exist():
        return {'embed': command_does_not_exist}

    @staticmethod
    async def confirm_channel_access(ctx: SlashContext, command_name: str):
        if CommandManager._commands.get(ctx.channel_id) is None or command_name not in CommandManager._commands.get(ctx.channel_id):
            await ctx.send(hidden=True, **CommandManager._command_does_not_exist())
            return False
        return True

    @staticmethod
    async def confirm_permission_access(ctx: SlashContext, has_permission: bool):
        if not has_permission:
            await ctx.send(hidden=True, **CommandManager._command_does_not_exist())
            return False
        return True

    @staticmethod
    def help(ctx: SlashContext, is_admin: bool):
        return {'embeds': get_help_embeds(ctx.channel_id, is_admin)}

    @staticmethod
    def avatar(ctx: SlashContext, user: discord.User):
        return {'embed': avatar(user.avatar_url, ctx.author.avatar_url, user.name, user.discriminator)}

    @staticmethod
    def player(nickname: str):
        player_data = parsers.player(nickname)
        if player_data is not None:
            return {'embed': player(player_data)}
        return {'embed': player_does_not_exist}

    @staticmethod
    def clan(clan_name: str):
        clan_data = parsers.clan(clan_name)
        if clan_data is not None:
            return {'embed': clan(clan_data)}
        return {'embed': clan_does_not_exist}

    @staticmethod
    def monitoring():
        return {'embed': monitoring(parsers.monitoring())}

    @staticmethod
    def online():
        return {'embed': online(parsers.online())}

    @staticmethod
    def votes():
        return {'embed': votes(parsers.votes())}

    @staticmethod
    def link(rank_manager: RankManager, nickname: str, discord_id: int):
        user = rank_manager.link(nickname, discord_id)
        if user is None:
            return {'embed': rank_user_does_not_exist, 'hidden': True}
        return {'content': f'Никнейм *{user.nickname}* успешно привязан к дискорд-аккаунту <@!{discord_id}>.', 'hidden': True}

    @staticmethod
    async def recruit(ctx: SlashContext, rank_manager: RankManager, nickname: str, name: str, user: discord.Member, mention: bool, term: int):
        if mention:
            await ctx.guild.get_channel(channels.CLAN).send(f'@here\nНовый учасник клана - <@!{user.id}>\nДлительность испытательного срока: **{term} дней**.')
        await user.edit(nick=f'{nickname} [{name}]', roles=[559479206376147648, 559498413872513064, 549187774104993803, 561183743679922196])
        return CommandManager.link(rank_manager, nickname, user.id)

    @staticmethod
    async def history_member_accept(ctx: SlashContext, nickname: str, date: str):
        await ctx.guild.get_channel(channels.HISTORY).send(f'{date} ↴\n<:h1:721631499690049536> **{nickname}** *принят в клан*.')
        return {'content': 'История была успешно обновлена!', 'hidden': True}

    @staticmethod
    async def history_member_kick(ctx: SlashContext, nickname: str, date: str):
        await ctx.guild.get_channel(channels.HISTORY).send(f'{date} ↴\n<:h2:721631500390498355> **{nickname}** *исключен из клана*.')
        return {'content': 'История была успешно обновлена!', 'hidden': True}

    @staticmethod
    async def history_member_reserve(ctx: SlashContext, nickname: str, date: str):
        await ctx.guild.get_channel(channels.HISTORY).send(f'{date} ↴\n<:h3:721632310255943680> **{nickname}** *переведён в резервный состав*.')
        return {'content': 'История была успешно обновлена!', 'hidden': True}

    @staticmethod
    async def history_member_return(ctx: SlashContext, nickname: str, date: str):
        await ctx.guild.get_channel(channels.HISTORY).send(f'{date} ↴\n<:h3:721632310255943680> **{nickname}** *переведён в основной состав*.')
        return {'content': 'История была успешно обновлена!', 'hidden': True}

    @staticmethod
    async def history_member_enhance(ctx: SlashContext, nickname: str, rank: str, date: str):
        await ctx.guild.get_channel(channels.HISTORY).send(f'{date} ↴\n<:h1:721631499690049536> **{nickname}** *повышен до звания __{rank}__*.')
        return {'content': 'История была успешно обновлена!', 'hidden': True}

    @staticmethod
    async def history_member_lower(ctx: SlashContext, nickname: str, rank: str, date: str):
        await ctx.guild.get_channel(channels.HISTORY).send(f'{date} ↴\n<:h2:721631500390498355> **{nickname}** *понижен до звания __{rank}__*.')
        return {'content': 'История была успешно обновлена!', 'hidden': True}

    @staticmethod
    async def history_clan_alliance(ctx: SlashContext, clan: str, date: str):
        await ctx.guild.get_channel(channels.HISTORY).send(f'{date} ↴\n<:h1:721631499690049536> *Заключен союз с кланом* **{clan}**.')
        return {'content': 'История была успешно обновлена!', 'hidden': True}

    @staticmethod
    async def history_clan_terminate_alliance(ctx: SlashContext, clan: str, date: str):
        await ctx.guild.get_channel(channels.HISTORY).send(f'{date} ↴\n<:h2:721631500390498355> *Расторжен союз с кланом* **{clan}**.')
        return {'content': 'История была успешно обновлена!', 'hidden': True}

    @staticmethod
    async def history_clan_war(ctx: SlashContext, clan: str, date: str):
        await ctx.guild.get_channel(channels.HISTORY).send(f'{date} ↴\n<:h2:721631500390498355> *Объявлена война клану* **{clan}**.')
        return {'content': 'История была успешно обновлена!', 'hidden': True}

    @staticmethod
    async def history_clan_truce(ctx: SlashContext, clan: str, date: str):
        await ctx.guild.get_channel(channels.HISTORY).send(f'{date} ↴\n<:h1:721631499690049536> *Объявлено перемирие (окончание войны) клану* **{clan}**.')
        return {'content': 'История была успешно обновлена!', 'hidden': True}

    @staticmethod
    def meme():
        return {'embed': meme(meme_cut(parsers.meme()))}
