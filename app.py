import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

########################### PREP ###########################

# Aanvoer, verwerking van afval bij recyclingbedrijven Nederland
recycling_NL = pd.read_csv('./data/Aanvoer,_verwerking_van_afval_bij_recyclingbedrijven_Nederland_1996-2016.csv', sep=';')
recycling_NL_melted = pd.melt(recycling_NL, ['Perioden'], ['Metaalafval_3', 'GlasPapierHoutKunststofED_4', 'DierlijkPlantaardigAfval_5', 'GemengdAfval_6', 'Slib_7', 'MineralenSteenachtigAfval_8', 'OverigNietChemischAfval_9', 'ChemischAfval_10'])

# UN Data: Total amount of municipal waste collected
tot_municipal_waste = pd.read_csv('./data/UNdata_Total_amount_of_municipal_waste_collected_worldwide_1990-2016.csv', encoding = "ISO-8859-1")
tot_municipal_waste['Value'] = tot_municipal_waste['Value'] * 1000000
tot_municipal_waste['Unit'] = 'kg'

world_pop = pd.read_csv('./data/world_population_altered.csv', delimiter=';')
columns = list(world_pop)
columns = columns[columns.index('y1990'):columns.index('y2016')+1] # List of all columns we need: 1990 - 2016
wp_melted = pd.melt(world_pop, id_vars=['Country_Name'], value_vars=columns, var_name='Year', value_name='population') #unpivot (melt) wp
wp_melted['Year'] = wp_melted['Year'].str[1:] # Remove y prefix from years
wp_melted['Year'] = pd.to_numeric(wp_melted['Year']) # convert Year to Int64
wp_melted['population'] = wp_melted['population'] * 1000 # convert to total amount of inhabitants

tot_municipal_waste = pd.merge(tot_municipal_waste, wp_melted, how='inner', left_on=['Year', 'Country or Area'], right_on=['Year', 'Country_Name'])
tot_municipal_waste['value_per_capita'] = tot_municipal_waste['Value'] / tot_municipal_waste['population']
tot_municipal_waste_grouped = tot_municipal_waste.groupby('Year', as_index = True).mean()


