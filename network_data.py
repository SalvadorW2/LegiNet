### Loading Package ###

import pandas as pd
import networkx as nx
import plotly.graph_objs as go


### Function for Processing Data ###

class Processing:

    def process_data(directory: str) -> pd.DataFrame:

        # Importing "people" CSV
        people = pd.read_csv(directory + "/csv/people.csv")

        people = people.drop(["first_name", "middle_name", "last_name", "suffix", "nickname", "party_id", "role_id", "ballotpedia"],
                            axis = 1)

        # Importing "bills" CSV
        bills = pd.read_csv(directory + "/csv/bills.csv")

        bills = bills.drop(["status", "committee_id"], axis = 1)

        # Importing "sponsors" CSV
        sponsors = pd.read_csv(directory + "/csv/sponsors.csv")

        merge_1 = pd.merge(left = people,
                           right = sponsors,
                           how = "left",
                           left_on = people["people_id"],
                           right_on = sponsors["people_id"],
                           copy = False)
        
        merge_1 = merge_1.drop(["people_id_y", "key_0"], axis = 1)

        merge_1 = merge_1.fillna(0)

        merge_2 = pd.merge(left = merge_1,
                           right = bills,
                           how = "left",
                           left_on = merge_1["bill_id"],
                           right_on = bills["bill_id"],
                           copy = False)

        # Subsetting columns used in network
        sponsor_data = merge_2[["people_id_x", "name", "party", "role", "district", "bill_number", "title", "description", "url"]]

        # Changing columns
        ## Turning off copy warning
        pd.set_option("mode.chained_assignment", None)
        
        ## Creating color column
        sponsor_data.loc[sponsor_data["party"] == "R", "color"] = "red"
        sponsor_data.loc[sponsor_data["party"] == "D", "color"] = "blue"

        ## Unabbreviating
        sponsor_data.loc[sponsor_data["party"] == "R", "party"] = "Republican"
        sponsor_data.loc[sponsor_data["party"] == "D", "party"] = "Democrat"

        sponsor_data.loc[sponsor_data["role"] == "Rep", "role"] = "Representative"
        sponsor_data.loc[sponsor_data["role"] == "Sen", "role"] = "Senator"

        # Dropping missing observations
        sponsor_data = sponsor_data.dropna()

        # Creating columns for number of bills sponsored per person and number of sponsors per bill
        sponsor_data["number_sponsors"] = sponsor_data.groupby("bill_number")["bill_number"].transform("size")
        sponsor_data["number_bills"] = sponsor_data.groupby("name")["name"].transform("size")

        # Copying columns for filtering
        sponsor_data["number_sponsors_used"] = sponsor_data["number_sponsors"]
        sponsor_data["number_bills_used"] = sponsor_data["number_bills"]

        return sponsor_data
    

class Graph:

    def create_graph(data: pd.DataFrame):
        # Creating graph from dataframe
        subgraph = nx.from_pandas_edgelist(df = data,
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
        for sponsor in zip(data["name"],
                           data["color"],
                           data["party"],
                           data["role"],
                           data["district"],
                           data["number_bills"]):

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
        for bill in zip(data["bill_number"],
                        data["title"],
                        data["description"],
                        data["url"],
                        data["number_sponsors"]):

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
    
        # Returning finished graph
        return figure
    
class Filtering:

    def chamber_filter(data: pd.DataFrame, selection: str) -> pd.DataFrame:

        if  selection == "Both":

            data = data

        else:

            data = data.loc[data["role"].str.contains(selection, case = False)]

        return data


    def party_filter(data: pd.DataFrame, selection: str) -> pd.DataFrame:

        if  selection == "Both":

            data = data

        else:

            data = data.loc[data["party"].str.contains(selection, case = False)]

        return data


    def keyword_filter(data: pd.DataFrame, selection: str) -> pd.DataFrame:

        data = data.loc[data["description"].str.contains(selection, case = False)]

        return data
    

    def name_filter(data: pd.DataFrame, selection: str) -> pd.DataFrame:

        data = data.loc[data["name"].str.contains(selection, case = False)]

        return data
    

    def bill_filter(data: pd.DataFrame, selection: str) -> pd.DataFrame:

        data = data.loc[data["bill_number"].str.contains(selection, case = False)]

        return data