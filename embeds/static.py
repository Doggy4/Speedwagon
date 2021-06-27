from embeds.custom_embed import CustomEmbed

from utils import colors

# Pending embed
pending = CustomEmbed(title='Пожалуйста, подождите...', description='Идет загрузка необходимой информации.', color=colors.midnightblue, image_url='https://i.imgur.com/yfDCSKl.gif')

# User does not exist embed
user_does_not_exist = CustomEmbed(title='Возникла **ошибка** при выполнении команды', description='Пользователь с указанным никнеймом не существует.', color=colors.wheat, thumbnail_url='https://i.imgur.com/7FcyvNM.png')

# Clan does not exist embed
clan_does_not_exist = CustomEmbed(title='Возникла **ошибка** при выполнении команды', description='Клан с указанным названием не существует.', color=colors.wheat, thumbnail_url='https://i.imgur.com/7FcyvNM.png')

# Rank user does not exist embed
rank_user_does_not_exist = CustomEmbed(title='Возникла **ошибка** при выполнении команды', description='Пользователь с указанным никнеймом не существует. *Возможно, пользователь не состоит в клане или синхронизация пользователей не была произведена до сих пор корректно.*\n\n', color=colors.wheat, thumbnail_url='https://i.imgur.com/7FcyvNM.png')

# Command does not exist embed
command_does_not_exist = CustomEmbed(title='Возникла **ошибка** при выполнении команды', description='Команда с указанными параметрами не существует.\n\n*Возможные причины возникновения ошибки:\n • Отсутствие прав на выполнение команды\n • Команда недоступна на указанном канале\n • Введены некорректные данные в качестве аргументов запроса команды*\n\nПомощь - `/help`', color=colors.darkcyan, image_url='https://i.imgur.com/RvMz1us.gif')
