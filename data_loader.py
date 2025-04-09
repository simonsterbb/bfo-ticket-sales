import pandas as pd
from urllib.request import urlopen
import json
from config import DATA_PATH_2024, ZIPCODE_URLS, CONCERT_DATES
import os
from utils import save_geojson
import geopandas as gpd

class TicketDataLoader:
    def __init__(self, base_path):
        self.base_path = base_path
        self.raw_data = None
        self.data = None
        self.geo_data = None
        self.concert_dates = CONCERT_DATES

    def load_raw_data(self):
        """Load the raw data from CSV."""
        self.raw_data = pd.read_csv(self.base_path)
        return self.raw_data

    def clean_data(self):
        """Clean and preprocess the raw ticket data."""
        if self.raw_data is None:
            self.load_raw_data()

        df = self.raw_data.copy()
        if "Buyer Name" in df.columns:
            return self.process_format_A(df) # Season 5
        elif "Buyer First Name" in df.columns:
            return self.process_format_B(df) # Season 4
        else:
            raise ValueError("Unknown file format")

    def process_format_A(self, df):
        print(df)
        # Take value per ticket and replicate rows
        df["Ticket Net Proceeds"] = round(df["Order Total"]/df["Tickets"], 2)
        df = df.loc[df.index.repeat(df["Tickets"])].reset_index(drop=True)



        # Set Ticket Type
        df["Ticket Type"] = "Other"
        df.loc[df["Ticket Net Proceeds"] == 53.63, "Ticket Type"] = "Premium"
        df.loc[df["Ticket Net Proceeds"] == 32.59, "Ticket Type"] = "Regular"
        df.loc[df["Ticket Net Proceeds"] < 32.59, "Ticket Type"] = "Pay What You Can"

        # Define Free Dickets
        df["Payment Type"] = "Online"
        df.loc[df["Ticket Net Proceeds"] == 0, "Payment Type"] = "Free"


        # Clean date and time

        df["Date & time"] = pd.to_datetime(df["Date & time"])#, format="%-m/%-d/%Y %H:%M")
        df["Time of Purchase"] = df['Date & time'].dt.time
        df["Date of Purchase"] =  pd.to_datetime(df['Date & time'].dt.date)




        # Clean postal codes and city names
        #print(["hi" + str(df['Buyer Postal Code'].iloc[j])for j in range(len(df))])
        df["Buyer Postal Code"] = pd.Series(["0" + str(code)
                                   if len(str(code)) == 4
                                   else code
                                   for code in df["Buyer Postal Code"]])
        df["Buyer City"] = df["Buyer City"].str.title()

        df["Tickets in Order"] = df["Tickets"]
        self.data = df

        return self.data


    def process_format_B(self, df):

        # Clean monetary values
        df["Ticket Net Proceeds"] = df["Ticket Net Proceeds"].replace({r'\$':''}, regex=True).replace(' -   ', 0).astype(float)

        # Clean date and time
        df["Date of Purchase"] = pd.to_datetime(df["Date of Purchase"], format="%m/%d/%y %H:%M")
        df["Time of Purchase"] = df["Date of Purchase"].dt.time
        df["Date of Purchase"] = pd.to_datetime(df["Date of Purchase"].dt.date)


        # Clean postal codes and city names
        df["Buyer Postal Code"] = df["Buyer Postal Code"].str.split("-").str[0]  # Clean up postal codes with a hyphen in them
        df["Buyer City"] = df["Buyer City"].str.title()
        self.data = df
        return self.data

    def get_data(self, clean=True):
        if self.data is None or clean:
            self.clean_data()
        return self.data

    def load_geo_data(self, state, state_zip_url):
        """Load GeoJSON data for choropleth maps."""
        print(state)
        # Check if file exists on computer
        state_zip_path = state + "_zip.geojson"
        if os.path.exists(state_zip_path):
            with open(state_zip_path, 'r') as f:
                self.geo_data = json.load(f)

        # Import file from the internet and save
        else:

            with urlopen(state_zip_url) as response:
                self.geo_data = json.load(response)
            save_geojson(state, self.geo_data)
        return self.geo_data

    def combine_geo_data(self, state_list):

        combined_features = []
        for state, state_zip_url in ZIPCODE_URLS.items():

            if state in state_list:


                geo_data = self.load_geo_data(state, state_zip_url)

                combined_features.extend(geo_data["features"])


        combined_geojson = {
            "type": "FeatureCollection",
            "features": combined_features,
        }

        return combined_geojson

    # def load_and_combine(self, states):
    #     combined_gdf = []
    #     state_str = ''
    #     for state in states:
    #         gdf_file = gpd.read_file(state + "_zip.geojson")
    #         gdf_file["geometry"] = gdf_file["geometry"].simplify(tolerance=0.01)
    #
    #         combined_gdf.append(gdf_file)
    #         state_str += state + "_"
    #
    #     combined_gdf = gpd.GeoDataFrame(pd.concat(combined_gdf, ignore_index=True))
    #     print(combined_gdf)
    #     cdf = combined_gdf.to_json()
    #     # with open(state_str + "simplified_zipcodes.geojson", 'w') as f:
    #     #     json.dump(combined_gdf, f)
    #     return cdf