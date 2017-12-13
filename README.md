# nbascraper
Data scraping and analysis on NBA teams via data from [basketball-reference.com](https://www.basketball-reference.com/). 

# Introduction
I will be using pandas, BeautifulSoup, numpy, and matplotlib libraries to pull and analyze statistics of NBA teams and players using data from the basketball-reference.com. I will be adding several different scripts doing different types of data analytics and will be glad to take any suggestions on what kind of analysis to perform.

## South Beach Flu
The first script I am writing will investigate (and hopefully validate) the myth of the "South Beach Flu", wherein opposing NBA teams, when visiting Miami (if they did not play the night before) will perform worse because they enjoyed a night on South Beach the night before (hence the name "South Beach Flu"). 

I will be comparing various statistics to try and verify a trend. I will also perform the same analysis on teams in other major cities like the New York Knicks, Brooklyn Nets, LA Clippers, and LA Lakers.


### Pull Game Log
The pullgamelog.py file uses the BeautifulSoup and Pandas libraries to pull the gamelogs of a team (in this case, the Miami Heat) and fit them to a dataframe. It takes the 3 digit abbeviation of any NBA team and pulls the game log for the 2015-2016 season. 
```python
    url = 'http://www.basketball-reference.com/teams/'+team+'/2016/gamelog'
    html = urlopen(url)
    soup = BeautifulSoup(html,'html.parser')
```
*Note: The season to be pulled can be easily changed by editing the variable 'url' to the year that is desired.*

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
