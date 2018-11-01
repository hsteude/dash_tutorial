
#import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import pandas as pd

#read valid user and key pairs from file
with open('key.txt','r') as f:
    VALID_USERNAME_PASSWORD_PAIRS = [f.read()[:-1].split(',')]

#read data
df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# Boostrap CSS.
#app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})
markdown_text = '...is running on AWS in a docker container'

#############################
#app Layout
#############################
app.layout = html.Div([
    html.Div([
        #headline
        html.H1(children='Playing around with dash'),
        #some markdown text
        dcc.Markdown(children=markdown_text),
        ##text input
        html.Div([
            dcc.Input(id='my-id', value='Type some nonsense', type='text'),
            html.Div(id='my-div'),
                ])
    ], className="row"),
    #multi select component
    #html.Div('Select Continent(s)'),
        html.Div([
            html.B('Select continents'),
            dcc.Dropdown(
                id='SelectContinent',
                options=[
                    {'label': df['continent'].unique()[0],
                    'value': df['continent'].unique()[0]},
                    {'label': df['continent'].unique()[1],
                    'value': df['continent'].unique()[1]},
                    {'label': df['continent'].unique()[2],
                    'value': df['continent'].unique()[2]},
                    {'label': df['continent'].unique()[3],
                    'value': df['continent'].unique()[3]},
                    {'label': df['continent'].unique()[4],
                    'value': df['continent'].unique()[4]}
                ],
                value=[df['continent'].unique()[0],
                        df['continent'].unique()[1],
                        df['continent'].unique()[2]],
                multi=True
            )
            ],className='six columns'),
        html.Div([
            html.Div([
                html.B('Select the year in question'),
                dcc.Slider(
                    id='year-slider',
                    min=df['year'].min(),
                    max=df['year'].max(),
                    value=df['year'].max(),
                    marks={str(year): str(year) for year in df['year'].unique()}
                )
                ],className='five columns')
    ], className="row"),
    #graph
    dcc.Graph(
        id='life-exp-vs-gdp'
    )
], className='ten columns offset-by-one'
)



#############################
#app callbacks
#############################
@app.callback(
    dash.dependencies.Output('life-exp-vs-gdp', 'figure'),
    [dash.dependencies.Input('SelectContinent', 'value'),
     dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_conti, selected_year):
    df1 = df[df['continent'].isin(selected_conti)]
    df1 = df1[df['year'] == selected_year]
    figure={
        'data': [
            go.Scatter(
                x=df1[df1['continent'] == i]['gdpPercap'],
                y=df1[df1['continent'] == i]['lifeExp'],
                text=df1[df1['continent'] == i]['country'],
                mode='markers',
                opacity=0.8,
                marker={
                    'size': 15
                },
                name=i
            ) for i in df1.continent.unique()
        ],
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
    return figure




@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    if (input_value == 'Type some nonsense' or len(input_value)==0):
        return ''
    else:
        out = len(input_value.split())
        return 'You\'ve entered '+str(out) +' words. Awesome!'


if __name__ == '__main__':
    app.run_server(debug=True, host= '0.0.0.0')
