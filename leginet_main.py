### Loading Packages ###

import dash
from dash import Input, Output
from network_layout import Layout
from network_data import Processing, Graph
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
     Input(component_id = "bill_number_input", component_property = "value")]
) # Function for updating network
def update_network(chosen_keyword, chosen_legislator, chosen_bill,
                   # chosen_chamber, chosen_party
                   ):

    # Copying dataframe
    network_data = sponsor_data.copy()


    ### Subsetting Based on User Input ###

    if ((chosen_keyword is not None) or (chosen_keyword.strip() != '')) and ((chosen_legislator is not None) or (chosen_legislator.strip() != '') and ((chosen_bill is not None) or (chosen_bill.strip() != ''))):

        network_data = network_data.loc[(network_data["description"].str.contains(chosen_keyword)) &
                                        (network_data["name"].str.contains(chosen_legislator, case = False)) &
                                        (network_data["bill_number"].str.contains(chosen_bill, case = False))]

    if ((chosen_keyword is not None) or (chosen_keyword.strip() != '')) and ((chosen_legislator is not None) or (chosen_legislator.strip() != '')) and ((chosen_bill is None) or (chosen_bill.strip() == '')):

        network_data = network_data.loc[(network_data["description"].str.contains(chosen_keyword, case = False)) &
                                        (network_data["name"].str.contains(chosen_legislator, case = False))]

    if ((chosen_keyword is None) or (chosen_keyword.strip() == '')) and ((chosen_legislator is not None) or (chosen_legislator.strip() != '')) and ((chosen_bill is not None) or (chosen_bill.strip() != '')):

        network_data = network_data.loc[(network_data["name"].str.contains(chosen_legislator, case = False)) &
                                        (network_data["bill_number"].str.contains(chosen_bill, case = False))]

    if ((chosen_keyword is not None) or (chosen_keyword.strip() != '')) and ((chosen_legislator is None) or (chosen_legislator.strip() == '')) and ((chosen_bill is not None) or (chosen_bill.strip() != '')):

        network_data = network_data.loc[(network_data["description"].str.contains(chosen_keyword, case = False)) &
                                        (network_data["bill_number"].str.contains(chosen_bill, case = False))]

    # Default
    if ((chosen_keyword is not None) or (chosen_keyword.strip() != '')) and ((chosen_legislator is None) or (chosen_legislator.strip() == '')) and ((chosen_bill is None) or (chosen_bill.strip() == '')):

        network_data = network_data.loc[network_data["description"].str.contains(chosen_keyword, case = False)]

    if ((chosen_keyword is None) or (chosen_keyword.strip() == '')) and ((chosen_legislator is not None) or (chosen_legislator.strip() != '')) and ((chosen_bill is None) or (chosen_bill.strip() == '')):

        network_data = network_data.loc[network_data["name"].str.contains(chosen_legislator, case = False)]

    if ((chosen_keyword is None) or (chosen_keyword.strip() == '')) and ((chosen_legislator is None) or (chosen_legislator.strip() == '')) and ((chosen_bill is not None) or (chosen_bill.strip() != '')):

        network_data = network_data.loc[network_data["bill_number"].str.contains(chosen_bill, case = False)]

    if ((chosen_keyword is None) or (chosen_keyword.strip() == '')) and ((chosen_legislator is None) or (chosen_legislator.strip() == '')) and ((chosen_bill is None) or (chosen_bill.strip() == '')):

        network_data = network_data



    # Wrapping title and description text
    network_data["title"] = network_data["title"].str.wrap(90)
    network_data["title"] = network_data["title"].apply(lambda x: x.replace("\n", "<br>"))

    network_data["description"] = network_data["description"].str.wrap(90)
    network_data["description"] = network_data["description"].apply(lambda x: x.replace("\n", "<br>"))

    # Creating subgraph
    figure = Graph.create_graph(network_data)

    # Returning figure
    return [go.Figure(data = figure)]


# @app.callback([Output("output-div", "children")],
#               [Input("network-graph", "clickData")]
# )
# def display_click_data(clickData):
#     if clickData and clickData["points"]:
#         point = clickData["points"][0]
#         if point["curveNumber"] == 0:  # Check if the point belongs to the scatter plot
#             if "doubleclick" in point and point["doubleclick"]:
#                 return f"Double-clicked on point ({point['x']}, {point['y']})"
#             else:
#                 return f"Clicked on point ({point['x']}, {point['y']})"
#     return ""


### Running App ###

if __name__ == "__main__":

    app.run_server(debug = True)