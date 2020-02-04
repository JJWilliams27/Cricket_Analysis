# Calculate Stats

# Modules
import json
import pdb
from collections import Counter
from tqdm import tqdm
import pandas as pd
import numpy as np
import math
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore")

## Main ##
print("Calculating Bowling Statistics")

# Read CSVs
df = pd.read_csv('Player_Rain_Percentage.csv')
all_matches = pd.read_csv('c_champ_matches.csv')
rain_matches = pd.read_csv('rain_matches.csv')
all_matches = all_matches.iloc[:,1:].values
rain_matches = rain_matches.iloc[:,1:].values

# Add columns to df
df['Overs_Bowled'] = 0
df['Balls_Bowled'] = 0
df['Runs_Conceded'] = 0
df['Maidens'] = 0
df['Wickets'] = 0
df['Bowl_Average'] = 0
df['Economy'] = 0
df['Bowl_Strike_Rate'] = 0
df['Best_Figures'] = '0/0'
df['Best_Figures_MatchID'] = np.nan
df['Worst_Figures'] = '0/0'
df['Worst_Figures_MatchID'] = np.nan
df['5W'] = 0
df['Wides'] = 0
df['NB'] = 0

df['Rain_Overs_Bowled'] = 0
df['Rain_Balls_Bowled'] = 0
df['Rain_Runs_Conceded'] = 0
df['Rain_Maidens'] = 0
df['Rain_Wickets'] = 0
df['Rain_Bowl_Average'] = 0
df['Rain_Economy'] = 0
df['Rain_Bowl_Strike_Rate'] = 0
df['Rain_Best_Figures'] = '0/0'
df['Rain_Best_Figures_MatchID'] = np.nan
df['Rain_Worst_Figures'] = '0/0'
df['Rain_Worst_Figures_MatchID'] = np.nan
df['Rain_5W'] = 0
df['Rain_Wides'] = 0
df['Rain_NB'] = 0

df['Overs_Bowled'] = df.astype({'Overs_Bowled': 'float64'}).dtypes
df['Rain_Overs_Bowled'] = df.astype({'Rain_Overs_Bowled': 'float64'}).dtypes
df['Bowl_Average'] = df.astype({'Bowl_Average': 'float64'}).dtypes
df['Rain_Bowl_Average'] = df.astype({'Rain_Bowl_Average': 'float64'}).dtypes
df['Economy'] = df.astype({'Economy': 'float64'}).dtypes
df['Rain_Economy'] = df.astype({'Rain_Economy': 'float64'}).dtypes
df['Bowl_Strike_Rate'] = df.astype({'Bowl_Strike_Rate': 'float64'}).dtypes
df['Rain_Bowl_Strike_Rate'] = df.astype({'Rain_Bowl_Strike_Rate': 'float64'}).dtypes

