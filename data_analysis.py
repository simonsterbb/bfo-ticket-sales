import pandas as pd
import numpy as np

class TicketAnalyzer:
    """Class for analyzing ticket sales data."""
    def __init__(self, data):
        """Initialize with preprocessed ticket data."""
        self.data = data

    def analyze_by_source(self):

        heard_about_df = self.data.groupby(
            by=["How did you hear about this event? (Buyer)", "Ticket Type"],
            as_index=False
        ).aggregate({
            "Ticket Net Proceeds": "sum",
            "Order ID": ["nunique"]
        })

        # Calculate average ticket price
        heard_about_df["Average Ticket Price"] = heard_about_df["Ticket Net Proceeds"]["sum"] / \
                                                 heard_about_df["Order ID"]["nunique"]
        # pd.set_option('display.max_columns', None)

        # Format df (Flatten column names
        flat_cols = []
        [flat_cols.append(i[0]) for i in
         heard_about_df.columns]  # iterate through this tuples and join them as single string
        heard_about_df.columns = flat_cols  # now assign the list of flattened columns to the grouped columns.

        # Sort by total sales
        category_sums = heard_about_df.groupby("How did you hear about this event? (Buyer)")["Order ID"].sum()
        sorted_categories = category_sums.sort_values(ascending=False).index
        heard_about_df["How did you hear about this event? (Buyer)"] = pd.Categorical(
            heard_about_df["How did you hear about this event? (Buyer)"],
            categories=sorted_categories,
            ordered=True)
        heard_about_df = heard_about_df.sort_values(by="How did you hear about this event? (Buyer)")

        return heard_about_df

    def analyze_by_city(self, select_top=10):
        """Analyze ticket data by city"""
        city_df = self.data.groupby(["Buyer City", "Ticket Type"]).aggregate({
            "Order ID": ["nunique", "count"]})

        city_df.columns = city_df.columns.droplevel(0)  # Necessary for chloropleth function
        city_df = city_df.reset_index()

        # Sort by top 10 total sales in a acity
        category_sums = city_df.groupby("Buyer City")["count"].sum()
        sorted_categories = category_sums.sort_values(ascending=False).index
        top_categories = sorted_categories[:select_top]

        # city_df_top = city_df[city_df["Buyer City"].isin(top_categories)]
        city_df["Buyer City"] = pd.Categorical(
            city_df["Buyer City"],
            categories=top_categories,
            ordered=True
        )
        city_df_top = city_df.sort_values(by="Buyer City")

        #pd.set_option("display.max_rows", None)

        # data_canada = px.data.gapminder().query("country == 'Canada'")
        return  city_df_top

    def analyze_zipcode_map(self, exclude_pwyc):
        zip_orders_df = self.data.groupby(
            ["Buyer Postal Code", "Ticket Type"]
        ).aggregate(
            {"Ticket Net Proceeds": "mean",#np.nanmean,
             "Order ID": ["nunique", "count"]})


        zip_orders_df.columns = zip_orders_df.columns.droplevel(0)  # Necessary for chloropleth function
        zip_orders_df = zip_orders_df.reset_index()

        # if exclude_pwyc:
        #     zip_orders_df = zip_orders_df[zip_orders_df["Ticket Type"] != "Pay What You Can"]

        # pd.set_option("display.max_rows", None)
        # print(zip_orders_df)
        return zip_orders_df

    def analyze_weekly(self):

        # Group by date, event, payment type
        grouped = self.data.groupby(["Date of Purchase", "Event", "Payment Type"])
        grouped = grouped.agg({
            'Ticket Net Proceeds': 'sum',
            'Tickets in Order': 'count'
        }).reset_index()

        # Add ticket proceeds together by week
        weekly_df = grouped.groupby(["Event", pd.Grouper(key="Date of Purchase", freq="W")])[
            "Ticket Net Proceeds"].sum().reset_index()
        return weekly_df

    def analyze_time_series(self):
        """Analyze ticket sales over time"""
        # Group by date, event, payment type
        grouped = self.data.groupby(["Date of Purchase", "Event", "Payment Type"])
        grouped = grouped.agg({
            'Ticket Net Proceeds': 'sum',
            'Tickets in Order': 'count'
        }).reset_index()

        # Pivot to get a time series for each event and payment type
        pivot_df = grouped.pivot(
            index="Date of Purchase",
            columns=["Event", "Payment Type"],
            values=["Tickets in Order", "Ticket Net Proceeds"])

        pivot_df = pivot_df.fillna(0)
        pivot_df = pivot_df.sort_index()
        stacked_data = pivot_df.cumsum()

        return grouped, pivot_df, stacked_data

    def analyze_cumulative_sales(self, concert_dates):

        _, _, stacked_data = self.analyze_time_series()

        # Cumulative Ticket Sales (including free tickets) over season
        df_unstacked = stacked_data["Tickets in Order"].stack(level=0,future_stack=True).reset_index()
        df_unstacked["Purchased"] = df_unstacked["Cash"] + df_unstacked["Ticketleap"]
        df_unstacked.drop(columns=["Cash", "Ticketleap"], inplace=True)

        # Convert to long format for easier plotting
        cumulative_df = df_unstacked.melt(id_vars=['Date of Purchase', 'Event'],
                                    var_name="Payment Type",
                                    value_name='Values')

        timing_stats = {}
        # Calculate the  free tickets given away per period of time
        for concert, concert_date in concert_dates.items():
            # Define time periods
            time_vector = pd.to_datetime(
                [(concert_date - pd.to_timedelta(60, unit='d')),  # Two months before
                 (concert_date - pd.to_timedelta(30, unit='d')),  # One month before
                 (concert_date - pd.to_timedelta(1, unit='w')),  # One week before
                 (concert_date - pd.to_timedelta(1, unit='d')),  # One day before
                 concert_date])  # Day of concert

            # Filter by concert and by Free status
            df_long_free = cumulative_df[
                (cumulative_df["Payment Type"] == "Free") &
                (cumulative_df["Event"] == concert)
            ]

            # Keep only the last row of every day
            df_by_day_free = df_long_free.sort_values("Date of Purchase").drop_duplicates("Date of Purchase",
                                                                                          keep="last")

            # Find the closest already-happened date to the defined time periods
            df_total_free_tickets = pd.merge_asof(
                pd.DataFrame({'target_date': time_vector}),  # Left side: your target dates
                df_by_day_free,  # Right side: the DataFrame you're matching against
                left_on='target_date',  # Column to match in target
                right_on='Date of Purchase',  # Column to match in the DataFrame
                direction='backward'  # Find the closest earlier date
            ).drop(["target_date"], axis=1)

            # Calculate new tickets sold in each time period
            df_total_free_tickets["Diff Sold"] = (
                        df_total_free_tickets["Values"] -
                        df_total_free_tickets["Values"].shift(1))

            # Fill first new tickets sold cell with total tickets sold
            df_total_free_tickets.fillna({"Diff Sold":df_total_free_tickets["Values"]}, inplace=True)

            # Calculate the percentage of total tickets sold in each time period
            df_total_free_tickets["Diff Sold (%)"] = (
                        df_total_free_tickets["Diff Sold"] /
                        df_total_free_tickets["Values"].max() * 100
            ).apply(lambda x: round(x, 0))

            timing_stats[concert] = df_total_free_tickets


        return cumulative_df, timing_stats

    def analyze_cumulative_income(self, concert_dates):
        _, _, stacked_data = self.analyze_time_series()

        cumulative_income_df = stacked_data["Ticket Net Proceeds"].stack(level=0, future_stack=True).reset_index()
        cumulative_income_df["Purchased"] = cumulative_income_df["Cash"] + cumulative_income_df["Ticketleap"]
        cumulative_income_df.drop(columns=["Cash", "Ticketleap", "Free"], inplace=True)

        return cumulative_income_df


