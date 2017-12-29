from bs4 import BeautifulSoup
import datetime as dt
from urllib2 import urlopen
import csv
import pickle
import re

""" 
NOTES 

Was getting server hangups when trying to pull the entire gamelogs table for 
each team in the teams_list file. Had to lighten the amount of data being 
pulled from basketballreference servers. Parsed the soup element to only 
include 'a' type elements, which contain the date of each game in the gamelog.
- SAH 07/12/2017 

"""

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

""" loading pickle that contains team and season that was passed to gamelog 
file so we can pass it to the url variable in the teamdate function """
with open("season.txt","rb") as seas:
    season = pickle.load(seas)

def backtoback(*pair):
    list(teams_list)
    list(dates_list)
    teamdate = zip(teams_list,dates_list)
    
    """ creating empty list for the usable games """
    usablegameslist = []
    backtobacklist = []

    
    for team,date in teamdate:
        print team
        """ feed 'team' value from function input """
        url = 'http://www.basketball-reference.com/teams/'+team+'/'+season+'/gamelog'
        html = urlopen(url)
        soup = BeautifulSoup(html,"html.parser")
        
        
        """ data_rows is beautifulsoup element of all the 'a' type elements
        from the dataset soup which contains the date"""
        data_rows = soup.findAll('tbody')[0].findAll('a')
                
        """ 'a' elements also includes another row from each game that needs 
        to be removed. All of the unneed rows are odd in the list index which
        can be removed by using a slice """
        del data_rows[1::2]
        list(data_rows)
        
        """ turning beautifulsoup elements into strings """
        
        opp_dates_list = [link.string for link in data_rows]
        opp_dates_list = [str(p) for p in opp_dates_list]
        
        """ forloop to iterate over data_rows, find the date value of the game 
        and return it as a string, where x is the index of the datarows """
        for x in range(len(opp_dates_list)):
        
            """ individual data_row where index is x """
            new_date = opp_dates_list[x]
            previous_date = opp_dates_list[x-1]
                        
            """ checking if given date is equal to the date in the datarow 
            we are currently examing """
            if date in new_date:

                """ converting date values to datetime value """
                dateconvert = dt.datetime.strptime(new_date,'%Y-%m-%d').date()
                print dateconvert
                previous_dateconvert = dt.datetime.strptime(previous_date,'%Y-%m-%d').date()
                print previous_dateconvert
                
                """ checking if the diff between the 2 dates is 1, if not
                then the date is usable """
                if dateconvert - previous_dateconvert != dt.timedelta(1):
                    usablegameslist.append(new_date)
                else:
                    backtobacklist.append(new_date)
            else:
                None
        
    return usablegameslist,backtobacklist,dateconvert,previous_dateconvert
    
def avgpointsonroad(*teamlist):
    avgpointslist = []
    for team in teamlist:
        
        """ I print the current team variable so I can see the function
        progressing """ 
        print team
        
        """ url and soup for team splits webpage to get average points on the
        road for team """
        url = 'http://www.basketball-reference.com/teams/'+team+'/'+season+'/splits'
        html = urlopen(url)
        soup = BeautifulSoup(html,"html.parser")
        
        """ pulling the avg points on the road for teams """
        avg_points_on_road = soup.findAll('tr')[5].findAll('td')[17]
        avg_points_on_road = str(avg_points_on_road)
        
        if '<' in avg_points_on_road[35:40]:
            avgpoints = avg_points_on_road[35:39]
        elif '<' not in avg_points_on_road[35:40]:
            avgpoints = avg_points_on_road[35:40]
        avgpointslist.append(avgpoints)

#        saturday_games_ppg = soup.find('body').\
#        find('div',id='all_team_splits').find('table').findAll('tr')[27].\
#        findAll('td')[17]
#        
#        saturday_games_ppg = str(saturday_games_ppg)
#        print saturday_games_ppg
#        saturday_games_ppg = re.findall(r"[-+]?\d*\.\d+|\d+",saturday_games_ppg)
#
#        saturday_games_ppg = saturday_games_ppg[0]
#        saturday_games_ppg = float(saturday_games_ppg)        
#        avgpoints = float(avgpoints)
#        satvsavg = avgpoints - saturday_games_ppg
#        print satvsavg
        
    return avgpointslist

usablegameslist,backtobacklist,new,previous = backtoback(*pair)
avgpointslist = avgpointsonroad(*teams_list)

""" writing usablegameslist and backtobacklist to text files """
usablegameslist = "\n".join(p for p in usablegameslist)
usablegamesfile = open("usable_games_file.txt","w")
usablegamesfile.write(usablegameslist)
usablegamesfile.close()

backtobacklist = "\n".join(p for p in backtobacklist)
backtobackfile = open("back_to_back.txt","w")
backtobackfile.write(backtobacklist)
backtobackfile.close()

avgpointslist = "\n".join(p for p in avgpointslist)
avgpointslistfile = open("avgpointslist.txt","w")
avgpointslistfile.write(avgpointslist)
avgpointslistfile.close()

