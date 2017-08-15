# nbascraper
Data scraping and analysis on NBA teams via data from [basketball-reference.com](https://www.basketball-reference.com/). 

# Introduction
I will be using pandas, BeautifulSoup, numpy, and matplotlib libraries to pull and analyze statistics of NBA teams and players using data from the basketball-reference.com. I will be adding several different scripts doing different types of data analytics and will be glad to take any suggestions on what kind of analysis to perform.

## South Beach Flu
The first script I am writing will investigate (and hopefully validate) the myth of the "South Beach Flu", wherein opposing NBA teams, when visiting Miami (if they did not play the night before) will perform worse because they enjoyed a night on South Beach the night before (hence the name "South Beach Flu"). 

I will be comparing statistics like team PPG, team turnovers, team PPG allowed to the team's average and try to identify a trend. I will also perform the same analysis on teams in other major cities such as the New York Knicks, Brooklyn Nets, LA Clippers, and LA Lakers.


### NBA Scraper
The nbascraper.py file uses the BeautifulSoup and Pandas libraries to pull the gamelogs of a team (in this case, the Miami Heat) and fit them to a dataframe. It takes the 3 digit abbeviation of any NBA team and pulls the game log for the 2015-2016 season. 
```python
    url = 'http://www.basketball-reference.com/teams/'+team+'/2016/gamelog'
    html = urlopen(url)
    soup = BeautifulSoup(html,'html.parser')
```
*Note: The season to be pulled can be easily changed by editing the variable 'url' to the year that is desired.*

Pulling out the gamelog with BeautifulSoup requires some inspecting of the gamelog webpage. If you are using Google Chrome, Ctrl+Shift+I or F12 will open the developer's tab. The developer's tab is a useful tool when doing any web scraping with BeautifulSoup

I remove the blank columns and rename the columns of the opponent's statistics to avoid duplicate column names. I make a complete dataframe (variable name 'df') of the entire game log minus the empty rows. I then make two seperate dataframes from the gamelog dataframe: one for only Miami home games (df2) and another with only the date and opposing team (df3). 


