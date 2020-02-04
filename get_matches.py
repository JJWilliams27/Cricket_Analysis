# Get Rain Affected Match IDs and save as CSVs

# Import Modules
from espncricinfo.player import Player
from espncricinfo.match import Match
from espncricinfo.series import Series
import json
import pdb
from collections import Counter
from tqdm import tqdm
import pandas as pd
import math
import csv
import os
import warnings 
warnings.filterwarnings("ignore")

## MAIN ##
max_overs = 272 # Max total overs - less than this value assumed to be rain affected

# Output filenames
rain_fname = 'rain_matches.csv'
all_fname = 'c_champ_matches.csv'
nbb_fname = 'nbb_matches.csv'
season_stats_fname = 'season_game_stats.csv'

# Configure arrays
all_c_champ_matches = []
matches_drawn = []
no_ball_bowled = []
rain_games_per_season = []
nbb_per_season = []
games_per_season = []

cchamp1 = Series('8052')
cchamp2 = Series('8204')

years = [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
#years = [2017,2018]
seasondict = {}

for yr in years:
	print('Getting Matches for %s' %(yr))
	seasondict["cc_{0}".format(yr)] = Series.get_events_for_season(cchamp1,yr)
	seasondict["cc_{0}_2".format(yr)] = Series.get_events_for_season(cchamp2,yr)

matchdict = {}
print('Sorting Matches into Dictionary')
for yr in years:
	temp_matches = []
	for i in list(range(0,len(seasondict['cc_%s' %(yr)]))):
		temp_matches.append(seasondict['cc_%s' %(yr)][i]['match_id'])
	for i in list(range(0,len(seasondict['cc_%s_2' %(yr)]))):
		temp_matches.append(seasondict['cc_%s_2' %(yr)][i]['match_id'])
	matchdict["matches{0}".format(yr)] = temp_matches

#cc_2018 = Series.get_events_for_season(cchamp1,2018)
#cc_2018_2 = Series.get_events_for_season(cchamp2,2018)

#matches18 = []
#for i in list(range(0,len(cc_2018))):
#	matches18.append(cc_2018[i]['match_id'])
#for i in list(range(0,len(cc_2018_2))):
#	matches18.append(cc_2018_2[i]['match_id'])

#cc_2017 = Series.get_events_for_season(cchamp1,2017)
#cc_2017_2 = Series.get_events_for_season(cchamp2,2017)

#matches17 = []
#for i in list(range(0,len(cc_2017))):
#	matches17.append(cc_2017[i]['match_id'])
#for i in list(range(0,len(cc_2017_2))):
#	matches17.append(cc_2017_2[i]['match_id'])

seasons=[*matchdict] # Get Keys from Dict
path=os.getcwd()
print("Getting Rain Affected Matches...")
for season in tqdm(seasons):
	rain_draws_season = 0
	games_season = 0
	matches = matchdict[season]
	for i in tqdm(matches):
		try:
			try:
				with open(path + '/Matches/' + i + '.json') as json_file: # If json exists, use that
					minfo = json.load(json_file)
					scorecard = minfo['scorecard']
					temp = minfo['result']
					totalovers = minfo['totalovers']
					all_c_champ_matches.append(i)
					games_season = games_season + 1
			except:
				try:
					m = Match(i) # Otherwise, scrape from cricinfo
					# Get squads
					team1squad = m.team_1_players
					team1squad_id = []
					team1squad_names = []
					for j in list(range(0,len(team1squad))):
						name = team1squad[j]['known_as']
						p_id = team1squad[j]['object_id']
						team1squad_names.append(name)
						team1squad_id.append(p_id)

					team2squad = m.team_2_players
					team2squad_id = []
					team2squad_names = []
					for j in list(range(0,len(team2squad))):
						name = team2squad[j]['known_as']
						p_id = team2squad[j]['object_id']
						team2squad_names.append(name)
						team2squad_id.append(p_id)

					# Get scorecards
					i1bat, i2bat, i3bat, i4bat = m.get_batcards()
					i1bowl, i2bowl, i3bowl, i4bowl = m.get_bowlcards()
					innings = m.innings
					try:
						i1stats = innings[0]
					except:
						i1stats = None
					try:
						i2stats = innings[1]
					except:
						i2stats = None
					try:
						i3stats = innings[2]
					except:
						i3stats = None
					try:
						i4stats = innings[3]
					except:
						i4stats = None
					scorecard = {'inn1': {'overview' : i1stats, 'batcard': i1bat, 'bowlcard' : i1bowl}, 'inn2' : {'overview' : i2stats, 'batcard': i2bat, 'bowlcard' : i2bowl}, 'inn3' : {'overview' : i3stats, 'batcard': i3bat, 'bowlcard' : i3bowl}, 'inn4' : {'overview' : i4stats, 'batcard': i4bat, 'bowlcard' : i4bowl}}
					temp = m.result
					totalovers = m.get_overs_in_match()
					all_c_champ_matches.append(i)
					games_season = games_season + 1
				except:
					temp='None'
					games_season = games_season + 1

			if temp == 'Match drawn':
				if totalovers <= max_overs:
					matches_drawn.append(i)
					rain_draws_season = rain_draws_season + 1

			# Save to json file for future use (if json doesn't already exist)
			if not os.path.isfile(path+'/Matches/' + i + '.json'):
				minfo = m.__dict__ # Convert to dictionary for saving as json
				dirname = path + '/Matches'
				if not os.path.exists(dirname):
					os.mkdir(dirname)
				outname = dirname + '/' + minfo['match_id'] + '.json'
				match_id = minfo['match_id']
				srs_id = minfo['series'][0]['core_recreation_id']
				srs = minfo['series'][0]['url_component']
				matchtype = minfo['match_class']
				result = minfo['result']
				start = minfo['start_datetime_local']
				venue = minfo['ground_name']
				venue_id =  minfo['ground_id']
				officials = m.officials
				lighting = m.lighting
				followon = m.followon
				toss_winner_id = m.toss_winner
				toss_decision = m.toss_decision
				toss = {'toss_winner_id' : toss_winner_id, 'toss_decision' : toss_decision}
				home_team = minfo['home_team']
				team1name = m.team_1['team_name']
				team2name = m.team_2['team_name']
				team1 = {'name' : team1name, 'squad' : team1squad_names, 'squad_id' : team1squad_id}
				team2 = {'name' : team2name, 'squad' : team2squad_names, 'squad_id' : team2squad_id}
				match_info = {'match_id' : match_id, 'srs_id' : srs_id, 'srs' : srs , \
				              'matchtype' : matchtype, 'result' : result, 'start' : start, \
				              'venue' : venue, 'venue_id' : venue_id, 'home_team' : home_team, \
				              'team1' : team1, 'team2' : team2, 'scorecard' : scorecard, \
				              'totalovers' : totalovers, 'officials' : officials, 'lighting' : lighting, \
				              'followon' : followon, 'toss' : toss}
				out_json = json.dumps(match_info)
				f = open(outname,"w")
				f.write(out_json)
				f.close()
		except:
			pass
	rain_games_per_season.append(rain_draws_season)
	games_per_season.append(games_season)

print("Matches Retrieved")

## Output Match IDs as CSV ##

pd.DataFrame(matches_drawn).to_csv(rain_fname)
pd.DataFrame(all_c_champ_matches).to_csv(all_fname)

match_df = pd.DataFrame(columns=['Season','Games','Rain_Affected_Draws'])
seasons=years
match_df['Season'] = seasons
match_df['Games'] = games_per_season
match_df['Rain_Affected_Draws'] = rain_games_per_season

match_df.to_csv(season_stats_fname)

print("Complete")
