# Calculate Team Stats

# Modules
from pycricbuzz import Cricbuzz
import json
import pdb
from collections import Counter
from tqdm import tqdm
import pandas as pd
import numpy as np
import math
import os
import warnings
warnings.filterwarnings("ignore")

print('Calculating Team Statistics')

df = pd.read_csv('Team_Rain_Percentage.csv')
all_matches = pd.read_csv('c_champ_matches.csv')
rain_matches = pd.read_csv('rain_matches.csv')
all_matches = all_matches.iloc[:,1:].values
rain_matches = rain_matches.iloc[:,1:].values

# Add columns to df
df['Innings_Batted'] = 0
df['Innings_Bowled'] = 0
df['Overs_Batted'] = 0
df['Overs_Bowled'] = 0
df['Total_Runs_Scored'] = 0
df['Total_Runs_Conceded'] = 0
df['Highest_Innings_Score'] = 0
df['Highest_Innings_Score_MatchID'] = np.nan
df['Lowest_Innings_Score'] = 0
df['Lowest_Innings_Score_MatchID'] = np.nan
df['Wickets_Taken'] = 0
df['Wickets_Lost'] = 0

df['Overs_Batted'] = df.astype({'Overs_Batted': 'float64'}).dtypes
df['Overs_Bowled'] = df.astype({'Overs_Bowled': 'float64'}).dtypes

df['Rain_Innings_Batted'] = 0
df['Rain_Innings_Bowled'] = 0
df['Rain_Overs_Batted'] = 0
df['Rain_Overs_Bowled'] = 0
df['Rain_Total_Runs_Scored'] = 0
df['Rain_Total_Runs_Conceded'] = 0
df['Rain_Highest_Innings_Score'] = 0
df['Rain_Highest_Innings_Score_MatchID'] = np.nan
df['Rain_Lowest_Innings_Score'] = 0
df['Rain_Lowest_Innings_Score_MatchID'] = np.nan
df['Rain_Wickets_Taken'] = 0
df['Rain_Wickets_Lost'] = 0

df['Rain_Overs_Batted'] = df.astype({'Rain_Overs_Batted': 'float64'}).dtypes
df['Rain_Overs_Bowled'] = df.astype({'Rain_Overs_Bowled': 'float64'}).dtypes

path = os.getcwd()

