### Loading Package ###

import pandas as pd


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