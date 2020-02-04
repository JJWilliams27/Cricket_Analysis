import pandas as pd
import pdb
import requests
from espncricinfo.player import Player
from espncricinfo.match import Match
from espncricinfo.series import Series

# Get cricket world cup 
#cwc19 = Series('8039')

# Get all matches
#matches = Series.get_events_for_season(cwc19,2019)

# Construct original table
#groupstage = pd.read_csv('cwc19_final_table.csv')

# Get County Championship
#cchamp1 = Series('8052')
#cchamp2 = Series('8204')

# Get county champsionship seasons
print('Getting Match IDs')
#matches = Series.get_events_for_season(cchamp1,2018)
#matches.append(Series.get_events_for_season(cchamp2,2018))

m=Match(1166949)
i1,i2,i3,i4 = m.getbattingdataframe()
pdb.set_trace()
req = requests.get(m.json_url)

url = m.espn_api_url

def get_json(url):
    r = requests.get(url)
    if r.status_code == 404:
        raise "Not Found"
    else:
        return r.json()

test = get_json(url)

#notes
#gameInfo
#debuts
#rosters
#matchcards
#news
#article
#videos
#leaders
#header


pdb.set_trace()