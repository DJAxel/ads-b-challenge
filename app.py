import dash
import dash_core_components as dcc
import dash_html_components as html

# from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

########################### PREP ###########################

# drinking water in 2017
water_data = pd.read_csv('./data/WSH_WATER_SAFELY_MANAGED,WSH_WATER_BASIC_xmart.csv')
water_data_zero_values = water_data.notna()[u'2017; Population using at least basic drinking-water services (%); Total']
water_data_sorted = water_data[water_data_zero_values].sort_values(by=u'2017; Population using at least basic drinking-water services (%); Total', ascending=True)

#drinking water in 2005
water_data_zero_values_2005 = water_data.notna()[u'2017; Population using at least basic drinking-water services (%); Total']
water_data_sorted_2005 = water_data[water_data_zero_values_2005].sort_values(by=u'2005; Population using at least basic drinking-water services (%); Total', ascending=True)

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
                children='Water',
                style=styles['h2'],
            ),
            html.P(
                children='Water is an important resource because all forms of life we know depend on it. The globe’s surface is covered in water for about 71% (United States Geological Survey, n.d.) , but of all water available, only less than 3% is fresh and drinkable. To top it off, 2.5 percenatge points of that is frozen in the artantica (United Nations, 2019). Water should therefor be used sparsely and recycled where possible.'
            ),
            html.H3(
                children='Fresh drinking water',
                style=styles['h3'],
            ),
            html.P(
                children='The most important water is the water that we drink in order to keep us hydrated. “Contaminated water and poor sanitation are linked to transmission of diseases such as cholera, diarrhoea, dysentery, hepatitis A, typhoid, and polio. Absent, inadequate, or inappropriately managed water and sanitation services expose individuals to preventable health risks.” (World Health Organization: WHO, 2019)'
            ),
            html.P(
                children='In the graph below are the percentage of people that had access to at least basic drinking-water services in 2017, that is “an improved drinking-water source within a round trip of 30 minutes to collect water” (World Health Organization: WHO, 2019). Most countries are doing fine, but in some countries as low as only 40% had access to these basic services. In total, 90% of the global population had access to basic drinking-water services in 2017.'
            ),
        ],
        style=styles['textContainer'],
    ),
    dcc.Graph(
        id='basic_drinking_water_access_2017',
        figure={
            'data': [
                go.Bar(
                    x=water_data_sorted['Country'],
                    y=water_data_sorted[u'2017; Population using at least basic drinking-water services (%); Total'],
                )
            ],
            'layout': go.Layout(
                xaxis={'visible': False},
                height=600,
                annotations=[
                    {
                        'x': 1,
                        'y': -0.1,
                        'text': 'Source: WHO',
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
                children='So are we on the right track? If we look at 2005, one of the first years where data from almost all countries is known, we can see that the curve used to be a lot worse with values of even around 25%.'
            ),
        ],
        style=styles['textContainer'],
    ),
    dcc.Graph(
        id='basic_drinking_water_access_2005',
        figure={
            'data': [
                go.Bar(
                    x=water_data_sorted_2005['Country'],
                    y=water_data_sorted_2005[u'2005; Population using at least basic drinking-water services (%); Total'],
                )
            ],
            'layout': go.Layout(
                xaxis={'visible': False},
                height=600,
                annotations=[
                    {
                        'x': 1,
                        'y': -0.1,
                        'text': 'Source: WHO',
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
                children='It’s interesting to see though that the percentage of countries scoring below 80% didn’t change much, but the countries scoring the worst made a great improvement. It is nevertheless still important to provide fresh drinking water for more people.'
            ),
        ],
        style=styles['textContainer'],
    ),
    html.Div(
        children=[
            html.H2(
                children='bibliography',
                style=styles['h2'],
            ),
            html.P(
                children='United Nations. (2019, July 23). Sustainable consumption and production. Retrieved May 4, 2020, from https://www.un.org/sustainabledevelopment/sustainable-consumption-production/'
            ),
            html.P(
                children='United States Geological Survey. (n.d.). How Much Water is There on Earth? Retrieved May 4, 2020, from https://www.usgs.gov/special-topic/water-science-school/science/how-much-water-there-earth?qt-science_center_objects=0#qt-science_center_objects'
            ),
        ],
        style=styles['textContainer'],
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
