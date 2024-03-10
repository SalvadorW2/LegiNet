### Loading Packages ###

import dash
from dash import dcc, html, Input, Output
from network_data import Data
import plotly.graph_objs as go
import networkx as nx


### Data Processing ###

# Getting directory
data_directory = r"C:/Users/scwag/Desktop/W/Network_Analysis/2023-2024_Regular_Session"

# Processing data
sponsor_data = Data.process_data(directory = data_directory)


### Configuring App Layout ###

# Initializing app
app = dash.Dash(__name__)

# Defining app layout
app.layout = html.Div(

    # Configuring app style
    style = {"width'": "100%",
             "height": "100vh"},

    children = [

        # Graph name
        html.H2("LegiNet Georgia", style = {"text-align": "center"}),

        # Legislative chamber input
        html.Div([

            html.Label(["Select legislative chamber: "], style = {"font-weight": "bold", "text-align": "center"}),

            dcc.Dropdown(id = "chamber_input",
                        options = [{"label": "Both", "value": "Both"},
                                   {"label": "House", "value": "Representative"},
                                   {"label": "Senate", "value": "Senator"}],
                        multi = False,
                        clearable = False,
                        value = "Both",
                        style = {"width": "40%"})

        ]),

        # Party input
        html.Div([

            html.Label(["Select party: "], style = {"font-weight": "bold", "text-align": "center"}),

            dcc.Dropdown(id = "party_input",
                        options = [{"label": "Both", "value": "Both"},
                                   {"label": "Democrat", "value": "Democrat"},
                                   {"label": "Republican", "value": "Republican"}],
                        multi = False,
                        clearable = False,
                        value = "Both",
                        style = {"width": "40%"})

        ]),

        # Keyword Input
        html.Div([

            html.Label(["Enter keyword: "], style = {"font-weight": "bold", "text-align": "center"}),
        
            dcc.Input(id = "keyword_input",
                      type = "text",
                      value = "mental health")

        ]),

        # Legislator name input
        html.Div([

            html.Label(["Enter legislator name: "], style = {"font-weight": "bold", "text-align": "center"}),
        
            dcc.Input(id = "legislator_name_input",
                      type = "text",
                      value = '')

        ]),

        # Bill number input
        html.Div([

            html.Label(["Enter bill number: "], style = {"font-weight": "bold", "text-align": "center"}),
        
            dcc.Input(id = "bill_number_input",
                      type = "text",
                      value = '')

        ]),

        # Graph output
        dcc.Graph(id = "network-graph",
                  style = {"height": "90%", "width": "100%"},
                  # figure = {"layout": {"dragmode": "pan"}},
                  config = {"scrollZoom": True}
        )

    ]

)


### Configuring App Functionality ###