# Loop through matches (need to do this for all matches and rain matches)
path = os.getcwd()
for n in tqdm(list(range(0,len(all_matches)))):
	mid = str(all_matches[n][0])
	with open(path + '/Matches/' + mid + '.json') as json_file:
	    minfo = json.load(json_file)
	    scard = minfo['scorecard'] # Grab scorecard from match info dictionary
	    try:
	    	inn1 = scard['inn1'] # Try getting innings, pass if dont exist (not all matches have 4 innings, some matches called off, etc)
	    	test = inn1['bowlcard'][0] # Test that the data is there by getting the first bowler of the innings
	    except:
	    	inn1=None
	    try:
	    	inn2 = scard['inn2'] 
	    	test = inn2['bowlcard'][0]
	    except:
	    	inn2=None
	    	pass
	    try:
	    	inn3 = scard['inn3']
	    	test = inn3['bowlcard'][0]
	    except:
	    	inn3=None
	    	pass
	    try:
	    	inn4 = scard['inn4']
	    	test = inn4['bowlcard'][0]
	    except:
	    	inn4=None
	    	pass
	    minfo.pop('scorecard',None) # Remove scorecard as it is now in its own dictionary for cleaner match info
	    innings = [inn1,inn2,inn3,inn4]

	for inn in innings:
		if inn != None:
			for i in list(range(0,len(inn['bowlcard']))):
				player_id = int(inn['bowlcard'][i]['id'])
				overs = float(inn['bowlcard'][i]['overs'])
				maidens = int(inn['bowlcard'][i]['maidens'])
				runs = int(inn['bowlcard'][i]['runs'])
				wickets = int(inn['bowlcard'][i]['wickets'])
				wides = int(inn['bowlcard'][i]['wides'])
				nb = int(inn['bowlcard'][i]['nballs'])	

				# Find in df
				idx = df.loc[df['PlayerID'] == player_id].index[0]

				# Update df
				orig_overs = df['Overs_Bowled'][idx]
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

				new_runs = df['Runs_Conceded'][idx] + runs
				new_maidens = df['Maidens'][idx] + maidens
				new_wickets = df['Wickets'][idx] + wickets
				new_wides= df['Wides'][idx] + wides
				new_nb = df['NB'][idx] + nb
				df.set_value(idx,'Overs_Bowled',new_overs)
				df.set_value(idx,'Runs_Conceded',new_runs)
				df.set_value(idx,'Maidens',new_maidens)
				df.set_value(idx,'Wickets',new_wickets)
				df.set_value(idx,'Wides',new_wides)
				df.set_value(idx,'NB',new_nb)

				if wickets >= 5:
					new_5w = df['5W'][idx] + 1
					df.set_value(idx,'5W',new_5w)

				best_wickets = int(df['Best_Figures'][idx].split('/')[0])
				best_runs = int(df['Best_Figures'][idx].split('/')[1])

				if df['Best_Figures'][idx] == '0/0':
					new_best = str('%s/%s' %(wickets,runs))
					df.set_value(idx,'Best_Figures',new_best)
					df.set_value(idx,'Best_Figures_MatchID',mid)
				else:
					if wickets == best_wickets:
						if runs < best_runs:
							new_best = str('%s/%s' %(wickets,runs))
							df.set_value(idx,'Best_Figures',new_best)
							df.set_value(idx,'Best_Figures_MatchID',mid)
					elif wickets > best_wickets:
						new_best = str('%s/%s' %(wickets,runs))
						df.set_value(idx,'Best_Figures',new_best)
						df.set_value(idx,'Best_Figures_MatchID',mid)

				worst_wickets = int(df['Worst_Figures'][idx].split('/')[0])
				worst_runs = int(df['Worst_Figures'][idx].split('/')[1])

				if df['Worst_Figures'][idx] == '0/0':
					new_worst = str('%s/%s' %(wickets,runs))
					df.set_value(idx,'Worst_Figures',new_worst)
					df.set_value(idx,'Worst_Figures_MatchID',mid)
				else:
					if wickets == worst_wickets:
						if runs > worst_runs:
							new_worst = str('%s/%s' %(wickets,runs))
							df.set_value(idx,'Worst_Figures',new_worst)
							df.set_value(idx,'Worst_Figures_MatchID',mid)
					elif wickets < worst_wickets:
						new_worst = str('%s/%s' %(wickets,runs))
						df.set_value(idx,'Worst_Figures',new_worst)
						df.set_value(idx,'Worst_Figures_MatchID',mid)

	if int(mid) in rain_matches:
		for inn in innings:
			if inn != None:
				for i in list(range(0,len(inn['bowlcard']))):
					player_id = int(inn['bowlcard'][i]['id'])
					overs = float(inn['bowlcard'][i]['overs'])
					maidens = int(inn['bowlcard'][i]['maidens'])
					runs = int(inn['bowlcard'][i]['runs'])
					wickets = int(inn['bowlcard'][i]['wickets'])
					wides = int(inn['bowlcard'][i]['wides'])
					nb = int(inn['bowlcard'][i]['nballs'])	

					# Find in df
					idx = df.loc[df['PlayerID'] == player_id].index[0]

					# Update df
					orig_overs = df['Rain_Overs_Bowled'][idx]
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

					new_runs = df['Rain_Runs_Conceded'][idx] + runs
					new_maidens = df['Rain_Maidens'][idx] + maidens
					new_wickets = df['Rain_Wickets'][idx] + wickets
					new_wides= df['Rain_Wides'][idx] + wides
					new_nb = df['Rain_NB'][idx] + nb
					df.set_value(idx,'Rain_Overs_Bowled',new_overs)
					df.set_value(idx,'Rain_Runs_Conceded',new_runs)
					df.set_value(idx,'Rain_Maidens',new_maidens)
					df.set_value(idx,'Rain_Wickets',new_wickets)
					df.set_value(idx,'Rain_Wides',new_wides)
					df.set_value(idx,'Rain_NB',new_nb)

					if wickets >= 5:
						new_5w = df['Rain_5W'][idx] + 1
						df.set_value(idx,'Rain_5W',new_5w)

					best_wickets = int(df['Rain_Best_Figures'][idx].split('/')[0])
					best_runs = int(df['Rain_Best_Figures'][idx].split('/')[1])

					if df['Rain_Best_Figures'][idx] == '0/0':
						new_best = str('%s/%s' %(wickets,runs))
						df.set_value(idx,'Rain_Best_Figures',new_best)
						df.set_value(idx,'Rain_Best_Figures_MatchID',mid)
					else:
						if wickets == best_wickets:
							if runs < best_runs:
								new_best = str('%s/%s' %(wickets,runs))
								df.set_value(idx,'Rain_Best_Figures',new_best)
								df.set_value(idx,'Rain_Best_Figures_MatchID',mid)
						elif wickets > best_wickets:
							new_best = str('%s/%s' %(wickets,runs))
							df.set_value(idx,'Rain_Best_Figures',new_best)
							df.set_value(idx,'Rain_Best_Figures_MatchID',mid)

					worst_wickets = int(df['Rain_Worst_Figures'][idx].split('/')[0])
					worst_runs = int(df['Rain_Worst_Figures'][idx].split('/')[1])

					if df['Rain_Worst_Figures'][idx] == '0/0':
						new_worst = str('%s/%s' %(wickets,runs))
						df.set_value(idx,'Rain_Worst_Figures',new_worst)
						df.set_value(idx,'Rain_Worst_Figures_MatchID',mid)
					else:
						if wickets == worst_wickets:
							if runs > worst_runs:
								new_worst = str('%s/%s' %(wickets,runs))
								df.set_value(idx,'Rain_Worst_Figures',new_worst)
								df.set_value(idx,'Rain_Worst_Figures_MatchID',mid)
						elif wickets < worst_wickets:
							new_worst = str('%s/%s' %(wickets,runs))
							df.set_value(idx,'Rain_Worst_Figures',new_worst)
							df.set_value(idx,'Rain_Worst_Figures_MatchID',mid)

