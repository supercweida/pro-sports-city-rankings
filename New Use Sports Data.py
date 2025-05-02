import pandas as pd
import warnings
import numpy as np
import sqlite3

# Establish the values for the formula

# Winning Percentage + Made Playoffs Bonus + Multiplier * (Playoff Distance Bonus/Max Playoff Points)

made_playoffs_bonus = 2

scoring_multiplier = 12

max_playoff_points = 400

champ_winner_bonus = 400
champ_loser_bonus = 200
semis_loser_bonus = 100
quarters_loser_bonus = 50
wc_loser_bonus = 25

# add in the league specific multiplier

nfl_revenue = 20.24 # NFL revenue was $20.24 Billion in 2023
mlb_revenue = 11.6 # MLB revenue was $11.6 Billion in 2023
nba_revenue = 11.34 # NBA revenue was $11.34 Billion in 2023
nhl_revenue = 6.3 # NHL revenue was $6.3 Billion in 2023
mls_revenue = 2 # MLS revenue was $2 Billion in 2023

total_revenue = (nfl_revenue + mlb_revenue + nba_revenue + nhl_revenue + mls_revenue)

nfl_revenue_multiplier = round(nfl_revenue / (total_revenue), 3) * 10
mlb_revenue_multiplier = round(mlb_revenue / (total_revenue), 3) * 10
nba_revenue_multiplier = round(nba_revenue / (total_revenue), 3) * 10
nhl_revenue_multiplier = round(nhl_revenue / (total_revenue), 3) * 10
mls_revenue_multiplier = round(mls_revenue / (total_revenue), 3) * 10

#print(nfl_revenue_multiplier)
#print(mls_revenue_multiplier)

# write the base data to dataframes for 1980 to present

folder_path = "./nfl"

nfl_regular_season_pre = pd.read_csv(folder_path + '/nfl_regular_season.csv')
nfl_playoffs_pre = pd.read_csv(folder_path + '/nfl_playoffs.csv')

folder_path = "./mlb"

mlb_regular_season_pre = pd.read_csv(folder_path + '/mlb_regular_season.csv')
mlb_playoffs_pre = pd.read_csv(folder_path + '/mlb_playoffs.csv')

folder_path = "./nba"

nba_regular_season_pre = pd.read_csv(folder_path + '/nba_regular_season.csv')
nba_playoffs_pre = pd.read_csv(folder_path + '/nba_playoffs.csv')

folder_path = "./nhl"

nhl_regular_season_pre = pd.read_csv(folder_path + '/nhl_regular_season.csv')
nhl_playoffs_pre = pd.read_csv(folder_path + '/nhl_playoffs.csv')

folder_path = "./mls"

mls_regular_season_pre = pd.read_csv(folder_path + '/mls_regular_season.csv')
mls_playoffs_pre = pd.read_csv(folder_path + '/mls_playoffs.csv')


# Read in the city to region mappings

sports_cities_df = pd.read_csv('./sports_cities_region.txt', sep="\t")

# functions to append any new years to the already existent base dataframes

def append_newest_year_regular_season(league, years_to_append, regular_season_df):
    regular_seasons_to_concat = []
    regular_seasons_to_concat.append(regular_season_df)
    
    if len(years_to_append) > 0:
    
        for year in years_to_append:
            league_name = league.upper()

            print(f'Appending regular season for {year} {league_name} season.')

            folder_path = f'./{league}'

            new_regular_season = pd.read_csv(folder_path + f'/{league}_{year}_regular_season.csv')
            
            regular_seasons_to_concat.append(new_regular_season)
            
        return pd.concat(regular_seasons_to_concat)
    
    else:
        league_name = league.upper()
        
        print(f'No regular season to append for the {league_name}.')
        
        return regular_season_df

def append_newest_year_playoffs(league, years_to_append, playoffs_df):
    playoffs_to_concat = []
    playoffs_to_concat.append(playoffs_df)
    
    if len(years_to_append) > 0:
    
        for year in years_to_append:
            league_name = league.upper()

            print(f'Appending playoffs for {year} {league_name} season.')

            folder_path = f'./{league}'

            new_playoffs = pd.read_csv(folder_path + f'/{league}_{year}_playoffs.csv')
            
            playoffs_to_concat.append(new_playoffs)
            
        return pd.concat(playoffs_to_concat)
    
    else:
        league_name = league.upper()
        
        print(f'No playoffs to append for the {league_name}.')
        
        return playoffs_df
    

# Apply the proper additions to each respective league - This will need to be adjusted periodically

years_to_append = [2024]

nfl_regular_season = append_newest_year_regular_season('nfl', years_to_append, nfl_regular_season_pre)
nfl_playoffs = append_newest_year_playoffs('nfl', years_to_append, nfl_playoffs_pre)

mlb_regular_season = append_newest_year_regular_season('mlb', years_to_append, mlb_regular_season_pre)
mlb_playoffs = append_newest_year_playoffs('mlb', years_to_append, mlb_playoffs_pre)

nba_regular_season = append_newest_year_regular_season('nba', years_to_append, nba_regular_season_pre)
nba_playoffs = append_newest_year_playoffs('nba', years_to_append, nba_playoffs_pre)

nhl_regular_season = append_newest_year_regular_season('nhl', years_to_append, nhl_regular_season_pre)
nhl_playoffs = append_newest_year_playoffs('nhl', years_to_append, nhl_playoffs_pre)

mls_regular_season = append_newest_year_regular_season('mls', years_to_append, mls_regular_season_pre)
mls_playoffs = append_newest_year_playoffs('mls', years_to_append, mls_playoffs_pre)

# re-format the NFL, MLB, NBA, NHL, MLS

