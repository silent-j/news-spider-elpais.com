import os
import sys
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
ElPais_FrontPageSpider(user_inp)





if not os.path.exists(os.path.join(frontpage_scraper.DB_PATH, 'frontpage-data.db')):
    # MAKE CONNECTION

    # CURSOR
    
    # CREATE TABLE
    
    # DEFINE AND EXECUTE INSERT COMMAND
else:
    # MAKE CONNECTION
    
    # CURSOR
    
    # DEFINE AND EXECUTE INSERT COMMAND


print("########## SCRAPING BACKPAGES ##########")

# SELECT FROM DB - url, scrape_id







# CLOSE CONNECTION