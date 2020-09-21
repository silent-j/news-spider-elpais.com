import os
from tqdm import tqdm
from bs4 import BeautifulSoup as soup
from urllib import request

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

def extract_top_section_links(section):

    title_and_hrefs = {}    
    articles = section.findAll("article")
    
    for i in tqdm(range(len(articles))):
        pane = articles[i].find("h2").a
        title = pane.text
        href = pane["href"]
        
        title_and_hrefs[i] = (title, href)
    return title_and_hrefs



if __name__=="__main__":
    sc = extract_top_section_links(section_c)

