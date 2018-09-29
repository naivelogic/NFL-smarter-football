import pandas as pd
import json


with open('./2017123108.json', 'r') as f:
    data = json.load(f)

### TODO: Develop script to get listing of Games by week 
"""
"""
gameid = '2017123108'
"""
## data[gameid]

dict_keys(['home', 'away', 'drives', 'scrsummary', 'weather', 'media', 
'yl', 'qtr', 'note', 'down', 'togo', 'redzone', 'clock', 'posteam', 'stadium'])
"""

# Drives
#drives = list(data[gameid]['drives'])[:-1]
drives = list(data[gameid]['drives'])[0]

"""
data[gameid]['away']['stats'].keys())
dict_keys(['passing', 'rushing', 'receiving', 'fumbles', 'kicking', 'punting', 'kickret
"""


# ---------------------------------------------------------------------------- #
#   Extract game data with given eid
#   - Fields parse from each 'play'
#     'drive',
#     'play',
#     'down',
#     'time',
#     'desc',
#     'ydstogo',
#     'qtr',
#     'ydsnet',
#     'yrdln',
#     'sp',
#     'posteam': offensive team
#     'note': Conclusion of each play
# ---------------------------------------------------------------------------- #

gamecenter = []
player_df = []

for drive in drives:    
    play_tb = {}
    plays = list(data[gameid]['drives'][drive]['plays'])
    
    
    
    cplay = data[gameid]['drives'][drive]['plays']
    for play in plays:
        
        
        play_tb['gameid'] = gameid
        play_tb['playid'] = play
        play_tb['drive'] = drive
        play_tb['qtr'] = cplay[play]['qtr']
        play_tb['down'] = cplay[play]['down']
        play_tb['time'] = cplay[play]['time']
        play_tb['yrdln'] = cplay[play]['yrdln']
        play_tb['ydstogo'] = cplay[play]['ydstogo']
        play_tb['posteam'] = cplay[play]['posteam']
        play_tb['desc'] = cplay[play]['desc']
        play_tb['sp'] = cplay[play]['sp']
        play_tb['note'] = cplay[play]['note']
        

        gamecenter.append(play_tb)
        
        
        player_tb = {}
        player_ids = list(cplay[play]['players'].keys())

        players_play = cplay[play]['players']

        for player_id in player_ids:
            for p in range(len(players_play[player_id])):
            
                player_tb['gameid'] = gameid
                player_tb['playid'] = play
                player_tb['playerName'] = players_play[player_id][p]['playerName']
                player_tb['playerID'] = player_id
                player_tb['yards'] = players_play[player_id][p]['yards']
                
                for info in players_play[player_ids[p]]:
                    if info['statId'] not in statmap.idmap: continue
                    statvals = statmap.values(info['statId'], info['yards'])

                    for k, v in enumerate(statvals):
                        print(v, statvals[v])
                        player_tb['action'] = v
                        player_tb['result'] = statvals[v]


                player_df.append(player_tb)
            

print(pd.DataFrame(gamecenter))


#################################################################################
### Players DF
player_df = []
player_tb = {}
player_ids = list(cplay[play]['players'].keys())

players_play = cplay[play]['players']

for player_id in player_ids:
    
    player_tb['gameid'] = gameid
    player_tb['playid'] = play
    player_tb['playerName'] = players_play[player_id]['playerName']
    player_tb['playerID'] = player_id
    player_tb['yards'] = players_play[player_id]['yards']
    
    
    player_df.append(player_tb)
    
t = play_stats_list[:3]

player_name_category = {
    'passer': ['passing'],
    'rusher': ['rushing'],
    'receiver': ['receiving'],
    'tackler1': ['defense_tkl', 'defense_tkl_primary', 'defense_tkl_loss'],
    'tackler2':['defense_ast'],
    'returner':['puntret', 'kickret']
}

