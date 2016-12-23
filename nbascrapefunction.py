from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
from urllib2 import urlopen

url = 'http://www.basketball-reference.com/teams/MIA/2016/gamelog'
html = urlopen(url)
soup = BeautifulSoup(html,"html.parser")
data_row = soup.findAll('tr')[3]
date = str(data_row.findAll('a'))
date2 = '2015-10-30'
if date2 in date:
    print 'yes'
    
def backtoback(team,date):

    """ feed 'team' value from function input """
    url = 'http://www.basketball-reference.com/teams/'+team+'/2016/gamelog'
    html = urlopen(url)
    soup = BeautifulSoup(html,"html.parser")
    
    """ pulling out the first table from the gamelog site """
    table = soup.findAll('tbody')[0]
    
    """ data_row is beautifulsoup element of all the gamelog rows """
    data_row = table.findAll('tr')
    
    """ creating empty list for the usable games """
    usablegameslist = []
    
    """ forloop to iterate over data_row, find the date value of the game 
    and return it as a string, where x is the index of the datarows """
    for x in range(len(data_row)):
    
        """ individual data_row where index is x """
        #if soup.findAll('tr',class="over_header thead")
        new_datarow = soup.findAll('tr')[x]
        previous_datarow = soup.findAll('tr')[x-1]
        
        """ converting the data value as a string, date value happens to be
        in first and only 'a' type child of the datarows """ 
        date_value = str(new_datarow.findAll('a'))
        previous_date_value = str(new_datarow.findAll('a'))
        
        """ checking if given date is equal to the date in the datarow 
        we are currently examing """
        if date in date_value:
        
            """ converting date values to datetime value """
            dateconvert = dt.datetime.strptime(date_value,'%Y-%m-%d').date()
            previous_dateconvert = dt.datetime.strp(previous_date_value,'%Y-%m-%d').date()
            
            """ checking if the diff between the 2 days is 1, if not
            then the date is usable """
            if dateconvert - previous_dateconvert != dt.timedelta(1):
                usablegameslist.append(date_value)
            else:
                None
    return usablegamesList

            
backtoback('HOU','2015-11-01')







