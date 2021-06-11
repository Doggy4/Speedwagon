class WelcomeStructure(object):
	def __init__(self, name: str, thumbnail: str, image_url: str, members_count: int):
		self.name = name
		self.thumbnail = thumbnail
		self.image_url = image_url
		self.members_count = members_count

class ServerStructure(object):
	def __init__(self, name: str, online: str, fullness: float):
		self.name = name
		self.online = online
		self.fullness = round(fullness, 2) if fullness is not None else None

class MonitoringStructure(object):
	def __init__(self, total_online: str, servers: [ServerStructure], fullness: float):
		self.total_online = total_online
		self.servers = servers
		self.fullness = round(fullness, 2)

class VotePlayerStructure(object):
	def __init__(self, nickname: str, place: int):
		self.nickname = nickname
		self.place = place

class VoteStructure(object):
	def __init__(self, players: [VotePlayerStructure]):
		self.players = players

class OnlinePlayerStructure(object):
	def __init__(self, nickname: str, online: int):
		self.nickname = nickname
		self.online = online

class OnlineStructure(object):
	def __init__(self, players: [OnlinePlayerStructure]):
		self.players = players

class PlayerStructure(object):
	def __init__(self, nickname: str, thumbnail: str, image_url: str, registration_date: str, monthly_online: int, all_time_online: int, status: str, clan: str, has_cape: bool):
		self.nickname = nickname
		self.thumbnail = thumbnail
		self.image_url = image_url
		self.registration_date = registration_date
		self.monthly_online = monthly_online
		self.all_time_online = all_time_online
		self.status = status
		self.clan = clan
		self.has_cape = has_cape

class ClanStructure(object):
	def __init__(self, name: str, thumbnail: str, motto: str, top_place: int, rating_place: int, votes: int, experience: int, players: int, all_time_online: int, monthly_online: int):
		self.name = name
		self.thumbnail = thumbnail
		self.motto = motto
		self.top_place = top_place
		self.rating_place = rating_place
		self.votes = votes
		self.experience = experience
		self.players = players
		self.all_time_online = all_time_online
		self.monthly_online = monthly_online

class ClanPlayerStructure(object):
	def __init__(self, nickname: str, votes_all_time: int, votes_this_month: int, xp_all_time: int, xp_this_month: int, online_all_time: int, online_this_month: int):
		self.nickname = nickname
		self.votes_all_time = votes_all_time
		self.votes_this_month = votes_this_month
		self.xp_all_time = xp_all_time
		self.xp_this_month = xp_this_month
		self.online_all_time = online_all_time
		self.online_this_month = online_this_month