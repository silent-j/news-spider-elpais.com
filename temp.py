# -*- coding: utf-8 -*-
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
# import os
# from tqdm import tqdm
from bs4 import BeautifulSoup as soup
from urllib import request
import pandas as pd
from datetime import date


url = "http://english.elpais.com"

# request & parse page source
client = request.urlopen(url)
page_source = client.read()
client.close()
page_soup = soup(page_source, 'html.parser')

# get front-page sections
section_b = page_soup.find("div", {"class":
                                      "section_b | col desktop_12 tablet_8 mobile_4"})
section_c = page_soup.find("div", {"class":
                                   "section_c | col desktop_12 tablet_8 mobile_4"})
thematic_section = page_soup.find("div", {"class":
                                   "thematic_section | col desktop_12 tablet_8 mobile_4"})    

top_section_title_hrefs = {}
theme_dict = {}
theme_title_hrefs = []
    
def extract_top_section_hrefs():
    
    panes = section_b.findAll("h2")
    panes_2 = section_c.findAll("h2")
    
    panes = panes + panes_2
    
    for pane in panes:
        title = pane.a.text
        href = pane.a["href"]
        top_section_title_hrefs[title] = href
    
def extract_theme_hrefs(theme):
    
    theme_div = thematic_section.find("div", {"id": theme})
    theme_headers = theme_div.findAll("h2")
    temp = {}
    
    for l in theme_headers:
        title = l.a.text
        href = l.a["href"]
        temp[title] = href
        
    return temp

def extract_all_themes():
    
    themes = thematic_section.findAll("div",
                         {"class":"thematic_chain | row margin_top margin_bottom_sm"})
    theme_with_adbanner = thematic_section.findAll("div", 
                                                   {"class":"thematic_chain thematic_chain_ad | row margin_top margin_bottom_sm"})
    themes = [t["id"] for t in themes]
    themes = themes + [t["id"] for t in theme_with_adbanner]
    
    for i in themes:
        theme_dict[i] = extract_theme_hrefs(i)
    

def extract_oped_hrefs():
    
    opeds = page_soup.find("div", {"class":"thematic_opinion | row margin_bottom_sm"})
    oped_title_hrefs = {}
    
    for h in opeds.findAll("h2"):
        oped_title_hrefs.update({h.a.text: h.a["href"]})
    
    return {"opinion": oped_title_hrefs}

if __name__=="__main__":
    
    extract_top_section_hrefs()
        
    extract_all_themes()
        
    theme_dict['opinion'] = extract_oped_hrefs()['opinion']

    frontpage_df = pd.DataFrame()
        
    frontpage_df['article_title'] = [k for k in top_section_title_hrefs.keys()]
    
    #top_section_df['url'] = ['https://english.elpais.com'+top_section_title_hrefs[k] for k in list(top_section_df.article_title)]
    frontpage_df['href'] = [top_section_title_hrefs[k] for k in list(frontpage_df.article_title)]
    
    frontpage_df['section'] = ['top-headlines' for i in frontpage_df.index]
        
    for k, v in theme_dict.items():
        for title, href in v.items():
            theme_title_hrefs.append({
                'article_title': title,
                'href': href,
                'section': 'thematic-'+k,})
    
    frontpage_df = pd.concat([frontpage_df, pd.DataFrame(theme_title_hrefs)])
    frontpage_df.reset_index(inplace=True)       
    frontpage_df.to_csv("frontpage-scraped_{}.csv".format(date.today()))    