for i in range(len(t)):
    
    for pid, stat in t[i]['players'].items():

        #print(pid)
        for events in stat:
            #print(events)
            dic_events = statmap.values(events['statId'], events['yards'])
            for event, result in dic_events.items():
                #t[i][event] = result
                if event == 'cat':
                    if result not in ['team', 'punting', 'kicking', 'fumbles', 'penalty']:
                        #print(dic_events[event])
                        if result == 'defense':
                            temp_ = [i for i in list(dic_events.keys()) if i != 'cat'][0]
                            for n, r in player_name_category.items():
                                if temp_ in r: 
                                    t[i][n] = events['playerName']
                        elif result in list(player_name_category.values()):
                            result_cat = list(player_name_category.keys())[list(player_name_category.values()).index(result)]
                            t[i][result_cat] = events['playerName']
                        else:
                            t[i][result] = events['playerName']


                else:
                    t[i][event] = result
    #                print(event, result, "play_id:", t[i]['play_id'] ,events['playerName'], events['yards'])

####################################################################################################################################
# Description Mining
import numpy as np
df_list = play_stats_list

# run play direction
direction = ['middle', 'left end', 'right end', 'left tackle', 'right tackle',
            'left guard', 'right guard']

# invese the quarter numbers in order to calculate the 'Time in Seconds' in the total game
inverse_qtr = [1, 4, 3, 2, 1, 1]
"""
DESCRIPTION MINING
"""
for i in range(len(df_list)):
    play_desc = df_list[i]['desc']

    # General Offense Stats
    
    if ' Shotgun ' in play_desc: df_list[i]['Shotgun'] = 1
    if ' No Huddle ' in play_desc: df_list[i]['No Huddle'] = 1
        
    ## Time Features
    """
    We created a list called `inverse_qtr` which we use to multiply agains tthe 
    total seconds of the clock in the game. This provides us a view of the 
    Seconds Elapsed throughout the game
    """
    df_list[i]['TimeSec'] = (float(df_list[i]['time'].minute) * 60 + float(df_list[i]['time'].second)) * inverse_qtr[df_list[i]['qtr']]  
    df_list[i]['SecLeftinHalf'] = float(df_list[i]['TimeSec']) * df_list[i]['TimeSec']
    df_list[i]['Last3mins'] = df_list[i]['SecLeftinHalf'] >= 1620
    
    # is it First Half or Second Half
    if df_list[i]['qtr'] <=2:
        df_list[i]['half'] = 1
    else:
        df_list[i]['half'] = 2
    
    
    # Passing Plays
    if ' pass ' in play_desc:
        df_list[i]['PlayType'] = 'pass'

        # search for distance and location
        result = re.search('pass \S+ \S+ \S+ ', play_desc)
        result = result.group(0).split()    # ['pass', 'incomplete', 'short', 'middle']

        # incomplete passes need to +1 on the result
        if ' incomplete ' in play_desc:
            df_list[i]['DIST'] = result[2]   # passing distance
            df_list[i]['LOC'] = result[3]    # passing location
        else:
            df_list[i]['DIST'] = result[1]   # passing distance
            df_list[i]['LOC'] = result[2]    # passing location


    # Running Plays
    if 'rushing_att' in list(df_list[i].keys()):
        df_list[i]['PlayType'] = 'run'
        
        # find direction of run play
        for s in direction:
            if s in play_desc:
                df_list[i]['LOC'] = s
            else: continue 
        #if direction_re.search(play_desc):
        #    df_list[i]['LOC'] = direction_re.search(play_desc)[0]   # running location
    
    # other play types
    play_notes = df_list[i]['note']
    if 'kneel' in play_desc: df_list[i]['PlayType'] = 'qb_kneel'
    elif 'Two-Minute Warning' in play_desc: df_list[i]['PlayType'] = 'NA'
    elif 'END ' in play_desc: df_list[i]['PlayType'] = 'NA'
    elif 'sacked ' in play_desc: df_list[i]['PlayType'] = 'pass'
    elif 'No Play' in play_desc: df_list[i]['PlayType'] = 'no_play'
        
    elif play_notes == 'KICKOFF': df_list[i]['PlayType'] = 'kickoff'
    elif play_notes == 'TIMEOUT': df_list[i]['PlayType'] = 'no_play'
    elif play_notes == 'FGM': df_list[i]['PlayType'] = 'field_goal'
    elif play_notes == 'FG': df_list[i]['PlayType'] = 'field_goal'
    elif play_notes == '2PR': df_list[i]['PlayType'] = 'run'
    elif play_notes == 'XP': df_list[i]['PlayType'] = 'extra_point'
    elif play_notes == 'PUNT': df_list[i]['PlayType'] = 'punt'
    
    
    # Include Appropriate `Yards Gained` based off of penalty
    if df_list[i]['note'] == 'PENALTY':
        result = re.search(" for \S+ yards", play_desc)
        if result is None: 
            df_list[i]['PlayType'] = 'no_play'
            continue; # no added yards to penalty
        result = result.group(0).split()    # ['pass', 'incomplete', 'short', 'middle']
        df_list[i]['yards_gain'] = int(result[1])
    