# Calculate Average and Economy
print('Calculating Averages, Economies and Strike Rates')
for i in tqdm(list(range(0,len(df)))):
	runs = df['Runs_Conceded'][i]
	overs = df['Overs_Bowled'][i]
	wickets = df['Wickets'][i]

	if not np.isnan(overs):
		if (overs).is_integer():
			econ = runs/overs
			balls = overs * 6
		else:
			full_overs = math.floor(overs)
			part_overs = overs - full_overs
			frac = part_overs/0.6
			calc_overs = full_overs + frac # Calculate actual overs as a fraction of 0.6 (i.e. 0.3 overs is half an over)
			econ = runs/calc_overs
			balls1 = full_overs * 6
			balls2 = int(part_overs * 10)
			balls = balls1 + balls2

		bowl_av = runs/wickets
		sr = balls/wickets

		try:
			df.set_value(i,'Bowl_Average',bowl_av)
			df.set_value(i,'Bowl_Strike_Rate',sr)
			df.set_value(i,'Balls_Bowled',balls)
			df.set_value(i,'Economy',econ)
		except:
			pass # Skip where players have no stats (i.e. testing fewer matches after extracting large player dataset)

		if np.isinf(df['Bowl_Average'][i]):
			df.set_value(i,'Bowl_Average',np.nan)
		if np.isinf(df['Bowl_Strike_Rate'][i]):
			df.set_value(i,'Bowl_Strike_Rate',np.nan)

	runs = df['Rain_Runs_Conceded'][i]
	overs = df['Rain_Overs_Bowled'][i]
	wickets = df['Rain_Wickets'][i]

	if not np.isnan(overs):
		if (overs).is_integer():
			econ = runs/overs
			balls = overs * 6
		else:
			full_overs = math.floor(overs)
			part_overs = overs - full_overs
			frac = part_overs/0.6
			calc_overs = full_overs + frac # Calculate actual overs as a fraction of 0.6 (i.e. 0.3 overs is half an over)
			econ = runs/calc_overs
			balls1 = full_overs * 6
			balls2 = int(part_overs * 10)
			balls = balls1 + balls2
			
		bowl_av = runs/wickets
		sr = balls/wickets

		try:
			df.set_value(i,'Rain_Bowl_Average',bowl_av)
			df.set_value(i,'Rain_Bowl_Strike_Rate',sr)
			df.set_value(i,'Rain_Balls_Bowled',balls)
			df.set_value(i,'Rain_Economy',econ)
		except:
			pass # Skip where players have no stats (i.e. testing fewer matches after extracting large player dataset)

		if np.isinf(df['Rain_Bowl_Average'][i]):
			df.set_value(i,'Rain_Bowl_Average',np.nan)
		if np.isinf(df['Rain_Bowl_Strike_Rate'][i]):
			df.set_value(i,'Rain_Bowl_Strike_Rate',np.nan)

# Save output DF
df.reset_index(drop=True, inplace=True)
df.to_csv('Player_Rain_Percentage.csv')