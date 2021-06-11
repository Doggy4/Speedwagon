import bs4
import json
import requests
import time

from images.image_processors import player_skin
from utils.structures import *
from utils.text import int_try_parse

def clan(name):
    cookies = json.loads(open('ex_parser/cookies.json', 'r').read())
    response = requests.post(url='https://excalibur-craft.ru/engine/ajax/clans/ajax.php', data={'action': 'clanListPagination', 'user_id': cookies['dle_user_id'], 'hash': cookies['dle_hash'], 'search_status': '1', 'search_lvl': '', 'search_name': name, 'search_motto': '', 'search_leader': '', 'search_player_amount': '', 'sort_status': '0', 'sort_lvl': 'DESC', 'sort_player_amount': 'DESC', 'page': '1'}, cookies=cookies)
    if len(json.loads(response.text)['pages']) < 5:
        return None
    soup = bs4.BeautifulSoup(requests.get(url=f'https://excalibur-craft.ru{bs4.BeautifulSoup(json.loads(response.text)["html_data"], "html.parser").find_all("a", href=True)[0]["href"]}', cookies=cookies).text, 'html.parser')
    indexes = soup.findAll('div', {'class': 'clans-profile-stats-index'})

    return ClanStructure(name=soup.findAll('div', {'class': 'clans-profile-clan-name'})[0].getText(), thumbnail=f'https://excalibur-craft.ru{soup.findAll("div", {"class": "clans-profile-flag-background"})[0].find("img")["src"]}', motto=soup.findAll('div', {'class': 'clans-profile-motto'})[0].getText(), top_place=indexes[0].getText(), rating_place=indexes[1].getText(), votes=indexes[2].getText(), experience=indexes[3].getText(), players=indexes[4].getText(), all_time_online=indexes[5].getText(), monthly_online=indexes[6].getText())

def player(nickname):
    cookies = json.loads(open('ex_parser/cookies.json', 'r').read())
    response = requests.post(url='https://excalibur-craft.ru/engine/ajax/profile/ajax.php', data={'action': 'loadProfile', 'user_id': cookies['dle_user_id'], 'hash': cookies['dle_hash'], 'name': nickname}, cookies=cookies)
    if len(response.text) < 5:
        return None
    soup = bs4.BeautifulSoup(json.loads(response.text)['data'], 'html.parser')
    columns = soup.findAll("div", {"class": "col-6"})
    clan_ = soup.find("div", {"class": "col-12"}).find('label')
    nickname = soup.select('div > div > div.col-8 > div.profile-head > h5 > b')[0].getText()
    image_url, has_cape = player_skin(nickname)
    return PlayerStructure(nickname=nickname, thumbnail=f'https://excalibur-craft.ru/engine/ajax/lk/skin3d.php?login={nickname}&mode=head&aa=true?{time.time()}', image_url=image_url, registration_date=columns[1].find('p').getText(), monthly_online=int(columns[3].find('p').getText()), all_time_online=int(columns[5].find('p').getText()), status=columns[7].find('p').getText(), clan=f'{clan_.getText().rsplit(" ", 1)[0]} [[{clan_.find("a").getText()}]]({clan_.find_all("a", href=True)[0]["href"]})' if clan_.getText() != 'Пользователь не состоит в клане' else clan_.getText(), has_cape=has_cape)

def clan_stats():
    cookies = json.loads(open('ex_parser/cookies.json', 'r').read())
    soup = bs4.BeautifulSoup(requests.get(url='https://excalibur-craft.ru/index.php?do=clans&go=lk&page=statistics', cookies=cookies).text, 'html.parser')
    table = soup.find('tbody')
    players = []
    for tr in table.findAll('tr'):
        tds = tr.findAll('td')
        players.append(ClanPlayerStructure(nickname=tds[0].getText(), votes_all_time=int(tds[1].getText()), votes_this_month=int(tds[2].getText()), xp_all_time=int(tds[3].getText()), xp_this_month=int(tds[4].getText()), online_all_time=int(tds[5].getText()), online_this_month=int(tds[6].getText())))

    return players

def votes():
    soup = bs4.BeautifulSoup(requests.get('https://excalibur-craft.ru/').text, 'html.parser')
    vote_players_structures = []
    for i, _player in enumerate(soup.find('div', {'class': 'quest'}).findAll('div', {'class': 'player'}), 1):
        vote_players_structures.append(VotePlayerStructure(nickname=_player.find('span').getText(), place=i))

    return VoteStructure(vote_players_structures)

def online():
    soup = bs4.BeautifulSoup(requests.get('https://excalibur-craft.ru/').text, 'html.parser')
    online_player_structures = []
    for _player in soup.find('div', {'class': 'time'}).findAll('div', {'class': 'row'}):
        online_player_structures.append(OnlinePlayerStructure(nickname=_player.find('div', {'class': 'player'}).find('span').getText(), online=int(_player.find('div', {'class': 'total'}).find('span').getText())))

    return OnlineStructure(online_player_structures)

def monitoring():
    soup = bs4.BeautifulSoup(requests.get('https://excalibur-craft.ru/').text, 'html.parser')
    servers = []
    for server in soup.find('div', {'class': 'right'}).findAll('div', {'class': 'server'}):
        servers.append(ServerStructure(name=server.find('span').getText(), online=server.find('div', {'class': 'online-number'}).getText().replace('\n', ''), fullness=eval(server.find('div', {'class': 'online-number'}).getText().replace('\n', '')) * 100 if int_try_parse(server.find('div', {'class': 'online-number'}).getText().replace('\n', ''))[1] else None))

    return MonitoringStructure(total_online=soup.select('#monitoring > div.left > div.total > div')[0].getText().replace('\n', ''), servers=servers, fullness=eval(soup.select('#monitoring > div.left > div.total > div')[0].getText().replace('\n', '')) * 100)
