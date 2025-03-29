import pandas as pd
from urllib.request import urlopen
import json
from config import DATA_PATH_2024, MASS_ZIP_CODE_URL, CONCERT_DATES

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

    def load_geo_data(self, zip_code_url):
        """Load GeoJSON data for choropleth maps."""
        with urlopen(zip_code_url) as response:
            self.geo_data = json.load(response)
        return self.geo_data

