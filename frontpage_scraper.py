import os
import uuid
import pandas as pd
from datetime import date, datetime
from urllib import request
from bs4 import BeautifulSoup as soup

BASE_PATH = ''
DB_PATH = os.path.join(BASE_PATH, 'data', 'db')
ARCHIVE_PATH = os.path.join(BASE_PATH, 'data', 'archive')

if not os.path.exists(DB_PATH):
    os.mkdir(DB_PATH)

if not os.path.exists(ARCHIVE_PATH):
    os.mkdir(ARCHIVE_PATH)

class ElPais_FrontPageSpider():
    """
    Class for parsing https://english.elpais.com landing page
    and extracting article titles & urls for storage in a database
    Parameters
    ----------
    url : STR
        THE URL TO EL PAIS LANDING PAGE (ie. https://english.elpais.com)

    Returns
    -------
    None.

    """
    def __init__(self, url):
        
        client = request.urlopen(url)
        page_source = client.read()
        client.close()
        self.page_soup = soup(page_source, 'html.parser')
        
        # get front-page sections
        self.section_b = self.page_soup.find("div", 
                                             {"class":
                                              "section_b | col desktop_12 tablet_8 mobile_4"
                                              })
        self.section_c = self.page_soup.find("div", 
                                             {"class":
                                              "section_c | col desktop_12 tablet_8 mobile_4"
                                              })
        self.thematic_section = self.page_soup.find("div", 
                                                    {"class":
                                                     "thematic_section | col desktop_12 tablet_8 mobile_4"
                                                     })    
        # containers
        self.top_section_title_hrefs = {}
        self.theme_dict = {}
        self.theme_title_hrefs = []
        self.frontpage_df = pd.DataFrame()
        
        # grab titles & hrefs
        self.extract_top_section_hrefs()
        self.extract_all_themes() # returns updated 'theme_dict'
        #self.theme_dict['opinion'] = self.extract_oped_hrefs()['opinion']
        
        
        self.frontpage_df['article_title'] = [k for k in self.top_section_title_hrefs.keys()]        
        self.frontpage_df['href'] = [self.top_section_title_hrefs[k] for k in list(self.frontpage_df.article_title)]    
        self.frontpage_df['section'] = ['top-headlines' for i in self.frontpage_df.index]
            
        for k, v in self.theme_dict.items():
            for title, href in v.items():
                self.theme_title_hrefs.append({'article_title':title,
                                               'href': href,
                                               'section': 'thematic-'+k})        
        # export to CSV
        self.frontpage_df = pd.concat([self.frontpage_df, pd.DataFrame(self.theme_title_hrefs)])
        self.frontpage_df['scrape_date'] = [date.today() for i in list(self.frontpage_df.index)]
        self.frontpage_df['scrape_id'] = [uuid.uuid4().fields[0] for i in list(self.frontpage_df.index)]

        self.frontpage_df.reset_index(inplace=True)
        self.frontpage_df.drop_duplicates(subset='href', keep='first', inplace=True)
        print(f"{self.frontpage_df.shape[0]} articles scraped")
        
        
        self.frontpage_df.to_csv(ARCHIVE_PATH + r"\frontpage-data_{}.csv".format(date.today()),
                                 index=0)  
        print("task ran successfully at {}".format(datetime.today()))
      
        
    def extract_top_section_hrefs(self):
        
        panes = self.section_b.findAll("h2")
        panes_2 = self.section_c.findAll("h2")
        panes = panes + panes_2
        
        for pane in panes:
            title = pane.a.text
            href = pane.a["href"]
            self.top_section_title_hrefs[title] = href
        
    def extract_theme_hrefs(self, theme):
        
        theme_div = self.thematic_section.find("div", {"id": theme})
        theme_headers = theme_div.findAll("h2")
        temp = {}
        
        for l in theme_headers:
            title = l.a.text
            href = l.a["href"]
            temp[title] = href
            
        return temp
    
    def extract_all_themes(self):
        
        # themes = self.thematic_section.findAll("div",
        #                      {"class":"thematic_chain | row margin_top margin_bottom_sm"})
        # theme_with_adbanner = self.thematic_section.findAll("div", 
        #                                                {"class":"thematic_chain thematic_chain_ad | row margin_top margin_bottom_sm"})
        themes = self.thematic_section.select('div[class*="thematic_chain | row margin_top margin_bottom_sm"]')
        
        theme_with_adbanner = self.thematic_section.select('div[class*="thematic_chain thematic_chain_ad | row margin_top margin_bottom_sm"]')
        
        
        themes = [t["id"] for t in themes]
        themes = themes + [t["id"] for t in theme_with_adbanner]
        
        for i in themes:
            self.theme_dict[i] = self.extract_theme_hrefs(i)

    def extract_oped_hrefs(self):
        
        opeds = self.page_soup.find("div", {"class":"b b__t b b__t__o thematic_opinion | row margin_bottom_sm"})
        oped_title_hrefs = {}
        
        for h in opeds.findAll("h2"):
            oped_title_hrefs.update({h.a.text: h.a["href"]})
        
        return {"opinion": oped_title_hrefs}
