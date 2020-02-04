# Calculate Stats

# Modules
import json
import pdb
from collections import Counter
from tqdm import tqdm
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore")

## Main ##
print("Calculating Batting Statistics")

# Read CSVs
df = pd.read_csv('Player_Rain_Percentage.csv')
all_matches = pd.read_csv('c_champ_matches.csv')
rain_matches = pd.read_csv('rain_matches.csv')
all_matches = all_matches.iloc[:,1:].values
rain_matches = rain_matches.iloc[:,1:].values

# Add columns to df
df['Innings'] = 0
df['Total_Runs'] = 0
df['Not_Out'] = 0
df['Bat_Average'] = 0
df['High_Score'] = 0
df['HS_MatchID'] = np.nan
df['Balls_Faced'] = 0
df['Strike_Rate'] = 0
df['Fours'] = 0
df['Sixes'] = 0
df['50s'] = 0
df['100s'] = 0
df['0s'] = 0

df['Rain_Innings'] = 0
df['Rain_Total_Runs'] = 0
df['Rain_Not_Out'] = 0
df['Rain_Bat_Average'] = 0
df['Rain_High_Score'] = 0
df['Rain_HS_MatchID'] = np.nan
df['Rain_Balls_Faced'] = 0
df['Rain_Strike_Rate'] = 0
df['Rain_Fours'] = 0
df['Rain_Sixes'] = 0
df['Rain_50s'] = 0
df['Rain_100s'] = 0
df['Rain_0s'] = 0

df['Bat_Average'] = df.astype({'Bat_Average': 'float64'}).dtypes
df['Rain_Bat_Average'] = df.astype({'Rain_Bat_Average': 'float64'}).dtypes
df['Strike_Rate'] = df.astype({'Strike_Rate': 'float64'}).dtypes
df['Rain_Strike_Rate'] = df.astype({'Rain_Strike_Rate': 'float64'}).dtypes

