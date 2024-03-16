### Loading Packages ###

import dash
from dash import Input, Output
from network_layout import Layout
from network_data import Processing, Filtering
import plotly.graph_objs as go
import networkx as nx


### Data Processing ###

# Getting directory
data_directory = r"C:/Users/scwag/Desktop/W/Network_Analysis/2023-2024_Regular_Session"

# Processing data
sponsor_data = Processing.process_data(directory = data_directory)


### Configuring App Layout ###

# Initializing app
app = dash.Dash(name = __name__)

# Defining app layout
app.layout = Layout.ui_layout


### Creating Graph ###

# Creating graph from dataframe
full_graph = nx.from_pandas_edgelist(df = sponsor_data,
                                     source = "name",
                                     target = "bill_number"
                                     )

# Assigning network physics
## position = nx.spring_layout(full_graph)


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
    network_data = Filtering.chamber_filter(data = network_data, selection = chosen_chamber)

    # Subsetting based on party
    network_data = Filtering.party_filter(data = network_data, selection = chosen_party)

    # Subsetting based on keyword
    network_data = Filtering.keyword_filter(data = network_data, selection = chosen_keyword)

    # Subsettign based on on legislator name
    network_data = Filtering.name_filter(data = network_data, selection = chosen_legislator)

    # Subsetting based on bill number
    network_data = Filtering.bill_filter(data = network_data, selection = chosen_bill)


    # Wrapping title and description text
    network_data["title"] = network_data["title"].str.wrap(90)
    network_data["title"] = network_data["title"].apply(lambda x: x.replace("\n", "<br>"))

    network_data["description"] = network_data["description"].str.wrap(90)
    network_data["description"] = network_data["description"].apply(lambda x: x.replace("\n", "<br>"))

    # Creating subgraph
    # Creating graph from dataframe
    subgraph = nx.from_pandas_edgelist(df = network_data,
                                       source = "name",
                                       target = "bill_number"
                                       )

    # Assigning network physics
    position = nx.spring_layout(subgraph)


    ### Creating Graph Figure ###

    # Creating network graph figure
    figure = go.Figure()

    # Adding edges
    for edge in subgraph.edges():
        figure.add_trace(
            go.Scatter(
                x = [position[edge[0]][0], position[edge[1]][0]],
                y = [position[edge[0]][1], position[edge[1]][1]],
                mode = "lines",
                line = dict(color = "black",
                            width = 0.5),
                opacity = 0.7
        ))
    
    # Adding source nodes to the graph
    for sponsor in zip(network_data["name"],
                       network_data["color"],
                       network_data["party"],
                       network_data["role"],
                       network_data["district"],
                       network_data["number_bills"]):

        # Assigning iterator names
        sponsor_name = sponsor[0]
        sponsor_color = sponsor[1]
        sponsor_party = sponsor[2]
        sponsor_role = sponsor[3]
        sponsor_district = sponsor[4]
        no_bills = sponsor[5]

        # Adding nodes
        figure.add_trace(go.Scatter(
            x = [position[sponsor_name][0]],
            y = [position[sponsor_name][1]],
            mode = "markers",
            marker = dict(
                size = 10,
                symbol = "circle",
                color = sponsor_color
            ),
            text = f"<b>Name:</b> {sponsor_name}<br><b>Party:</b> {sponsor_party}<br><b>Role:</b> {sponsor_role}<br><b>District:</b> {sponsor_district}<br><b>Number of Bills Sponsored:<b> {no_bills}",
            hoverinfo = "text" # Showing node information on hover
        ))

    # Adding destination nodes to the graph
    for bill in zip(network_data["bill_number"],
                    network_data["title"],
                    network_data["description"],
                    network_data["url"],
                    network_data["number_sponsors"]):

        # Assigning iterator names
        bill_id = bill[0]
        bill_title = bill[1]
        bill_description = bill[2]
        bill_link = bill[3]
        no_sponsors = bill[4]

        # Adding nodes
        figure.add_trace(go.Scatter(
            x = [position[bill_id][0]],
            y = [position[bill_id][1]],
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