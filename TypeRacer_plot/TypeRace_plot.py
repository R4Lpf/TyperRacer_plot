# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:54:12 2020

@author: porsche
"""

import pandas as pd
from datetime import datetime,date # almost inutile
import plotly
import plotly.graph_objects as go


# Scrapes typeracer stats from typeracer.com and generates a csv file

# USERNAME: (string) type racer user name
USERNAME = ''

# RACES: (string) this is how many races should the program shearch in you history of races
# To see all the races i recommend a high number like 9999999 so you don't have to change it everytime you run it
RACES = ''

# CSV_OUT: (string) path to the csv file to be written to
# Example: '/Users/kondavarsha/Documents/Python/TypeRacer_plot/output.csv'
CSV_OUT = ''

# URL: url of the page for scraping the stats
# Example: 'https://data.typeracer.com/pit/race_history?user=slow_penguin&universe=play&n=500&cursor=&startDate='
URL = 'https://data.typeracer.com/pit/race_history?user=' + USERNAME + '&universe=play&n=' + RACES + '&cursor=&startDate='

dfs = pd.read_html(URL, header=0)
csvfile = open(CSV_OUT, 'w');
for df in dfs[1:]:
    df.to_csv(csvfile)

df = df.sort_values("Speed").reset_index(drop=True)
trace = go.Scatter(
    y = df['Speed'],
    x = df['Race #'],
    mode = 'markers',
    marker = dict(
    size = 10,
    sizemode='area',
    sizeref=1,
    color=[eval(x[:-1]) for x in df['Accuracy']], #set color equal to a variable
    colorscale='Magma', # one of plotly colorscales
    showscale=True,
    colorbar=dict(title="Accuracy")
    )
)

figura = [trace]
layout = dict(title = 'Speed in Races over time (2020)',
              yaxis = dict(zeroline = True,
                title="Speed (WPM)"),
              xaxis = dict(zeroline = True,
                title="Race #")
             )

fig = dict(data = figura,layout = layout)
plotly.offline.plot(fig, filename='bruh.html', auto_open=True)
