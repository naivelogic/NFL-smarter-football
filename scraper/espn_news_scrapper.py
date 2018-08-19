import pandas as pd
import lxml
from lxml import etree
import requests
import datetime

# initial listing for news feeds 

url_list = [
    "http://www.espn.com/espn/rss/nfl/news",
    "http://www.espn.com/blog/feed?blog=nflnation",
    "https://profootballtalk.nbcsports.com/feed/atom/",
]
documents = []

for url in url_list:
    response = requests.get(url)
    xml_page = response.text
    parser = lxml.etree.XMLParser(recover=True, encoding='utf-8')
    documents.append(lxml.etree.fromstring(xml_page.encode("utf-8"), parser=parser))
    

# Generate Table 
title_list = []
description_list = []
category_list = []
article_url_list = []
date_list = []

for xml_doc in documents:
    try:
        articles = xml_doc.xpath("//item")
        for article in articles:
            title_list.append(article[0].text)
            description_list.append(article[1].text)
            category_list.append(article[4].text)
            article_url_list.append(article[2].text)
            date_list.append(article[3].text)
            
    except:
        continue
        

news_data = pd.DataFrame(title_list, columns=["title"])
news_data["category"] = category_list
news_data["description"] = description_list
news_data["short_description"] = [item[item.find(" - ")+3:item.find("<")] for item in news_data["description"]]
news_data["date"] = date_list
news_data["article_url"] = article_url_list
news_data


# Dafame to be stored as sqlite
# create an in-memory SQLite Datebase
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine('sqlite:///nfl_news.db')   #  to connect to your database.
url = engine.url
print(url)

news_data.to_sql('news', con=engine, if_exists='replace', index_label='id')
engine.execute("SELECT * FROM news").fetchall()
session = Session(engine)