nfl_regular_season_new = nfl_regular_season[['year', 'Tm', 'W-L%', 'W', 'L']]
nfl_regular_season_new.columns = ['Year', 'Team', 'WP', 'W', 'L']

nfl_playoffs_new = nfl_playoffs[['year', 'Week', 'Winner/tie', 'Loser/tie']]
nfl_playoffs_new.columns = ['Year', 'Round', 'Winner', 'Loser']

mlb_regular_season_new = mlb_regular_season[['year', 'Tm', 'W-L%', 'W', 'L']]
mlb_regular_season_new.columns = ['Year', 'Team', 'WP', 'W', 'L']

mlb_playoffs_new = mlb_playoffs[['year', 'Round', 'Winner', 'Loser']]
mlb_playoffs_new.columns = ['Year', 'Round', 'Winner', 'Loser']

nba_regular_season_new = nba_regular_season[['year', 'Team', 'W/L%', 'W', 'L']]
nba_regular_season_new.columns = ['Year', 'Team', 'WP', 'W', 'L']

nba_playoffs_new = nba_playoffs[['year', 'Round', 'Winner', 'Loser']]
nba_playoffs_new.columns = ['Year', 'Round', 'Winner', 'Loser']

nhl_regular_season['WL%'] = round(nhl_regular_season['W'] / nhl_regular_season['GP'], 3)
nhl_regular_season_new = nhl_regular_season[['year', 'Team', 'WL%', 'W', 'L', 'T']]
nhl_regular_season_new.columns = ['Year', 'Team', 'WP', 'W', 'L', 'T']

nhl_playoffs_new = nhl_playoffs[['year', 'Round', 'Winner', 'Loser']]
nhl_playoffs_new.columns = ['Year', 'Round', 'Winner', 'Loser']

mls_regular_season['WL%'] = round(mls_regular_season['W'] / mls_regular_season['MP'], 3)
mls_regular_season_new = mls_regular_season[['year', 'Squad', 'WL%', 'W', 'L', 'D']]
mls_regular_season_new.columns = ['Year', 'Team', 'WP', 'W', 'L', 'T']

mls_playoffs_new = mls_playoffs[['year', 'Round', 'Winner', 'Loser']]
mls_playoffs_new.columns = ['Year', 'Round', 'Winner', 'Loser']

# write a function that joins up the regular season and playoffs for the NFL

# should have a column for what happened in the playoffs, 1 or 0

def get_nfl_indicator_columns(regular_season, playoffs):
    
    results = regular_season.copy()

    for playoff_round in list(playoffs['Round'].unique()):

        current_round = playoffs[playoffs['Round'] == playoff_round]

        winners_merge = pd.merge(regular_season, current_round, left_on = ['Year', 'Team'],
                             right_on = ['Year', 'Winner'], how = 'left')
        losers_merge = pd.merge(regular_season, current_round, left_on = ['Year', 'Team'],
                         right_on = ['Year', 'Loser'], how = 'left')

        results[f'{playoff_round} Winner'] = (winners_merge['Team'] == winners_merge['Winner']).astype(int)
        results[f'{playoff_round} Loser'] = (losers_merge['Team'] == losers_merge['Loser']).astype(int)

    return results

# reformat the NFL specifically, joining up the two dataframes

warnings.filterwarnings('ignore')

# first need to reformat the Team column to not have the asterisk or plus sign

nfl_regular_season_new['Team'] = nfl_regular_season_new['Team'].str.replace("*","")
nfl_regular_season_new['Team'] = nfl_regular_season_new['Team'].str.replace("+","")

# Save the results

nfl_results = get_nfl_indicator_columns(nfl_regular_season_new, nfl_playoffs_new)

# implement the universal formula

# Winning Percentage + Made Playoffs Bonus + Multiplier * (Playoff Distance Bonus/Max Playoff Points)

# Create a copy of the df

nfl_results_copy = nfl_results.copy()

# Find the teams that made the playoffs

nfl_results_copy['Playoff Sum'] = (nfl_results_copy['WildCard Winner'] + nfl_results_copy['WildCard Loser'] + 
                                   nfl_results_copy['Division Winner'] + nfl_results_copy['Division Loser'] + 
                                   nfl_results_copy['ConfChamp Winner'] + nfl_results_copy['ConfChamp Loser'] +
                                   nfl_results_copy['SuperBowl Winner'] + nfl_results_copy['SuperBowl Loser'])

# Create a playoff indicator column

nfl_results_copy['Playoff Indicator'] = np.where(nfl_results_copy['Playoff Sum'] > 0, 1, 0)

# Assign the playoff bonuses to new columns and an aggregated column

nfl_results_copy['Made Playoffs Bonus'] = np.where(nfl_results_copy['Playoff Indicator'] == 1, made_playoffs_bonus, 0)

nfl_results_copy['SB Winner Bonus'] = np.where(nfl_results_copy['SuperBowl Winner'] == 1, champ_winner_bonus, 0)
nfl_results_copy['SB Loser Bonus'] = np.where(nfl_results_copy['SuperBowl Loser'] == 1, champ_loser_bonus, 0)
nfl_results_copy['CC Loser Bonus'] = np.where(nfl_results_copy['ConfChamp Loser'] == 1, semis_loser_bonus, 0)
nfl_results_copy['DIV Loser Bonus'] = np.where(nfl_results_copy['Division Loser'] == 1, quarters_loser_bonus, 0)
nfl_results_copy['WC Loser Bonus'] = np.where(nfl_results_copy['WildCard Loser'] == 1, wc_loser_bonus, 0)

nfl_results_copy['Playoff Distance Bonus'] = (nfl_results_copy['SB Winner Bonus'] + nfl_results_copy['SB Loser Bonus'] +
                                             nfl_results_copy['CC Loser Bonus'] + nfl_results_copy['DIV Loser Bonus'] +
                                             nfl_results_copy['WC Loser Bonus'])

