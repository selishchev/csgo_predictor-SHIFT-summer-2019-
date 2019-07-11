import requests
from bs4 import BeautifulSoup
import warnings
import datetime
warnings.filterwarnings('ignore')

# url = 'https://www.hltv.org/matches/2334827/nemiga-vs-ago-gameagents-league-season-3'
# html = requests.get(url).text
# soup = BeautifulSoup(html)


def get_href(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    href = soup.find_all(class_='box-headline')
    href_lst = []
    try:
        for i in href:
            for link in i:
                href_lst.append(link.get('href'))
    except AttributeError:
        pass
    for i in href_lst:
        if not i:
            href_lst.remove(i)
    return href_lst


def get_team_href(href_lst):
    link_lst = []
    for i in href_lst:
        link = 'https://www.hltv.org' + i
        link_lst.append(link)
    return link_lst


print(get_team_href(get_href('https://www.hltv.org/matches/2334827/nemiga-vs-ago-gameagents-league-season-3')))


def get_rankings(link_lst):
    ranks_lst = []
    lst = []
    for i in link_lst:
        html = requests.get(i).text
        soup = BeautifulSoup(html)
        rank = soup.find_all(class_='profile-team-stat')
        for j in rank:
            j = str(j)
            if '#' in j:
                lst.append(j)
    for i in lst:
        a = i.find('#')
        b = i.find('</a>')
        ranks_lst.append(int(i[a+1:b]))
    return ranks_lst


def get_players_links(link_lst):
    players_links = []
    today = str(datetime.datetime.date(datetime.datetime.today()))
    minus_six = int(today[today.find('-')+1:today.rfind('-')]) - 6
    six_months_ago = today[:today.find('-')+1] + '0' + str(minus_six) + today[today.rfind('-'):]
    for i in link_lst:
        html = requests.get(i).text
        soup = BeautifulSoup(html)
        div = soup.find(class_='bodyshot-team')
        links = div.find_all('a')
        for link in links:
            link = 'https://www.hltv.org/stats' + link.get('href')
            # обрезаем строку, чтобы вставить нужный адрес страницы со всей статой игрока
            a = link.rfind('player')
            b = link[a+6:]
            # скрепляем все переменные в нужный нам адрес со статой игрока
            link = 'https://www.hltv.org/stats' + '/players' + b + '?startDate=' + six_months_ago + \
                   '&endDate=' + today
            players_links.append(link)
    return players_links


# if '.' not in ...
def get_players_stats(players_links):
    player_stats = []
    for i in players_links:
        html = requests.get(i).text
        soup = BeautifulSoup(html)
        div = soup.find_all(class_='stats-row')
        for j in div:
            for child in j.children:
                player_stats.append(child.string)
    return player_stats


def get_winrate(link_lst):
    stats_links = []
    winrates = []
    final_winrates = []
    today = str(datetime.datetime.date(datetime.datetime.today()))
    minus_six = int(today[today.find('-') + 1:today.rfind('-')]) - 6
    six_months_ago = today[:today.find('-') + 1] + '0' + str(minus_six) + today[today.rfind('-'):]
    for i in link_lst:
        html = requests.get(i).text
        soup = BeautifulSoup(html)
        div = soup.find_all(class_='moreButton')
        for j in div:
            if 'All stats for' in str(j):
                link = 'https://www.hltv.org' + j.get('href') + '?startDate=' + six_months_ago + \
                       '&endDate=' + today
                stats_links.append(link)
    for link in stats_links:
        html = requests.get(link).text
        soup = BeautifulSoup(html)
        div = soup.find_all(class_='large-strong')
        for wr in div:
            if '/' in wr.get_text():
                winrates.append(wr.get_text())
    for wr in winrates:
        win = int(wr[:wr.find('/')-1])
        loss = int(wr[wr.rfind('/')+1:])
        winrate = win / (win + loss)
        final_winrates.append(round(winrate, 2))
    return final_winrates


def main():
    f1 = get_href('https://www.hltv.org/matches/2334827/nemiga-vs-ago-gameagents-league-season-3')
    f2 = get_team_href(f1)
    f3 = get_rankings(f2)
    f4 = get_players_links(f2)
    f5 = get_players_stats(f4)
    f6 = get_winrate(f2)
    print(f3)
    print(f4)
    print(f5)
    print(f6)


if __name__ == '__main__':
    main()
