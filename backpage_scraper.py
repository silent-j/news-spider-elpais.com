
import os
import pandas as pd
from datetime import date
from urllib import request
from bs4 import BeautifulSoup as soup


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

if __name__=="__main__":
    frontpage_df = pd.read_csv(r'C:\Users\James\Documents\Scraping\elpais-news-scraper\frontpage-scraped_2020-09-23.csv',
                           index_col=0)

    crawl_depo = r'C:\Users\James\Documents\Scraping\elpais-news-scraper\crawled_docs_{}'.format(date.today())
    
    article_metadata = []
    
    if not os.path.exists(crawl_depo):
        os.mkdir(crawl_depo)
    
    for i in frontpage_df.index:
        
        base_url = 'https://english.elpais.com'
        href = frontpage_df.loc[i, 'href']
        
        client = request.urlopen(base_url+href)
        page_source = client.read()
        client.close()
        
        page_soup = soup(page_source, 'html.parser')
        
        metadata = scrape_article_metadata(page_soup)
        
        article_metadata.append(metadata)
        
        article_text = scrape_article_text(page_soup)
        
        with open(os.path.join(crawl_depo, f'{i}_{metadata["pub_date"]}.txt'), 'w') as outfile:
            for l in article_text:
                outfile.write(l, '\n')
            outfile.close()
        break