# Implement the formula into a new column

nfl_results_copy['Formula Result'] = (nfl_results_copy['WP'] + nfl_results_copy['Made Playoffs Bonus'] +
                                      scoring_multiplier * 
                                      (nfl_results_copy['Playoff Distance Bonus']/max_playoff_points))

# Save the results to a final dataframe with the forumula's result

nfl_results_final = nfl_results_copy[['Year', 'Team', 'Formula Result']]

# Get the distinct list of hosts for the NFL

#nfl_results_1 = pd.DataFrame(nfl_results_final.groupby('Team')['Formula Result'].sum())

nfl_hosts = []

for team in nfl_results_final['Team'].unique():
    current_team = team.split(' ')
    #print(current_team)
    if len(current_team) == 2:
        nfl_hosts.append(current_team[0])
    elif current_team[0] == 'Washington':
        nfl_hosts.append(current_team[0])
    else:
        multi = current_team[0] + ' ' + current_team[1]
        nfl_hosts.append(multi)
        
nfl_host_cities = list(set(nfl_hosts))

# write a function that joins up the regular season and playoffs for the MLB

# should have a column for what happened in the playoffs, 1 or 0

def get_mlb_indicator_columns(regular_season, playoffs):

    new_mlb = []
    
    years_list = list(regular_season['Year'].unique())

    for year in years_list:

        mlb_play = playoffs[playoffs['Year'] == year]
        mlb_reg = regular_season[regular_season['Year'] == year]

        new_mlb_temp = mlb_reg.copy().copy()

        for playoff_round in list(mlb_play['Round'].unique()):

            current_round = mlb_play[mlb_play['Round'] == playoff_round]

            round_winners = list(current_round['Winner'])

            round_losers = list(current_round['Loser'])  

            winner_list = []
            loser_list = []

            for index, row in mlb_reg.iterrows():
                if row['Team'] in round_losers:
                    loser_list.append(1)
                else:
                    loser_list.append(0)
                if row['Team'] in round_winners:
                    winner_list.append(1)
                else:
                    winner_list.append(0)

            new_mlb_temp[f'{playoff_round} Winner'] = winner_list
            new_mlb_temp[f'{playoff_round} Loser'] = loser_list

        new_mlb.append(new_mlb_temp)

    mlb_new_df = pd.concat(new_mlb)

    return mlb_new_df

# save the MLB results

mlb_results = get_mlb_indicator_columns(mlb_regular_season_new, mlb_playoffs_new)

# implement the universal formula

# Winning Percentage + Made Playoffs Bonus + Multiplier * (Playoff Distance Bonus/Max Playoff Points)


# Create a copy of the df

mlb_results_copy = mlb_results.copy()

# Combine the Wild Card round columns

mlb_results_copy['WC Winner'] = (mlb_results_copy['Wild Card Game Winner'].fillna(0) + 
                                 mlb_results_copy['Wild Card Series Winner'].fillna(0))

mlb_results_copy['WC Loser'] = (mlb_results_copy['Wild Card Game Loser'].fillna(0) + 
                                 mlb_results_copy['Wild Card Series Loser'].fillna(0))

# Find the teams that made the playoffs

mlb_results_copy['Made Playoffs Indicator'] = (mlb_results_copy['World Series Winner'].fillna(0) + 
                                               mlb_results_copy['World Series Loser'].fillna(0) +
                                              mlb_results_copy['ALCS Winner'].fillna(0) +
                                              mlb_results_copy['NLCS Winner'].fillna(0) +
                                              mlb_results_copy['ALCS Loser'].fillna(0) +
                                              mlb_results_copy['NLCS Loser'].fillna(0) +
                                              mlb_results_copy['AL Division Series Winner'].fillna(0) +
                                              mlb_results_copy['AL Division Series Loser'].fillna(0) +
                                              mlb_results_copy['NL Division Series Winner'].fillna(0) +
                                              mlb_results_copy['NL Division Series Loser'].fillna(0) +
                                              mlb_results_copy['WC Winner'] + mlb_results_copy['WC Loser'])

# Create a playoff indicator column

mlb_results_copy['Playoff Indicator'] = np.where(mlb_results_copy['Made Playoffs Indicator'] > 0, 1, 0)

# Assign the playoff bonuses to a new column and make an aggregated column

mlb_results_copy['Made Playoffs Bonus'] = np.where(mlb_results_copy['Playoff Indicator'] == 1, made_playoffs_bonus, 0)

mlb_results_copy['WS Winner Bonus'] = np.where(mlb_results_copy['World Series Winner'] == 1, champ_winner_bonus, 0)
mlb_results_copy['WS Loser Bonus'] = np.where(mlb_results_copy['World Series Loser'] == 1, champ_loser_bonus, 0)
mlb_results_copy['ALCS Loser Bonus'] = np.where(mlb_results_copy['ALCS Loser'] == 1, semis_loser_bonus, 0)
mlb_results_copy['NLCS Loser Bonus'] = np.where(mlb_results_copy['NLCS Loser'] == 1, semis_loser_bonus, 0)
mlb_results_copy['ALDS Loser Bonus'] = np.where(mlb_results_copy['AL Division Series Loser'] == 1, 
                                                quarters_loser_bonus, 0)
mlb_results_copy['NLDS Loser Bonus'] = np.where(mlb_results_copy['NL Division Series Loser'] == 1, 
                                                quarters_loser_bonus, 0)
mlb_results_copy['WC Loser'] = np.where(mlb_results_copy['WC Loser'] == 1, wc_loser_bonus, 0)