# Linking input and output with "callback" decorator
@app.callback(
    [Output(component_id = "network-graph", component_property = "figure")],

    [Input(component_id = "keyword_input", component_property = "value"),
     Input(component_id = "legislator_name_input", component_property = "value"),
     Input(component_id = "bill_number_input", component_property = "value"),
     Input(component_id = "chamber_input", component_property = "value"),
     Input(component_id = "party_input", component_property = "value")]
) # Function for updating network
def update_network(chosen_keyword, chosen_legislator, chosen_bill, chosen_chamber, chosen_party):


    ### Copying Dataframe ###
    network_data = sponsor_data.copy()


    ### Subsetting Based on User Input ###

    # Subsetting based on chamber
    if  chosen_chamber == "Both":

        network_data = network_data

    else:

        network_data = network_data.loc[network_data["role"].str.contains(chosen_chamber, case = False)]

    # Subsetting based on chamber
    if  chosen_party == "Both":

        network_data = network_data

    else:

        network_data = network_data.loc[network_data["party"].str.contains(chosen_party, case = False)]

    # Subsetting based on keyword
    network_data = network_data.loc[network_data["description"].str.contains(chosen_keyword, case = False)]

    # Subsettign based on on legislator name
    network_data = network_data.loc[network_data["name"].str.contains(chosen_legislator, case = False)]

    # Subsetting based on bill number
    network_data = network_data.loc[network_data["bill_number"].str.contains(chosen_bill, case = False)]


    ### Wrapping Title and Description Text ###

    network_data["title"] = network_data["title"].str.wrap(90)
    network_data["title"] = network_data["title"].apply(lambda x: x.replace("\n", "<br>"))

    network_data["description"] = network_data["description"].str.wrap(90)
    network_data["description"] = network_data["description"].apply(lambda x: x.replace("\n", "<br>"))


    ### Creating Graph ###

    # Creating graph from dataframe
    graph = nx.from_pandas_edgelist(df = network_data,
                                    source = "name",
                                    target = "bill_number")
    
    pos = nx.spring_layout(graph)


    ### Creating Graph Figure ###

    # Creating network graph figure
    figure = go.Figure()

    # Adding edges
    for edge in graph.edges():
        figure.add_trace(
            go.Scatter(
                x = [pos[edge[0]][0], pos[edge[1]][0]],
                y = [pos[edge[0]][1], pos[edge[1]][1]],
                mode = "lines",
                line = dict(color = "black",
                            width = 0.5),
                opacity = 0.5
        ))
        
    # Creating series for sponsor iterators
    sponsor_names = network_data["name"]
    sponsor_colors = network_data["color"]
    sponsor_parties = network_data["party"]
    sponsor_roles = network_data["role"]
    sponsor_districts = network_data["district"]
    sponsor_bill_number = network_data["number_bills"]
        
    # Adding source nodes to the graph
    sponsor_nodes = zip(sponsor_names, sponsor_colors, sponsor_parties, sponsor_roles, sponsor_districts, sponsor_bill_number)

    for sponsor in sponsor_nodes:

        sponsor_name = sponsor[0]
        sponsor_color = sponsor[1]
        sponsor_party = sponsor[2]
        sponsor_role = sponsor[3]
        sponsor_district = sponsor[4]
        no_bills = sponsor[5]

        figure.add_trace(go.Scatter(
            x = [pos[sponsor_name][0]],
            y = [pos[sponsor_name][1]],
            mode = "markers",
            marker = dict(
                size = 10,
                symbol = "circle",
                color = sponsor_color
            ),
            text = f"<b>Name:</b> {sponsor_name}<br><b>Party:</b> {sponsor_party}<br><b>Role:</b> {sponsor_role}<br><b>District:</b> {sponsor_district}<br><b>Number of Bills Sponsored:<b> {no_bills}",
            hoverinfo = "text" # Showing node information on hover
        ))

    # Creating series for bill iterators
    bill_numbers = network_data["bill_number"]
    bill_titles = network_data["title"]
    bill_descriptions = network_data["description"]
    bill_links = network_data["url"]
    bill_sponsor_number = network_data["number_sponsors"]

    # Adding destination nodes to the graph
    bill_nodes = zip(bill_numbers, bill_titles, bill_descriptions, bill_links, bill_sponsor_number)

    for bill in bill_nodes:

        bill_id = bill[0]
        bill_title = bill[1]
        bill_description = bill[2]
        bill_link = bill[3]
        no_sponsors = bill[4]

        figure.add_trace(go.Scatter(
            x = [pos[bill_id][0]],
            y = [pos[bill_id][1]],
            mode = "markers",
            marker = dict(
                size = 10,
                symbol = "square",
                color = "green"
            ),
            text = f"<b>Bill Number:</b> {bill_id}<br><b>Bill Title:</b> {bill_title}<br><b>Bill Description:</b> {bill_description}<br><b>URL: </b><a href = \"{bill_link}\">{bill_link}</a><br><b>Number of Sponsors: </b>{no_sponsors}",
            hoverinfo = "text" # Showing node information on hover
        ))

    # Updating graph layout
    figure.update_layout(
        showlegend = False,
        xaxis = dict(visible = True, showticklabels = True),
        yaxis = dict(visible = True, showticklabels = True)
    )

    # Configuring figure layout
    figure.update_layout(modebar_remove = ["zoom", "lasso2d", "select2d"])
    
    # Returning figure
    return [go.Figure(data = figure)]


### Running App ###

if __name__ == "__main__":

    app.run_server(debug = True)