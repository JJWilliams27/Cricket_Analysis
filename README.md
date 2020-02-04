# Cricket_Analysis
Access cricket data from ESPN Cricinfo and aggregate into a Pandas dataframe/excel sheet to analyse the impact of rain-affected matches on team/individual statistics.
 
# Requirements
To access the cricinfo data, you will need to use my version of dwillis' python-espncricinfo (https://github.com/JJWilliams27/python-espncricinfo) which allows access to full batting and bowling scorecards.

# Running the code
Follow the script order section below. 

The code is currently set up to acquire county championship data from 2000-2018 and to analyse the impact of rain-affected matches, and so you will need to edit the code a little if you wish to look into something else (generic codes will be provided in future). For example, the 'max overs' parameter in 'get_matches' is used for an example analysis of rain affected matches. Set this to a high value (i.e. 500) if you wish to get all data. To choose a competition, you will need to series code which can be found by navigating to cricinfo and looking at the url (i.e. https://www.espncricinfo.com/series/_/id/19286/england-tour-of-south-africa gives a series code of 19286).
 
# Script order:

get_matches
get_teams_players
percentage_rain_affected

Then in any order:

rain_team_stats
rain_batting_stats
rain_bowling_stats