mlb_results_copy['Playoff Distance Bonus'] = (mlb_results_copy['WS Winner Bonus'] + 
                                              mlb_results_copy['WS Loser Bonus'] +
                                             mlb_results_copy['ALCS Loser Bonus'] +
                                             mlb_results_copy['NLCS Loser Bonus'] +
                                             mlb_results_copy['ALDS Loser Bonus'] +
                                             mlb_results_copy['NLDS Loser Bonus'] +
                                             mlb_results_copy['WC Loser'])

# Implement the formula into a new column

mlb_results_copy['Formula Result'] = (mlb_results_copy['WP'] + mlb_results_copy['Made Playoffs Bonus'] +
                                      scoring_multiplier * 
                                      (mlb_results_copy['Playoff Distance Bonus']/max_playoff_points))

# Save the results to a final dataframe with the forumula's result

mlb_results_final = mlb_results_copy[['Year', 'Team', 'Formula Result']]


# Get the distinct list of hosts for the MLB

#mlb_results_1 = pd.DataFrame(mlb_results_final.groupby('Team')['Formula Result'].sum())

mlb_hosts = []

for team in mlb_results_final['Team'].unique():
    current_team = team.split(' ')
    if len(current_team) == 2:
        mlb_hosts.append(current_team[0])
    else:
        if current_team[0] in ['Boston', 'Toronto', 'Chicago']:
            mlb_hosts.append(current_team[0])
        else:
            multi = current_team[0] + ' ' + current_team[1]
            mlb_hosts.append(multi)
        
mlb_host_cities = list(set(mlb_hosts))

# write a function that joins up the regular season and playoffs for the NBA

# should have a column for what happened in the playoffs, 1 or 0

def get_indicator_columns(regular_season, playoffs):

    new_league_list = []
    
    years_list = list(regular_season['Year'].unique())

    for year in years_list:

        league_play = playoffs[playoffs['Year'] == year]
        league_reg = regular_season[regular_season['Year'] == year]

        new_league_temp = league_reg.copy().copy()

        for playoff_round in list(league_play['Round'].unique()):

            current_round = league_play[league_play['Round'] == playoff_round]

            round_winners = list(current_round['Winner'])

            round_losers = list(current_round['Loser'])  

            winner_list = []
            loser_list = []

            for index, row in league_reg.iterrows():
                if row['Team'] in round_losers:
                    loser_list.append(1)
                else:
                    loser_list.append(0)
                if row['Team'] in round_winners:
                    winner_list.append(1)
                else:
                    winner_list.append(0)

            new_league_temp[f'{playoff_round} Winner'] = winner_list
            new_league_temp[f'{playoff_round} Loser'] = loser_list

        new_league_list.append(new_league_temp)

    league_new_df = pd.concat(new_league_list)

    return league_new_df

# Save the results

nba_results = get_indicator_columns(nba_regular_season_new, nba_playoffs_new)

# implement the universal formula

# Winning Percentage + Made Playoffs Bonus + Multiplier * (Playoff Distance Bonus/Max Playoff Points)


# Create a copy of the df

nba_results_copy = nba_results.copy()

# Find the teams that made the playoffs

nba_results_copy['Made Playoffs'] = (nba_results_copy['Finals Winner'] + nba_results_copy['Finals Loser'] +
                                    nba_results_copy['Eastern Conference Finals Loser'] +
                                    nba_results_copy['Western Conference Finals Loser'] +
                                    nba_results_copy['Eastern Conference Semifinals Loser'] +
                                    nba_results_copy['Western Conference Semifinals Loser'] +
                                    nba_results_copy['Eastern Conference First Round Loser'] +
                                    nba_results_copy['Western Conference First Round Loser'])

# Create a playoff indicator column

nba_results_copy['Playoff Indicator'] = np.where(nba_results_copy['Made Playoffs'] > 0, 1, 0)

# Assign the playoff bonuses to a new column and make an aggregated column

nba_results_copy['Made Playoffs Bonus'] = np.where(nba_results_copy['Playoff Indicator'] == 1, made_playoffs_bonus, 0)

nba_results_copy['Finals Winner Bonus'] = np.where(nba_results_copy['Finals Winner'] == 1, champ_winner_bonus, 0)
nba_results_copy['Finals Loser Bonus'] = np.where(nba_results_copy['Finals Loser'] == 1, champ_loser_bonus, 0)
nba_results_copy['WCF Loser Bonus'] = np.where(nba_results_copy['Western Conference Finals Loser'] == 1,
                                              semis_loser_bonus, 0)
nba_results_copy['ECF Loser Bonus'] = np.where(nba_results_copy['Eastern Conference Finals Loser'] == 1,
                                              semis_loser_bonus, 0)
nba_results_copy['WCSF Loser Bonus'] = np.where(nba_results_copy['Western Conference Semifinals Loser'] == 1,
                                              quarters_loser_bonus, 0)
nba_results_copy['ECSF Loser Bonus'] = np.where(nba_results_copy['Eastern Conference Semifinals Loser'] == 1,
                                              quarters_loser_bonus, 0)
nba_results_copy['WCFR Loser Bonus'] = np.where(nba_results_copy['Western Conference First Round Loser'] == 1,
                                              wc_loser_bonus, 0)
nba_results_copy['ECFR Loser Bonus'] = np.where(nba_results_copy['Eastern Conference First Round Loser'] == 1,
                                              wc_loser_bonus, 0)

nba_results_copy['Playoff Distance Bonus'] = (nba_results_copy['Finals Winner Bonus'] +
                                             nba_results_copy['Finals Loser Bonus'] +
                                             nba_results_copy['WCF Loser Bonus'] +
                                             nba_results_copy['ECF Loser Bonus'] +
                                             nba_results_copy['WCSF Loser Bonus'] +
                                             nba_results_copy['ECSF Loser Bonus'] +
                                             nba_results_copy['WCFR Loser Bonus'] +
                                             nba_results_copy['ECFR Loser Bonus'])

