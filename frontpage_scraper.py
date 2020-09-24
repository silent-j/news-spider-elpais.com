import os
import pandas as pd
from datetime import date
from urllib import request
from bs4 import BeautifulSoup as soup

class ElPais_FrontPageSpider():
    
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
        self.theme_dict['opinion'] = self.extract_oped_hrefs()['opinion']

        
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
        self.frontpage_df.reset_index(inplace=True)       
        self.frontpage_df.to_csv("frontpage-scraped_{}.csv".format(date.today()))
        
        print(self.frontpage_df)
        
        
        
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
        
        themes = self.thematic_section.findAll("div",
                             {"class":"thematic_chain | row margin_top margin_bottom_sm"})
        theme_with_adbanner = self.thematic_section.findAll("div", 
                                                       {"class":"thematic_chain thematic_chain_ad | row margin_top margin_bottom_sm"})
        themes = [t["id"] for t in themes]
        themes = themes + [t["id"] for t in theme_with_adbanner]
        
        for i in themes:
            self.theme_dict[i] = self.extract_theme_hrefs(i)

    def extract_oped_hrefs(self):
        
        opeds = self.page_soup.find("div", {"class":"thematic_opinion | row margin_bottom_sm"})
        oped_title_hrefs = {}
        
        for h in opeds.findAll("h2"):
            oped_title_hrefs.update({h.a.text: h.a["href"]})
        
        return {"opinion": oped_title_hrefs}