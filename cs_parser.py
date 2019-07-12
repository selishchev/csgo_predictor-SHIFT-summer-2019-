import requests
from bs4 import BeautifulSoup
import warnings
import datetime
warnings.filterwarnings('ignore')


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


def get_teams(url):
    teams_lst = []
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    div = soup.find_all(class_='teamName')
    for i in div:
        if i.get_text() not in teams_lst:
            teams_lst.append(i.get_text())
    return teams_lst


def get_team_href(href_lst):
    link_lst = []
    for i in href_lst:
        link = 'https://www.hltv.org' + i
        link_lst.append(link)
    return link_lst


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
            a = link.rfind('player')
            b = link[a+6:]
            link = 'https://www.hltv.org/stats' + '/players' + b + '?startDate=' + six_months_ago + \
                   '&endDate=' + today
            players_links.append(link)
    return players_links


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


def get_features(player_stats):
    features_name = []
    features_values = player_stats.copy()
    for i in player_stats:
        if ' ' in i:
            features_values.remove(i)
        if i not in features_name and ' ' in i:
            features_name.append(i)
    return features_name, features_values


def main():
    url = 'https://www.hltv.org/matches/2334868/g2-vs-winstrike-good-game-league-2019'
    f1 = get_href(url)
    f2 = get_team_href(f1)
    f3 = get_rankings(f2)
    f4 = get_players_links(f2)
    f5 = get_players_stats(f4)
    f6 = get_winrate(f2)
    f7 = get_features(f5)
    f8 = get_teams(url)
    print(f8)
    print(f3)
    print(f4)
    print(f5)
    print(f6)
    print(f7)


if __name__ == '__main__':
    main()
