 # -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 15:22:36 2016

@author: SHarris
"""


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
type(columns)

column_headers = []
for th in columns:
	column_headers.append(th.getText())
	
#column_headers = [th.getText() for th in columns]
column_headers.pop(0)

""" creating list of column names for opposing team stats """
column_headersopp = column_headers[23:]
column_headersopp = [x + 'opp' for x in column_headersopp]

""" creating list of column names for home team, just going to use original
the original column names """
column_headershome = column_headers[:23]

""" renaming 3rd column """
column_headershome[2] = 'home/away'
column_headershome[6] = 'opponent points'

""" combining home and away column headers """
column_headers_complete = column_headershome + column_headersopp

""" pulling the game data from the url """
data_rows = soup.findAll('tr')[2:]
game_data = []
for i in range(len(data_rows)):
	game_row = []
	
	for td in data_rows[i].findAll('td'):
		game_row.append(td.getText())
	game_data.append(game_row)
 
""" removing the empty rows (might be unneccessary as you can use 
df.G.notnull()] but will leave it like this for now) """
remove_indexes = [20,21,42,43,64,65,86,87]
for x in sorted(remove_indexes, reverse=True):
    del game_data[x]

""" creating dataframe """
df = pd.DataFrame(game_data,columns = column_headers_complete)

""" converting integer values in data frame from objects to floats """
df = df.convert_objects(convert_numeric=True)



