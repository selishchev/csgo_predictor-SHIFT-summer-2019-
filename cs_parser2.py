

import requests
from bs4 import BeautifulSoup
import warnings
import csv
from multiprocessing import Pool

f = open('data.txt', 'a', encoding='utf-8')

warnings.filterwarnings('ignore')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
}

m = []

for i in range(27, 46):

    url = f'https://www.hltv.org/results?offset={i * 100}'
    html = requests.get(url, headers=headers).text

    soup = BeautifulSoup(requests.get(url, headers=headers).text)

    matches = soup.find_all(class_='result-con')
    m.append(matches)



def get_match_info(matches):
    f = []
    for match_soup in matches:
        team_left = match_soup.find(class_='line-align team1').text.strip()
        team_right = match_soup.find(class_='line-align team2').text.strip()
        loss_score = match_soup.find(class_='score-lost').text.strip()
        win_score = match_soup.find(class_='score-won').text.strip()
        str_match = str(match_soup)
        ind_lost, ind_won = str_match.find('score-lost'), str_match.find('score-won')
        score_first = -1
        score_second = -1
        if ind_lost < ind_won:
            score_first = loss_score
            score_second = win_score
        if ind_lost > ind_won:
            score_first = win_score
            score_second = loss_score
        try:
            href = match_soup.find('a')['href']
            url_stats = f'https://www.hltv.org//{href}'
            html_stats = requests.get(url_stats, headers=headers).text
            soup_stats = BeautifulSoup(html_stats)
            stats = soup_stats.find(class_='small-padding stats-detailed-stats').find('a')['href']
        except AttributeError:
            pass
        soup1 = BeautifulSoup(requests.get(f'https://www.hltv.org//{stats}', headers=headers).text)
        s = soup1.find_all('tbody')
        k = []
        a = []
        d = []
        adr = []
        rating = []
        final_stats = {}
        final_stats['team1'] = team_left
        final_stats['team2'] = team_right
        for i in s:
            for n in i.find_all(class_='st-kills'):
                k.append(int(n.text.split()[0]))
            k1 = k[0:5]
            final_stats['kills1'] = k1
            k2 = k[5:]
            final_stats['kills2'] = k2

            for n in i.find_all(class_='st-assists'):
                a.append(int(n.text.split()[0]))
            a1 = a[0:5]
            final_stats['assists1'] = a1
            a2 = a[5:]
            final_stats['assists2'] = a2

            for n in i.find_all(class_='st-deaths'):
                d.append(int(n.text.split()[0]))
            d1 = d[0:5]
            final_stats['deaths1'] = d1
            d2 = d[5:]
            final_stats['deaths2'] = d2

            for n in i.find_all(class_='st-adr'):
                try:
                    adr.append(float(n.text.split()[0]))
                except ValueError:
                    adr.append(n.text.split()[0])
            adr1 = adr[0:5]
            final_stats['adr1'] = adr1
            adr2 = adr[5:]
            final_stats['adr2'] = adr2

            for n in i.find_all(class_='st-rating'):
                rating.append(float(n.text.split()[0]))
            rating1 = rating[0:5]
            final_stats['rating1'] = rating1
            rating2 = rating[5:]
            final_stats['rating2'] = rating2

        teams = {}
        teams[team_left] = score_first
        teams[team_right] = score_second

        if teams[team_left] > teams[team_right]:
            final_stats['win1'] = 1
            final_stats['lose1'] = 0
            final_stats['win2'] = 0
            final_stats['lose2'] = 1
        else:
            final_stats['win1'] = 0
            final_stats['lose1'] = 1
            final_stats['win2'] = 1
            final_stats['lose2'] = 0

        f.append(final_stats)
    return f

for match in m:
    dicts = get_match_info(match)

    for dic in dicts:
        for i in range(1, 6):
            dic[f'team1 p{i} kills'] = dic['kills1'][i - 1]
            dic[f'team1 p{i} assists'] = dic['assists1'][i - 1]
            dic[f'team1 p{i} deaths'] = dic['deaths1'][i - 1]
            dic[f'team1 p{i} adr'] = dic['adr1'][i - 1]
            dic[f'team1 p{i} rating'] = dic['rating1'][i - 1]
        for i in range(1, 6):
            dic[f'team2 p{i} kills'] = dic['kills2'][i - 1]
            dic[f'team2 p{i} assists'] = dic['assists2'][i - 1]
            dic[f'team2 p{i} deaths'] = dic['deaths2'][i - 1]
            dic[f'team2 p{i} adr'] = dic['adr2'][i - 1]
            dic[f'team2 p{i} rating'] = dic['rating2'][i - 1]
        dic.pop('kills1')
        dic.pop('assists1')
        dic.pop('deaths1')
        dic.pop('adr1')
        dic.pop('rating1')

        dic.pop('kills2')
        dic.pop('assists2')
        dic.pop('deaths2')
        dic.pop('adr2')
        dic.pop('rating2')
        for value in dic.values():
            if type(value) == str:
                value = value.encode('utf-8').decode('utf-8')
        print(dic)
        dic_values = ''
        for v in dic.values():
            dic_values += str(v) + ', '
        f.write(dic_values + '\n'.encode('utf-8').decode('utf-8'))



        """fieldnames = ['team1', 'team2', 'win1', 'lose1', 'win2', 'lose2',
                          'team1 p1 kills', 'team1 p1 assists', 'team1 p1 deaths', 'team1 p1 adr', 'team1 p1 rating',
                          'team1 p2 kills', 'team1 p2 assists', 'team1 p2 deaths', 'team1 p2 adr', 'team1 p2 rating',
                          'team1 p3 kills', 'team1 p3 assists', 'team1 p3 deaths', 'team1 p3 adr', 'team1 p3 rating',
                          'team1 p4 kills', 'team1 p4 assists', 'team1 p4 deaths', 'team1 p4 adr', 'team1 p4 rating',
                          'team1 p5 kills', 'team1 p5 assists', 'team1 p5 deaths', 'team1 p5 adr', 'team1 p5 rating',
                          'team2 p1 kills', 'team2 p1 assists', 'team2 p1 deaths', 'team2 p1 adr', 'team2 p1 rating',
                          'team2 p2 kills', 'team2 p2 assists', 'team2 p2 deaths', 'team2 p2 adr', 'team2 p2 rating',
                          'team2 p3 kills', 'team2 p3 assists', 'team2 p3 deaths', 'team2 p3 adr', 'team2 p3 rating',
                          'team2 p4 kills', 'team2 p4 assists', 'team2 p4 deaths', 'team2 p4 adr', 'team2 p4 rating',
                          'team2 p5 kills', 'team2 p5 assists', 'team2 p5 deaths', 'team2 p5 adr', 'team2 p5 rating']
            writer = csv.DictWriter(data, fieldnames=fieldnames, delimiter=' ')
            writer.writeheader()
            writer.writerow(dic)"""

