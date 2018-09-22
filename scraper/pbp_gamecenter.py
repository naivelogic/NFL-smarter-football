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


print("\n")


"""
data[gameid]['away']['stats'].keys())

dict_keys(['passing', 'rushing', 'receiving', 'fumbles', 'kicking', 'punting', 'kickret
"""

# Plays IDs

#for drive in driveids:
#    print(data[gameid]['drives'][drive]['plays'])

#print(data[gameid]['drives'][drives[0]]['plays'].keys())

#print(data[gameid]['drives'][drives[0]]['plays']['37'])


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


print(cplay['37'].keys())

# players
print(cplay['37']['players'].keys())
"""
dict_keys(['00-0030968', '00-0030465', '00-0028660'])
"""
print(cplay['37']['players']['00-0028660'])
