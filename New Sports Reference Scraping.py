import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from IPython.core.display import Image
import itertools
import os


def get_nfl_regular_season(year):
    url = f'https://www.pro-football-reference.com/years/{year}/index.htm'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    
    # wait to not go to jail
    time.sleep(8)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('div', class_='table_wrapper')
    df_rows = []

    for table in tables:
        for tab in table.find_all('table'):
            headers_list = []

            # Get the headers
            for headers in tab.find('thead'):
                # skip the Navigable strings
                try:
                    if headers.find_all('th'):
                        for header in headers.find_all('th'):
                            headers_list.append(header.text)
                except AttributeError:
                    continue

            # Get the body data
            table_body = tab.find('tbody')
            for row in table_body.find_all('tr'):
                rows = []
                # skip the division name
                if row.find('td', class_='right left'):
                    continue
                for team in row.find_all('th'):
                    rows.append(team.text)
                for td in row.find_all('td'):
                    rows.append(td.text)
                df_rows.append(rows)
                
    df = pd.DataFrame(df_rows, columns=headers_list)
    df['year'] = year
    
    print(f'Success for {year} NFL regular season!')
    
    return df

def get_nfl_playoffs(year):
    options = Options()
    options.headless = True
    b = webdriver.Chrome(options=options)

    b.get(f'https://www.pro-football-reference.com/years/{year}/index.htm')

    soup = BeautifulSoup(b.page_source)
    
    time.sleep(4)
    
    playoffs = soup.find('div', {'class': 'table_container is_setup', 'id': 'div_playoff_results'})
    
    b.close()
    
    # wait to not go to jail
    time.sleep(4)

    # Get Headers
    headers_list = []
    for headers in playoffs.find('thead'):
        try:
            iterator = 1
            for header in headers.find_all('th'):
                if header.text == '':
                    headers_list.append(f'Filler Column {iterator}')
                    iterator += 1
                else:
                    headers_list.append(header.text)
        except AttributeError:
            continue

    # Get Body Data
    df_rows = []
    for body_data in playoffs.find_all('tbody'):

        try:
            for body_row in body_data.find_all('tr'):
                row_list = []

                # get Round Name
                for round_name in body_row.find('th'):
                    row_list.append(round_name.text)

                # get data for Round
                for data in body_row.find_all('td'):
                    row_list.append(data.text)

                df_rows.append(row_list)

        except AttributeError:
            continue


    df = pd.DataFrame(df_rows, columns = headers_list)

    df['year'] = year
    
    print(f'Success for {year} NFL playoffs!')

    return df

def get_mlb_regular_season(year):
    url = f'https://www.baseball-reference.com/leagues/majors/{year}-standings.shtml'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    
    # wait to not go to jail
    time.sleep(8)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('div', class_='table_wrapper')
    df_rows = []

    for table in tables:
        for tab in table.find_all('table'):
            headers_list = []

            # Get the headers
            for headers in tab.find('thead'):
                # skip the Navigable strings
                try:
                    if headers.find_all('th'):
                        for header in headers.find_all('th'):
                            headers_list.append(header.text)
                except AttributeError:
                    continue

            # Get the body data
            table_body = tab.find('tbody')
            for row in table_body.find_all('tr'):
                rows = []
                # skip the division name
                if row.find('td', class_='right left'):
                    continue
                for team in row.find_all('th'):
                    rows.append(team.text)
                for td in row.find_all('td'):
                    rows.append(td.text)
                df_rows.append(rows)
                
    df = pd.DataFrame(df_rows, columns=headers_list)
    df['year'] = year
    
    print(f'Success for {year} regular season!')
    
    return df

def get_mlb_playoffs(year):
    options = Options()
    options.headless = True
    b = webdriver.Chrome(options=options)

    b.get(f'https://www.baseball-reference.com/leagues/majors/{year}.shtml')

    soup = BeautifulSoup(b.page_source)
    
    time.sleep(4)
    
    b.close()

    # wait to not go to jail
    time.sleep(4)

    playoffs = soup.find('div', {'class': 'table_container is_setup', 'id': 'div_postseason'})

    df_rows = []
    headers_list = ['Round', 'Final Score', 'Winner', 'Loser']

    # Get the body data
    table_body = playoffs.find('tbody')
    for row in table_body.find_all('tr'):
        rows = []
        for td in row.find_all('td'):
            data = td.text
            split_data = data.split(' over ')
            rows.append(split_data)
        rows_flat = [item for sublist in rows for item in sublist]
        df_rows.append(rows_flat)

    df = pd.DataFrame(df_rows, columns=headers_list)

    df['year'] = year

    print(f'Success for {year} playoffs!')

    return df

