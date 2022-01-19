"""
Created on Wed Nov 18 10:54:12 2020
@author: porsche
"""

import pandas as pd
from datetime import datetime,date # almost inutile
import plotly
import plotly.graph_objects as go
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen, FancyURLopener
import time
import argparse

parser = argparse.ArgumentParser(description='Parser for user info')
parser.add_argument("-u", "--user", type=str, help="User name (must be in a 'username' format)", default="")
parser.add_argument("-nR", "--races", type=int, help="how many races you want to consider in the plot", default=3000)
parser.add_argument("-sl", "--slow", type=int, help="this is what you consider a slow wpm for yourself", default=70)

args = parser.parse_args()
u = args.user
nR = args.races
sl = args.slow

today = date.today()
today = today.strftime("%b. %d, %Y")

USERNAME = u
slow = sl

url = "https://data.typeracer.com/pit/race_history?user={0}&universe=play&n={1}".format(USERNAME, nR)

def rows(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=hdr)
    page = urlopen(req)
    soup = bs(page)
    table = soup.find("div",{"class":"themeContent pit"})
    if table != None:
        r = table.find_all("div",{"class":"Scores__Table__Row"})
        if r != None:
            return r
        
def rowAttributes(row):
    nRace = row.find("div",{"class":"profileTableHeaderUniverse"}).find("a").text.strip()
    SA = row.find_all("div",{"class":"profileTableHeaderRaces"})
    speed = SA[0].text.strip()
    accuracy = SA[1].text.strip()
    rankInRace = row.find("div",{"class":"profileTableHeaderPoints"}).text.strip()
    date = row.find("div",{"class":"profileTableHeaderDate"}).text.strip()
    if date == "today":
        date = today
    return nRace, speed, accuracy, rankInRace, date

def fillDictionary(history = dict()):
    R = rows(url)
    for r in R:
        attr = rowAttributes(r)
        nRace = int(attr[0])
        speed = attr[1]
        accuracy = attr[2]
        rankInRace = attr[3]
        date = attr[4]
        history[nRace] = {}
        history[nRace]["speed"] = speed
        history[nRace]["accuracy"] = accuracy
        history[nRace]["rankInRace"] = rankInRace
        history[nRace]["date"] = date
    return history

d = fillDictionary()



#dfUpdate = pd.read_csv("RaceHistory.csv")

try:
    dfUpdate = pd.read_csv("RaceHistory.csv")
except:
    newData = pd.DataFrame(data=d).T
    newData.to_csv("RaceHistory.csv") 
    
dfUpdate = pd.read_csv("RaceHistory.csv")

dfUpdate = dfUpdate.set_index("Unnamed: 0")

for i in d:
    if i not in dfUpdate.index:
        #print(i,"non sono dentro")
        da_aggiungere = {i:d[i]}
        dfDA = pd.DataFrame(data = da_aggiungere).T
        dfUpdate = dfUpdate.append(dfDA)
    else:
        continue
        #print(i,"sono dentro")
        
dfUpdate = dfUpdate.sort_index()
df = dfUpdate

largest_race_number = int(df.index.max())
m = int(df['speed'].max().replace(" WPM",""))+3
l = int(df['speed'].min().replace(" WPM",""))-1  


fig = go.Figure(
    data = go.Scatter(
                x=df.index,
                y = df['speed'].apply(lambda x: int(x.replace("WPM",""))),
                mode = 'markers',
                marker = dict(
                    size = 8,
                    sizemode='area',
                    sizeref=1,
                    color=[eval(x[:-1]) for x in df['accuracy']], #set color equal to a variable
                    colorscale= 'rdylgn', # one of plotly colorscales
                    showscale=True,
                    colorbar=dict(title="<b>Accuracy</b>")   #<b> and </b> is to change the title to bold
                    ),
                line=dict(
                    color='gold',
                    width=0.5
                    ),
                showlegend=False,   
                text = df[['date','accuracy']],
                hovertemplate =
                    '<b>%{text[0]}</b>'+
                    '<br><i>Speed</i>: <b>%{y}</b></br>'+ 
                    '<i>Accuracy</i>: <b>%{text[1]}</b>'+ 
                    '<br>Race #: <b>%{x}</b><extra></extra></br>',
                ),
                
    layout = dict(
        title = '<b>Speed in Races over time</b>',
        yaxis = dict(zeroline = True,
        title="<b>Speed (WPM)</b>"),
# =============================================================================
# =============================================================================
# =============================================================================
# # #         xaxis = dict(zeroline = True,
# # #         title="<b>Race #</b>"),
# =============================================================================
# =============================================================================
# =============================================================================
        sliders = []
        ),
    #INSIDE "frames" the initial idea was to put inside it:
    #go.Frame(data=[go.Scatter(x=[d['Race #']], y=[d['Speed']])]) for i,d in df.iterrows() if d['Race #']>=0
    frames = [] #In the end the content of frames is put later.
    
)

