from bs4 import BeautifulSoup
import pandas as pd
from urllib2 import urlopen
#import nbascrapefunction.py 

#url = 'http://www.basketball-reference.com/teams/MIA/2016/gamelog'
#print url
#html = urlopen(url)
#soup = BeautifulSoup(html,'html.parser')
#table = soup.findAll('tbody')[0].findAll('a')
#letters = soup.findAll("div", class_="right endpoint tooltip")

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
#    print column_headers

    """ creating the dataframe """
    df = pd.DataFrame(game_data, columns = column_headers_complete)
    
    """creating dataframe of only home games"""
    df2 = df.loc[df['home/away'] == '']
    
    """ creating dataframe of only date and opponent team name """
    df3 = df2.loc[:,["Date","Opp"]]
    
    """creating list of dates and list of teams to pass to backtoback function
    and writing lists to text file"""
    dateslist = df3['Date'].tolist()
    dateslist = '\n'.join(str(p) for p in dateslist)
    dateslistfile = open("dates_list_text.txt","w")
    dateslistfile.write(dateslist)
    dateslistfile.close()
    
    teamslist = df3['Opp'].tolist()
    teamslist = '\n'.join(str(p) for p in teamslist)
    teamslistfile = open("teams_list_text.txt","w")
    teamslistfile.write(teamslist)
    teamslistfile.close()
    
    usablegameslist = ['2015-11-01','2015-12-05']
    df4 = df3[df3['Date'].isin(usablegameslist)]
    return dateslist,teamslist,df2,df3,df4

            
        
dateslist,teamslist,df2,df3,df4 = pullgamelog('MIA')

df2.to_pickle("C:\Users\sharris\Documents\Python Scripts\gamedf.pkl")