def get_nba_regular_season(year):
    url = f'https://www.basketball-reference.com/leagues/NBA_{year}.html'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    # wait to not go to jail
    time.sleep(8)

    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find('div', class_='standings_divs data_grid section_wrapper')
    df_rows = []


    for table in tables:

        # Get headers
        try:
            if table.find('table'):

                try:
                    for headers in table.find_all('thead'):
                        headers_list = []

                        try:
                            if headers.find_all('th'):
                                for header in headers.find_all('th'):
                                    headers_list.append(header.text)

                        except AttributeError:
                            continue

                except TypeError:
                    continue

        except AttributeError:
             continue

        headers_list[0] = 'Team' # Get rid of conference name, replace with Team column header

        # Get the body data
        df_rows = []
        for table_body in table.find_all('tbody'):
            #print(table_body.text)

            for row in table_body.find_all('tr'):
                row_list = []

                # skip the division name
                if(len(row) <= 1):
                    continue

                # get team name
                for team in row.find('th'):

                    # skip the *
                    if len(team.text) <= 1:
                        continue
                    row_list.append(team.text)

                # get data for team
                for td in row.find_all('td'):
                    row_list.append(td.text)

                df_rows.append(row_list)

    df = pd.DataFrame(df_rows, columns=headers_list)

    df['year'] = year

    print(f'Success for {year} regular season!')
    
    return df

def get_nba_playoffs(year):
    options = Options()
    options.headless = True
    b = webdriver.Chrome(options=options)

    b.get(f'https://www.basketball-reference.com/leagues/NBA_{year}.html')

    soup = BeautifulSoup(b.page_source)
    
    time.sleep(5)

    b.close()
    
    # wait to not go to jail
    time.sleep(5)

    playoffs = soup.find('div', {'class': 'table_container', 'id': 'div_all_playoffs'})
    playoff_round = playoffs.find('tbody')

    df_rows = []
    headers_list = ['Round', 'Winner', 'Loser', 'Filler']

    # Get the body data
    for row in playoff_round.find_all('tr'):
        row_list = []
        for td in row.find_all('td'):
            data = td.text
            new_data = data.replace('\n', '')
            row_list.append(new_data.split(' over '))
        rows_list_flat = [item for sublist in row_list for item in sublist]

        if ('game' not in rows_list_flat[0].lower()) & (len(rows_list_flat) > 1):
            df_rows.append(rows_list_flat)

    df = pd.DataFrame(df_rows, columns=headers_list)

    # pull the loser's column out
    row_idx = 0
    records = []

    for loser in df['Loser']:
        df.iloc[row_idx, 2] = loser.split('\xa0')[0]
        records.append(loser.split('\xa0')[1])
        row_idx += 1

    df['Series Score'] = records
    df.drop('Filler', axis=1, inplace=True)
    
    df['year'] = year

    print(f'Success for {year} playoffs!')
    
    return df

def get_nhl_regular_season(year):
    url = f'https://www.hockey-reference.com/leagues/NHL_{year}_standings.html'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    # wait to not go to jail
    time.sleep(8)

    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find('div', class_='content_grid')
    df_rows = []


    for table in tables:

        # Get headers
        try:
            if table.find('table'):

                try:
                    for headers in table.find_all('thead'):
                        headers_list = []

                        try:
                            if headers.find_all('th'):
                                for header in headers.find_all('th'):
                                    headers_list.append(header.text)

                        except AttributeError:
                            continue

                except TypeError:
                    continue

        except AttributeError:
             continue

        headers_list[0] = 'Team' # Get rid of conference name, replace with Team column header

        # Get the body data
        for table_body in table.find_all('tbody'):
            #print(table_body.text)

            for row in table_body.find_all('tr'):
                row_list = []

                # skip the division name
                if(len(row) <= 1):
                    continue

                # get team name
                for team in row.find('th'):

                    # skip the *
                    if len(team.text) <= 1:
                        continue
                    row_list.append(team.text)

                # get data for team
                for td in row.find_all('td'):
                    row_list.append(td.text)

                df_rows.append(row_list)

    df = pd.DataFrame(df_rows, columns=headers_list)

    df['year'] = year
    
    print(f'Success for {year} regular season!')

    return df