fig.update_yaxes(ticksuffix=" WPM")

    

# =============================================================================
# FIRST SCATTER GL
# Here i change the color of the lines to red if my writing speed 
# is slower than "slow"
# =============================================================================

  #You can change this value however you like it to be just remember it is 
           #the lower boundary where below it red lines start appearing

fig.add_scattergl(
    x=df.index, 
    y=df['speed'].apply(lambda x: int(x.replace("WPM",""))).where(df['speed'].apply(lambda x: int(x.replace("WPM","")))<slow), 
    mode = 'markers',
    line=dict(
        color='red',
        width=1
        ),
    marker = dict(
        size = 8,
        sizemode='area',
        sizeref=1,
        color=[eval(x[:-1]) for x in df['accuracy']], #set color equal to a variable
        colorscale= 'rdylgn', # one of plotly colorscales
        ),
    showlegend=False
    )

# =============================================================================
# SECOND SCATTER GL
# Here i change the color of the lines to green if my writing speed 
# is faster than slow
# =============================================================================

fig.add_scattergl(
    x=df.index, 
    y=df['speed'].apply(lambda x: int(x.replace("WPM",""))).where(df['speed'].apply(lambda x: int(x.replace("WPM","")))>=slow), 
    mode = 'markers',
    line=dict(
        color='green',
        width=1
        ),
    marker = dict(
        size = 8,
        sizemode='area',
        sizeref=1,
        color=[eval(x[:-1]) for x in df['accuracy']], #set color equal to a variable
        colorscale= 'rdylgn', # one of plotly colorscales
        ),
    showlegend=False
    )

# =============================================================================
# ANIMATION PART: I had to put the red and green lines in the animation as well 
# =============================================================================

fig["frames"] = [
    # Foundamental idea for x = df['Race #'].where((df['Race #']>=x-101) & (df['Race #']<x))
    # Foundamental idea to change mode = fig['data'][0]['mode']
        go.Frame(
            data=[
                go.Scatter(
                    x = df.index.where((df.index>=x-501) & (df.index<x)),
                    y = df['speed'].apply(lambda x: int(x.replace("WPM",""))),
                    mode = 'markers',
                    text = df[['date','accuracy']],
                    hovertemplate =
                        '<b>%{text[0]}</b>'+
                        '<br><i>Speed</i>: <b>%{y}</b></br>'+ 
                        '<i>Accuracy</i>: <b>%{text[1]}</b>'+ 
                        '<br>Race #: <b>%{x}</b><extra></extra></br>',
                    line=dict(
                        color='gold',
                        width=1
                    )
                ),  
                go.Scatter(
                    x = df.index.where((df.index>=x-501) & (df.index<x)),
                    y = df['speed'].apply(lambda x: int(x.replace("WPM",""))).where(df['speed'].apply(lambda x: int(x.replace("WPM","")))<slow),
                    mode = 'markers',
                    text = df[['date','accuracy']],
                    hovertemplate =
                        '<b>%{text[0]}</b>'+
                        '<br><i>Speed</i>: <b>%{y}</b></br>'+ 
                        '<i>Accuracy</i>: <b>%{text[1]}</b>'+ 
                        '<br>Race #: <b>%{x}</b><extra></extra></br>',
                    line=dict(
                        color='red',
                        width=1
                    ) 
                ),
                go.Scatter(
                    x = df.index.where((df.index>=x-501) & (df.index<x)),
                    y = df['speed'].apply(lambda x: int(x.replace("WPM",""))).where(df['speed'].apply(lambda x: int(x.replace("WPM","")))>=slow),
                    mode = 'markers',
                    text = df[['date','accuracy']],
                    hovertemplate =
                        '<b>%{text[0]}</b>'+
                        '<br><i>Speed</i>: <b>%{y}</b></br>'+ 
                        '<i>Accuracy</i>: <b>%{text[1]}</b>'+ 
                        '<br>Race #: <b>%{x}</b><extra></extra></br>',
                    line=dict(
                        color='green',
                        width=1
                    )  
                )
                
            ]
                 
        ) for x in range(501,largest_race_number+100,500)]

