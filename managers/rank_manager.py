from ex_parser.parsers import clan_stats
from managers.database_manager import RankDatabaseManager
from utils.users import clan_player_to_rank_user

class RankManager(object):
	def __init__(self):
		self.rank_database_manager = RankDatabaseManager()
		self.database_rank_users = self.rank_database_manager.get_sorted_user_list()
		self.updated_rank_users = list(map(clan_player_to_rank_user, clan_stats()))

	def link(self, nickname, discord_id):
		user = self.rank_database_manager.get_user_by_nickname(nickname)
		if user is None:
			return None
		user.discord_id = discord_id
		self.rank_database_manager.add_update_user(user)
		self.rank_database_manager.commit()
		return user

	def sync(self):
		map(self.rank_database_manager.add_update_user, self.updated_rank_users)

	def nicknames(self):
		return list(map(lambda x: x.nickname, self.updated_rank_users))
