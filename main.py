import os
import sys
import sqlite3
sys.path.append(r'C:\Users\James\Documents\Scraping\elpais-news-scraper')
import pandas as pd
import frontpage_scraper, backpage_scraper
from frontpage_scraper import ElPais_FrontPageSpider
from backpage_scraper import ElPais_BackPageSpider

BASE_PATH = r'C:\Users\James\Documents\Scraping\elpais-news-scraper'

frontpage_scraper.BASE_PATH = BASE_PATH
backpage_scraper.BASE_PATH  = BASE_PATH


user_inp = "https://english.elpais.com"

print("########## SCRAPING FRONTPAGE ##########")
current_spider = ElPais_FrontPageSpider(user_inp)

"""
if not os.path.exists(os.path.join(frontpage_scraper.DB_PATH, 'frontpage-data.db')):
    # MAKE CONNECTION
    connection = sqlite3.connect(os.path.join(frontpage_scraper.DB_PATH, 'frontpage-data.db'))
    # CURSOR
    c = connection.cursor()
    
    # CREATE TABLE
    c.execute('''CREATE TABLE ARTICLES
              (index INTEGER,
              article_title VARCHAR,
              href VARCHAR,
              section VARCHAR,
              scrape_date DATE,
              scrape_id INTEGER,
              author VARCHAR,
              pub_date DATE,
              location VARCHAR,
              word_count VARCHAR)
              ''')
    print("created table ARTICLES in frontpage-data.db")
    connection.close()"""

# GET NEWLY CRAWLED DATA FROM THE CURRENT SPIDER
new_data = current_spider.frontpage_df

# FORMAT THE ARGS FOR THE BACKPAGE SPIDER
backpage_scraper_args = list(zip(new_data['href'], new_data['scrape_id']))

print("########## SCRAPING BACKPAGES ##########")

# PASS LIST OF URLS, IDS TO BACKPAGESPIDER 

for t in backpage_scraper_args:
    
    ElPais_BackPageSpider(user_inp+t[0], t[1])  
    

# INSERT METADATA FIELDS
ARTICLE_METADATA = backpage_scraper.ARTICLE_METADATA

print(pd.join(new_data, pd.DataFrame(ARTICLE_METADATA), on='scrape_id', kind='inner'))

# CLOSE CONNECTION
