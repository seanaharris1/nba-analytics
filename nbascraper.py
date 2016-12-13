# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 15:22:36 2016

@author: SHarris
"""

#from lxml import html
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib2 import urlopen

#page = requests.get('http://www.basketball-reference.com/teams/MIA/2016/gamelog')
#tree = html.fromstring(page.content)
#
##buyers = tree.xpath('//div[@title="buyer-name"]/text()')
##prices = tree.xpath('//span[@class="item-price"]/text()')
#print buyers
#print prices
#table = tree.xpath('//*[@id="tgl_basic"]/tbody/tr/text()')
#print table
##//*[@id="div_tgl_basic"]
##//*[@id="tgl_basic"]

url = 'http://www.basketball-reference.com/teams/MIA/2016/gamelog'
html = urlopen(url)
soup = BeautifulSoup(html,"html.parser")
print type(soup)
soup.findAll('tr', limit=2)
soup.findAll('tr',limit=2)[1]
columns = soup.findAll('tr',limit=2)[1].findAll('th')
column_headers = [th.getText() for th in columns]
data_rows = soup.findAll('tr')[2:]
type(data_rows)
for i in range(len(data_rows)):
    gamelog = [[td.getText() for tr in data_rows[i].findAll('tr')]]
