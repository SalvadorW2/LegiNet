### Loading Packages ###

from dash import dcc, html
# import dash_bootstrap_components as dbc


### Creating UI Layout ###

class Layout:

    ui_layout = html.Div([

        # Graph name
        html.Div([
            
            html.H2("LegiNet Georgia", style = {"text-align": "center"}),

            html.Br()
        
        ], style = {"padding": 10, "flex": 1}),

        html.Div([

            html.Div([

                # Legislative chamber input

                html.Label(["Chamber: "], style = {"font-weight": "bold", "text-align": "center"}),

                dcc.Dropdown(id = "chamber_input",
                            options = [{"label": "Both", "value": "Both"},
                                    {"label": "House", "value": "Representative"},
                                    {"label": "Senate", "value": "Senator"}],
                            multi = False,
                            clearable = False,
                            value = "Both",
                            style = {"width": "40%"}),

                html.Br(),

                    # Party input

                html.Label(["Party: "], style = {"font-weight": "bold", "text-align": "center"}),

                dcc.Dropdown(id = "party_input",
                            options = [{"label": "Both", "value": "Both"},
                                    {"label": "Democrat", "value": "Democrat"},
                                    {"label": "Republican", "value": "Republican"}],
                            multi = False,
                            clearable = False,
                            value = "Both",
                            style = {"width": "40%"}),

                html.Br(),

                    # Keyword Input

                html.Label(["Keyword: "], style = {"font-weight": "bold", "text-align": "center"}),
            
                dcc.Input(id = "keyword_input",
                        type = "text",
                        value = "mental health"),

                html.Br(),

                    # Legislator name input

                html.Label(["Legislator: "], style = {"font-weight": "bold", "text-align": "center"}),
            
                dcc.Input(id = "legislator_name_input",
                        type = "text",
                        value = ''),

                html.Br(),

                    # Bill number input

                html.Label(["Bill: "], style = {"font-weight": "bold", "text-align": "center"}),
            
                dcc.Input(id = "bill_number_input",
                        type = "text",
                        value = '')

            ],  style = {"width": "100%", "height": "100vh", "padding": 10, "flex": 1}),

            html.Div([

                # Graph output
                dcc.Graph(id = "network-graph",
                        style = {"height": "100%", "width": "80%"},
                        # figure = {"layout": {"dragmode": "pan"}},
                        config = {"scrollZoom": True}
                )

            ], style = {"padding": 10, "flex": 1})

        ], style = {"display": "flex", "flexDirection": "row"})

    ], style = {"display": "flex", "flexDirection": "column"})