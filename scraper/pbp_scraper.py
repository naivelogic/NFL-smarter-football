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
    
#soup = grab_data('https://www.pro-football-reference.com/boxscores/201809060phi.htm', blocks=True)
#df = play_by_play(soup)
