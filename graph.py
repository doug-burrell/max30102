import plotly
import random
import plotly.graph_objs as go
from collections import deque

X = deque(maxlen = 20)
X.append(1)

Y = deque(maxlen = 20)
Y.append(1)

## ------------------------ varios plot
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_bar = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df_bar, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div([
		dcc.Graph(id = 'live-graph', animate = True),
		dcc.Interval(
			id = 'graph-update',
			interval = 1000,
			n_intervals = 0
		),
	], className='six columns'),
        html.Div([
            html.H1(children='Hello Dash [2]'),

            html.Div(children='''
                Dash: A web application framework for Python.
            '''),

            dcc.Graph(
                id='graph2',
                figure=fig
            ),  
        ], className='six columns'),
    ], className='row'),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='Hello Dash [3]'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='graph3',
            figure=fig
        ),  
    ], className='row'),
])

@app.callback(
	Output('live-graph', 'figure'),
	[ Input('graph-update', 'n_intervals') ]
)

def update_graph_scatter(n):
	X.append(X[-1]+1)
	Y.append(Y[-1]+Y[-1] * random.uniform(-0.1,0.1))

	data = plotly.graph_objs.Scatter(
			x=list(X),
			y=list(Y),
			name='Scatter',
			mode= 'lines+markers'
	)

	return {'data': [data],
			'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [min(Y),max(Y)]),)}


if __name__ == '__main__':
    app.run_server(debug=True)