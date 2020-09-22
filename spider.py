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

top_section_title_hrefs = {}
    
def extract_top_section_hrefs():
    panes = section_b.findAll("h2")
    panes_2 = section_c.findAll("h2")
    
    panes = panes + panes_2
    
    for pane in panes:
        title = pane.a.text
        href = pane.a["href"]
        top_section_title_hrefs[title] = href
    #return self



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
    
    theme_title_hrefs = {}
    themes = thematic_section.findAll("div",
                         {"class":"thematic_chain | row margin_top margin_bottom_sm"})
    themes = [t["id"] for t in themes]
    
    for i in themes:
        theme_title_hrefs[i] = extract_theme_hrefs(i)
        
# the opinion pieces are found in the 'thematic section' but go by 
# a different identifier. Easier to just single them out
def extract_oped_hrefs():
    op_eds = page_soup.find("div", {"class":"thematic_opinion | row margin_bottom_sm"})
    ops_title_hrefs = {}
    
    for h in op_eds.findAll("h2"):
        ops_title_hrefs.update({h.a.text: h.a["href"]})
    
    return {"opinion": ops_title_hrefs}  