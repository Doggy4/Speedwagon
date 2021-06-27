from channels import channels
from embeds.custom_embed import CustomEmbed, EmbedField
from utils import colors

# Rank-help embed
_rank = CustomEmbed(title='**Speedwagon Support**', description='Информация по системе рангов', color=colors.green, thumbnail_url='https://i.imgur.com/TaaRJIY.png',
                    fields=[EmbedField(name='**Что такое система рангов?**', value='Система рангов - система, разработанная для клана BestLife, позволяюшая отслеживать и поощрать активность участников клана'), EmbedField(name='**Как получать ранг?**', value='Уровень (ранг) пользователя расчитывается, исходя из его месячного онлайна и количества внесенных за месяц голосов'), EmbedField(name='**Что дает ранг?**', value='Топ пользователей по рангу в конце месяца получает призы в Личный Кабинет, дополнительные роли и возможность создавать собственные'), EmbedField(name='**Как узнать свой текущий ранг?**', value='Команда **/rank**'), EmbedField(name='**Как узнать ранг другого игрока?**', value='Команда **/rank <ник>**'), EmbedField(name='**Как узнать текущий топ по рангу?**', value='Команда **/toprank**'), EmbedField(name='**Как вывести данное сообщение?**', value='Команда **/help**'),
                            EmbedField(name='**Как включить / выключить оповещение о получении нового уровня?**', value='Команда **/notifications | /nots**')])

# Commands-help embed
_commands = CustomEmbed(title='**Speedwagon Support**', description='Общие команды', color=colors.yellow, thumbnail_url='https://i.imgur.com/fStCJ0l.png', fields=[EmbedField(name='**/avatar**', value='Аватар пользователя'), EmbedField(name='**/top online**', value='Топ по часам'), EmbedField(name='**/top votes**', value='Топ по голосам'), EmbedField(name='**/monitoring**', value='Мониторинг серверов'), EmbedField(name='**/player**', value='Информация о пользователе'), EmbedField(name='**/clan**', value='Информация о клане')])

# Common-help embed
_common = CustomEmbed(title='**Speedwagon Support**', description='Общая информация', color=colors.darkcyan, thumbnail_url='https://i.imgur.com/SpPfR0n.png', fields=[EmbedField(name='**Общение с другими участниками сервера: **', value=f'<#{channels.COMMUNITY}>'), EmbedField(name='**Speedwagon (клановый бот): **', value=f'<#{channels.SPEEDWAGON}>'), EmbedField(name='**Дискорд конференции официальных кланов:**', value=f'<#{channels.OFFICIAL_CLANS}>'), EmbedField(name='**Ссылка на набор в клан:**', value='[Нажми на меня](https://forum.excalibur-craft.ru/forum/125-BestLife/)'), EmbedField(name='**Бессрочное приглашение на наш сервер:**', value='[Нажми на меня](https://discord.gg/ER5Vfmx)')])

# Admin-help embed
_admin = CustomEmbed(title='**Speedwagon Support**', description='Команды администратора', color=colors.red, thumbnail_url='https://i.imgur.com/cEj9Zh9.png', fields=[EmbedField(name='**/ban**', value='Бан (бессрочная блокировка) пользователя'), EmbedField(name='**/kick**', value='Кик (исключение с сервера) пользователя'), EmbedField(name='**/link**', value='Привязка игрового аккаунта к дискорд-аккаунту'), EmbedField(name='**/purge**', value='Чистка большого количества сообщений'), EmbedField(name='**/recruit**', value='Принятие новобранца в клан и привязка дискорд-аккаунта'), EmbedField(name='**/history**', value='Обновление истории клана'), EmbedField(name='**/rank update**', value='Принудительная синхронизация ранга')])

# Channel-switch dictionary-getter
def get_help_embeds(channel: int, is_admin: bool):
    return [{channels.RANK: _rank, channels.SPEEDWAGON: _commands, channels.BOT_TESTING: _commands}.get(channel, _common), _admin] if is_admin else [{channels.RANK: _rank, channels.SPEEDWAGON: _commands, channels.BOT_TESTING: _commands}.get(channel, _common)]