for n in tqdm(list(range(0,len(all_matches)))):
	mid = str(all_matches[n][0])
	with open(path + '/Matches/' + mid + '.json') as json_file:
	    minfo = json.load(json_file)
	    scard = minfo['scorecard'] # Grab scorecard from match info dictionary
	    try:
	    	inn1 = scard['inn1'] # Try getting innings, pass if dont exist (not all matches have 4 innings, some matches called off, etc)
	    	test = inn1['batcard'][0] # Test that the innings data is there by getting the first batsman, else pass
	    except:
	    	inn1=None
	    try:
	    	inn2 = scard['inn2'] 
	    	test = inn2['batcard'][0]
	    except:
	    	inn2=None
	    	pass
	    try:
	    	inn3 = scard['inn3']
	    	test = inn3['batcard'][0]
	    except:
	    	inn3=None
	    	pass
	    try:
	    	inn4 = scard['inn4']
	    	test = inn4['batcard'][0]
	    except:
	    	inn4=None
	    	pass
	    minfo.pop('scorecard',None)
	    innings = [inn1,inn2,inn3,inn4]

	for inn in innings:
		if inn != None:
			batteam = inn['batcard'][0]['team']

			if minfo['team1']['name'] == batteam:
				bowlteam = minfo['team2']['name']
			else:
				bowlteam = minfo['team1']['name']

			runs_scored = int(inn['overview']['runs'])
			wickets = int(inn['overview']['wickets'])
			overs = float(inn['overview']['overs'])

			# Find in df:
			idx1 = df.loc[df['TeamName'] == batteam].index[0]
			idx2 = df.loc[df['TeamName'] == bowlteam].index[0]

			# Update df
			new_innings_bat = df['Innings_Batted'][idx1] + 1
			new_innings_bowl = df['Innings_Bowled'][idx2] + 1
			new_runs_scored = df['Total_Runs_Scored'][idx1] + runs_scored
			new_runs_conceded = df['Total_Runs_Conceded'][idx2] + runs_scored
			new_wickets_lost = df['Wickets_Lost'][idx1] + wickets
			new_wickets_taken = df['Wickets_Taken'][idx2] + wickets

			df.set_value(idx1,'Innings_Batted',new_innings_bat)
			df.set_value(idx2,'Innings_Bowled',new_innings_bowl)
			df.set_value(idx1,'Total_Runs_Scored',new_runs_scored)
			df.set_value(idx2,'Total_Runs_Conceded',new_runs_conceded)
			df.set_value(idx1,'Wickets_Lost',new_wickets_lost)
			df.set_value(idx2,'Wickets_Taken',new_wickets_taken)

			if runs_scored > df['Highest_Innings_Score'][idx1]:
				df.set_value(idx1,'Highest_Innings_Score',runs_scored)
				df.set_value(idx1,'Highest_Innings_Score_MatchID',mid)

			if df['Lowest_Innings_Score'][idx1] == 0:
				df.set_value(idx1,'Lowest_Innings_Score',runs_scored)
				df.set_value(idx1,'Lowest_Innings_Score_MatchID',mid)

			elif runs_scored < df['Lowest_Innings_Score'][idx1]:
				df.set_value(idx1,'Lowest_Innings_Score',runs_scored)
				df.set_value(idx1,'Lowest_Innings_Score_MatchID',mid)

			orig_overs = df['Overs_Batted'][idx1]
			if np.isnan(orig_overs):
				new_overs = overs
			elif (orig_overs).is_integer() or (overs.is_integer()):
				new_overs = orig_overs + overs
			else: 
				full_orig_overs = math.floor(orig_overs)
				part_orig_overs = orig_overs - full_orig_overs
				full_overs = math.floor(overs)
				part_overs = overs - full_overs
				total_full = full_orig_overs + full_overs
				total_part = part_orig_overs + part_overs
				if total_part < 0.6:
					total_part = total_part
				elif total_part >= 0.6:
					total_part = total_part + 0.4

				new_overs = total_full + total_part

			df.set_value(idx1,'Overs_Batted',new_overs)

			orig_overs = df['Overs_Bowled'][idx2]
			if np.isnan(orig_overs):
				new_overs = overs
			elif (orig_overs).is_integer() or (overs.is_integer()):
				new_overs = orig_overs + overs
			else: 
				full_orig_overs = math.floor(orig_overs)
				part_orig_overs = orig_overs - full_orig_overs
				full_overs = math.floor(overs)
				part_overs = overs - full_overs
				total_full = full_orig_overs + full_overs
				total_part = part_orig_overs + part_overs
				if total_part < 0.6:
					total_part = total_part
				elif total_part >= 0.6:
					total_part = total_part + 0.4

				new_overs = total_full + total_part

			df.set_value(idx2,'Overs_Bowled',new_overs)

	if int(mid) in rain_matches:
		for inn in innings:
			if inn != None:
				batteam = inn['batcard'][0]['team']

				if minfo['team1']['name'] == batteam:
					bowlteam = minfo['team2']['name']
				else:
					bowlteam = minfo['team1']['name']


				runs_scored = int(inn['overview']['runs'])
				wickets = int(inn['overview']['wickets'])
				overs = float(inn['overview']['overs'])

				# Find in df
				idx1 = df.loc[df['TeamName'] == batteam].index[0]
				idx2 = df.loc[df['TeamName'] == bowlteam].index[0]

				# Update df
				new_innings_bat = df['Rain_Innings_Batted'][idx1] + 1
				new_innings_bowl = df['Rain_Innings_Bowled'][idx2] + 1
				new_runs_scored = df['Rain_Total_Runs_Scored'][idx1] + runs_scored
				new_runs_conceded = df['Rain_Total_Runs_Conceded'][idx2] + runs_scored
				new_wickets_lost = df['Rain_Wickets_Lost'][idx1] + wickets
				new_wickets_taken = df['Rain_Wickets_Taken'][idx2] + wickets

				df.set_value(idx1,'Rain_Innings_Batted',new_innings_bat)
				df.set_value(idx2,'Rain_Innings_Bowled',new_innings_bowl)
				df.set_value(idx1,'Rain_Total_Runs_Scored',new_runs_scored)
				df.set_value(idx2,'Rain_Total_Runs_Conceded',new_runs_conceded)
				df.set_value(idx1,'Rain_Wickets_Lost',new_wickets_lost)
				df.set_value(idx2,'Rain_Wickets_Taken',new_wickets_taken)

				if runs_scored > df['Rain_Highest_Innings_Score'][idx1]:
					df.set_value(idx1,'Rain_Highest_Innings_Score',runs_scored)
					df.set_value(idx1,'Rain_Highest_Innings_Score_MatchID',mid)

				if df['Rain_Lowest_Innings_Score'][idx1] == 0:
					df.set_value(idx1,'Rain_Lowest_Innings_Score',runs_scored)
					df.set_value(idx1,'Rain_Lowest_Innings_Score_MatchID',mid)

				elif runs_scored < df['Rain_Lowest_Innings_Score'][idx1]:
					df.set_value(idx1,'Rain_Lowest_Innings_Score',runs_scored)
					df.set_value(idx1,'Rain_Lowest_Innings_Score_MatchID',mid)

				orig_overs = df['Rain_Overs_Batted'][idx1]
				if np.isnan(orig_overs):
					new_overs = overs
				elif (orig_overs).is_integer() or (overs.is_integer()):
					new_overs = orig_overs + overs
				else: 
					full_orig_overs = math.floor(orig_overs)
					part_orig_overs = orig_overs - full_orig_overs
					full_overs = math.floor(overs)
					part_overs = overs - full_overs
					total_full = full_orig_overs + full_overs
					total_part = part_orig_overs + part_overs
					if total_part < 0.6:
						total_part = total_part
					elif total_part >= 0.6:
						total_part = total_part + 0.4

					new_overs = total_full + total_part

				df.set_value(idx1,'Rain_Overs_Batted',new_overs)

				orig_overs = df['Rain_Overs_Bowled'][idx2]
				if np.isnan(orig_overs):
					new_overs = overs
				elif (orig_overs).is_integer() or (overs.is_integer()):
					new_overs = orig_overs + overs
				else: 
					full_orig_overs = math.floor(orig_overs)
					part_orig_overs = orig_overs - full_orig_overs
					full_overs = math.floor(overs)
					part_overs = overs - full_overs
					total_full = full_orig_overs + full_overs
					total_part = part_orig_overs + part_overs
					if total_part < 0.6:
						total_part = total_part
					elif total_part >= 0.6:
						total_part = total_part + 0.4

					new_overs = total_full + total_part

				df.set_value(idx2,'Rain_Overs_Bowled',new_overs)

# Save DataFrame
df.reset_index(drop=True, inplace=True)
df.to_csv('Team_Rain_Percentage.csv')