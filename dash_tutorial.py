
#import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import pandas as pd

app = dash.Dash()

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')


df.head()
df.info()

markdown_text = '''
$a/b$
'''
len(df['continent'].unique())

#############################
#app Layout
#############################
app.layout = html.Div([
    #headline
    html.H1(children='Hello Dash'),
    #some markdown text
    dcc.Markdown(children=markdown_text),
    ##text input
    html.Div([
        dcc.Input(id='my-id', value='Dash App', type='text'),
        html.Div(id='my-div'),
        html.Div(id='my2-div')
            ]),
    #multi select component
    html.Label('Select Continent'),
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
            value=[],
            multi=True
        ),
    #graph
    dcc.Graph(
        id='life-exp-vs-gdp'
    ),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()}
    )
])



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
    dash.dependencies.Output('my2-div', component_property='children'),
    [dash.dependencies.Input('SelectContinent', 'value')])
def update_selection(selected_conti):
    return selected_conti



@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server()
