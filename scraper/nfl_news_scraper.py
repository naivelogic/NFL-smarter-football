"""
Development of a python scraper to pull articles from NFL Teams News 
RSS Feeds. This scripts parses the rss feed,and organizes in to the necessary
fields and saves it to a CSV file. We are working on pulling this directly in
to a SQLite database. 

This code is heavily reliant on Newspaper, here is the documentations:https://newspaper.readthedocs.io/en/latest/
"""

import os
import newspaper
from newspaper import Article
import pandas as pd
from datetime import datetime

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

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
    if len(news) != 0:
        print("List keys: ",news[0].keys())
        print("List keywords", news[0]['keywords'])
    
    return news

if __name__ == '__main__':
    """
    This is the most annoying thing about newspaper... i love it but, there is a manual 
    hack that i had to put in because the articles wouldnt cache correcntly. 
    """
    cache_to_remove = '<INSERT HOME DIR> + .newspaper_scraper/feed_category_cache> + HASH'

    spyder_feed = {
        'ravens':'http://sportspyder.com/nfl/baltimore-ravens/news',
        'bills':'http://sportspyder.com/nfl/buffalo-bills/news',
        'bengals':'http://sportspyder.com/nfl/cincinnati-bengals/news',
        'browns':'http://sportspyder.com/nfl/cleveland-browns/news',
        'broncos':'http://sportspyder.com/nfl/denver-broncos/news',
        'texans':'http://sportspyder.com/nfl/houston-texans/news',
        'colts':'http://sportspyder.com/nfl/indianapolis-colts/news',
        'jaguars':'http://sportspyder.com/nfl/jacksonville-jaguars/news',
        'chiefs':'http://sportspyder.com/nfl/kansas-city-chiefs/news',
        'chargers':'http://sportspyder.com/nfl/san-diego-chargers/news',
        'dolphins':'http://sportspyder.com/nfl/miami-dolphins/news',
        'patriots':'http://sportspyder.com/nfl/new-england-patriots/news', 
        'jets':'http://sportspyder.com/nfl/new-york-jets/news',
        'raiders':'http://sportspyder.com/nfl/oakland-raiders/news',
        'steelers':'http://sportspyder.com/nfl/pittsburgh-steelers/news',
        'titans':'http://sportspyder.com/nfl/tennessee-titans/news',
        'cardinals':'http://sportspyder.com/nfl/arizona-cardinals/news', 
        'falcons':'http://sportspyder.com/nfl/atlanta-falcons/news',
        'panthers':'http://sportspyder.com/nfl/carolina-panthers/news',
        'bears':'http://sportspyder.com/nfl/chicago-bears/news',
        'cowboys':'http://sportspyder.com/nfl/dallas-cowboys/news',
        'lions':'http://sportspyder.com/nfl/detroit-lions/news',
        'packers':'http://sportspyder.com/nfl/green-bay-packers/news',
        'rams':'http://sportspyder.com/nfl/los-angeles-rams/news',
        'vikings':'http://sportspyder.com/nfl/minnesota-vikings/news',
        'saints':'http://sportspyder.com/nfl/new-orleans-saints/news',
        'giants':'http://sportspyder.com/nfl/new-york-giants/news',
        'eagles':'http://sportspyder.com/nfl/philadelphia-eagles/news',
        'niners':'http://sportspyder.com/nfl/san-francisco-49ers/news',
        'seahawks':'http://sportspyder.com/nfl/seattle-seahawks/news',
        'buccaneers':'http://sportspyder.com/nfl/tampa-bay-buccaneers/news',
        'redskins':'http://sportspyder.com/nfl/washington-redskins/news'
    }

    df = []
    for team in spyder_feed:
        result = sbnation_scraper(spyder_feed[team], team)
        table = pd.DataFrame(result)
        df.append(table)
    
    """
    -------------------------------------------------------------------------------
    # of articles found:  151
    # of articles:  151
    List keys:  dict_keys(['url', 'date', 'title', 'keywords', 'text'])
    List keywords ['thing', 'mock', 'hit', 'midpreseason', 'followed', 'watch', 'seahawks', 'vs', 'draft', '3000', 'thats', 'rob', 'weeks', 'nfl', 'vikings', 'twitter']
    -------------------------------------------------------------------------------
    """
    
    nfl = pd.concat(df)
    nfl.loc[nfl.date.asobject == None, 'date'] = nfl[nfl.date.asobject != None]['date'].unique()[0]
    
    da = datetime.today()
    file = './rss_feed/spyder_{}.csv'.format(da)
    nfl.to_csv(file , encoding='utf-8', index=False)
    