# Implement the formula into a new column

nba_results_copy['Formula Result'] = (nba_results_copy['WP'] + nba_results_copy['Made Playoffs Bonus'] +
                                      scoring_multiplier * 
                                      (nba_results_copy['Playoff Distance Bonus']/max_playoff_points))

# Save the results to a final dataframe with the forumula's result

nba_results_final = nba_results_copy[['Year', 'Team', 'Formula Result']]


# Get the distinct list of hosts for the MLB

#nba_results_1 = pd.DataFrame(nba_results_final.groupby('Team')['Formula Result'].sum())

nba_hosts = []

for team in nba_results_final['Team'].unique():
    current_team = team.split(' ')
    if len(current_team) == 2:
        nba_hosts.append(current_team[0])
    else:
        if current_team[0] in ['Portland']:
            nba_hosts.append(current_team[0])
        else:
            if 'Oklahoma' in current_team[1]:
                nba_hosts.append('New Orleans')
            else:
                multi = current_team[0] + ' ' + current_team[1]
                nba_hosts.append(multi)
        
nba_host_cities = list(set(nba_hosts))

# Save the results

nhl_results = get_indicator_columns(nhl_regular_season_new, nhl_playoffs_new)


# implement the universal formula for the NHL

# Winning Percentage + Made Playoffs Bonus + Multiplier * (Playoff Distance Bonus/Max Playoff Points)

# Create a copy of the df

nhl_results_copy = nhl_results.copy()

# Find the teams that made the playoffs

nhl_results_copy['Made Playoffs'] = (nhl_results_copy['Final Winner'].fillna(0) + 
                                    nhl_results_copy['Final Loser'].fillna(0) +
                                    nhl_results_copy['Semi-Finals Winner'].fillna(0) +
                                    nhl_results_copy['Semi-Finals Loser'].fillna(0) +
                                    nhl_results_copy['Quarter-Finals Winner'].fillna(0) +
                                     nhl_results_copy['Quarter-Finals Loser'].fillna(0) +
                                     nhl_results_copy['Preliminary Round Winner'].fillna(0) +
                                     nhl_results_copy['Preliminary Round Loser'].fillna(0) +
                                     nhl_results_copy['Conference Finals Winner'].fillna(0) +
                                     nhl_results_copy['Conference Finals Loser'].fillna(0) +
                                     nhl_results_copy['Division Finals Winner'].fillna(0) +
                                     nhl_results_copy['Division Finals Loser'].fillna(0) +
                                     nhl_results_copy['Division Semi-Finals Winner'].fillna(0) +
                                     nhl_results_copy['Division Semi-Finals Loser'].fillna(0) +
                                     nhl_results_copy['Conference Semi-Finals Winner'].fillna(0) +
                                     nhl_results_copy['Conference Semi-Finals Loser'].fillna(0) +
                                     nhl_results_copy['Conference Quarter-Finals Winner'].fillna(0) +
                                     nhl_results_copy['Conference Quarter-Finals Loser'].fillna(0) +
                                     nhl_results_copy['Second Round Winner'].fillna(0) +
                                     nhl_results_copy['Second Round Loser'].fillna(0) +
                                     nhl_results_copy['First Round Winner'].fillna(0) +
                                     nhl_results_copy['First Round Loser'].fillna(0) +
                                     nhl_results_copy['Qualifying Round Winner'].fillna(0) +
                                     nhl_results_copy['Qualifying Round Loser'].fillna(0))

# Create a playoff indicator column

nhl_results_copy['Playoff Indicator'] = np.where(nhl_results_copy['Made Playoffs'] > 0, 1, 0)

# Assign the playoff bonuses to a new column and make an aggregated column

nhl_results_copy['Made Playoffs Bonus'] = np.where(nhl_results_copy['Playoff Indicator'] == 1, made_playoffs_bonus, 0)


nhl_results_copy['Finals Winner Bonus'] = np.where(nhl_results_copy['Final Winner'] == 1, 
                                                   champ_winner_bonus, 0)
nhl_results_copy['Finals Loser Bonus'] = np.where(nhl_results_copy['Final Loser'] == 1, 
                                                  champ_loser_bonus, 0)
nhl_results_copy['Semi-Finals Loser Bonus'] = np.where(nhl_results_copy['Semi-Finals Loser'] == 1, 
                                                       semis_loser_bonus, 0)
nhl_results_copy['Quarter-Finals Loser Bonus'] = np.where(nhl_results_copy['Quarter-Finals Loser'] == 1, 
                                                          quarters_loser_bonus, 0)
nhl_results_copy['Prelim Loser Bonus'] = np.where(nhl_results_copy['Preliminary Round Loser'] == 1, 
                                                  wc_loser_bonus, 0)
nhl_results_copy['Conference Finals Loser Bonus'] = np.where(nhl_results_copy['Conference Finals Loser'] == 1, 
                                                             semis_loser_bonus, 0)
nhl_results_copy['Division Finals Loser Bonus'] = np.where(nhl_results_copy['Division Finals Loser'] == 1, 
                                                           quarters_loser_bonus, 0)
nhl_results_copy['Division Semi-Finals Loser Bonus'] = np.where(nhl_results_copy['Division Semi-Finals Loser'] == 1, 
                                                                wc_loser_bonus, 0)
nhl_results_copy['Conference Semi-Finals Loser Bonus'] = np.where(nhl_results_copy['Conference Semi-Finals Loser'] == 1, 
                                                                  quarters_loser_bonus, 0)
