"""
Created on Thu Dec 08 15:22:36 2016

@author: SHarris
"""


from bs4 import BeautifulSoup
import pandas as pd
from urllib2 import urlopen
import pickle
import re 
def pullgamelog(team,season):
    """ pulling gamelog data from basketball-reference using BeautifulSoup """
    url = 'http://www.basketball-reference.com/teams/'+team+'/'+season+'/gamelog'
    html = urlopen(url)
    soup = BeautifulSoup(html,'html.parser')
    
    """ pulling the full team name """
    teamname = str(soup.find('body').findAll('h1'))
    
    """ returns the entire string that has h1 tag, putting all items with span
    tag in the string using re library """
    teamname = re.findall(r'span(.*?)</span>',teamname)
    
    """ team name is 2nd element in the returned list """
    teamname = teamname[1]
    
    """ stripping first character from the string """
    teamname = teamname[1:]
    
    """ getting team and opponent avg points per game """
    ppgstring = soup.select("body > div > div:nth-of-type(2) > div > div > p:nth-of-type(5)")
    ppgstring = str(ppgstring)
    
    """ home team avg ppg """
    if "(" in ppgstring[38:44]:
        homeppgavg = ppgstring[38:42]      
    elif "(" in ppgstring[38:45]:
        homeppgavg = ppgstring[38:43]
    
    """ opponent avg ppg """ 
    if "(" in ppgstring[99:106]:
        awayppgavg = ppgstring[99:104]
    elif "(" in ppgstring[99:107]:
        awayppgavg = ppgstring[99:105]
    
    """ removing whitespace """
    homeppgavg = homeppgavg.strip()
    awayppgavg = awayppgavg.strip()
    
    """ putting avg pts values into a list """ 
    avgpointslist = []
    avgpointslist.append(homeppgavg)
    avgpointslist.append(awayppgavg)
    avgpointslist.append(teamname)
    
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

    """ creating the dataframe """
    df = pd.DataFrame(game_data, columns = column_headers_complete)
    
    """creating dataframe of only home games"""
    df2 = df.loc[df['home/away'] == '']
    
    """ creating dataframe of only date and opponent team name """
    df3 = df2.loc[:,["Date","Opp"]]
    
    """creating list of dates and list of teams to pass to nbascrapefunction
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
    
    """ saving points per game list to pickle """
    with open("pointslist.txt","wb") as pl:
        pickle.dump(avgpointslist,pl)
    
    """ saving season inputted by user to pickle """
    with open("season.txt","wb") as seas:
        pickle.dump(season,seas)
    
    
    return dateslist,teamslist,df2,df3,avgpointslist

            
        
dateslist,teamslist,df2,df3,avgpointslist = pullgamelog('MIA','2016')

df2.to_pickle("C:\Users\sharris\Documents\Python Scripts\gamedf.pkl")

    
    
    
