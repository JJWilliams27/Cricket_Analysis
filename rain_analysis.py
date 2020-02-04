# Rain Analysis - Player Stats

# Calculate Stats

# Modules
from espncricinfo.player import Player
from espncricinfo.match import Match
from espncricinfo.series import Series
import json
import matplotlib.pyplot as plt
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

# Read CSVs
df = pd.read_csv('Player_Rain_Percentage.csv')

### Create Comparative Metrics ###
def adjusted_average_div(average1,average2):
	adj_average = average1/average2 # Divide so normalised
	return adj_average

def adjusted_average_perc(average1,average2):
	adj_average = average1/average2
	if adj_average < 1:
		adj_average = (-adj_average)/1 # Make so equal either side (though can't get values between -1 and 1)
	return adj_average

# Normal Average - Rain Average (postive value means better average with no rain, negative means better average in rain affected draw)
def adjusted_average_sub(average1,average2):
	adj_average = average1 - average2 # Subtract for actual values
	return adj_average


df['Adjusted_Batting_Average'] = df.apply(lambda x: adjusted_average_sub(x.Bat_Average, x.Rain_Bat_Average), axis=1)
df['Adjusted_Batting_SR'] = df.apply(lambda x: adjusted_average_sub(x.Strike_Rate, x.Rain_Strike_Rate), axis=1)
df['Adjusted_Batting_HS'] = df.apply(lambda x: adjusted_average_sub(x.High_Score, x.Rain_High_Score), axis=1)
# Inverse as bowling averages are better when lower
df['Adjusted_Bowling_Average'] = df.apply(lambda x: adjusted_average_sub(x.Rain_Bowl_Average, x.Bowl_Average), axis=1) 
df['Adjusted_Bowling_SR'] = df.apply(lambda x: adjusted_average_sub(x.Rain_Bowl_Strike_Rate, x.Bowl_Strike_Rate), axis=1)
df['Adjusted_Bowling_Econ'] = df.apply(lambda x: adjusted_average_sub(x.Rain_Economy, x.Economy), axis=1)

df['Adjusted_Batting_Average_Perc'] = df.apply(lambda x: adjusted_average_perc(x.Bat_Average, x.Rain_Bat_Average), axis=1)
df['Adjusted_Batting_SR_Perc'] = df.apply(lambda x: adjusted_average_perc(x.Strike_Rate, x.Rain_Strike_Rate), axis=1)
df['Adjusted_Batting_HS_Perc'] = df.apply(lambda x: adjusted_average_perc(x.High_Score, x.Rain_High_Score), axis=1)
# Inverse as bowling averages are better when lower
df['Adjusted_Bowling_Average_Perc'] = df.apply(lambda x: adjusted_average_perc(x.Rain_Bowl_Average, x.Bowl_Average), axis=1) 
df['Adjusted_Bowling_SR_Perc'] = df.apply(lambda x: adjusted_average_perc(x.Rain_Bowl_Strike_Rate, x.Bowl_Strike_Rate), axis=1)
df['Adjusted_Bowling_Econ_Perc'] = df.apply(lambda x: adjusted_average_perc(x.Rain_Economy, x.Economy), axis=1)

# High Score Extremity - How much of an outlier is a player's high score (HS/Batting Average - Higher = more extreme high score)
df['HS_Extremity'] = df.apply(lambda x: adjusted_average_div(x.High_Score, x.Bat_Average),axis=1)
df['Rain_HS_Extremity'] = df.apply(lambda x: adjusted_average_div(x.Rain_High_Score, x.Rain_Bat_Average),axis=1)
df['Adjusted_HS_Extremity'] = df.apply(lambda x: adjusted_average_sub(x.HS_Extremity, x.Rain_HS_Extremity),axis=1)




# Output csv with news metrics
df.reset_index(drop=True, inplace=True)
df.to_csv('Player_Rain_Percentage.csv')