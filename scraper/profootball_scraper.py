"""

"""

# Imports and Date Processing
import feedparser
import pandas as pd
import re
from datetime import datetime
import feedparser

# Create dataframe to collect NFL team team taxonomy from 
# profootball talk site. Each team is organized by:
# /team/[conference]/[team name]/feed/

nfl_teams_for_parser = [
    "afc/baltimore-ravens/feed/",
    "afc/buffalo-bills/feed/",
    "afc/cincinnati-bengals/feed/",
    "afc/cleveland-browns/feed/",
    "afc/denver-broncos/feed/",
    "afc/houston-texans/feed/",
    "afc/indianapolis-colts/feed/",
    "afc/jacksonville-jaguars/feed/",
    "afc/kansas-city-chiefs/feed/",
    "afc/los-angeles-chargers/feed/",
    "afc/miami-dolphins/feed/",
    "afc/new-england-patriots/feed/",
    "afc/new-york-jets/feed/",
    "afc/oakland-raiders/feed/",
    "afc/pittsburgh-steelers/feed/",
    "afc/tennessee-titans/feed/",
    "nfc/arizona-cardinals/feed/",
    "nfc/atlanta-falcons/feed/",
    "nfc/carolina-panthers/feed/",
    "nfc/chicago-bears/feed/",
    "nfc/dallas-cowboys/feed/",
    "nfc/detroit-lions/feed/",
    "nfc/green-bay-packers/feed/",
    "nfc/los-angeles-rams/feed/",
    "nfc/minnesota-vikings/feed/",
    "nfc/new-orleans-saints/feed/",
    "nfc/new-york-giants/feed/",
    "nfc/philadelphia-eagles/feed/",
    "nfc/san-francisco-49ers/feed/",
    "nfc/seattle-seahawks/feed/",
    "nfc/tampa-bay-buccaneers/feed/",
    "nfc/washington-redskins/feed/"
]


def set_url(team):
    urls = ["https://profootballtalk.nbcsports.com/category/teams/"+str(x) for x in team]
    return urls
 
import newspaper
from newspaper import Article

def newspaper_parser(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    article.summary
    k = article.text
    return k
  
 
def profootball_parser(team):
    url = feedparser.parse(team)
    post = []
    for i, entry in enumerate(url['entries']):
        row = {}
        row['id'] = entry['id']
        row['id_num'] = re.findall('\d+', entry['id'] )
        #row['authors'] = entry['authors']
        
        # The RSS Feed only provides a limited summary
        # .. the function below enables us to extract the full 
        # .. full articles text based off the RSS URL procided
        link_to_detail_article = entry['link']
        row['article'] = newspaper_parser(link_to_detail_article)
        
        row['summary'] = entry['summary_detail']['value'].split('[')[0]
        #row['summary'] = entry['summary']
        row['link'] = entry['link']
        date = entry['published']
        row['date'] = pd.to_datetime(date).date()
        row['tags'] = [j['term'] for j in entry['tags']]   
        post.append(row)
    return post
  
  
urls = set_url(nfl_teams_for_parser)
df = {}

for url in urls:
    table = profootball_parser(url)
    team = url[57:-6]
    df[team] = table

    df.keys()
  

# save to json
import json
#df1 = json.dumps(df)
df1 = json.dumps(df, indent=4, sort_keys=True, default=str)


with open('profootball.json', 'w') as outfile:
    json.dump(df1, outfile)
  
