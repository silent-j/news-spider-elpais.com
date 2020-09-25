import os
import sys
import sqlite3
from tqdm import tqdm
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


# GET NEWLY CRAWLED DATA FROM THE CURRENT SPIDER
new_data = current_spider.frontpage_df

# FORMAT THE ARGS FOR THE BACKPAGE SPIDER
backpage_scraper_args = list(zip(new_data['href'], new_data['scrape_id']))

print("\n########## SCRAPING BACKPAGES ##########")

# PASS LIST OF URLS, IDS TO BACKPAGESPIDER 
# TODO: MULTIPROCESSING
for t in tqdm(backpage_scraper_args):
    
    ElPais_BackPageSpider(user_inp+t[0], t[1])  


# CONNECT TO DATABASE    
ARTICLE_METADATA = backpage_scraper.ARTICLE_METADATA

DATA_TO_BE_INSERTED = pd.concat([new_data, pd.DataFrame(ARTICLE_METADATA)], axis=1)

DATA_TO_BE_INSERTED = DATA_TO_BE_INSERTED[['article_title', 'href', 'section', 'scrape_date',
                                           'scrape_id', 'author', 'pub_date', 'location', 'word_count']]

if not os.path.exists(os.path.join(frontpage_scraper.DB_PATH, 'frontpage-data.db')):
    # MAKE CONNECTION
    connection = sqlite3.connect(os.path.join(frontpage_scraper.DB_PATH, 'frontpage-data.db'))
    # CURSOR
    c = connection.cursor()
    
    # CREATE TABLE
    c.execute('''CREATE TABLE ARTICLES
              (article_title text,
              href text,
              section text,
              scrape_date date,
              scrape_id integer,
              author text,
              pub_date date,
              location text,
              word_count text)''')
              
    print("created table ARTICLES in frontpage-data.db")

else:
    connection = sqlite3.connect(os.path.join(frontpage_scraper.DB_PATH,'frontpage-data.db'))
    
    
DATA_TO_BE_INSERTED.to_sql('ARTICLES', connection, if_exists='append', index=False)

connection.close()