nhl_results_copy['Conference Quarter-Finals Loser Bonus'] = np.where(nhl_results_copy['Conference Quarter-Finals Loser'] == 1, 
                                                                     wc_loser_bonus, 0)
nhl_results_copy['Second Round Loser Bonus'] = np.where(nhl_results_copy['Second Round Loser'] == 1, 
                                                        quarters_loser_bonus, 0)
nhl_results_copy['First Round Loser Bonus'] = np.where(nhl_results_copy['First Round Loser'] == 1, 
                                                       wc_loser_bonus, 0)
nhl_results_copy['Qualifying Round Loser Bonus'] = np.where(nhl_results_copy['Qualifying Round Loser'] == 1, 
                                                            wc_loser_bonus, 0)


nhl_results_copy['Playoff Distance Bonus'] = (nhl_results_copy['Finals Winner Bonus'] +
                                             nhl_results_copy['Finals Loser Bonus'] +
                                             nhl_results_copy['Semi-Finals Loser Bonus'] +
                                             nhl_results_copy['Quarter-Finals Loser Bonus'] +
                                             nhl_results_copy['Prelim Loser Bonus'] +
                                             nhl_results_copy['Conference Finals Loser Bonus'] +
                                             nhl_results_copy['Division Finals Loser Bonus'] +
                                             nhl_results_copy['Division Semi-Finals Loser Bonus'] +
                                             nhl_results_copy['Conference Semi-Finals Loser Bonus'] +
                                             nhl_results_copy['Conference Quarter-Finals Loser Bonus'] +
                                             nhl_results_copy['Second Round Loser Bonus'] +
                                             nhl_results_copy['First Round Loser Bonus'] +
                                             nhl_results_copy['Qualifying Round Loser Bonus'])

# Implement the formula into a new column

nhl_results_copy['Formula Result'] = (nhl_results_copy['WP'] + nhl_results_copy['Made Playoffs Bonus'] +
                                      scoring_multiplier * 
                                      (nhl_results_copy['Playoff Distance Bonus']/max_playoff_points))

# Save the results to a final dataframe with the forumula's result

nhl_results_final = nhl_results_copy[['Year', 'Team', 'Formula Result']]


# Get the distinct list of hosts for the NHL

#nhl_results_1 = pd.DataFrame(nhl_results_final.groupby('Team')['Formula Result'].sum())

nhl_hosts = []

for team in nhl_results_final['Team'].unique():
    current_team = team.split(' ')
    if len(current_team) == 2:
        nhl_hosts.append(current_team[0])
    else:
        if current_team[0] in ['Chicago', 'Minnesota', 'Toronto', 'Detroit', 'Columbus', 'Vegas']:
            nhl_hosts.append(current_team[0])
        else:
            if 'Anaheim' in current_team:
                nhl_hosts.append('Anaheim')
            else:
                multi = current_team[0] + ' ' + current_team[1]
                nhl_hosts.append(multi)
        
nhl_host_cities = list(set(nhl_hosts))

# Write a function to get MLS indicator columns

def get_mls_indicator_columns(regular_season, playoffs):

    new_league_list = []
    
    years_list = list(regular_season['Year'].unique())

    for year in years_list:

        league_play = playoffs[playoffs['Year'] == year]
        league_reg = regular_season[regular_season['Year'] == year]

        new_league_temp = league_reg.copy().copy()

        for playoff_round in list(league_play['Round'].unique()):
            #print(playoff_round)

            current_round = league_play[league_play['Round'] == playoff_round]

            round_winners = list(current_round['Winner'])
            #print(round_winners)

            round_losers = list(current_round['Loser'])  
            
            #print(round_losers)

            winner_list = []
            loser_list = []

            for index, row in league_reg.iterrows():
                new_row = row['Team'].strip()
                if new_row in round_losers:
                    loser_list.append(1)
                else:
                    loser_list.append(0)
                if new_row in round_winners:
                    winner_list.append(1)
                else:
                    winner_list.append(0)

            new_league_temp[f'{playoff_round} Winner'] = winner_list
            new_league_temp[f'{playoff_round} Loser'] = loser_list

        new_league_list.append(new_league_temp)

    league_new_df = pd.concat(new_league_list)

    return league_new_df

mls_results = get_mls_indicator_columns(mls_regular_season_new, mls_playoffs_new)

# Reformat the MLS to be more usable

mls_results_copy = mls_results.copy()

mls_results_copy['MLS Cup Winner Indicator'] = (mls_results_copy['MLS Cup Winner'].fillna(0) +
                             mls_results_copy['MLS Cup 2003 Winner'].fillna(0) +
                             mls_results_copy['MLS Cup 2004 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2005 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2006 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2007 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2008 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2009 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2010 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2011 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2012 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2013 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2014 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2015 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2016 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2017 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2018 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2019 Winner'].fillna(0) +
                               mls_results_copy['MLS Cup 2020 Winner'].fillna(0))

mls_results_copy['MLS Cup Loser Indicator'] = (mls_results_copy['MLS Cup Loser'].fillna(0) +
                             mls_results_copy['MLS Cup 2003 Loser'].fillna(0) +
                             mls_results_copy['MLS Cup 2004 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2005 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2006 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2007 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2008 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2009 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2010 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2011 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2012 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2013 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2014 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2015 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2016 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2017 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2018 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2019 Loser'].fillna(0) +
                               mls_results_copy['MLS Cup 2020 Loser'].fillna(0))

# Get an indicator for which teams made the playoffs

