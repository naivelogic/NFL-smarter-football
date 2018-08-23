import newspaper
from newspaper import Article

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


def newspaper_parser(url):
    article = Article(url)

    return article

def feedburner_scraper(url_list):
    feed_articles = []
    for url in url_list:     
        row = {}
        post = newspaper_parser(url)
        post.download()
        post.parse()
        post.nlp()

        row['url'] = post.url
        row['date'] = post.publish_date
        row['title'] = post.title
        row['keywords'] = post.keywords
        row['text'] = post.text
        feed_articles.append(row)
    
    
    
    return feed_articles
    
def sbnation_scraper(url):
    newys = newspaper.build(url, memoize_articles=False)
    newsy_urls = []
    for article in newys.articles:
        if '2018' in article.url:
            newsy_urls.append(article.url)
    
    print("# of articles found: ", len(newsy_urls))
    
    news = feedburner_scraper(newsy_urls)
    print("# of articles: ", len(news))
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


# Save to json
import json
def save_to_json(doc, label):
    doc = json.dumps(doc, indent=4, sort_keys=True, default=str)
    with open(label+'_news.json', 'w') as outfile:
        json.dump(doc, outfile)

doc = {
    'hawks':hawks
    }

[save_to_json(doc[y], y) for x,y in enumerate(doc)]
        
# Open json
from pprint import pprint
with open('hawks_news.json', encoding='utf-8') as f:
    df = json.load(f)
df = json.loads(df)
       
