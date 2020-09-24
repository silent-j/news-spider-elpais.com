
import os
import pandas as pd
from urllib import request
from bs4 import BeautifulSoup as soup

BASE_PATH = ''
DB_PATH = os.path.join(BASE_PATH, 'data', 'db')
DL_PATH = os.path.join(BASE_PATH, 'data', 'crawled_docs')

if not os.path.exists(DL_PATH):
    os.mkdir(DL_PATH)


def scrape_article_metadata(page_soup):    

    author = page_soup.find("a", {"class":"a_aut_n | color_black"}).text
    location = page_soup.find("span", {"class":"a_pl | capitalize color_black"}).text
    pub_date = pd.to_datetime(page_soup.find("a", {"class":"a_ti"}).text)    
    pub_date = pub_date.strftime("%Y-%m-%d")
    
    return {'author':author, 'pub_date':pub_date, 'location':location}
   
def scrape_article_text(page_soup):
    
    article_body = page_soup.find("div", {"class":"a_b article_body | color_gray_dark"})
    p_search = article_body.findAll("p")
    
    paragraphs = []
    
    for p in p_search:
        paragraphs.append(p.text)
        
    return paragraphs

def ElPais_BackPageSpider(url, uid):
    """

    Parameters
    ----------
    url : STR
        THE URL TO AN ARTICLE SCRAPED FROM THE EL PAIS LANDING PAGE.
    uid : INT
        IDENTIFIER FROM THE FRONTPAGE DATABASE ASSOCIATED WITH PROVIDED URL.

    Returns
    -------
    None.

    """
    article_metadata = []
    
    client = request.urlopen(url)
    page_source = client.read()
    client.close()
    
    page_soup = soup(page_source, 'html.parser')
    
    article_text = scrape_article_text(page_soup)
    
    word_count = len(''.join(article_text).split(' '))
        
    metadata = scrape_article_metadata(page_soup)   
    metadata['scrape_id'] = uid
    metadata['word_count'] = word_count
    article_metadata.append(metadata)

    
    with open(os.path.join(DL_PATH, f'{uid}_{metadata["pub_date"]}.txt'), 'w') as outfile:
        for l in article_text:
            outfile.write(l, '\n')
        outfile.close()
    
    return article_metadata