mls_results_copy['Playoff Indicator'] = (mls_results_copy['MLS Cup Winner Indicator'].fillna(0) +
                                        mls_results_copy['MLS Cup Loser Indicator'].fillna(0) +
                                        mls_results_copy['Conference Finals Loser'].fillna(0) +
                                        mls_results_copy['Conference Semifinal Loser'].fillna(0) +
                                        mls_results_copy['Conference Final Loser'].fillna(0) +
                                        mls_results_copy['Conference Semifinals Loser'].fillna(0) +
                                        mls_results_copy['Conference Quarterfinal Loser'].fillna(0) +
                                        mls_results_copy['Knockout round Loser'].fillna(0) +
                                        mls_results_copy['Round 1 Loser'].fillna(0) +
                                        mls_results_copy['First Round Loser'].fillna(0) +
                                        mls_results_copy['Round One Loser'].fillna(0) +
                                        mls_results_copy['Wild Card Round Loser'].fillna(0))

# Assign the playoff bonuses to a new column and make an aggregated column

mls_results_copy['Made Playoffs Bonus'] = np.where(mls_results_copy['Playoff Indicator'] == 1, made_playoffs_bonus, 0)

# semis = Conference Finals, Conference Semifinal, Conference Final
# quarters = Conference Semifinals, Conference Quarterfinal
# wildcard = Knockout round, Round 1, First Round, Round One, Wild Card Round

mls_results_copy['MLS Cup Winner Bonus'] = np.where(mls_results_copy['MLS Cup Winner Indicator'] == 1, 
                                                    champ_winner_bonus, 0)
mls_results_copy['MLS Cup Loser Bonus'] = np.where(mls_results_copy['MLS Cup Loser Indicator'] == 1, 
                                                   champ_loser_bonus, 0)
mls_results_copy['Conference Finals Loser Bonus'] = np.where(mls_results_copy['Conference Finals Loser'] == 1, 
                                                             semis_loser_bonus, 0)
mls_results_copy['Conference Semifinal Loser Bonus'] = np.where(mls_results_copy['Conference Semifinal Loser'] == 1, 
                                                                semis_loser_bonus, 0)
mls_results_copy['Conference Final Loser Bonus'] = np.where(mls_results_copy['Conference Final Loser'] == 1, 
                                                            semis_loser_bonus, 0)
mls_results_copy['Conference Semifinals Loser Bonus'] = np.where(mls_results_copy['Conference Semifinals Loser'] == 1, 
                                                                 quarters_loser_bonus, 0)
mls_results_copy['Conference Quarterfinal Loser Bonus'] = np.where(mls_results_copy['Conference Quarterfinal Loser'] == 1, 
                                                                   quarters_loser_bonus, 0)
mls_results_copy['Knockout round Loser Bonus'] = np.where(mls_results_copy['Knockout round Loser'] == 1, 
                                                          wc_loser_bonus, 0)
mls_results_copy['Round 1 Loser Bonus'] = np.where(mls_results_copy['Round 1 Loser'] == 1, 
                                                   wc_loser_bonus, 0)
mls_results_copy['First Round Loser Bonus'] = np.where(mls_results_copy['First Round Loser'] == 1, 
                                                       wc_loser_bonus, 0)
mls_results_copy['Round One Loser Bonus'] = np.where(mls_results_copy['Round One Loser'] == 1, 
                                                     wc_loser_bonus, 0)
mls_results_copy['Wild Card Round Loser Bonus'] = np.where(mls_results_copy['Wild Card Round Loser'] == 1, 
                                                           wc_loser_bonus, 0)

mls_results_copy['Playoff Distance Bonus'] = (mls_results_copy['MLS Cup Winner Bonus'] +
                                             mls_results_copy['MLS Cup Loser Bonus'] +
                                             mls_results_copy['Conference Finals Loser Bonus'] +
                                             mls_results_copy['Conference Semifinal Loser Bonus'] +
                                             mls_results_copy['Conference Final Loser Bonus'] +
                                             mls_results_copy['Conference Semifinals Loser Bonus'] +
                                             mls_results_copy['Conference Quarterfinal Loser Bonus'] +
                                             mls_results_copy['Knockout round Loser Bonus'] +
                                             mls_results_copy['Round 1 Loser Bonus'] +
                                             mls_results_copy['First Round Loser Bonus'] +
                                             mls_results_copy['Round One Loser Bonus'] +
                                             mls_results_copy['Wild Card Round Loser Bonus'])

# Implement the formula into a new column

mls_results_copy['Formula Result'] = (mls_results_copy['WP'] + mls_results_copy['Made Playoffs Bonus'] +
                                      scoring_multiplier * 
                                      (mls_results_copy['Playoff Distance Bonus']/max_playoff_points))

# Save the results to a final dataframe with the forumula's result

mls_results_final = mls_results_copy[['Year', 'Team', 'Formula Result']]

# Get the distinct list of hosts for the MLS

#mls_results_1 = pd.DataFrame(mls_results_final.groupby('Team')['Formula Result'].sum())

mls_hosts = []

for team in mls_results_final['Team'].unique():
    current_team = team.split(' ')
    #print(current_team)
    if len(current_team) == 2:
        #print(current_team)
        mls_hosts.append(current_team[1])
    else:
        #print(current_team)
        if current_team[1] in ['Salt', 'Chivas', 'Sporting', 'FC', 'Inter', 'CF', 'St.']:
            #print(current_team)
            #mls_hosts.append(current_team[0])
            mls_hosts.append('Dallas')
            mls_hosts.append('Chivas')
            mls_hosts.append('KC')
            mls_hosts.append('Cincinnati')
            mls_hosts.append('Miami')
            mls_hosts.append('Montréal')
            mls_hosts.append('St. Louis')
        elif len(current_team) == 3:
            mls_hosts.append(current_team[1])
        else:
            #print(current_team)
            mls_hosts.append('Seattle')
            mls_hosts.append('Salt Lake')
            mls_hosts.append('NY')
        
mls_host_cities = list(set(mls_hosts))

