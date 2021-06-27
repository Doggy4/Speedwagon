import psycopg2

from utils import config_parser
from utils.users import LeftUser, RankUser


class DatabaseManager(object):
    def __init__(self, table_name):
        self.table_name = f'speedwagon.{table_name}'
        self.connection = psycopg2.connect(**config_parser.get_section_params('database'))
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def __del__(self):
        self.connection.commit()
        self.cursor.close()


class RankDatabaseManager(DatabaseManager):
    def __init__(self):
        super().__init__(table_name='rank_users')

    def add_update_user(self, user: RankUser):
        """
        Adds or updates an existing user

        :param user: RankUser object
        :type user: RankUser
        """

        self.cursor.execute(f"""INSERT INTO {self.table_name} (nickname, xp, is_mentionable, discord_id) VALUES (%s, %s, %s, %s) ON CONFLICT (nickname) DO UPDATE SET xp = '{user.xp}', is_mentionable = {user.is_mentionable}, discord_id = '{user.discord_id}';""", (user.nickname, user.xp, user.is_mentionable, user.discord_id))

    def update_discord_mention_user(self, user: RankUser):
        """
        Updates user's discord mention

        :param user: RankUser object
        :type user: RankUser
        """
        self.cursor.execute(f"""UPDATE {self.table_name} SET is_mentionable = {user.is_mentionable} WHERE nickname ILIKE '{user.nickname}'""")

    def get_user_by_nickname(self, nickname: str):
        """
        Returns the user by his nickname

        :param nickname: User nickname
        :type nickname: str
        """

        self.cursor.execute(f"""SELECT * FROM {self.table_name} WHERE nickname ILIKE '{nickname}'""")
        user = self.cursor.fetchone()
        return RankUser(*user) if user is not None else None

    def get_sorted_user_list(self):
        """
        Returns a list of users sorted by xp
        """

        self.cursor.execute(f"""SELECT * FROM {self.table_name} ORDER BY xp desc;""")
        users = self.cursor.fetchall()
        return list(map(lambda s: RankUser(*s), users)) if users is not None else None

    def get_user_by_discord_id(self, discord_id: int):
        """
        Returns the user by his discord id

        :param discord_id: User discord ID
        :type discord_id: int
        """

        self.cursor.execute(f"""SELECT * FROM {self.table_name} WHERE discord_id={discord_id}""")
        user = self.cursor.fetchone()
        return RankUser(*user) if user is not None else None

    def __del__(self):
        super(RankDatabaseManager, self).__del__()


class LeftMembersDatabaseManager(DatabaseManager):
    def __init__(self):
        super().__init__(table_name='left_users')

    def get_delete_user(self, discord_id):
        """
        Returns and deletes the user by his ID

        :param discord_id: User discord ID
        :type discord_id: int
        """

        self.cursor.execute(f"""SELECT * FROM {self.table_name} WHERE discord_id={discord_id};""")
        fetchone = self.cursor.fetchone()
        self.cursor.execute(f"""DELETE FROM {self.table_name} WHERE discord_id={discord_id}""")

        return LeftUser(*fetchone) if fetchone is not None else None

    def add_update_user(self, user: LeftUser):
        """
        Adds or updates an existing user

        :param user: LeftUser object
        :type user: LeftUser
        """

        self.cursor.execute(f"""INSERT INTO {self.table_name} (discord_id, display_name, roles_ids)	VALUES ({user.discord_id}, '{user.display_name}', ARRAY{user.roles_ids}) ON CONFLICT (discord_id) DO UPDATE SET display_name = '{user.display_name}', roles_ids = ARRAY{user.roles_ids};""")

    def __del__(self):
        super(LeftMembersDatabaseManager, self).__del__()
