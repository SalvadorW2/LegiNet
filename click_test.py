import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go

app = dash.Dash(__name__)

# Sample data
x_data = [1, 2, 3, 4, 5]
y_data = [2, 3, 5, 7, 11]

app.layout = html.Div([
    dcc.Graph(
        id='scatter-plot',
        figure={
            'data': [
                go.Scatter(
                    x=x_data,
                    y=y_data,
                    mode='markers',
                    marker=dict(size=10)
                )
            ],
            'layout': go.Layout(
                title='Scatter Plot',
                hovermode='closest'
            )
        }
    ),
    html.Div(id='output-div')
])

# Callback to handle double-click event
@app.callback(
    Output('output-div', 'children'),
    [Input('scatter-plot', 'clickData')]
)
def display_click_data(clickData):
    if clickData and clickData['points']:
        point = clickData['points'][0]
        if point['curveNumber'] == 0:  # Check if the point belongs to the scatter plot
            if 'doubleclick' in point and point['doubleclick']:
                return f"Double-clicked on point ({point['x']}, {point['y']})"
            else:
                return f"Clicked on point ({point['x']}, {point['y']})"
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)