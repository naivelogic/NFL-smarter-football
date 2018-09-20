import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import urllib3

def grab_data(url, blocks=False):
    """
    function to get soup
    """
    r = requests.get(url)
    if blocks == False:
        soup = BeautifulSoup(r.text, 'html.parser')
    else:
        # needs to remove the <-- -->
        block = re.compile("<!--|-->")
        soup = BeautifulSoup(block.sub("", r.text), 'lxml')

    return soup

def box_score_urls(week_num):
    url = ('https://www.pro-football-reference.com/years/2018/week_{0}.htm'.format(week_num))
    
    # scrape data
    soup = grab_date(url)
    
    # create box score url list
    game_id = []
    for i in soup.find_all("td", class_ = "right gamelink"):
        game_id.append("https://www.pro-football-reference.com" + i.find('a')['href'])
    
    return game_id
    
def play_by_play(url):
  tb = soup.findAll("div", id = "div_pbp")
  tr = tb[0].find_all('tr')

  pbp = [[td.getText() for td in tr[i].find_all(['th', 'td'])] for i in range(len(tr))]

  df = pd.DataFrame(pbp)

  # new headers
  df.columns = pbp[0]
  df = df[2:]

  df = df[~df.Quarter.isin(['Quarter',  '2nd Quarter', '3rd Quarter','4th Quarter', 'End of Regulation']) ].reset_index(drop=True)

  return df
    
soup = grab_data('https://www.pro-football-reference.com/boxscores/201809060phi.htm', blocks=True)
## Need to work on for loop to loop through each week box score provided by the box_score_urls function
df = play_by_play(soup)

# indicate home and away teams
home_drives['pos'] = df.columns[7]
away_drives['pos'] = df.columns[6]


def pullTable(url, tableID, header = True):
# https://github.com/BenKite/football_data/blob/master/profootballReferenceScrape.py

    res = requests.get(url)
    ## Work around comments
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
    tables = soup.findAll('table', id = tableID)
    data_rows = tables[0].findAll('tr')
    game_data = [[td.getText() for td in data_rows[i].findAll(['th','td'])]
        for i in range(len(data_rows))
        ]
    data = pd.DataFrame(game_data)
    if header == True:
        data_header = tables[0].findAll('thead')
        data_header = data_header[0].findAll("tr")
        data_header = data_header[0].findAll("th")
        header = []
        for i in range(len(data.columns)):
            header.append(data_header[i].getText())
        data.columns = header
        data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)
    return(data)

### Identify Offensive Possession ###
home_drives = pullTable('https://www.pro-football-reference.com/boxscores/201809060phi.htm', 'home_drives')
away_drives = pullTable('https://www.pro-football-reference.com/boxscores/201809060phi.htm', 'vis_drives')

# creat table for game drives
drives = away_drives.append(home_drives).reset_index(drop=True)

drives['FTime'] = pd.to_datetime(drives['Time'])
drives['#'] = drives['#'].astype(int)
drives = drives.sort_values(by=['Quarter','Time'], ascending=[True,False])
drives = drives.reset_index(drop=True)

# create loop to define offensive that has possession of the ball in the `df` dataframe
for i in range(len(drives)):
    df.loc[(df.FTime <= drives.FTime[i]) & (df.Quarter == drives.Quarter[i]) &
           (df.Time!=''), 'pos'] = drives.pos[i]

# add new features for adjustment on time 
        #    WIP    #
    

# NFL Data Table Fields
## Passing Data Table
passing_features = []

for i,play in df.iterrows():
    play_tb = {}
    
    desc = play['Detail']
    play_tb['playid'] = play.playid
    
    # Penalty
    if ' Penalty ' and '(no play)' in desc:
        play_tb['penalty'] = 1
        continue 
        
    elif 'Penalty ' in desc:
        result = re.search(', \S+ yards ', desc)
        # [',', '5', 'yards']
        play_tb['yds'] = result[1]
        
        """
        
        << Need to determine the direction of the Penalty >>
        
        """
        
    
    # Passing Plays
    passing = {}
    
    if ' pass ' in desc:
        passing['playid'] = play.playid
        passing['passer'] = desc.split(' pass ')[0]
        
        if ' challenged ' in desc:
            
            """
            NOT SURE WHAT TO DO HERE
            
            """
        
        # pass successful?
        if ' complete ' in desc:
            passing['succ'] = 1
            
            result = re.search('complete \S+ \S+ to \S+ \S+ for \S+ ', desc)
            #['complete', 'deep', 'left', 'to', 'Julio', 'Jones', 'for', '33']
            result = result.group(0).split()
            passing['DIST'] = result[1]   # passing Distance
            passing['LOC'] = result[2]   # passing location
            passing['target'] = result[4] + ' ' + result[5]   # passing target
            passing['yds'] = result[7]  # yards gained
            
        # incomplete passes
        else:
            passing['succ'] = 0
            if 'intended for' in desc:
                result = re.search('incomplete \S+ \S+ intended for \S+ \S+', desc)
                
                if result is None: 
                    continue; # ball thrown away
                
                result = result.group(0).split()
                # ['incomplete', 'short', 'left', 'intended', 'for', 'Julio', 'Jones']
                passing['DIST'] = result[1]   # passing Distance
                passing['LOC'] = result[2]   # passing location
                passing['target'] = result[5] + ' ' + result[6]   # passing target
                passing['yds'] = 0
    
    passing_features.append(passing) 

    
## Passing Data Table
running_features = []

for i,play in df.iterrows():
    # Running Plays
    running = {}
    
    if ' run ' in desc:
        running['playid'] = play.playid
        running['runner'] = desc.split(' run ')[0]
    
    
    running_features.append(running) 

