import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from matplotlib.font_manager import FontProperties
import seaborn as sns
import pickle

""" opening pickle of dataframe from nbascraper file """
gamelogdf = pd.read_pickle("C:\Users\sharris\Documents\Python Scripts\gamedf.pkl")

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

""" loading home and away points per game, and teamname pickle """
with open("pointslist.txt","rb") as pl:
    avgppg = pickle.load(pl)
avghomepoints = float(avgppg[0])
avgawaypoints = float(avgppg[1])
teamname = avgppg[2]

""" adding the avg points on the road for each team in the gamelog df """
gamelogdf['avg_road_points'] = pd.Series(avgpointslist, index=gamelogdf.index)
gamelogdf = gamelogdf.apply(pd.to_numeric, errors='ignore')
roadpointsmean = gamelogdf['avg_road_points'].mean()

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
#%% Away Team Dataframes
""" Away Team """
awayteam_usabledf = gamelogdf.loc[:,["Date","opponent points","FGopp","FG%opp",
"3P%opp","FT%opp","ORBopp","TRBopp","TOVopp","PFopp"]]
awayteam_usabledf =gamelogdf[gamelogdf['Date'].isin(usablegameslist)]

""" resetting the index """
awayteam_usabledf = awayteam_usabledf.reset_index(drop=True)

""" converting columns with number stats to float type """
awayteam_usabledf = awayteam_usabledf.apply(pd.to_numeric, errors ='ignore')

awayteam_backtobackdf = gamelogdf.loc[:,["Date","opponent points","FGopp",
"FG%opp","3P%opp","FT%opp","ORBopp","TRBopp","TOVopp","PFopp"]]
awayteam_backtobackdf = awayteam_backtobackdf[awayteam_backtobackdf['Date'].isin(backtobacklist)]
awayteam_backtobackdf = awayteam_backtobackdf.reset_index(drop=True)
awayteam_backtobackdf = awayteam_backtobackdf.apply(pd.to_numeric, errors='ignore')

""" extracting away team values """ 
awayteamfgavgbtb = awayteam_backtobackdf['FG%opp'].mean()
awayteamfgavguse = awayteam_usabledf['FG%opp'].mean()
awayteamtpavgbtb = awayteam_backtobackdf['3P%opp'].mean()
awayteamtpavguse = awayteam_usabledf['3P%opp'].mean()
awayteamtovavgbtb = awayteam_backtobackdf['TOVopp'].mean()
awayteamtovavguse = awayteam_usabledf['TOVopp'].mean()
awayteampfavgbtb = awayteam_backtobackdf['PFopp'].mean()
awayteampfavguse = awayteam_usabledf['PFopp'].mean()
awayteamptavgbtb = awayteam_backtobackdf['opponent points'].mean()
awayteamptavguse = awayteam_usabledf['opponent points'].mean()

#%% Creating Graphs

""" bar graph for field goal percentage and 3 point shooting percentage """
n_groups = 4
means_1 = (awayteamfgavgbtb,hometeamfgavgbtb,awayteamtpavgbtb,hometeamtpavgbtb)
means_2 = (awayteamfgavguse,hometeamfgavguse,awayteamtpavguse,hometeamtpavguse)

""" converting to percentages """
means_1 = tuple(100*x for x in means_1)
means_2 = tuple(100*x for x in means_2)
fig, ac = plt.subplots()
index = np.arange(n_groups)

""" creating graph for avg FG% and 3P%  """
bar_width = 0.35
opacity = 0.6

rects1 = plt.bar(index, means_1, bar_width,
                 alpha = opacity,
                 color = 'b',
                 label = 'back-to-back games')
                 
rects2 = plt.bar(index + bar_width, means_2, bar_width,
                 alpha = opacity,
                 color = 'g',
                 label = 'non back-to-back games')


plt.ylabel('Shooting Percentage',fontname = 'Arial', fontsize=14)
plt.title(teamname + ' Home Games', fontname = 'Arial', fontsize=20)
plt.xticks(index + bar_width, ('Away team FG%','Home team FG%',
                               'Away team 3P%', 'Home team 3P%'),
                               fontsize = 10)
                               
""" setting location of the legend because it was interfering with the bars,
changing fontsize, adding a box around it with frameon=True """
leg = plt.legend(bbox_to_anchor=(1,0.9), loc='center left', ncol=1,fontsize = 14,
           frameon=True)

""" making the frame black """
leg.get_frame().set_edgecolor('k')

""" removing gridlines """
plt.grid(False)
plt.tight_layout()
plt.show()

