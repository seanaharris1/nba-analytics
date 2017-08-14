from bs4 import BeautifulSoup
import datetime as dt
from urllib2 import urlopen
import csv


#url = 'http://www.basketball-reference.com/teams/MIA/2016/gamelog'
#html = urlopen(url)
#soup = BeautifulSoup(html,"html.parser")
#data_row = soup.findAll('tr')[3]
#date = str(data_row.findAll('a'))
#date2 = '2015-10-30'
#if date2 in date:
#    print 'yes'
#
#date3 = dt.datetime.strptime(date3,'%Y-%m-%d').date()

""" 
NOTES 

Was getting server hangups when trying to pull the entire gamelogs table for 
each team in the teams_list file. Had to lighten the amount of data being 
pulled from basketballreference servers. Parsed the soup element to only 
include 'a' type elements, which contain the date of each game in the gamelog.
- SAH 07/12/2017 

"""

def backtoback(*pair):
    list(teams_list)
    list(dates_list)
    teamdate = zip(teams_list,dates_list)
    print type(teams_list)
    
    """ creating empty list for the usable games """
    usablegameslist = []
    backtobacklist = []
    
    for team,date in teamdate:
        print team
        """ feed 'team' value from function input """
        url = 'http://www.basketball-reference.com/teams/'+team+'/2016/gamelog'
        html = urlopen(url)
        soup = BeautifulSoup(html,"html.parser")
        
        """ pulling out the first table from the gamelog site """
    #        table = soup.findAll('tbody')[0]
        
        """ data_rows is beautifulsoup element of all the 'a' type elements
        from the dataset soup which contains the date"""
    #        data_row = table.findAll('tr')
        data_rows = soup.findAll('tbody')[0].findAll('a')
        
        """ 'a' elements also includes another row from each game that needs 
        to be removed. All of the unneed rows are odd in the list index which
        can be removed by using a slice """
        del data_rows[1::2]
        list(data_rows)
        #print type(data_rows)
        
        """ turning beautifulsoup elements into strings """
        
        opp_dates_list = [link.string for link in data_rows]
        print type(opp_dates_list[0])
        opp_dates_list = [str(p) for p in opp_dates_list]
        print type(opp_dates_list[0])
        
        """ forloop to iterate over data_rows, find the date value of the game 
        and return it as a string, where x is the index of the datarows """
        for x in range(len(opp_dates_list)):
        
            """ individual data_row where index is x """
            #if soup.findAll('tr',class="over_header thead")
            new_date = opp_dates_list[x]
            #print new_date
            previous_date = opp_dates_list[x-1]
            #print previous_date
            
            """ converting elements from data_rows to string types """
            #date_value = str(new_datarow.findAll('a'))[39:49]
            #date_value = new_datarow
            #previous_date_value = previous_datarow[39:49]
            
    #        previous_date_value = str(previous_datarow.findAll('td')[1])[40:50]
            
            """ checking if given date is equal to the date in the datarow 
            we are currently examing """
            if date in new_date:
                
                #previous_date_value = '2015-10-26'
                #previous_date_value = str(previous_datarow.findAll('a'))[39:49]
                

                """ converting date values to datetime value """
                dateconvert = dt.datetime.strptime(new_date,'%Y-%m-%d').date()
                print dateconvert
                previous_dateconvert = dt.datetime.strptime(previous_date,'%Y-%m-%d').date()
                print previous_dateconvert
                
                """ checking if the diff between the 2 dates is 1, if not
                then the date is usable """
                #timed = dateconvert - previous_dateconvert
                #print dateconvert - previous_dateconvert
                if dateconvert - previous_dateconvert != dt.timedelta(1):
                    usablegameslist.append(new_date)
                else:
                    backtobacklist.append(new_date)
            else:
                None
        
    print usablegameslist   
    return usablegameslist,backtobacklist,dateconvert,previous_dateconvert
    return data_rows
    
""" creating empty lists """
dates_list = []
teams_list = []

""" calling the text files created in nbascraper file """
with open("dates_list_text.txt","r") as dateslist:
    for date in csv.reader(dateslist):
        dates_list.append(date)
dates_list = [''.join(x) for x in dates_list]

with open("teams_list_text.txt","r") as teamslist:
    for team in csv.reader(teamslist):
        teams_list.append(team)
teams_list = [''.join(x) for x in teams_list]

""" zipping the 2 lists so it can be passed to the backtoback function """
pair = zip(teams_list,dates_list)

#backtoback(*pair)
usablegameslist,backtobacklist,new,previous = backtoback(*pair)

""" writing usablegameslist and backtobacklist to text files """
usablegameslist = "\n".join(p for p in usablegameslist)
usablegamesfile = open("usable_games_file.txt","w")
usablegamesfile.write(usablegameslist)
usablegamesfile.close()

backtobacklist = "\n".join(p for p in backtobacklist)
backtobackfile = open("back_to_back.txt","w")
backtobackfile.write(backtobacklist)
backtobackfile.close()
