"""
Development of a python scraper to pull articles from NFL Teams News 
RSS Feeds. This scripts parses the rss feed,and organizes in to the necessary
fields and saves it to a CSV file. We are working on pulling this directly in
to a SQLite database. 

This code is heavily reliant on Newspaper, here is the documentations:https://newspaper.readthedocs.io/en/latest/
"""

import newspaper
from newspaper import Article
import pandas as pd
from datetime import datetime

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import os
"""
This is the most annoying thing about newspaper... i love it but, there is a manual 
hack that i had to put in because the articles wouldnt cache correcntly. 
"""
cache_to_remove = '<INSERT HOME DIR> + .newspaper_scraper/feed_category_cache> + HASH'

def newspaper_parser(url):
    article = Article(url, memoize_articles=True, fetch_images=False)

    return article

def feedburner_scraper(url_list, team):
    from datetime import datetime
    feed_articles = []
    for url in url_list:     
        row = {}
        post = newspaper_parser(url)
        post.download()
        if post.download_state != 2:
            print("URL not downloaded: ", url)
            continue
        post.parse()
        post.nlp()

        row['url'] = post.url
        if post.publish_date is None:
            row['date'] = None
        else:
            row['date'] = pd.to_datetime(post.publish_date).date()
        row['title'] = post.title
        row['keywords'] = post.keywords
        #row['text'] = post.summary
        row['text'] = post.text
        row['team'] = team
        feed_articles.append(row)
        
    try: os.remove(cache_to_remove)
    except OSError: pass
    
    return feed_articles

    
def sbnation_scraper(url, team):
    """
    function to pull the rss/news URL with the team name and necessary fields using the
    `feedburner_scraper` function listed above. 
    """
    newys = newspaper.build(url, memoize_articles=True, fetch_images=False)
    newsy_urls = []
    for article in newys.articles:
        if 'sportspyder.com/' not in article.url:
            newsy_urls.append(article.url)
    
    print("------------ ",team," -----------")
    print("# of articles found: ", len(newsy_urls))
    
    news = feedburner_scraper(newsy_urls, team)
    
    print("# of articles processed: ", len(news))
    print("List keys: ",news[0].keys())
    print("List keywords", news[0]['keywords'])
    
    return news
    
# hawks = sbnation_scraper('https://www.fieldgulls.com')

"""
-------------------------------------------------------------------------------
# of articles found:  151
# of articles:  151
List keys:  dict_keys(['url', 'date', 'title', 'keywords', 'text'])
List keywords ['thing', 'mock', 'hit', 'midpreseason', 'followed', 'watch', 'seahawks', 'vs', 'draft', '3000', 'thats', 'rob', 'weeks', 'nfl', 'vikings', 'twitter']
-------------------------------------------------------------------------------
"""

# using feedparser to get url listing then fead it through feedburner_scraper
import feedparser
def feedparser_search(url_string, team):
    urls = feedparser.parse(url_string)
    pat_urls = []
    for url in urls['entries']:
        x = url['links'][0]['href']
        pat_urls.append(x)
    
    print("------------ ",team," -----------")
    print("Number of articles: ", len(pat_urls))
    
    tables = feedburner_scraper(pat_urls, team)
    
       
    print("# of articles processed: ", len(tables))
    print("List keys: ",tables[0].keys())
    print("List keywords", tables[0]['keywords'])
    
    return tables

# nflnation = feedparser_search('http://www.espn.com/blog/feed?blog=nflnation')

def get_feed(feed_dict):
    df = []
    for team in feed_dict:
        result = feedparser_search(feed_dict[team], team)
        table = pd.DataFrame(result)
        df.append(table)

    nfl = pd.concat(df)
    nfl = nfl.drop_duplicates(subset='title').reset_index(drop=True)
    
    return nfl



# Get Transcripts from youtube videos
from youtube_transcript_api import YouTubeTranscriptApi
def youtube_scraper(url_string):
    urls = feedparser.parse(url_string)
    pat_urls = []
    for url in urls['entries']:
        x = url['links'][0]['href']
        pat_urls.append(x)
    
    
    newsy_urls = []
    for youtube_url in pat_urls:
        youtube = YouTubeTranscriptApi.get_transcript(youtube_url[32:])
        transcripts = []
        [transcripts.append(vid['text']) for vid in youtube if vid['text'] != '[Music]' and vid['text'] != '[Applause]']
        newsy_urls.append(transcripts)
    

    return newsy_urls

# nfl_youtube = youtube_scraper('https://www.youtube.com/feeds/videos.xml?user=NFL')

# Save to json
import json
def save_to_json(doc, label):
    doc = json.dumps(doc, indent=4, sort_keys=True, default=str)
    with open(label+'_news.json', 'w') as outfile:
        json.dump(doc, outfile)

#doc = {'hawks':hawks }

#[save_to_json(doc[y], y) for x,y in enumerate(doc)]
        
# Open json
import pandas as pd
import json
from pprint import pprint
def open_new_json(doc):
    with open(doc+'_news.json', encoding='utf-8') as f:
        dat = json.load(f)
    dat = json.loads(dat)
    df = pd.DataFrame(dat)
    df['team'] = doc
    
    return df


document =[
    'hawks',
    'patriots',
    'steelers',
    'cheese',
    'panthers',
    'cardinals',
    'cowboys'
]

def open_json():
    df = {}
    for doc in document:
        df[doc] = open_json(doc)
    nfl = pd.concat(df.values())
    
    nfl = nfl.drop_duplicates(subset='text').reset_index(drop=True)
    nfl['date'] = pd.to_datetime(nfl['date'], format="%Y%m%d %H:%M:%S").dt.date
    nfl['day'] =  pd.to_datetime(nfl['date']).dt.day
    
    return nfl
