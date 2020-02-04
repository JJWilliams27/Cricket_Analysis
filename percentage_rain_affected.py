# Calculate Percentage Rain Affected Matches for Each Player

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
import warnings
warnings.filterwarnings("ignore")

## Main ##
path = os.getcwd()
print("Calculating Percentage of Rain Affected Matches for each Player")

# Read CSV
all_players = pd.read_csv('All_Player_Frequency.csv')
rain_players = pd.read_csv('Rain_Player_Frequency.csv')

# Add Columns to Dataframe
all_players['Rain_Affected_Draws'] = "0"
all_players['Rain_Percentage'] = "0"
all_players['Name'] = 'Unknown'

for index, row in rain_players.iterrows():
	playerid = row[1]
	draws = row[2]
	if playerid in all_players.PlayerID.values:
		idx = all_players[all_players['PlayerID']==playerid].index.values.astype(int)[0]
		all_players['Rain_Affected_Draws'][idx] = draws
		all_players['Rain_Percentage'][idx] = (draws/all_players['Total_Matches'][idx])*100


num_players = len(all_players)
# Get Names
for index, row in all_players.iterrows(): # For some reason tqdm doesnt work here
	print('%s / %s' %(index,num_players)) # So print progress instead
	playerid = row[1]
	try:
		with open(path + '/Players/' + str(playerid) + '.json') as json_file: # If json exists, use that
			pinfo = json.load(json_file)
			all_players['Name'][index] = pinfo['name']
	except:
		try:
			pinfo = Player(playerid) # If no json, scrape the data from cricinfo and save to json for future use
			name = pinfo.name
			all_players['Name'][index] = name
			dob = pinfo.date_of_birth
			major_teams = pinfo.major_teams
			role = pinfo.playing_role
			bat_style = pinfo.batting_style
			bowl_style = pinfo.bowling_style
			bat_field_averages = pinfo.batting_fielding_averages
			bowl_averages = pinfo.bowling_averages
			test_debut = pinfo.test_debut
			last_test = pinfo.last_test
			tests = {'debut' : test_debut, 'most_recent' : last_test}
			odi_debut = pinfo.odi_debut
			last_odi = pinfo.last_odi
			odis = {'debut' : odi_debut, 'most_recent' : last_odi}
			t20i_debut = pinfo.t20i_debut
			last_t20i = pinfo.last_t20i
			t20i = {'debut' : t20i_debut, 'most_recent' : last_t20i}
			first_class_debut = pinfo.first_class_debut
			last_first_class = pinfo.last_first_class
			first_class = {'debut' : first_class_debut, 'most_recent' : last_first_class}
			list_a_debut = pinfo.list_a_debut
			last_list_a = pinfo.last_list_a
			list_a = {'debut' : list_a_debut, 'most_recent' : last_list_a}
			t20_debut = pinfo.t20_debut
			last_t20 = pinfo.last_t20
			t20 = {'debut' : t20_debut, 'most_recent' : last_t20}
			# Save player data
			dirname = path + '/Players'
			if not os.path.exists(dirname):
				os.mkdir(dirname)
			outname = dirname + '/' + str(playerid) + '.json'
			player_info = {'name' : name, 'dob' : dob, 'major_teams' : major_teams, 'playing_role' : role, \
			'batting_style' : bat_style, 'bowling_style' : bowl_style, 'bat_field_averages' : bat_field_averages, \
			'bowl_averages' : bowl_averages, 'tests' : tests, 'odis' : odis, 't20i' : t20i, 'first_class' : first_class, \
			'list_a' : list_a, 't20' : t20}

			out_json = json.dumps(player_info)
			f = open(outname,"w")
			f.write(out_json)
			f.close()
		except:
			all_players['Name'][index] = 'Unknown'

cols = ['PlayerID','Name','Total_Matches','Rain_Affected_Draws','Rain_Percentage']
all_players = all_players[cols]

all_players.reset_index(drop=True, inplace=True)
all_players.to_csv('Player_Rain_Percentage.csv')