nfl_df = pd.DataFrame(df_list)

# if doing this for just a single game, some games dont have interceptions so 
# we may have to check for that manually and create zeros
if 'passing_int' not in list(df.columns):
    df['passing_int'] = 0

################################################################################################
# Creating the Scoring System
"""
from the notes column in the dataframe here are the key notes that indicates a score (in defferent of possession or defensive socre):
        `['TD', 'XP', 'FG', '2PR','FGM', '2PS' ]`. 
To identfy defensive score we use `defense_tds = 1`
"""
import numpy as np
# Team Indications 
away_abbr = str(game_data_dict['away']['abbr'])
home_abbr = str(game_data_dict['home']['abbr'])


# home team and away team indication
df['home_team'] = home_abbr
df['away_team'] = away_abbr

# defensive team indication
df['defteam'] = np.where(df.posteam == home_abbr, away_abbr, home_abbr)


df['posteam_score'] = 0
df['defteam_score'] = 0
df.loc[df.note == 'TD', 'posteam_score'] = 6
df.loc[(df.note == 'XP') & (df.desc.str.contains('GOOD')), 'posteam_score'] = 1
df.loc[(df.note == 'FG') & (df.desc.str.contains('GOOD')), 'posteam_score'] = 3
df.loc[(df.note == '2PR') & (df.desc.str.contains('SUCCEEDS')), 'posteam_score'] = 2
df.loc[(df.note == '2PS') & (df.desc.str.contains('SUCCEEDS')), 'posteam_score'] = 2

# scknoledge defense team score and remove from possession team
df.loc[df.defense_tds ==1, 'defteam_score' ] = 7 # defensive TD
df.loc[df.defense_tds ==1, 'posteam_score' ] = 0 # defensive TD

# set home and away team score
df['home_team_score'] = df[(df.posteam==home_abbr)].posteam_score
df['away_team_score'] = df[(df.posteam==away_abbr)].posteam_score
df.loc[(df.defense_tds ==1) & (df.defteam==home_abbr), 'home_team_score' ] = 7 # defensive TD
df.loc[(df.defense_tds ==1) & (df.defteam==away_abbr), 'away_team_score' ] = 7 # defensive TD

# cumulative sum for home and away scores
df['home_team_score']  = df.home_team_score.cumsum()
df['away_team_score']  = df.away_team_score.cumsum()

# differnece in score
df['score_diff'] = df.home_team_score - df.away_team_score









######################################################################################################################
# Create DataFrame Specifically for Passing    
pass_columns = ['play_id', 'passer', 'receiver', 'yards_gain','DIST','LOC','passing_tds' ,'passing_yds','passing_att',
                 'passing_cmp','passing_int','passing_cmp_air_yds', 'passing_int', 'passing_first_down']
pass_ = nfl_df[nfl_df.PlayType=='pass'][pass_columns]
[pass_[i].fillna(0, inplace=True) for i in pass_.columns]
#pass_.to_csv('pass_.csv')
pass_.head()

#####################################################################################################################
# Create DataFrame Specifically for Rushing    
run_columns = ['play_id', 'passer', 'receiver', 'yards_gain','DIST','LOC','rushing_tds' ,'rushing_yds','rushing_att',
               'rushing_first_down']
run_ = nfl_df[nfl_df.PlayType=='run'][run_columns]
[run_[i].fillna(0, inplace=True) for i in run_.columns]
#run_.to_csv('run_.csv')
run_.head()