# Add in the league name

nfl_results_final['League'] = 'NFL'
mlb_results_final['League'] = 'MLB'
nba_results_final['League'] = 'NBA'
nhl_results_final['League'] = 'NHL'
mls_results_final['League'] = 'MLS'

# Get a region column for the Leagues

def categorize_nfl(value):
    for city in nfl_host_cities:
        if city in value:
            return city
            
nfl_results_final['City'] = nfl_results_final['Team'].apply(categorize_nfl)

def categorize_mlb(value):
    for city in mlb_host_cities:
        if city in value:
            return city
            
mlb_results_final['City'] = mlb_results_final['Team'].apply(categorize_mlb)

def categorize_nba(value):
    for city in nba_host_cities:
        if city in value:
            return city
            
nba_results_final['City'] = nba_results_final['Team'].apply(categorize_nba)

def categorize_nhl(value):
    for city in nhl_host_cities:
        if city in value:
            return city
            
nhl_results_final['City'] = nhl_results_final['Team'].apply(categorize_nhl)

def categorize_mls(value):
    for city in mls_host_cities:
        if city in value:
            return city
            
mls_results_final['City'] = mls_results_final['Team'].apply(categorize_mls)

# Apply the league multiplier

nfl_results_final['Weighted Formula'] = nfl_results_final['Formula Result'] * 1 #nfl_revenue_multiplier
mlb_results_final['Weighted Formula'] = mlb_results_final['Formula Result'] * 1 #mlb_revenue_multiplier
nba_results_final['Weighted Formula'] = nba_results_final['Formula Result'] * 1 #nba_revenue_multiplier
nhl_results_final['Weighted Formula'] = nhl_results_final['Formula Result'] * 1 #nhl_revenue_multiplier
mls_results_final['Weighted Formula'] = mls_results_final['Formula Result'] * 1 #mls_revenue_multiplier

# Comine the dataframes into one

league_results = [
    nfl_results_final,
    mlb_results_final,
    nba_results_final,
    nhl_results_final,
    mls_results_final
]

league_results_stage = pd.concat(league_results)

# Get the column for the region of the season/league

def get_region(value):
    cities = list(sports_cities_df['City'])
    regions = list(sports_cities_df['Region'])
    
    idx = cities.index(value)
    
    return regions[idx]

league_results_stage['Region'] = league_results_stage['City'].apply(get_region)

# Apply the weighted multiplier for recency of the season

max_year = league_results_stage['Year'].max()

def get_recency_multiplier(value):
    multiplier = 1
    scalar_down = (max_year - value) * .015
    return round(1 - scalar_down, 2)

league_results_stage['Recency Multiplier'] = league_results_stage['Year'].apply(get_recency_multiplier)
league_results_stage['Final Weighted Formula'] = round(league_results_stage['Recency Multiplier'] * league_results_stage['Weighted Formula'], 3)

def get_standings_for_league(league):
    
    # Filter to just one league
    league_slice = league_results_stage[league_results_stage['League'] == league]

    # Get a dataframe for the team counts and average Final Weighted Formula per Year, Region

    # Create an in-memory database
    conn = sqlite3.connect(':memory:')

    # Write the DataFrame to the database
    league_slice.to_sql('results_stage', conn, index=False)

    # Write a query
    query = """
    SELECT Year, Region, max(League), count(Team) as [Team Count], avg([Final Weighted Formula]) as [Average Formula Pre]
    FROM results_stage
    GROUP BY Year, Region
    """
    league_slice_pre = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    # Sum the Formula's result over all time for that Region

    league_slice_results = league_slice_pre.groupby('Region').agg({'Average Formula Pre': 'sum'}).sort_values('Average Formula Pre',
                                                                                                   ascending = False)

    # Obtain the number of years this Region had an NFL team, join to the NFL slice

    region_years = league_slice_pre.groupby(['Region']).agg({'Year': 'count'})

    league_slice_2 = pd.merge(league_slice_results, region_years, on='Region', how = 'left')

    # Compute the Standardized score for this region based on how many years it had an NFL team

    league_slice_2['Averaged Sum'] = league_slice_2['Average Formula Pre'] / league_slice_2['Year']

    # Re-order and format the frame, displaying both scoring versions

    league_slice_3 = league_slice_2.sort_values('Averaged Sum', ascending = False)

    league_slice_4 = league_slice_3.reset_index()

    league_slice_final = league_slice_4[['Region', 'Year', 'Averaged Sum', 'Average Formula Pre']]

    # Rename some columns

    league_slice_final = league_slice_final.rename(columns = {'Year': 'Year Count'
                                            , 'Averaged Sum': 'Averaged Score'
                                            , 'Average Formula Pre': 'Total Score'})
    
    # Round some columns
    
    league_slice_final['Averaged Score'] = league_slice_final['Averaged Score'].round(3)
    league_slice_final['Total Score'] = league_slice_final['Total Score'].round(3)
    
    return league_slice_final

# place ranked data into Data Frames

nfl_slice = get_standings_for_league('NFL')
mlb_slice = get_standings_for_league('MLB')
nba_slice = get_standings_for_league('NBA')
nhl_slice = get_standings_for_league('NHL')
mls_slice = get_standings_for_league('MLS')

# save the sliced, ranked data into .csv files

folder_path = "./league_rankings"

nfl_slice.to_csv(folder_path + '/nfl_rankings.csv', index = False)
mlb_slice.to_csv(folder_path + '/mlb_rankings.csv', index = False)
nba_slice.to_csv(folder_path + '/nba_rankings.csv', index = False)
nhl_slice.to_csv(folder_path + '/nhl_rankings.csv', index = False)
mls_slice.to_csv(folder_path + '/mls_rankings.csv', index = False)


