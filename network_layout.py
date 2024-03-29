### Loading Packages ###

from dash import dcc, html
# import dash_bootstrap_components as dbc


### Creating UI Layout ###

class Layout:

    ui_layout = html.Div([

        # Graph name
        html.Div([
            
            html.H2("LegiNet Georgia", style = {"text-align": "center"}),
        
        ], style = {"padding": 10, "flex": 1}),

        html.Div([

            html.Div([

                # Keyword Input

                html.Label(["Keyword: "], style = {"font-weight": "bold", "text-align": "center"}),
            
                dcc.Input(id = "keyword_input",
                        type = "text",
                        value = "mental health"),

                html.Br(),
                html.Br(),

                # Legislator name input

                html.Label(["Legislator: "], style = {"font-weight": "bold", "text-align": "center"}),
            
                dcc.Input(id = "legislator_name_input",
                        type = "text",
                        value = ''),

                html.Br(),
                html.Br(),

                # Bill number input

                html.Label(["Bill: "], style = {"font-weight": "bold", "text-align": "center"}),
            
                dcc.Input(id = "bill_number_input",
                        type = "text",
                        value = ''),

                html.Br(),
                html.Br(),

                html.Button("Apply Changes", id = "apply_button", n_clicks = 0)

            ],  style = {"width": "20%", "height": "100vh", "padding": 10, "flex": 1}),

            html.Div([

                # Graph output
                dcc.Graph(id = "network-graph",
                        style = {"height": "100%", "width": "80%"},
                        # figure = {"layout": {"dragmode": "pan"}},
                        config = {"scrollZoom": True}
                )

            ], style = {"padding": 10, "width": "80%"})

        ], style = {"display": "flex", "flexDirection": "row"}) # ,

        # html.Div(id = "output-div")

    ], style = {"display": "flex", "flexDirection": "column"})