fig["frames"] = fig['frames'] + tuple([
    go.Frame(
        data = [
            go.Scatter(
                    x = df.index,
                    y = df['speed'].apply(lambda x: int(x.replace("WPM",""))),
                    mode = 'markers',
                    text = df[['date','accuracy']],
                    hovertemplate =
                        '<b>%{text[0]}</b>'+
                        '<br><i>Speed</i>: <b>%{y}</b></br>'+ 
                        '<i>Accuracy</i>: <b>%{text[1]}</b>'+ 
                        '<br>Race #: <b>%{x}</b><extra></extra></br>',
                    line=dict(
                        color='gold',
                        width=1
                    )
                ),
            go.Scatter(
                    x = df.index,
                    y = df['speed'].apply(lambda x: int(x.replace("WPM",""))).where(df['speed'].apply(lambda x: int(x.replace("WPM","")))<slow),
                    mode = 'markers',
                    text = df[['date','accuracy']],
                    hovertemplate =
                        '<b>%{text[0]}</b>'+
                        '<br><i>Speed</i>: <b>%{y}</b></br>'+ 
                        '<i>Accuracy</i>: <b>%{text[1]}</b>'+ 
                        '<br>Race #: <b>%{x}</b><extra></extra></br>',
                    line=dict(
                        color='red',
                        width=1
                    )
                ),
            go.Scatter(
                    x = df.index,
                    y = df['speed'].apply(lambda x: int(x.replace("WPM",""))).where(df['speed'].apply(lambda x: int(x.replace("WPM","")))>=slow),
                    mode = 'markers',
                    text = df[['date','accuracy']],
                    hovertemplate =
                        '<b>%{text[0]}</b>'+
                        '<br><i>Speed</i>: <b>%{y}</b></br>'+ 
                        '<i>Accuracy</i>: <b>%{text[1]}</b>'+ 
                        '<br>Race #: <b>%{x}</b><extra></extra></br>',
                    line=dict(
                        color='green',
                        width=1
                    )
                ),
            ],
        
        layout = dict(
            xaxis=dict(
                range = [-10,largest_race_number+10],
                rangeslider=dict(
                    visible=True
                    ),
                type="linear"
            ),
            )

        )
])

# =============================================================================
# END ANIMATION PART
# =============================================================================

# =============================================================================
# FIRST LAYOUT UPDATE
# Here i create some Visualization Buttons ad range slider
# =============================================================================

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=1,
            x=0.57,
            y=1.2,
            buttons=list([
                dict(label="Lines",
                     method="update",
                     args=[{
                         "mode": "lines"}]),
                dict(label="Markers",
                     method="update",
                     args=[{"mode": "markers"}]),
                dict(label="Lines&Markers",
                     method="update",
                     args=[{"mode": "lines+markers"}]),
                ]   
            )
        ),
# =============================================================================
#         PLAY AND PAUSE BUTTON FOR ANIMATION INSIDE LAYOUT UPDATE 
# =============================================================================
        dict(
            type = "buttons",
            direction = "left",
            showactive = False,
            pad = dict(
                r = 10,
                t = 100
            ),
            x = -0.02,
            xanchor = "right",
            y = 0,
            yanchor = "top",
            buttons = list([
                {
                "args": [None, {
                    "frame": {"duration": 600, "redraw": False},
                    "fromcurrent": True, "transition": {"duration": 500,"easing": "quadratic-in-out"}
                    }],
                "label": "Play",
                "method": "animate"
                },
                {
                'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
                }
            ])
        )
# =============================================================================
#         TRENDLINE BUTTON: work in progress
# =============================================================================
        #dict()
    ],
# =============================================================================
#     RANGE SLIDER inside first update_layout
# =============================================================================
    xaxis=dict(
        range = [0,largest_race_number+10],
        rangeslider=dict(
        visible=True
        ),
        type="linear"
    ),
    
)




plotly.offline.plot(fig, filename='bruh.html', auto_open=True,auto_play=False)
print (dfUpdate)