def get_nhl_playoffs(year):
    url = f'https://www.hockey-reference.com/playoffs/NHL_{year}.html'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('tbody')
    
    # wait to not go to jail
    time.sleep(8)

    headers_list = ['Round', 'Series Score', 'Winner', 'Loser']

    df_rows = []

    for table_row in table.find_all('tr'):
        row_list = []

        for td in table_row.find_all('td'):
            if ' over ' in td.text:
                td_new = td.text
                row_list.append(td_new.split(' over '))
            else:
                row_list.append(td.text)

        rows_list_flat = row_list

        if 'Game' not in rows_list_flat[0] and len(rows_list_flat) > 1:
            row_list.pop(4)
            row_list.pop(3)
            df_rows.append(rows_list_flat)

    # flatten the rows
    new_df_rows = []

    for row in df_rows:
        new_row = []

        for item in row:
            if isinstance(item, list):
                for list_item in item:
                    new_row.append(list_item)
            else:
                new_row.append(item)

        new_df_rows.append(new_row)

    df = pd.DataFrame(new_df_rows, columns = headers_list)
    
    df['year'] = year

    print(f'Success for {year} playoffs!')
    
    return df

def get_mls_regular_season(year):
    url = f'https://fbref.com/en/comps/22/{year}/{year}-Major-League-Soccer-Stats'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    # wait to not go to jail
    time.sleep(7)

    soup = BeautifulSoup(response.text, 'html.parser')
    df_rows = []
    section = soup.find('div', {'class': 'section_content', 'id': 'div_Regular Season'})
    
    try:
        tables = section.find_all('table')
    
    except AttributeError:
        section = soup.find('div', {'id': f'all_results{year}221', 'class': 'table_wrapper tabbed'})
        tables = section.find_all('table')


    for table in tables:

        # Skip the Home/Away section
        header_section = table.find('thead')
        if header_section.find('tr', class_='over_header'):
            continue

        # Get headers
        for headers in table.find_all('thead'):
            headers_list = []
            if headers.find_all('th'):
                for header in headers.find_all('th'):
                    headers_list.append(header.text)

        # Get the body data
        for table_body in table.find_all('tbody'):
            for row in table_body.find_all('tr'):
                row_list = []

                # get team name
                for team in row.find('th'):
                    row_list.append(team.text)

                # get data for team
                for td in row.find_all('td'):
                    row_list.append(td.text)

                df_rows.append(row_list)

                
    df = pd.DataFrame(df_rows, columns=headers_list)

    df['year'] = year

    print(f'Success for {year} regular season!')

    return df