# Loop through matches (need to do this for all matches and rain matches)
path = os.getcwd()
for n in tqdm(list(range(0,len(all_matches)))):
	mid = str(all_matches[n][0])
	with open(path + '/Matches/' + mid + '.json') as json_file:
	    minfo = json.load(json_file)
	    scard = minfo['scorecard'] # Grab scorecard from match info dictionary
	    try:
	    	inn1 = scard['inn1'] # Try getting innings, pass if dont exist (not all matches have 4 innings, some matches called off, etc)
	    	test = inn1['batcard'][0] # Test that the data for this innings exists by getting the first batsman's data
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
	    minfo.pop('scorecard',None) # Remove scorecard as it is now in its own dictionary for cleaner match info
	    innings = [inn1,inn2,inn3,inn4]

	for inn in innings:
		if inn != None:
			for i in list(range(0,len(inn['batcard']))):
				player_id = int(inn['batcard'][i]['id'])
				runs = int(inn['batcard'][i]['runs'])
				balls = int(inn['batcard'][i]['balls'])
				fours = int(inn['batcard'][i]['fours'])
				sixes = int(inn['batcard'][i]['sixes'])
				if inn['batcard'][i]['not_out'] == False:
					notout = 0
				else:
					notout = 1

				# Find in df
				try:
					idx = df.loc[df['PlayerID'] == player_id].index[0]	
				except:
					print(player_id)
					print(mid)

				# Update df
				new_innings = df['Innings'][idx] + 1
				new_runs = df['Total_Runs'][idx] + runs
				new_no = df['Not_Out'][idx] + notout
				new_bf = df['Balls_Faced'][idx] + balls
				new_fours = df['Fours'][idx] + fours
				new_sixes = df['Sixes'][idx] + sixes
				df.set_value(idx,'Innings',new_innings)
				df.set_value(idx,'Total_Runs',new_runs)
				df.set_value(idx,'Not_Out',new_no)
				df.set_value(idx,'Balls_Faced',new_bf)
				df.set_value(idx,'Fours',new_fours)
				df.set_value(idx,'Sixes',new_sixes)
				if runs > df['High_Score'][idx]:
					df.set_value(idx,'High_Score',runs)
					df.set_value(idx,'HS_MatchID',mid)
				if runs >= 100:
					new_100s = df['100s'][idx] + 1
					df.set_value(idx,'100s',new_100s)
				if 50 <= runs < 100:
					new_50s = df['50s'][idx] + 1
					df.set_value(idx,'50s',new_50s)
				if runs == 0:
					new_0s = df['0s'][idx] + 1
					df.set_value(idx,'0s',new_0s)

	if int(mid) in rain_matches:
		for inn in innings:
			if inn != None:
				for i in list(range(0,len(inn['batcard']))):
					player_id = int(inn['batcard'][i]['id'])
					runs = int(inn['batcard'][i]['runs'])
					balls = int(inn['batcard'][i]['balls'])
					fours = int(inn['batcard'][i]['fours'])
					sixes = int(inn['batcard'][i]['sixes'])
					if inn['batcard'][i]['not_out'] == False:
						notout = 0
					else:
						notout = 1

					# Find in df
					idx = df.loc[df['PlayerID'] == player_id].index[0]

					# Update df
					new_innings = df['Rain_Innings'][idx] + 1
					new_runs = df['Rain_Total_Runs'][idx] + runs
					new_no = df['Rain_Not_Out'][idx] + notout
					new_bf = df['Rain_Balls_Faced'][idx] + balls
					new_fours = df['Rain_Fours'][idx] + fours
					new_sixes = df['Rain_Sixes'][idx] + sixes
					df.set_value(idx,'Rain_Innings',new_innings)
					df.set_value(idx,'Rain_Total_Runs',new_runs)
					df.set_value(idx,'Rain_Not_Out',new_no)
					df.set_value(idx,'Rain_Balls_Faced',new_bf)
					df.set_value(idx,'Rain_Fours',new_fours)
					df.set_value(idx,'Rain_Sixes',new_sixes)
					if runs > df['Rain_High_Score'][idx]:
						df.set_value(idx,'Rain_High_Score',runs)
						df.set_value(idx,'Rain_HS_MatchID',mid)
					if runs >= 100:
						new_100s = df['Rain_100s'][idx] + 1
						df.set_value(idx,'Rain_100s',new_100s)
					if 50 <= runs < 100:
						new_50s = df['Rain_50s'][idx] + 1
						df.set_value(idx,'Rain_50s',new_50s)
					if runs == 0:
						new_0s = df['Rain_0s'][idx] + 1
						df.set_value(idx,'Rain_0s',new_0s)

# Calculate Batting Averages and Strike Rates
print('Calculating Averages and Strike Rates')
for i in tqdm(list(range(0,len(df)))):
	runs = df['Total_Runs'][i]
	inns = df['Innings'][i]
	notout = df['Not_Out'][i]
	inns = inns - notout
	balls = df['Balls_Faced'][i]
	av = float(runs/inns)
	sr = float((runs/balls)*100)
	if np.isinf(av):
		av = np.nan
	if np.isinf(sr):
		sr = np.nan
	try:
		df.set_value(i,'Bat_Average',av)
		df.set_value(i,'Strike_Rate',sr)
	except:
		pass # Skip where players have no stats (i.e. testing fewer matches after extracting large player dataset)
	runs = df['Rain_Total_Runs'][i]
	inns = df['Rain_Innings'][i]
	notout = df['Rain_Not_Out'][i]
	inns = inns - notout
	balls = df['Rain_Balls_Faced'][i]
	av = float(runs/inns)
	sr = float((runs/balls)*100)
	if np.isinf(av):
		av = np.nan
	if np.isinf(sr):
		sr = np.nan
	try:
		df.set_value(i,'Rain_Bat_Average',av)
		df.set_value(i,'Rain_Strike_Rate',sr)
	except:
		pass

# Save output DF
df.reset_index(drop=True, inplace=True)
df.to_csv('Player_Rain_Percentage.csv')