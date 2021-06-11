from datetime import datetime

from utils.structures import ClanPlayerStructure

class RankUser(object):
	def __init__(self, nickname: str, xp: float, discord_id: int = 0, is_mentionable: bool = True, is_active: bool = True):
		self.nickname = nickname
		self.xp = xp
		self.discord_id = discord_id
		self.is_mentionable = is_mentionable
		self.is_active = is_active

class LeftUser(object):
	def __init__(self, discord_id: int, display_name: str, roles_ids: [int], added_at: datetime = None):
		self.discord_id = discord_id
		self.display_name = display_name
		self.roles_ids = roles_ids
		self.added_at = added_at

def clan_player_to_rank_user(clan_player: ClanPlayerStructure):
	xp_this_month = 1 if clan_player.online_this_month > 0 and clan_player.xp_this_month < 0 else clan_player.xp_this_month
	online_this_month = 1 if clan_player.xp_this_month > 0 and clan_player.online_this_month < 0 else clan_player.online_this_month
	xp = xp_this_month * online_this_month * 0.1
	return RankUser(nickname=clan_player.nickname, xp=xp)