def get_mls_playoffs(year):
    url = f'https://fbref.com/en/comps/22/{year}/{year}-Major-League-Soccer-Stats'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    
    # wait to not go to jail
    time.sleep(7)
    

    playoffs = soup.find('div', {'id': 'content', 'role': 'main'})
    section = playoffs.find_all('table')

    df_rows = []

    if playoffs.find('div', {'class': 'section_wrapper', 'id': 'all_Conference Semifinals'}):
        #print('there are semis')

        semis = playoffs.find('div', {'class': 'section_wrapper', 'id': 'all_Conference Semifinals'})

        for table in semis.find_all('table'):
            data_row_semis = []

            try:
                team = table.find_all('td', {'class': 'left', 'data-stat': 'team'})
                for team_name in team:
                    teamname = team_name.text
                    data_row_semis.append(teamname.strip())

            except AttributeError:
                team = table.find('td', {'class': 'left', 'data-stat': 'team'})
                teamname = team.text
                data_row_semis.append(teamname.strip())

            data_row_semis.append('Conference Semifinal')
            df_rows.append(data_row_semis)

    if playoffs.find('div', {'class': 'section_wrapper', 'id': 'all_Quarter-finals'}):
        #print('there are quarters')

        quarters = playoffs.find('div', {'class': 'section_wrapper', 'id': 'all_Quarter-finals'})

        for table in quarters.find_all('table'):
            data_row_quarters = []

            try:
                team = table.find_all('td', {'class': 'left', 'data-stat': 'team'})
                for team_name in team:
                    teamname = team_name.text
                    data_row_quarters.append(teamname.strip())

            except AttributeError:
                team = table.find('td', {'class': 'left', 'data-stat': 'team'})
                teamname = team.text
                data_row_quarters.append(teamname.strip())

            data_row_quarters.append('Conference Quarterfinal')
            df_rows.append(data_row_quarters)

    if playoffs.find('div', {'class': 'section_wrapper', 'id': 'all_Semi-finals'}):
        #print('there are semis')

        semis = playoffs.find('div', {'class': 'section_wrapper', 'id': 'all_Semi-finals'})

        for table in semis.find_all('table'):
            data_row_semis = []

            try:
                team = table.find_all('td', {'class': 'left', 'data-stat': 'team'})
                for team_name in team:
                    teamname = team_name.text
                    data_row_semis.append(teamname.strip())

            except AttributeError:
                team = table.find('td', {'class': 'left', 'data-stat': 'team'})
                teamname = team.text
                data_row_semis.append(teamname.strip())

            data_row_semis.append('Conference Semifinal')
            df_rows.append(data_row_semis)

    if playoffs.find('div', {'class': 'section_wrapper', 'id': 'all_Conference Finals'}):
        #print('there are conference finals')

        conf_finals = playoffs.find('div', {'class': 'section_wrapper', 'id': 'all_Conference Finals'})

        for table in conf_finals.find_all('table'):
            data_row_conf = []

            try:
                team = table.find_all('td', {'class': 'left', 'data-stat': 'team'})
                for team_name in team:
                    teamname = team_name.text
                    data_row_conf.append(teamname.strip())

            except AttributeError:
                team = table.find('td', {'class': 'left', 'data-stat': 'team'})
                teamname = team.text
                data_row_conf.append(teamname.strip())

            data_row_conf.append('Conference Final')
            df_rows.append(data_row_conf)

    match_summary = playoffs.find_all('div', class_='match-summary')
    match_note = playoffs.find_all('div', class_='matchup-note')

    round_headers = playoffs.find_all('h3')
    #print(round_headers)

    if len(match_summary) == 1:
        matchup = match_summary[0]

        matchup_list = []
        for a in matchup.find_all('a'):
            matchup_list.append(a.text)

        score = matchup_list[1]
        scoreboard = score.split('–')

        home_score = scoreboard[0]
        home_team = matchup_list[0]

        away_score = scoreboard[1]
        away_team = matchup_list[2]

        if home_score > away_score:
            winner = home_team
            loser = away_team
        else:
            winner = away_team
            loser = home_team

        championship = []

        championship.append(winner)
        championship.append(loser)
        championship.append('MLS Cup')
        df_rows.append(championship)

    if len(match_summary) == 7:           # no knockout round format - 7 matches, starts 2003
        round_counter = 0

        for match in match_summary:
            round_counter += 1

            matchup_list = match.find_all('a')

            if len(matchup_list) == 2:

                home_team = matchup_list[0]
                away_team = matchup_list[1]


                score = match.find('div', class_='match-detail')
                game_score = score.text
                scores = game_score.split('–')

                home_score = scores[0].strip()
                away_score = scores[1].strip()
                
#                 print(f'home team is {home_team.text}')
#                 print(f'home score is {home_score}')
#                 print(f'away team is {away_team.text}')
#                 print(f'away score is {away_score}')

                if home_score > away_score:
                    #print(f'home team wins')
                    winner = home_team.text
                    loser = away_team.text
                elif away_score > home_score:
#                     print(f'away team wins {away_score} to {home_score}')
                    winner = away_team.text
                    loser = home_team.text
                else:
#                     print('heres a tie')
#                     print(f'away team is {away_team.text}')
#                     print(f'home team is {home_team.text}')
                    
                    winner = match_note[round_counter - 1].find('b').text

                    if winner == away_team.text:
#                         print('winner logic')
#                         print(f'winner is {winner}')
                        loser = home_team.text
#                         print(f'loser is {loser}')
                    else:
#                         print('loser logic')
#                         print(f'winner is {winner}')
                        loser = away_team.text
#                         print(f'loser is {loser}')

                championship = []

                championship.append(winner)
                championship.append(loser)
                championship.append(round_headers[0].text)
                df_rows.append(championship)

            if len(matchup_list) == 3:

                home_team = matchup_list[0]
                score = matchup_list[1]
                away_team = matchup_list[2]

                game_score = score.text
                scores = game_score.split('–')

                home_score = scores[0].strip()
                away_score = scores[1].strip()
                
#                 print(f'home team is {home_team.text}')
#                 print(f'home score is {home_score}')
#                 print(f'away team is {away_team.text}')
#                 print(f'away score is {away_score}')

                if home_score > away_score:
                    winner = home_team.text
                    loser = away_team.text
                elif away_score > home_score:
                    winner = away_team.text
                    loser = home_team.text
                else:
#                     print('heres a tie')
#                     print(f'away team is {away_team.text}')
#                     print(f'home team is {home_team.text}')
                    
                    winner = match_note[round_counter - 1].find('b').text
                    

                    if winner == away_team.text:
#                         print('winner logic')
#                         print(f'winner is {winner}')
                        loser = home_team.text
#                         print(f'loser is {loser}')
                    else:
#                         print('loser logic')
#                         print(f'winner is {winner}')
                        loser = away_team.text
