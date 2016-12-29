 # -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 15:22:36 2016

@author: SHarris
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib2 import urlopen


def pullgamelog(team):
    """ pulling gamelog data from basketball-reference using BeautifulSoup """
    url = 'http://www.basketball-reference.com/teams/'+team+'/2016/gamelog'
    print url
    html = urlopen(url)
    soup = BeautifulSoup(html,'html.parser')
    
    """ getting columns for dataframe from the first table 
    from the game logs page """
    columns = soup.findAll('tr',limit=2)[1].findAll('th')
    column_headers = []
    for th in columns:
        column_headers.append(th.getText())
  
    """ cleaning up the columns tab, renaming duplicate column names """
    column_headers.pop(0)
    column_headersopp = column_headers[23:]
    column_headersopp = [x+ 'opp' for x in column_headersopp]
    column_headershome = column_headers[:23]
    
    """ renaming columns 3 and 7 """
    column_headershome[2] = 'home/away'
    column_headershome[6] = 'opponent points'
    
    """ combining home and away columns """
    column_headers_complete = column_headershome + column_headersopp
    
    """ pulling data from gamelog table """
    data_rows = soup.findAll('tr')[2:]
    game_data = []
    for i in range(len(data_rows)):
        game_row = []
    
        for td in data_rows[i].findAll('td'):
            game_row.append(td.getText())
        game_data.append(game_row)

    """ removing empty rows """
    remove_indexes = [20,21,42,43,64,65,86,87]
    for x in sorted(remove_indexes,reverse = True):
        del game_data[x]
    #print column_headers

    """ creating the dataframe """
    df = pd.DataFrame(game_data, columns = column_headers_complete)
    
    """creating dataframe of only home games"""
    df2 = df.loc[df['home/away'] == '']
    
    """ creating dataframe of only date and opponent team name """
    df3 = df2.loc[:,['Date','Opp']]
    
    """creating list of dates and list of teams to pass to backtoback function """
    dateslist = df3['Date'].tolist()
    teamslist = df3['Opp'].tolist()
    return dateslist,teamslist,df2

dateslist,teamslist,df2 = pullgamelog('MIA')

    
    
    
    
