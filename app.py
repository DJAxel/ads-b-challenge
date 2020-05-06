import dash
import dash_core_components as dcc
import dash_html_components as html

# from dash.dependencies import Input, Output
# import pandas as pd
# import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#FFF',
    'text': '#000'
}
styles = {
    'paragraph': {
        'textAlign': 'left',
        'color': colors['text'],
    },
    'h2': {

    },
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
        style={
            'maxWidth': '768px',
            'margin': 'auto',
        }
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
