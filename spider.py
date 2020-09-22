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

# the opinion pieces are found in the 'thematic section' but go by 
# a different identifier. Easier to just single them out
op_eds = page_soup.find("div", {"class":"thematic_opinion | row margin_bottom_sm"})
ops_title_and_hrefs = {}

for h in op_eds.findAll("h2"):
    ups_title_hrefs.update({h.a.text: h.a["href"]})
    
def extract_top_section_links(section):

    title_and_hrefs = {}    
    articles = section.findAll("article")
    
    for i in tqdm(range(len(articles))):
        pane = articles[i].find("h2").a
        title = pane.text
        href = pane["href"]
        
        #title_and_hrefs[i] = (title, href)
        title_and_hrefs[title] = href

    return title_and_hrefs

def extract_thematic_section_links(section):
    
    theme_title_links = {}
    themes = section.findAll("div",
                         {"class":"thematic_chain | row margin_top margin_bottom_sm"})
    themes = [t["id"] for t in themes]
    
    for i in themes:
        theme_title_links[i] = []
        
        
    

if __name__=="__main__":
    sc = extract_top_section_links(section_c)

