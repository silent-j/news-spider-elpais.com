import os
import sys
import sqlite3
import argparse
from tqdm import tqdm
#sys.path.append(r'C:\Users\James\Documents\Scraping\elpais-news-scraper')
import pandas as pd
import frontpage_scraper, backpage_scraper
from frontpage_scraper import ElPais_FrontPageSpider
from backpage_scraper import ElPais_BackPageSpider

# ARG PARSING

def parse_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('BASE_PATH', action='store', type=str)
    parser.add_argument('URL', action='store', type=str)
    
    return parser.parse_args()

def create_connection(path):

    connection = sqlite3.connect(os.path.join(frontpage_scraper.DB_PATH, 'frontpage-data.db'))    
    c = connection.cursor()
    
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
    return connection

if __name__=="__main__":
    
    args = parse_args()
    
    BASE_PATH = args.BASE_PATH
    URL = args.URL
    
    frontpage_scraper.BASE_PATH = BASE_PATH
    backpage_scraper.BASE_PATH  = BASE_PATH
    
    
    print("########## SCRAPING FRONTPAGE ##########")
    current_spider = ElPais_FrontPageSpider(URL)
        
    # GET NEWLY CRAWLED DATA FROM THE CURRENT SPIDER
    new_data = current_spider.frontpage_df
    
    # FORMAT THE ARGS FOR THE BACKPAGE SPIDER
    backpage_scraper_args = list(zip(new_data['href'], new_data['scrape_id']))
    
    print("\n########## SCRAPING BACKPAGES ##########")    

    # TODO: MULTIPROCESSING
    for t in tqdm(backpage_scraper_args):
        
        ElPais_BackPageSpider(URL+t[0], t[1])  
        

    ARTICLE_METADATA = backpage_scraper.ARTICLE_METADATA
    
    DATA_TO_BE_INSERTED = pd.concat([new_data, pd.DataFrame(ARTICLE_METADATA)], axis=1)
    
    DATA_TO_BE_INSERTED = DATA_TO_BE_INSERTED[['article_title', 'href', 'section', 'scrape_date',
                                               'scrape_id', 'author', 'pub_date', 'location', 'word_count']]
    
    # CONNECT TO DB & INSERT DATA
    if not os.path.exists(os.path.join(frontpage_scraper.DB_PATH, 'frontpage-data.db')):    
        
        create_connection(os.path.join(frontpage_scraper.DB_PATH, 'frontpage-data.db'))        
    else:
        connection = sqlite3.connect(os.path.join(frontpage_scraper.DB_PATH,'frontpage-data.db'))
        
    # INSERT DATA    
    DATA_TO_BE_INSERTED.to_sql('ARTICLES', connection, if_exists='append', index=False)
    
    connection.close()