""" bar graph for turnovers per game """
n_groups = 2
tovmeanbtb = (awayteamtovavgbtb,hometeamtovavgbtb)
tovmeanuse = (awayteamtovavguse,hometeamtovavguse)
fig, ac = plt.subplots()

index = np.arange(n_groups)

bar_width = 0.3
opacity = 0.6

bar1 = plt.bar(index, tovmeanbtb, bar_width,
               alpha = opacity,
               color = 'b',
               label = 'back-to-back games')
               
bar2 = plt.bar(index + bar_width, tovmeanuse, bar_width,
               alpha = opacity,
               color = 'g',
               label = 'non back-to-back games')


plt.ylabel('Turnovers Per Game', fontname = 'Arial', fontsize = 14)

plt.title(teamname + ' Home Games', fontname = 'Arial',
          fontsize = '20',
          loc='center')
plt.xticks(index + bar_width, ('Away team turnovers/game',
                               'Home team turnovers/game'),
                               fontsize = 13,
                               fontname = 'Arial')
leg = plt.legend(bbox_to_anchor=(1,0.9), loc='center left', ncol=1,
                 fontsize = 14, frameon=True)
leg.get_frame().set_edgecolor('k')
plt.grid(False)
plt.tight_layout()
plt.show()

""" bar graph for fouls per game """
n_groups = 2
foulsmeanbtb = (awayteampfavgbtb,hometeampfavgbtb)
foulsmeanuse = (awayteampfavguse,hometeampfavguse)
fig, ac = plt.subplots()

index = np.arange(n_groups)

bar_width = 0.30
opacity = 0.6

bar_1 = plt.bar(index, foulsmeanbtb, bar_width,
                alpha = opacity,
                color = 'b',
                label = 'back-to-back games')
                
bar_2 = plt.bar(index + bar_width, foulsmeanuse, bar_width,
                alpha = opacity,
                color = 'g',
                label = 'non back-to-back games')
                
plt.ylabel('Fouls Per Games', fontname = 'Arial', fontsize = 14)

plt.title(teamname + ' Home Games', fontname = 'Arial',
          fontsize = 20,
          loc = 'center')
          
plt.xticks(index + bar_width, ('Away team fouls/game',
                               'Home team fouls/game'),
                               fontsize = 13,
                               fontname = 'Arial')
                               
leg = plt.legend(bbox_to_anchor=(1,0.9), loc='center left', ncol=1,
                 fontsize = 14, frameon=True)
leg.get_frame().set_edgecolor('k')
plt.grid(False)
plt.tight_layout()
plt.show()

""" bar graph for points scored vs avg points per game """
n_groups = 3
awaypoints = (awayteamptavgbtb,awayteamptavguse,avgawaypoints)
homepoints = (hometeamptavgbtb,hometeamptavguse,avghomepoints)
fig, ac = plt.subplots()

index = np.arange(n_groups)

barwidth = 0.15
opacity = 0.6

bar_1 = plt.bar(index, awaypoints, bar_width,
                alpha = opacity,
                color = 'y',
                label = 'Away Team PPG')

bar_2 = plt.bar(index + bar_width, homepoints, bar_width,
                alpha = opacity,
                color = 'r',
                label = teamname + ' PPG')

plt.ylabel('Points Per Game', fontname = 'Arial', fontsize = 14)

plt.title(teamname + ' Home Games', fontname = 'Arial',
          fontsize = 20,
          loc = 'center')

plt.xticks(index + bar_width, ('back-to-back PPG',
                               'non back-to-back PPG',
                               'Season Average PPG'),
                               fontsize = 11,
                               fontname = 'Arial')
leg = plt.legend(bbox_to_anchor=(1,0.9), loc='center left', ncol=1,
                 fontsize = 14,frameon=True)
  
leg.get_frame().set_edgecolor('k')
plt.grid(False)
plt.tight_layout()
plt.show()

""" scatter plots """
xdata = range(0,len(awayteam_usabledf['opponent points']),1)
plt.axhline(y=avgawaypoints, color = 'k')
plt.plot(range(0,len(awayteam_backtobackdf['opponent points']),1),
         awayteam_backtobackdf['opponent points'],'o',color = 'g')
plt.show()
plt.axhline(y = avgawaypoints, color = 'k')
plt.plot(xdata,awayteam_usabledf['opponent points'],'o',color = 'r')
plt.show()
count = 0
for x in awayteam_usabledf['opponent points']:
    if x < avgawaypoints:
        count = count + 1
print count 
