# TyperRacer History Plot
This is my attempt at making a python program to plot your race history in TypeRacer to have a clear picture of your progress
# Run
Run the python program from terminal with your username:
```
python TypeRace_plot.py -u "username"
```
- -u is for your username (must be in the "username" format)
- -nR is the number of Races you want to include in the plot
- -sl is what you consider a slow WPM for your standards
Example:
```
python TypeRace_plot.py -u "username" -nR 4000 -sl 70
```
## Example plot 1:
![newplot (1)](https://user-images.githubusercontent.com/37660959/99654347-77302800-2a5a-11eb-8267-494e2992e9cc.png)
## Example plot 2: 
Here I just changed the colorscale attribute of 'trace' from 'Magma' to 'rdylgn'
![newplot (2)](https://user-images.githubusercontent.com/37660959/99801639-aae08000-2b36-11eb-9994-db3b4a99063d.png)

## UPDATE:
Now you can change the the view mode of the graph to lines, markers and line&markers, a range bar was added to view the progress in a specific part of your journey and now there are a play and a pause button for the animation of your progress in parts of 100 races each.
### Markers
<img width="960" alt="markers update" src="https://user-images.githubusercontent.com/37660959/104643253-6c85be00-56ac-11eb-94e3-86568d04d3b9.png">

### Lines
<img width="960" alt="lines update" src="https://user-images.githubusercontent.com/37660959/104643294-7dceca80-56ac-11eb-97a0-d823414959f0.png">

### Lines & Markers
<img width="960" alt="lines+markers update" src="https://user-images.githubusercontent.com/37660959/104643306-832c1500-56ac-11eb-83d8-2fa26552d66b.png">


## Installation
Before you run the program install _**pandas**_ and _**plotly**_ libraries if you don't have them installed already:
* Open up your comand promt and type:
    * _**-pip install pandas**_
    * _**-pip install plotly**_

