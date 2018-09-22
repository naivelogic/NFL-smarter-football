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


for drive in drives:    
    plays = list(data[gameid]['drives'][drive]['plays'])
    
    print("For drive: {0}, this is the list of plays{1}".format(drive,plays))

    
    
    
    cplay = data[gameid]['drives'][drive]['plays']
    for play in plays:
        play_tb = {}

        play_tb['gameid'] = gameid
        play_tb['playid'] = play
        play_tb['drive'] = drive
        play_tb['qtr'] = cplay[play]['qtr']
        play_tb['down'] = cplay[play]['down']
        play_tb['time'] = cplay[play]['time']
        play_tb['yrdln'] = cplay[play]['yrdln']
        play_tb['ydstogo'] = cplay[play]['ydstogo']
        play_tb['desc'] = cplay[play]['desc']

    gamecenter.append(play_tb)

print(pd.DataFrame(gamecenter))


print(cplay['37'].keys())

# players
print(cplay['37']['players'].keys())
"""
dict_keys(['00-0030968', '00-0030465', '00-0028660'])
"""
print(cplay['37']['players']['00-0028660'])
