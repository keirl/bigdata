#Import the numpy and pandas libraries
import pandas as pd
import plotly.plotly as plotly
import os

#Get the OS folder/directory path
data_path = os.path.join(os.path.dirname(__file__),os.pardir,'rawdata')

#Read the csv file with the state statistic results
df = pd.read_csv(data_path+'/STATE_SUMMARY.CSV');

#Define a colorscale for the map
clrscl = [[0.0,'rgb(0,255,0)'],[0.25,'rgb(128,255,0)'],[0.5,'rgb(255,255,0)'],\
            [0.75,'rgb(255,128,0)'],[1.0,'rgb(255,0,0)']]

#Define the data to be plotted and labels to be applied
data = [ dict(
            type = 'choropleth',
            colorscale = clrscl,
            autocolorscale = False,
            locations=df['STATEABBR'],
            z = df['GASCAPITA'].astype(float),
            locationmode = 'USA-states',
            text = 'Annual Gasoline Consumption Per Capita',
            marker = dict(
                line = dict(color = 'rgb(255,255,255)',width = 2)
        ),
        colorbar = dict(title = "Gallons")
    ) ]

#Define which type of map to use
layout = dict(
        title = 'US Gasoline Consumption by State Per Capita',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)',
        ),
    )

#Create the figure from the data and the layout defined
fig = dict( data=data, layout=layout )

#Plot the figure and load it as an html in a browser
url = plotly.plot( fig, filename='gasoline_consumption_per_capita_map' )
