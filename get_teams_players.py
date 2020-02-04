# Read Matches and Find Players

# Modules
from espncricinfo.player import Player
from espncricinfo.match import Match
from espncricinfo.series import Series
import json
import pdb
from collections import Counter
from tqdm import tqdm
import pandas as pd
import os

## TO ADD: OUTPUT TOTAL MATCHES AND NUMBER OF RAIN AFFECTED MATCHES

path = os.getcwd()

# Read CSVs

all_matches = pd.read_csv('c_champ_matches.csv')
rain_matches = pd.read_csv('rain_matches.csv')

all_matches = all_matches.iloc[:,1:].values
rain_matches = rain_matches.iloc[:,1:].values

players_all_games = []
teams_all_games = []
draw_teams = []
draw_players = []

all_m = len(all_matches)

print("Analysing All Matches")
for i in tqdm(list(range(0,all_m))):
	match = all_matches[i][0]
	with open(path + '/Matches/' + str(match) + '.json') as json_file: # If json exists, use that
		minfo = json.load(json_file)
	team1name = minfo['team1']['name']
	team2name = minfo['team2']['name']
	teams_all_games.append(team1name)
	teams_all_games.append(team2name)
	players_all_games.append(minfo['team1']['squad_id'])
	players_all_games.append(minfo['team2']['squad_id'])

players_all_games = [x for y in players_all_games for x in y]

print("All Matches Analysed")
print("Analysing Rain Affected Matches")

all_d = len(rain_matches)

for ii in tqdm(list(range(0,all_d))):
	match = rain_matches[ii][0]
	with open(path + '/Matches/' + str(match) + '.json') as json_file: # If json exists, use that
		minfo = json.load(json_file)
	team1name = minfo['team1']['name']
	team2name = minfo['team2']['name']
	draw_teams.append(team1name)
	draw_teams.append(team2name)
	draw_players.append(minfo['team1']['squad_id'])
	draw_players.append(minfo['team2']['squad_id'])

draw_players = [x for y in draw_players for x in y]

draw_teams_counter = Counter(draw_teams)
draw_teams_counter = dict(draw_teams_counter)
#draw_teams_df = pd.DataFrame(draw_teams_counter.items())
#draw_teams_df.columns = ['TeamName','Draws']
#draw_teams_df.to_csv('Rain_Teams_Frequency.csv')

draw_players_counter = Counter(draw_players)
draw_players_counter = dict(draw_players_counter)
draw_players_df = pd.DataFrame(draw_players_counter.items())
draw_players_df.columns = ['PlayerID','Draws']
draw_players_df.to_csv('Rain_Player_Frequency.csv')

all_players_counter = Counter(players_all_games)
all_players_counter = dict(all_players_counter)
all_players_df = pd.DataFrame(all_players_counter.items())
all_players_df.columns = ['PlayerID','Total_Matches']
all_players_df.to_csv('All_Player_Frequency.csv')

all_teams_counter = Counter(teams_all_games)
all_teams_counter = dict(all_teams_counter)
#all_teams_df = pd.DataFrame(all_teams_counter.items())
#all_teams_df.columns = ['TeamName','Total_Matches']
#all_teams_df.to_csv('All_Teams_Frequency.csv')

team_stats = pd.DataFrame(columns=['TeamName','Total_Matches','Rain_Matches','Rain_Percentage'])

for key in all_teams_counter.keys() & draw_teams_counter.keys():
	team = key
	total = all_teams_counter[key]
	rain = draw_teams_counter[key]
	perc = (rain/total)*100
	team_stats = team_stats.append({'TeamName' : team, 'Total_Matches' : total, 'Rain_Matches' : rain, 'Rain_Percentage' : perc}, ignore_index=True)

team_stats.to_csv('Team_Rain_Percentage.csv')
