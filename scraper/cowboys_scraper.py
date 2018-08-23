"""

"""


import newspaper
from newspaper import Article
def cowboys_scraper():
    dal_news = newspaper.build('http://cowboys.xanadu-fx.com/')
    dal_articles = []
    for post in dal_news.articles:     
        row = {}
        post.download()
        post.parse()
        post.nlp()

        row['url'] = post.url
        row['date'] = post.publish_date
        row['title'] = post.title
        row['keywords'] = post.keywords
        row['text'] = post.text
        dal_articles.append(row)
    
    
    
    return dal_articles


dal_news = cowboys_scraper() 
