# Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_excel('C:/Users/ianli/OneDrive/Desktop/testing 2.xlsx')

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='Dashboard'),
    dcc.Dropdown(['Temperature', 'Humidity', 'Illumination'], 'Select Data'),
    dcc.Checklist(['Node 1', 'Node 2', 'Node 3']),
    dash_table.DataTable(data=df.to_dict('records'), page_size=100),

    dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=df['Time'].tolist(),
                    y=df['Temperature '].tolist(),
                    name='Temperature',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                ),
                dict(
                    x=df['Time'].tolist(),
                    y=df['Humidity'].tolist(),
                    name='Humidity',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                ),
                dict(
                    x=df['Time'].tolist(),
                    y=df['Illumination'].tolist(),
                    name='Illumination',
                    marker=dict(
                        color='rgb(10, 200, 255)'
                    )
                )
            ],
            layout=dict(
                title='Time-series Graph',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 600},
        id='my-graph-example'
    )
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)