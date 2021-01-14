# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:54:12 2020

@author: porsche
"""

import pandas as pd
from datetime import datetime,date # almost inutile
import plotly
import plotly.graph_objects as go

# =============================================================================
# =============================================================================
# # MISSING TRENDLINE, CHANGING OF FRAME MODE ON BUTTON PRESSED
# =============================================================================
# =============================================================================

# Scrapes typeracer stats from typeracer.com and generates a csv file

# USERNAME: (string) type racer user name (you can put the username of any typeracer player)
USERNAME = ''

# RACES: (string) this is how many races should the program shearch in you history of races
# To see all the races i recommend a high number like 9999999 so you don't have to change it everytime you run it
RACES = ''

# CSV_OUT: (string) path to the csv file to be written to
# Example: '/Users/r4lpf/Documents/Python/TypeRacer_plot/output.csv' (or wherever you put the master folder)
CSV_OUT = ''

# URL: url of the page for scraping the stats
# Example: 'https://data.typeracer.com/pit/race_history?user=slow_penguin&universe=play&n=500&cursor=&startDate='
URL = 'https://data.typeracer.com/pit/race_history?user=' + USERNAME + '&universe=play&n=' + RACES + '&cursor=&startDate='

dfs = pd.read_html(URL, header=0)
csvfile = open(CSV_OUT, 'w');
for df in dfs[1:]:
    df.to_csv(csvfile)

mesi = {
    '01' : 'Jan.',
    '02' : 'Feb.',
    '03' : 'Mar.',
    '04' : 'Apr.',
    '05' : 'May',
    '06' : 'Jun.',
    '07' : 'Jul.',
    '08' : 'Aug.',
    '09' : 'Sep.',
    '10' : 'Oct.',
    '11' : 'Nov.',
    '12' : 'Dec.'
    }

def today(d): 
    if d == 'today':
        t = datetime.today().strftime('%Y-%m-%d').split("-")
        return mesi[t[1]]+' '+t[2]+','+' '+t[0]
    else:
        return d



df["Date"] = df["Date"].apply(lambda d : today(d))

# =============================================================================
# DF_CONTROL is a DataFrame with control values having 
# m as the maximum WPM and l as the lowest WPM 
# I create this control dataframe because I was having trouble with the sorting
# I probably just made a TYPO but i cannot be arsed to find it so i did this
# =============================================================================
largest_race_number = int(df['Race #'].max())
m = int(df['Speed'].max().replace(" WPM",""))+3
l = int(df['Speed'].min().replace(" WPM",""))-1   

df_control = pd.DataFrame({
    "Race #":[float('nan') for x in range(l,m)],#This just places the control values on the far left of the graph
    "Speed":[str(x)+" WPM" for x in range(l,m)],
    "Accuracy":["100.0%" for x in range(l,m)],
    "Points":[0 for x in range(l,m)],
    "Place":[0 for x in range(l,m)],
    "Date":["Jan. 1, 1999" for x in range(l,m)]
    
    }
)
df = df.sort_values(["Race #","Speed"],ascending = [True,True]).reset_index(drop=True)

df = df_control.append(df,ignore_index=True,sort=True)

#Now i have all the data that i need to complete the plot of the history type racer


fig = go.Figure(
    data = go.Scatter(
    x=df['Race #'].where(df['Race #']>=0),
    y = df['Speed'],
    mode = 'markers',
    marker = dict(
        size = 8,
        sizemode='area',
        sizeref=1,
        color=[eval(x[:-1]) for x in df['Accuracy']], #set color equal to a variable
        colorscale= 'rdylgn', # one of plotly colorscales
        showscale=True,
        colorbar=dict(title="<b>Accuracy</b>")   #<b> and </b> is to change the title to bold
        ),
    line=dict(
        color='gold',
        width=0.5
        ),
    showlegend=False,
    
    text = df[['Date','Accuracy']],
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
        xaxis = dict(zeroline = True,
        title="<b>Race #</b>"),
        sliders = []
        ),
    #INSIDE "frames" the initial idea was to put inside it:
    #go.Frame(data=[go.Scatter(x=[d['Race #']], y=[d['Speed']])]) for i,d in df.iterrows() if d['Race #']>=0
    frames = [] #In the end the content of frames is put later.
    
)
    

# =============================================================================
# FIRST SCATTER GL
# Here i change the color of the lines to red if my writing speed 
# is slower than "slow"
# =============================================================================

slow = 55  #You can change this value however you like it to be just remember it is 
           #the lower boundary where below it red lines start appearing

fig.add_scattergl(
    x=df['Race #'].where(df['Race #']>=0), 
    y=df['Speed'].where(df['Speed'] < str(slow) + " WPM"), 
    mode = 'markers',
    line=dict(
        color='red',
        width=1
        ),
    marker = dict(
        size = 8,
        sizemode='area',
        sizeref=1,
        color=[eval(x[:-1]) for x in df['Accuracy']], #set color equal to a variable
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
    x=df['Race #'].where(df['Race #']>=0), 
    y=df['Speed'].where(df['Speed'] >= str(slow)+" WPM"), 
    mode = 'markers',
    line=dict(
        color='green',
        width=1
        ),
    marker = dict(
        size = 8,
        sizemode='area',
        sizeref=1,
        color=[eval(x[:-1]) for x in df['Accuracy']], #set color equal to a variable
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
                    x = df['Race #'].where((df['Race #']>=x-101) & (df['Race #']<x)),
                    y = df['Speed'],
                    mode = 'markers',
                    text = df[['Date','Accuracy']],
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
                    x = df['Race #'].where((df['Race #']>=x-101) & (df['Race #']<x)),
                    y = df['Speed'].where(df['Speed'] < str(slow) + " WPM"),
                    mode = 'markers',
                    text = df[['Date','Accuracy']],
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
                    x = df['Race #'].where((df['Race #']>=x-101) & (df['Race #']<x)),
                    y = df['Speed'].where(df['Speed'] > str(slow) + " WPM"),
                    mode = 'markers',
                    text = df[['Date','Accuracy']],
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
                 
        ) for x in range(101,largest_race_number+100,100)]

fig["frames"] = fig['frames'] + tuple([
    go.Frame(
        data = [
            go.Scatter(
                    x = df['Race #'].where(df['Race #']>=0),
                    y = df['Speed'],
                    mode = 'markers',
                    text = df[['Date','Accuracy']],
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
                    x = df['Race #'].where(df['Race #']>=0),
                    y = df['Speed'].where(df['Speed'] < str(slow) + " WPM"),
                    mode = 'markers',
                    text = df[['Date','Accuracy']],
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
                    x = df['Race #'].where(df['Race #']>=0),
                    y = df['Speed'].where(df['Speed'] >= str(slow) + " WPM"),
                    mode = 'markers',
                    text = df[['Date','Accuracy']],
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
            x = 0.1,
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
        range = [-10,largest_race_number+10],
        rangeslider=dict(
        visible=True
        ),
        type="linear"
    ),
    
)




plotly.offline.plot(fig, filename='bruh.html', auto_open=True,auto_play=False)