#                         print(f'loser is {loser}')

                championship = []

                championship.append(winner)
                championship.append(loser)
                if round_counter == len(match_summary):
                    championship.append(round_headers[2].text)
                else:
                    championship.append(round_headers[1].text)
                df_rows.append(championship)

    #print(len(match_summary))

    if len(match_summary) == 9 and len(round_headers) == 5:               # Knockout round format - 9 matches
        round_counter = 0

        for match in match_summary:
            round_counter += 1

            #print(match.text)

            matchup_list = match.find_all('a')

            #print(len(matchup_list))

            if len(matchup_list) == 2:

                home_team = matchup_list[0]
                away_team = matchup_list[1]


                score = match.find('div', class_='match-detail')
                game_score = score.text
                scores = game_score.split('–')

                home_score = scores[0].strip()
                away_score = scores[1].strip()

                if home_score > away_score:
                    winner = home_team.text
                    loser = away_team.text
                elif away_score > home_score:
                    winner = away_team.text
                    loser = home_team.text
                else:
                    winner = match_note[round_counter - 1].find('b').text

                    if winner == away_team.text:
                        loser = home_team.text
                    else:
                        loser = away_team.text

                championship = []

                championship.append(winner)
                championship.append(loser)
                championship.append(round_headers[1].text)
                df_rows.append(championship)

            if len(matchup_list) == 3:

                home_team = matchup_list[0]
                score = matchup_list[1]
                away_team = matchup_list[2]

                game_score = score.text
                scores = game_score.split('–')

                home_score = scores[0].strip()
                away_score = scores[1].strip()

                if home_score > away_score:
                    winner = home_team.text
                    loser = away_team.text
                elif away_score > home_score:
                    winner = away_team.text
                    loser = home_team.text
                else:
                    winner = match_note[round_counter - 1].find('b').text

                    if winner == away_team.text:
                        loser = home_team.text
                    else:
                        loser = away_team.text

                championship = []

                championship.append(winner)
                championship.append(loser)
                if round_counter == len(match_summary):
                    championship.append(round_headers[3].text)
                elif round_counter == 1 or round_counter == 2:
                    championship.append(round_headers[0].text)
                else:
                    championship.append(round_headers[2].text)
                df_rows.append(championship)

    # need to do the 11 match playoffs now, starts 2015
    if len(match_summary) == 11:               # Knockout round format - 11 matches
        round_counter = 0

        for match in match_summary:
            round_counter += 1

            #print(match.text)

            matchup_list = match.find_all('a')

            #print(len(matchup_list))

            if len(matchup_list) == 2:

                home_team = matchup_list[0]
                away_team = matchup_list[1]


                score = match.find('div', class_='match-detail')
                game_score = score.text
                scores = game_score.split('–')

                home_score = scores[0].strip()
                away_score = scores[1].strip()

                if home_score > away_score:
                    winner = home_team.text
                    loser = away_team.text
                elif away_score > home_score:
                    winner = away_team.text
                    loser = home_team.text
                else:
                    winner = match_note[round_counter - 1].find('b').text

                    if winner == away_team.text:
                        loser = home_team.text
                    else:
                        loser = away_team.text

                championship = []

                championship.append(winner)
                championship.append(loser)
                if round_counter in [5, 6, 7, 8]:
                    championship.append(round_headers[1].text)
                else:
                    championship.append(round_headers[2].text)
                df_rows.append(championship)

            if len(matchup_list) == 3:

                home_team = matchup_list[0]
                score = matchup_list[1]
                away_team = matchup_list[2]

                game_score = score.text
                scores = game_score.split('–')

                home_score = scores[0].strip()
                away_score = scores[1].strip()

                if home_score > away_score:
                    winner = home_team.text
                    loser = away_team.text
                elif away_score > home_score:
                    winner = away_team.text
                    loser = home_team.text
                else:
                    winner = match_note[round_counter - 1].find('b').text

                    if winner == away_team.text:
                        loser = home_team.text
                    else:
                        loser = away_team.text

                championship = []

                championship.append(winner)
                championship.append(loser)
                if round_counter == len(match_summary):
                    championship.append(round_headers[3].text)
                elif round_counter in [1, 2, 3, 4]:
                    championship.append(round_headers[0].text)
                else:
                    championship.append(round_headers[2].text)
                df_rows.append(championship)

    # 13 round format next
    if len(match_summary) == 13:               # Round 1 format - 13 matches
        round_counter = 0

        for match in match_summary:
            round_counter += 1

            #print(match.text)

            matchup_list = match.find_all('a')

            #print(len(matchup_list))

            if len(matchup_list) == 2:

                home_team = matchup_list[0]
                away_team = matchup_list[1]


                score = match.find('div', class_='match-detail')
                game_score = score.text
                scores = game_score.split('–')

                home_score = scores[0].strip()
                away_score = scores[1].strip()

                if home_score > away_score:
                    winner = home_team.text
                    loser = away_team.text
                elif away_score > home_score:
                    winner = away_team.text
                    loser = home_team.text
                else:
                    winner = match_note[round_counter - 1].find('b').text

                    if winner == away_team.text:
                        loser = home_team.text
                    else:
                        loser = away_team.text

                championship = []

                championship.append(winner)
                championship.append(loser)
                if round_counter in [5, 6, 7, 8]:
                    championship.append(round_headers[1].text)
                else:
                    championship.append(round_headers[2].text)
                df_rows.append(championship)

            if len(matchup_list) == 3:

                home_team = matchup_list[0]
                score = matchup_list[1]
                away_team = matchup_list[2]

                game_score = score.text
                scores = game_score.split('–')

                home_score = scores[0].strip()
                away_score = scores[1].strip()

                if home_score > away_score:
                    winner = home_team.text
                    loser = away_team.text
                elif away_score > home_score:
                    winner = away_team.text
                    loser = home_team.text
                else:
                    winner = match_note[round_counter - 1].find('b').text

                    if winner == away_team.text:
                        loser = home_team.text
                    else:
                        loser = away_team.text

                championship = []

                championship.append(winner)
                championship.append(loser)
                if round_counter == len(match_summary):
                    championship.append(round_headers[3].text)
                elif round_counter in [1, 2, 3, 4, 5, 6]:
                    championship.append(round_headers[0].text)
                elif round_counter in [7, 8, 9, 10]:
                    championship.append(round_headers[1].text)
                else:
                    championship.append(round_headers[2].text)
                df_rows.append(championship)
                
    # 2020 is super weird
    if len(match_summary) == 30:
        round_counter = 0
        
        forbidden = list(range(0, 16))
        #print(forbidden)

        for match in match_summary:
            round_counter += 1
            if round_counter in forbidden:
                continue

            #print(match.text)

            matchup_list = match.find_all('a')

            #print(len(matchup_list))

            if len(matchup_list) == 3:

                home_team = matchup_list[0]
                score = matchup_list[1]
                away_team = matchup_list[2]

                game_score = score.text
                scores = game_score.split('–')

                home_score = scores[0].strip()
                away_score = scores[1].strip()

                if home_score > away_score:
                    winner = home_team.text
                    loser = away_team.text
                elif away_score > home_score:
                    winner = away_team.text
                    loser = home_team.text
                else:
                    winner = match_note[round_counter - 1].find('b').text

                    if winner == away_team.text:
                        loser = home_team.text
                    else:
                        loser = away_team.text

                championship = []

                championship.append(winner)
                championship.append(loser)
                if round_counter == len(match_summary):
                    championship.append(round_headers[13].text)
                elif round_counter in [16, 17, 18, 19, 20, 21, 22, 23]:
                    championship.append(round_headers[10].text)
                elif round_counter in [24, 25, 26, 27]:
                    championship.append(round_headers[11].text)
                else:
                    championship.append(round_headers[12].text)
                df_rows.append(championship)
        

    # 2023 has a unique format, 9 match_summary but more than that actually, combo of above
    if len(match_summary) == 9 and len(round_headers) == 13:
        round_counter = 0

        for match in match_summary:
            round_counter += 1

            matchup_list = match.find_all('a')

            if len(matchup_list) == 3:

                home_team = matchup_list[0]
                score = matchup_list[1]
                away_team = matchup_list[2]

                game_score = score.text
                scores = game_score.split('–')

                home_score = scores[0].strip()
                away_score = scores[1].strip()

                if home_score > away_score:
                    winner = home_team.text
                    loser = away_team.text
                elif away_score > home_score:
                    winner = away_team.text
                    loser = home_team.text
                else:
                    winner = match_note[round_counter - 1].find('b').text

                    if winner == away_team.text:
                        loser = home_team.text
                    else:
                        loser = away_team.text

                championship = []

                championship.append(winner)
                championship.append(loser)
                if round_counter == len(match_summary):
                    championship.append(round_headers[11].text)
                elif round_counter in [1, 2]:
                    championship.append(round_headers[0].text)
                elif round_counter in [3, 4, 5, 6]:
                    championship.append(round_headers[9].text)
                else:
                    championship.append(round_headers[10].text)
                df_rows.append(championship)

        round_one = soup.find('div', {'class': 'section_content', 'id': 'div_Round One'})
        for table in round_one.find_all('tbody'):
            round_one_row = []

            for row in table.find_all('tr'):
                team = row.find('a')
                round_one_row.append(team.text)

            round_one_row.append('Round One')

            df_rows.append(round_one_row)
            
    df = pd.DataFrame(df_rows, columns = ['Winner', 'Loser', 'Round'])
    
    df['year'] = year
    
    print(f'Success for {year} playoffs!')

    return df

# function that will write any given year to separate reg and playoff files in that league's folder

def get_next_year(league, year):
    if league == 'nfl':
        reg_season = get_nfl_regular_season(year)
        playoffs = get_nfl_playoffs(year)
    elif league == 'mlb':
        reg_season = get_mlb_regular_season(year)
        playoffs = get_mlb_playoffs(year)
    elif league == 'nba':
        reg_season = get_nba_regular_season(year)
        playoffs = get_nba_playoffs(year)
    elif league == 'nhl':
        reg_season = get_nhl_regular_season(year)
        playoffs = get_nhl_playoffs(year)
    elif league == 'mls':
        reg_season = get_mls_regular_season(year)
        playoffs = get_mls_playoffs(year)
        
    folder_path = f'./{league}'
    
    reg_season.to_csv(folder_path + f'/{league}_{year}_regular_season.csv', index = False)
    playoffs.to_csv(folder_path + f'/{league}_{year}_playoffs.csv', index = False)
    
    league_name = league.upper()
    
    return print(f'Saved files for the {year} {league_name} season!')

#get_next_year('mls', 2024)

#get_next_year('nfl', 2024)