########################## LAYOUT ##########################
colors = {
    'background': '#FFF',
    'text': '#000'
}
styles = {
    'paragraph': {
        'textAlign': 'left',
        'color': colors['text'],
    },
    'textContainer': {
        'maxWidth': '768px',
        'margin': 'auto',
    },
    'graphs': {
        'width': '1160px',
        'margin': 'auto',
    },
    'h2': {},
    'h3': {},
}
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Challenge data story',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'marginBottom': '.5rem',
        }
    ),
    html.Div(children='SDG 12: sustainable consumption and production', style={
        'textAlign': 'center',
        'color': colors['text'],
        'fontSize': '1.2em',
        'marginBottom': '2rem',
    }),
    html.Div(
        children=[
            html.P(
                children='In 2015, a set of 17 goals was set by the United Nations to be met in 2030, in order to make our planet more sustainable and a better place for us all. One of those goals was to “ensure sustainable consumption and production patterns”, meaning that governmants, civilians and the industry should become more aware of the resources used for the products and services they create and use.',
                style=styles['paragraph'],
            ),
            html.P(
                children='The main topics include water, energy and food: things we often take for granted, but might not be that accessable for developing countries and are running out if we keep using them in the current pace. This article looks for the trends from the past years and the answer to the question: are we heading towards the right direction to meet this goal?',
                style=styles['paragraph'],
            ),
            html.H2(
                children='Recycling',
                style=styles['h2'],
            ),
            html.P(
                children='So what kind of garbage is being collected and seperated and in what propotions does this happen? It’s hard to compare this over multiple countries in one graph as different countries combine different sorts of waste together. Looking at just the Netherlands we can see that the most collected category is ‘rocks and minerals’ by a long mile. The amount of metal waste is about the same as ‘glas/paper/wood/plastic’. Then at the lower end, we have animal/vegetable waste, mixed waste and   other non-chemical waste. Sludge and chemical waste have both taken a massive dive between 2006-2008 and 2012-2014 respectively. The sludge has been stable for a few years now, but it’s to soon to tell if this will be the same case for chemical waste as well.'
            ),
            html.P(
                children='Keep in mind that the following graph has a logarithmic scale due to the fact that the rocks and minerals have much higher values than the other types of waste.'
            ),
        ],
        style=styles['textContainer'],
    ),
    dcc.Graph(
        id='preprocessing_waste_dutch_recycling_companies_components',
        figure={
            'data': [
                go.Scatter(
                    x=recycling_NL['Perioden'],
                    y=recycling_NL['Metaalafval_3'],
                    name='Metal',
                ),
                go.Scatter(
                    x=recycling_NL['Perioden'],
                    y=recycling_NL['GlasPapierHoutKunststofED_4'],
                    name='Glass/paper/wood/plastic',
                ),
                go.Scatter(
                    x=recycling_NL['Perioden'],
                    y=recycling_NL['DierlijkPlantaardigAfval_5'],
                    name='Animal/vegetable',
                ),
                go.Scatter(
                    x=recycling_NL['Perioden'],
                    y=recycling_NL['GemengdAfval_6'],
                    name='Mixed',
                ),
                go.Scatter(
                    x=recycling_NL['Perioden'],
                    y=recycling_NL['Slib_7'],
                    name='Sludge',
                ),
                go.Scatter(
                    x=recycling_NL['Perioden'],
                    y=recycling_NL['MineralenSteenachtigAfval_8'],
                    name='Rocks/minerals',
                ),
                go.Scatter(
                    x=recycling_NL['Perioden'],
                    y=recycling_NL['OverigNietChemischAfval_9'],
                    name='Other not chemical',
                ),
                go.Scatter(
                    x=recycling_NL['Perioden'],
                    y=recycling_NL['ChemischAfval_10'],
                    name='Chemical',
                ),
            ],
            'layout': go.Layout(
                title='Pre-processing of waste in Dutch recycling companies',
                xaxis={'title': 'Year', 'range': [2004, 2016]},
                yaxis={'title': 'Supplied materials (× 1000 tonnes)', 'type': 'log'},
                height=600,
                annotations=[
                    {
                        'x': 1,
                        'y': -0.1,
                        'text': 'Source: CBS',
                        'showarrow': False,
                        'xref': 'paper',
                        'yref': 'paper',
                        'xanchor': 'right',
                        'yanchor': 'auto',
                        'xshift': 0,
                        'yshift': 0,
                        'font': {'size': 15},
                    }
                ]
            )
        },
        style=styles['graphs']
    ),
    html.Div(
        children=[
            html.P(
                children='When looking at the total amount of waste collected for recycling in the Netherlands, there is a slightly positive trendline visible. This linear trend doesn’t say very much though, as the actual trend is fluctuating and R² is close to 0.14. The amount of waste supplied to companies for recycling in the Netherlands has steadily increased between 1998 and 2006, but made an equally stable decrease between 2006 and 2014. In 2016, the amount of supplied waste increased a little again.'
            )
        ],
        style=styles['textContainer'],
    ),
    dcc.Graph(
        id='preprocessing_waste_dutch_recycling_companies_total',
        figure=px.scatter(recycling_NL, x="Perioden", y="TotaalAanvoerAfval_1", trendline="ols")
            .update_layout(
                title="Total amount of supplied waste for recycling in the Netherlands",
                xaxis={'title': 'Year'},
                yaxis={'title': 'Supplied materials (× 1000 tonnes)'},
                annotations=[
                    {
                        'x': 1,
                        'y': -0.14,
                        'text': 'Source: CBS',
                        'showarrow': False,
                        'xref': 'paper',
                        'yref': 'paper',
                        'xanchor': 'right',
                        'yanchor': 'auto',
                        'xshift': 0,
                        'yshift': 0,
                        'font': {'size': 15},
                    }
                ]
            ),
        style=styles['graphs']
    ),
    html.Div(
        children=[
            html.P(
                children='Another positive trend can be seen when looking at what happened with the waste after it has been collected for recycling. Some of this waste will still get burned (orange line), altough this amount is relatively low and has been stable over the last two decades. On the other side, there is a great increase as of 2006 from waste used for useful applications (green line).'
            )
        ],
        style=styles['textContainer'],
    ),
    dcc.Graph(
        id='preprocessing_waste_dutch_recycling_companies_after',
        figure={
            'data': [
                go.Scatter(
                    x=recycling_NL['Perioden'],
                    y=recycling_NL['NuttigeToepassing_14'],
                    name='Useful applications',
                    line = {'color': 'rgb(44, 160, 44)'},
                ),
                go.Scatter(
                    x=recycling_NL['Perioden'],
                    y=recycling_NL['Verbranden_15'],
                    name='Burned',
                    line = {'color': 'rgb(255, 127, 14)'},
                ),
            ],
            'layout': go.Layout(
                title='Processing of waste supplied for recycling',
                xaxis={'title': 'Year'},
                yaxis={'title': 'Waste (× 1000 tonnes)'},
                height=600,
                annotations=[
                    {
                        'x': 1,
                        'y': -0.1,
                        'text': 'Source: CBS',
                        'showarrow': False,
                        'xref': 'paper',
                        'yref': 'paper',
                        'xanchor': 'right',
                        'yanchor': 'auto',
                        'xshift': 0,
                        'yshift': 0,
                        'font': {'size': 15},
                    }
                ]
            )
        },
        style=styles['graphs']
    ),
    html.Div(
        children=[
            html.P(
                children='This detailed information of seperated waste streams and what happened to the collected waste is not easy to project n a worldwide scale; Every country measures these values differently. The total amount of waste is one of the measures that is easily comparable though, and looking at the amount of waste per person, it’s easy to see how much materials humans have been consuming over the past years.'
            ),
            html.P(
                children='Let’s be honest: it’s not very feasable that the average annual amount of waste per person is about half a kilogram, so more data is needed to show a reliable output. There was no time to sort this out however, so I added the graph anyway. I also didn’t find an explanation for the two outliers in 2013 and 2015 yet. Mind the y-axis has a logarithmic scale once again.'
            ),
        ],
        style=styles['textContainer'],
    ),
    dcc.Graph(
        id='municipal_waste_footprint_per_capita',
        figure={
            'data': [
                go.Scatter(
                    x=tot_municipal_waste_grouped.index,
                    y=tot_municipal_waste_grouped['value_per_capita'],
                    name='Waste per capita',
                ),
            ],
            'layout': go.Layout(
                title='Worldwide waste per capita',
                xaxis={'title': 'Year'},
                yaxis={'title': 'Waste per capita (kg)', 'type': 'log'},
                height=600,
                annotations=[
                    {
                        'x': 1,
                        'y': -0.1,
                        'text': 'Source: United Nations',
                        'showarrow': False,
                        'xref': 'paper',
                        'yref': 'paper',
                        'xanchor': 'right',
                        'yanchor': 'auto',
                        'xshift': 0,
                        'yshift': 0,
                        'font': {'size': 15},
                    }
                ]
            )
        },
        style=styles['graphs']
    ),
    html.Div(
        children=[
            html.P(
                children='In conclusion, it’s hard to say how the world is doing when every country is using it’s own methods of measuring and there are so many factors at stake. Comparing data from the same country works very well, as the same context applies to (almost) all data. Zooming out get’s more and more difficult.'
            ),
            html.P(
                children='It looks like recycling levels go up slightly since a few years now, and the total amount of waste – although probably not showing the right absolute amount – shows a small decreasing trend as well. The best way to make sure of that however remains taking our own responsibility, by recycling, repairing, buying second hand and boycotting products with lots of hazardous material or unnecesary packaging.'
            ),
        ],
        style=styles['textContainer'],
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
