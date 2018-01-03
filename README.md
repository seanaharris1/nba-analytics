# NBA Data Analytics
Data scraping and analysis on NBA teams via data from [basketball-reference.com](https://www.basketball-reference.com/). 

# Introduction
This project will investigate (and hopefully validate) the myth of the "South Beach Flu", wherein opposing NBA teams, when visiting Miami (if they did not play the night before) will perform worse because they enjoyed a night on South Beach the night before (hence the name "South Beach Flu"). 

I will be using pandas, BeautifulSoup, numpy, and matplotlib libraries to pull and analyze statistics of NBA teams and players using data from the basketball-reference.com. I will be adding several different scripts doing different types of data analytics and will be glad to take any suggestions on what kind of analysis to perform.

## Required Libraries
```python
from bs4 import BeautifulSoup
import pandas as pd
import csv
import matplotlib.pyplot as plt
import datetime as dt
from urllib2 import urlopen
import numpy as np
import pickle
```
The code in this depository is written in Python 2.7 but all of the required libraries will work with Python 3 as well. If you are using an IDE like Anaconda, you will have most of the required libraries except for Beautiful Soup 4. Beautiful Soup 4 can be install with ``` pip install bs4 ```


# Walkthrough

## Pull Game Log
The pullgamelog.py file uses the BeautifulSoup and Pandas libraries to pull the gamelogs of a team (in this case, the Miami Heat) and fit them to a dataframe. It takes the 3 character abbeviation of any NBA team entered by the user and the 4 digit number for the year (*i.e., '2016' will result in the 2015-2016 season.*) and pulls the game log. 
```python
url = 'http://www.basketball-reference.com/teams/'+team+'/'+season+'/gamelog'
html = urlopen(url)
soup = BeautifulSoup(html,'html.parser')
```

*Note: The season to be pulled can be easily changed by editing the variable 'url' to the year that is desired.*

### Pulling Team Name and Average Points Per Game 
We start by pulling the full team name. The full name is stored in the only "h1" tag in the body of the webpage.

```python
""" pulling the full team name """
teamname = str(soup.find('body').findAll('h1'))
```

The full team name is stored in between <span> tags in the resulting string. To make this easier, we can use the **re** library (re = regular expression). The function **re.findall** will find all strings between a defined start and end string and output the results in a list. The full team name is in the 2nd element of the returned list. I remove the first character of the string.

```python
""" returns the entire string that has h1 tag, putting all items with span
tag in the string using re library """
teamname = re.findall(r'span(.*?)</span>',teamname)

""" team name is 2nd element in the returned list """
teamname = teamname[1]

""" stripping first character from the string """
teamname = teamname[1:]
```

I also want to pull the home team's average points per game as well as their opponent's average points per game. To do this, I can use the **soup.select** function. There is no easy way to pull the information we need from the returned value, so I have to write a short if-statement to pull out the strings that contain the average points per game values.

```python
""" home team avg ppg """
if "(" in ppgstring[38:44]:
    print 'yes'        
    homeppgavg = ppgstring[38:42]      
elif "(" in ppgstring[38:45]:
    homeppgavg = ppgstring[38:43]

""" opponent avg ppg """ 
if "(" in ppgstring[99:106]:
    awayppgavg = ppgstring[99:104]
elif "(" in ppgstring[99:107]:
    awayppgavg = ppgstring[99:105]
```

After, I remove the whitespaces and append the home average points per game, opponent average points per game, and full team name to a list so we can save it to a pickle to be opened in the nbascrapefunction.
```python
""" removing whitespace """
homeppgavg = homeppgavg.strip()
awayppgavg = awayppgavg.strip()

""" putting avg pts values into a list """ 
avgpointslist = []
avgpointslist.append(homeppgavg)
avgpointslist.append(awayppgavg)
avgpointslist.append(teamname)
```
### Pulling the gamelog
Pulling out the gamelog with BeautifulSoup requires some inspecting of the gamelog webpage. If you are using Google Chrome, Ctrl+Shift+I or F12 will open the developer's tab. The developer's tab is a useful tool when doing any web scraping with BeautifulSoup. It will highlight the webpage element as you hover over it.

![basketball-reference gamelog table](https://user-images.githubusercontent.com/24396902/29322699-6106e726-81ac-11e7-800b-82bf0f1c67ff.png)

I found the BeautifulSoup tutorial from [www.crummy.com](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) very useful when first learning the BeautifulSoup library. 

After some trial and error I am able to pull the data from basketball-reference and fit it to a pandas dataframe.
```python
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
```

I removed the blank columns and renamed the columns of the opponent's statistics to avoid duplicate column names. I make a complete dataframe (variable name 'df') of the entire game log minus the empty rows. I then make two seperate dataframes from the gamelog dataframe: one for only Miami home games (df2) and another with only the date and opposing team (df3). *Note: one could avoid creating df3 by writing the Date and Opp columns to lists from the df2 dataframe but I will leave it as is for now.*

```python 
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
```
![resulting dataframe df2](https://user-images.githubusercontent.com/24396902/33956579-f9cc7566-e00c-11e7-83bd-9f9e632077b0.PNG)

I will create lists from the *Date* and *Opp* columns from df3 (*again, we could use df2 to do this. Will probably eliminate df2 in a later edit*). I then write these lists to text files so we can pass them to the nbascrapefunction. An easier way to do this would be to save the lists as a pickle (like we did with the avg points list) but this is a method I learned after I wrote the original code. 
```python
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
```
Save the points per game list and season variable to pickles to be opened up in the nbascrapefunction and return the dateslist, teamslist, df2, df3, avgpointslist, and ppgstring just so I can make sure the function is returning the correct values. df2 is saved to a pickle to be passed to the nbadatavis file.

```python 
    """ saving points per game list to pickle """
    with open("pointslist.txt","wb") as pl:
        pickle.dump(avgpointslist,pl)
    
    """ saving season inputted by user to pickle """
    with open("season.txt","wb") as seas:
        pickle.dump(season,seas)
    
    
    return dateslist,teamslist,df2,df3,avgpointslist,ppgstring
       
dateslist,teamslist,df2,df3,avgpointslist,ppgstring = pullgamelog('MIA','2016')

df2.to_pickle("C:\Users\******\Documents\Python Scripts\gamedf.pkl")
```

## Sorting the Games 

To sort the games I use the **backtoback** function in the **nbascrapefunction.py** file. In this function it takes the dates_list_text.txt and teams_list_text.txt created from the pullgamelog function. The two text files are unpacked and put into lists which are zipped using the **zip** function and passed to the backtoback function. The 'team' and 'season' values we used in the pullgamelog that was saved in a pickle is also loaded.

```python
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
```

The backtoback takes a pair of lists and passes 1 element (team and season) of each list to a for loop. The elements are passed to the basketball reference URL string. The dates of the game are stored in the hyperlink (in an *a* tag) of each data row. The dates are then checked to see if the team passed from the *team* variable most recent game is the day before using the **datetime** library. The dates are then sorted into the *usablegameslist* and *backtobacklist* lists. Usable games are those where the road team did not play the day before. Back to back games are those where the road team played the day before.

```python
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
```
I do the same and pull the average points scored on the road for each team passed from the *teamslist* list. 

```python
def avgpointsonroad(*teamlist):
    avgpointslist = []
    for team in teamlist:
                
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
        
        avgpointslist = "\n".join(p for p in avgpointslist)
        avgpointslistfile = open("avgpointslist.txt","w")
        avgpointslistfile.write(avgpointslist)
        avgpointslistfile.close()
```
Now that all the data has been pulled from basketball-reference, I can move on to visually illustrating it.

## Data Visualization

To visually represent the data, I will use the **matplotlib** library. In the **nbadatavis.py** file, I load the required libraries, the *gamelog* dataframe, the lists created in the *nbascraper.py* file, and the average home and opponent score.

```python
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import pickle

""" opening pickle of dataframe from nbascraper file """
gamelogdf = pd.read_pickle("C:\Users\******\Documents\Python Scripts\gamedf.pkl")

""" creating empty lists and writing the usable games and back to back text 
files to the lists """
usablegameslist = []
backtobacklist = []
avgpointslist = [] 



with open("usable_games_file.txt","r") as usablegames:
    for game in csv.reader(usablegames):
        usablegameslist.append(game)
usablegameslist = [''.join(x) for x in usablegameslist]

with open("back_to_back.txt","r") as backtoback:
    for game in csv.reader(backtoback):
        backtobacklist.append(game)
backtobacklist = [''.join(x) for x in backtobacklist]

with open("avgpointslist.txt","r") as avgpoints:
    for game in csv.reader(avgpoints):
        avgpointslist.append(game)
avgpointslist = [''.join(x) for x in avgpointslist]
```
### Sorting the data 

After adding the average points of each team as a column in the *gamelog* dataframe, I convert any number strings into floats and get the average points scored at home by Miami and the average points scored by the road teams when playing @ Miami. 

4 new dataframes are created from the *gamelog* dataframe using the *usablegameslist* and *backtobacklist* to sort between the home team and away team back-to-back and non back-to-back statistics. I only use a few stats but any stat in the gamelog could be used (*I'll only show the hometeam dataframes being created. The away team is the same process with the corresponding columns*). I use the average values of the selected stats to be represented by a bar graph. 
```python
""" adding the avg points on the road for each team in the gamelog df """
gamelogdf['avg_road_points'] = pd.Series(avgpointslist, index=gamelogdf.index)
gamelogdf = gamelogdf.apply(pd.to_numeric, errors='ignore')
roadpointsmean = gamelogdf['avg_road_points'].mean()
avghomepoints = gamelogdf['Tm'].mean()

#%% Home team Dataframes
""" hometeam_usabledf is the dataframe of the home team stats when facing a team
that has not played the night before (not on the 2nd night of back to back). 
Only using a few home team stats """
hometeam_usabledf = gamelogdf.loc[:,["Date","W/L","Tm","FG%","3P%","FT%","ORB",
"TRB","TOV","PF"]]
hometeam_usabledf = gamelogdf[gamelogdf['Date'].isin(usablegameslist)]

""" resetting the index """
hometeam_usabledf = hometeam_usabledf.reset_index(drop=True)

""" converting columns with number stats to float type """
hometeam_usabledf = hometeam_usabledf.apply(pd.to_numeric, errors='ignore')

""" doing the same for back to back games """
hometeam_backtobackdf = gamelogdf.loc[:,["Date","W/L","Tm","FG%","3P%","FT%","ORB",
"TRB","TOV","PF"]]
hometeam_backtobackdf = hometeam_backtobackdf[hometeam_backtobackdf['Date'].isin(backtobacklist)]
hometeam_backtobackdf = hometeam_backtobackdf.reset_index(drop=True)
hometeam_backtobackdf = hometeam_backtobackdf.apply(pd.to_numeric, errors='ignore')

""" extracting home team values """
hometeamfgavgbtb = hometeam_backtobackdf['FG%'].mean()
hometeamfgavguse = hometeam_usabledf['FG%'].mean()
hometeamtpavgbtb = hometeam_backtobackdf['3P%'].mean()
hometeamtpavguse = hometeam_usabledf['3P%'].mean()
hometeamtovavgbtb = hometeam_backtobackdf['TOV'].mean()
hometeamtovavguse = hometeam_usabledf['TOV'].mean()
hometeampfavgbtb = hometeam_backtobackdf['PF'].mean()
hometeampfavguse = hometeam_usabledf['PF'].mean()
hometeamptavgbtb = hometeam_backtobackdf['Tm'].mean()
hometeamptavguse = hometeam_usabledf['Tm'].mean()
```

### Graphing the data

To represent the data I use simple bar graphs, created with the **matplotlib** library. To accurately display the values of the data, I label the individual bars with their numerical value. I got this solution from a blog post on Composition Al. The blog post along with a full explanation of the code can be found [here](http://composition.al/blog/2015/11/29/a-better-way-to-add-labels-to-bar-charts-with-matplotlib/). The **autolabel** function only has to be included once and call 

```python
""" bar graph for points scored vs avg points per game """
n_groups = 3
awaypoints = (awayteamptavgbtb,awayteamptavguse,avgawaypoints)
homepoints = (hometeamptavgbtb,hometeamptavguse,avghomepoints)
fig,ac = plt.subplots()

index = np.arange(n_groups)

barwidth = 0.20
opacity = 0.6

bar_1 = plt.bar(index, awaypoints, bar_width,
                alpha = opacity,
                color = 'y',
                label = 'Away Team Points Per Game')

bar_2 = plt.bar(index + bar_width, homepoints, bar_width,
                alpha = opacity,
                color = 'r',
                label = teamname + ' Points Per Game')

plt.ylabel('Points Per Game', fontname = 'Arial', fontsize = 14)

plt.title(teamname + ' Home Games', fontname = 'Arial',
          fontsize = 20,
          loc = 'center')
          
plt.xticks(index + bar_width, ('back-to-back PPG',
                               'non back-to-back PPG',
                               'total PPG'),
                               fontsize = 12,
                               fontname = 'Arial')
                               
leg = plt.legend(bbox_to_anchor=(0.07,-0.2), loc = 'center left', ncol=1,
                 fontsize = 14, frameon=True)
leg.get_frame().set_edgecolor('k')

""" adding labels to bars, credit to Composition Al """
def autolabel(rects, ac):
    # Get y-axis height to calculate label position from.
    (y_bottom, y_top) = ac.get_ylim()
    y_height = y_top - y_bottom

    for rect in rects:
        height = rect.get_height()

        # Fraction of axis height taken up by this rectangle
        p_height = (height / y_height)

        # If we can fit the label above the column, do that;
        # otherwise, put it inside the column.
        if p_height > 0.95: # arbitrary; 95% looked good to me.
            label_position = height - (y_height * 0.05)
        else:
            label_position = height + (y_height * 0.01)

        ac.text(rect.get_x() + rect.get_width()/2., label_position,
                float(round(height,1)),
                ha='center', va='bottom')

autolabel(bar_1, ac)
autolabel(bar_2, ac)

plt.grid(False)
plt.tight_layout()
plt.show()
```
![points per game graph](https://user-images.githubusercontent.com/24396902/34539555-ec51e05e-f09e-11e7-9af2-7aeb553d73e2.png)

The resulting graph will print to the console but it can be saved to your computer with the **matplotlib.pyplot.savefig()** function. This can be repeated for any of the counting stats that are in the gamelog. I'll be adding the slightly altered versions of the files that will take multiple seasons of a team and fit it to a dataframe, but I won't cover that in the readme. 



