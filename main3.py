import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from urllib.request import urlopen
import json

# MASSACHUSETTS ONLY
with urlopen('https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ma_massachusetts_zip_codes_geo.min.json') as response:
    zipcodes_MA = json.load(response)

# with urlopen('https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ny_new_york_zip_codes_geo.min.json') as response:
#      zipcodes_NY = json.load(response)




# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)

FILE_NAME = "S4 Ticket Data COMPLETE.csv"
CONCERT_DATE = {'FIREBIRD': datetime(2024,7,14).date(),
                'SCHEHERAZADE': datetime(2024,7,28).date()}



def load_data(file_path):
    return pd.read_csv(FILE_NAME)

def clean_data(df):
    df["Ticket Net Proceeds"] = df["Ticket Net Proceeds"].replace('[\$]', '', regex=True).replace(' -   ', 0).astype(
        float)
    df["Date of Purchase"] = pd.to_datetime(df["Date of Purchase"])
    df["Time of Purchase"] = df["Date of Purchase"].dt.time
    df["Date of Purchase"] = pd.to_datetime(df["Date of Purchase"].dt.date)
    df["Buyer Postal Code"] = df["Buyer Postal Code"].str.split("-").str[
        0]  # Clean up postal codes with a hyphen in them
    df["Buyer City"] = df["Buyer City"].str.title()
    return df

def print_hi(name):
    # Ticket Net Proceeds; Buyer Postal Code, Billing Postal Code; Date of Purchase; Referrer
    # Tickets in Order, Order Total; Ticket Type; Section; Accessibility Options;
    # Are you interested in subscribing to the monthly BFO newsletter? (Buyer)
    # How did you hear about this event? (Buyer)
    df = load_data(FILE_NAME)
    df_clean = clean_data(df)
    #zipcode_df = pd.DataFrame(data=df['Buyer Postal Code'].value_counts()).rename_axis("Buyer Postal Code").reset_index("Counts")
    # zipcode_df = zipcode_df.rename(columns=["Buyer Postal Code"])
    # Blank for free or for not online tickets

    zipcode_df = df['Buyer Postal Code'].value_counts().rename_axis("Buyer Postal Code").reset_index(name='Counts') # Make a new df sorted by zipcode
    international_df = zipcode_df[~zipcode_df["Buyer Postal Code"].str.contains(r'[0-9]{5}')] # Find zip codes outside of US
    zipcode_df = zipcode_df.astype({"Counts": np.float64}) # Convert to float

    # df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
    #                  dtype={"fips": str})

    #data.groupby('Buyer Postal Code').mean()["Tickets in Order"]

    #print(type(zipcodes_MA))

    if True:
        heard_about_df = df_clean.groupby(by=["How did you hear about this event? (Buyer)", "Ticket Type"],
                                          as_index=False).aggregate({
            "Ticket Net Proceeds":sum,
                "Order ID":["nunique"]},)
        heard_about_df["Average Ticket Price"] = heard_about_df["Ticket Net Proceeds"]["sum"]/heard_about_df["Order ID"]["nunique"]
        pd.set_option('display.max_columns', None)




        # Format df
        flat_cols = []
        [flat_cols.append(i[0]) for i in heard_about_df.columns] # iterate through this tuples and join them as single string
        heard_about_df.columns = flat_cols # now assign the list of flattened columns to the grouped columns.

        # Sort by total sales
        category_sums = heard_about_df.groupby("How did you hear about this event? (Buyer)")["Order ID"].sum()
        sorted_categories = category_sums.sort_values(ascending=False).index
        heard_about_df["How did you hear about this event? (Buyer)"] = pd.Categorical(heard_about_df["How did you hear about this event? (Buyer)"],
                                                                                      categories=sorted_categories,
                                                                                      ordered=True)
        heard_about_df = heard_about_df.sort_values(by="How did you hear about this event? (Buyer)")

        if True:
            print(heard_about_df[heard_about_df["Ticket Type"] == "Pay What You Can"])
            heard_about_df_PWYC = heard_about_df[heard_about_df["Ticket Type"] == "Pay What You Can"].sort_values("Average Ticket Price",ascending=False)

            fig = px.bar(heard_about_df_PWYC,
                         x="How did you hear about this event? (Buyer)",
                         y="Average Ticket Price",
                         labels={
                             "How did you hear about this event? (Buyer)": "How did you hear about this event?",
                         },
                         )

            fig.update_layout(xaxis={'tickfont_size': 20,
                                     "gridcolor": "gainsboro",
                                     "tickangle": 45,
                                     "tickvals": ["Word of Mouth", "Social Media", "Other",
                                                  "Online Events Calendar (The Boston Calendar, ArtsBoston, etc.)",
                                                  "Previous BFO Event", "BFO Newsletter", "Flyer/Poster",
                                                  "Advertisement",
                                                  "Newspaper"],
                                     "ticktext": ["Word of Mouth", "Social Media", "Other", "Events Calendar",
                                                  "Previous BFO Event", "BFO Newsletter", "Flyer", "Advertisement",
                                                  "Newspaper"]},
                              yaxis={'tickfont_size': 20, "gridcolor": "lightgray"},
                              yaxis_tickprefix='$', yaxis_tickformat=',.2f', # Set to dollars
                              xaxis_title=dict(font=dict(size=30)),
                              yaxis_title=dict(font=dict(size=30)),
                              paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)',
                              legend=dict(font=dict(size=30)),
                              legend_title_text='')

            fig.show()


        if False:
            fig = px.bar(heard_about_df,
                         x="How did you hear about this event? (Buyer)",
                         y= "Order ID",
                         color="Ticket Type",
                         barmode="group",
                         labels={
                             "How did you hear about this event? (Buyer)": "How did you hear about this event?",
                             "Order ID": "Total Number of Tickets",
                         },
                         )

            fig.update_layout(xaxis={'tickfont_size': 20,
                                     "gridcolor": "gainsboro",
                                     "tickvals": ["Word of Mouth", "Social Media", "Other",
                                                  "Online Events Calendar (The Boston Calendar, ArtsBoston, etc.)",
                                                  "Previous BFO Event", "BFO Newsletter", "Flyer/Poster", "Advertisement",
                                                  "Newspaper"],
                                     "ticktext": ["Word of Mouth", "Social Media", "Other", "Events Calendar",
                                                  "Previous BFO Event", "BFO Newsletter", "Flyer", "Advertisement",
                                                  "Newspaper"]},
                              yaxis={'tickfont_size': 20, "gridcolor": "lightgray"},
                              xaxis_title=dict(font=dict(size=30)),
                              yaxis_title=dict(font=dict(size=30)),
                              paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)',
                              legend=dict(font=dict(size=30)),
                              legend_title_text='')
            fig.show()


    if False:
        ###### Not yet
        pwyc_df = df_clean.groupby(["Ticket Type"])["Ticket Net Proceeds"].mean()
        pwyc_df_med = df_clean.groupby(["Ticket Type"])["Ticket Net Proceeds"].median()
        print(pwyc_df)
        print(pwyc_df_med)

    if False:
        city_df = df_clean.groupby(["Buyer City","Ticket Type"]).aggregate({"Order ID": ["nunique", "count"]})

        city_df.columns = city_df.columns.droplevel(0) # Necessary for chloropleth function
        city_df = city_df.reset_index()

        # Sort by top 10 total sales in a acity
        category_sums = city_df.groupby("Buyer City")["count"].sum()
        sorted_categories = category_sums.sort_values(ascending=False).index
        top_categories = sorted_categories[:10]
        #city_df_top = city_df[city_df["Buyer City"].isin(top_categories)]
        city_df["Buyer City"] = pd.Categorical(city_df["Buyer City"], categories=top_categories, ordered=True)
        city_df_top = city_df.sort_values(by="Buyer City")

        pd.set_option("display.max_rows", None)

        #data_canada = px.data.gapminder().query("country == 'Canada'")

        fig = px.bar(city_df_top,
                     x="Buyer City",
                     y="count",
                     color="Ticket Type",
                     barmode="group",
                     labels={
                         "Buyer City": "City",
                         "count": "Total Number of Tickets",
                     },
                     )

        fig.update_layout(xaxis={'tickfont_size': 20, "gridcolor": "gainsboro"},
                          yaxis={'tickfont_size': 20, "gridcolor": "lightgray"},
                          xaxis_title=dict(font=dict(size=30)),
                          yaxis_title=dict(font=dict(size=30)),
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          legend=dict(font=dict(size=30)),
                          legend_title_text='')

        fig.show()
        print(city_df_top)



    # Good maps
    if False:
        zip_orders_df_h = df_clean.groupby(["Buyer Postal Code", "Ticket Type"]).aggregate(
            {"Ticket Net Proceeds": np.nanmean, "Order ID": ["nunique", "count"]})
        zip_orders_df_h.columns = zip_orders_df_h.columns.droplevel(0) # Necessary for chloropleth function
        zip_orders_df_h = zip_orders_df_h.reset_index()

        pd.set_option("display.max_rows", None)
        print(zip_orders_df_h)

        fig = px.choropleth_mapbox(zip_orders_df_h[zip_orders_df_h["Ticket Type"] != "Pay What You Can"], geojson=zipcodes_MA,
                                   locations="Buyer Postal Code",
                                   color="count",
                                   color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",
                                   zoom=8, center={"lat": 42.363075, "lon": -71.058690},
                                   featureidkey="properties.ZCTA5CE10",
                                   opacity=0.5,
                                   labels={'count': 'Tickets Sold'})

        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.show()

#Probably BADDDD (NOT INCORPORATED IN)
    if False:
        fig = px.choropleth_mapbox(zipcode_df, geojson=zipcodes_MA,
                            locations="Buyer Postal Code",
                            color="Counts",
                            color_continuous_scale="Viridis",
                            mapbox_style="carto-positron",
                            zoom=8, center={"lat": 42.363075, "lon": -71.058690},
                            featureidkey="properties.ZCTA5CE10",
                            opacity=0.5,
                            labels={'Counts': 'Tickets Sold'})

        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.show()



        # Count orders of multiple tickets as a single purchase
        zip_orders_df = df.groupby(["Buyer Postal Code"])["Tickets in Order"].value_counts().reset_index(name="Count")
        zip_orders_df["Individual Purchase Correction"] = zip_orders_df["Count"] - zip_orders_df["Count"]/zip_orders_df["Tickets in Order"]
        zipcode_df = pd.merge(zipcode_df, zip_orders_df.groupby("Buyer Postal Code")["Individual Purchase Correction"].sum(), on="Buyer Postal Code")
        zipcode_df["Individual Purchases"] = zipcode_df["Counts"] - zipcode_df["Individual Purchase Correction"]

        zip_orders_df_pwyc = df[df["Ticket Type"] == "Pay What You Can"].groupby(["Buyer Postal Code"])["Tickets in Order"].value_counts().reset_index(name="Count")
        zip_orders_df_pwyc["Individual Purchase Correction"] = zip_orders_df_pwyc["Count"] - zip_orders_df_pwyc["Count"]/zip_orders_df_pwyc["Tickets in Order"]

        zip_orders_df_g = df.groupby(["Buyer Postal Code", "Ticket Type"])["Tickets in Order"].value_counts().reset_index(name="Count")
        zip_orders_df_h = df.groupby(["Buyer Postal Code", "Ticket Type"]).aggregate({ "Ticket Net Proceeds": np.nanmean, "Order ID":["nunique", "count"]}).reset_index()
        print(zip_orders_df_h)

        # print(df[df["Ticket Type"] == "Pay What You Can"].groupby(["Buyer Postal Code"])["Ticket Net Proceeds"].mean().reset_index(name="Amount Paid"))
        # print(df["Buyer Postal Code"].unique())

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    grouped = df.groupby(["Date of Purchase",  "Event", "Payment Type"])
    grouped = grouped.agg({
    'Ticket Net Proceeds': 'sum',
    'Tickets in Order': 'count'
}).reset_index()


    pivot_df = grouped.pivot(index="Date of Purchase", columns=["Event", "Payment Type"], values=["Tickets in Order", "Ticket Net Proceeds"])
    pivot_df = pivot_df.fillna(0)
    pivot_df = pivot_df.sort_index()


    if False:
        # Add ticket proceeds together by week
        df_weekly_proceeds = grouped.groupby(["Event", pd.Grouper(key="Date of Purchase", freq="W")])["Ticket Net Proceeds"].sum().reset_index()


        #print(df_weekly_proceeds)

        fig = px.line(df_weekly_proceeds,
                      x="Date of Purchase",
                      y="Ticket Net Proceeds",
                      color="Event",

                      labels={
                          "Date of Purchase": "Date of Purchase",
                          "Ticket Net Proceeds": "Weekly Ticket Proceeds ($)",
                      },
                      )

        fig.update_layout(xaxis={'tickfont_size': 20, "gridcolor": "gainsboro"},
                          yaxis={'tickfont_size': 20, "gridcolor": "lightgray"},
                          xaxis_title=dict(font=dict(size=30)),
                          yaxis_title=dict(font=dict(size=30)),
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          legend=dict(font=dict(size=30)),
                          legend_title_text='')

        fig.update_traces(line=dict(width=5))
        fig.update_yaxes(range=[0, 6000],linecolor='black', linewidth=6)
        fig.update_xaxes(linecolor='black', linewidth=6, dtick=86400000.0*7) # Set x-axis by week

        fig.show()

    stacked_data = pivot_df.cumsum()


    # Cumulative Ticket Sales (including free tickets) over season
    if True:
        df_unstacked = stacked_data["Tickets in Order"].stack(level=0).reset_index()
        df_unstacked["Purchased"] = df_unstacked["Cash"] + df_unstacked["Ticketleap"]
        df_unstacked.drop(columns=["Cash", "Ticketleap"], inplace=True)
        df_long = df_unstacked.melt(id_vars=['Date of Purchase', 'Event'],
                                    var_name="Payment Type",
                                    value_name='Values')

        if False:

            df_long_sampled = df_long.sample(frac=0.2).sort_index() # Reduce points so dotted lines don't look janky

            # Calculate the the free tickets given away per period of time
            for concert in CONCERT_DATE:

                # Define time periods
                time_vector = pd.to_datetime(
                               [(CONCERT_DATE[concert]-pd.to_timedelta(60, unit='d')),  # Two months before
                               (CONCERT_DATE[concert] - pd.to_timedelta(30, unit='d')),  # One month before
                               (CONCERT_DATE[concert] - pd.to_timedelta(1, unit='w')),  # One week before
                               (CONCERT_DATE[concert]-pd.to_timedelta(1, unit='d')),  # One day before
                               CONCERT_DATE[concert]]) # Day of concert

                df_long_free = df_long[(df_long["Payment Type"] == "Free") & (df_long["Event"] == concert)] # Filter by concert and by Free status
                df_by_day_free = df_long_free.sort_values("Date of Purchase").drop_duplicates("Date of Purchase", keep="last") # Keep only the last row of every day

                # Find the closest already-happened date to the defined time periods
                df_total_free_tickets = pd.merge_asof(
                    pd.DataFrame({'target_date': time_vector}),  # Left side: your target dates
                    df_by_day_free,  # Right side: the DataFrame you're matching against
                    left_on='target_date',  # Column to match in target
                    right_on='Date of Purchase',  # Column to match in the DataFrame
                    direction='backward'  # Find the closest earlier date
                ).drop(["target_date"], axis=1)

                df_total_free_tickets["Diff Sold"] = (df_total_free_tickets["Values"] - df_total_free_tickets["Values"].shift(1)) # Find new tickets sold in each time period
                df_total_free_tickets["Diff Sold"].fillna(df_total_free_tickets["Values"], inplace=True) # Fill first new tickets sold cell with the total tickets sold
                df_total_free_tickets["Diff Sold (%)"] = (df_total_free_tickets["Diff Sold"]/df_total_free_tickets["Values"].max()*100).apply(lambda x: round(x, 0)) # Calculate the percentage of total tickets sold in each time period


                print(df_total_free_tickets)

            fig = px.line(df_long_sampled,
                          x="Date of Purchase",
                          y="Values",
                          color="Event",
                          line_dash="Payment Type",

                          category_orders = {"Payment Type":["Purchased", "Free"]},
                          labels={
                              "Date of Purchase": "Date of Purchase",
                              "Purchased": "Total Tickets Sold",
                          },
                          )


            fig.update_layout(xaxis={'tickfont_size': 20, "gridcolor": "gainsboro"},
                              yaxis={'tickfont_size': 20, "gridcolor": "lightgray"},
                              xaxis_title=dict(font=dict(size=30)),
                              yaxis_title=dict(font=dict(size=30)),
                              paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)',
                              legend=dict(font=dict(size=30)),
                              legend_title_text='')

            fig.update_traces(line=dict(width=5))
            fig.update_yaxes(range=[0, 550],linecolor='black', linewidth=6)
            fig.update_xaxes(linecolor='black', linewidth=6)
            line_styles = iter(['solid', 'dot', 'solid', 'dot'])
            for d in fig.data:
                d.line["dash"] =next(line_styles)
            fig.show()


    # Cumulative income over the season
    if False:
        df_unstacked_money = stacked_data["Ticket Net Proceeds"].stack(level=0).reset_index()
        df_unstacked_money["Purchased"] = df_unstacked_money["Cash"] + df_unstacked_money["Ticketleap"]
        df_unstacked_money.drop(columns=["Cash", "Ticketleap", "Free"], inplace=True)
        print(df_unstacked_money)
        fig = px.line(df_unstacked_money,
                      x="Date of Purchase",
                      y="Purchased",
                      color="Event",
                      labels={
                          "Date of Purchase": "Date of Purchase",
                          "Purchased": "Total Income ($)",
                      },

                      )

        fig.update_layout(xaxis={'tickfont_size': 20, "gridcolor": "gainsboro"},
                          yaxis={'tickfont_size': 20, "gridcolor": "lightgray"},
                          xaxis_title=dict(font=dict(size=30)),
                          yaxis_title=dict(font=dict(size=30)),
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          legend=dict(font=dict(size=30)),
                          legend_title_text='')

        fig.update_traces(line=dict(width=5))
        fig.update_yaxes(range=[0, 13000],linecolor='black', linewidth=6)
        fig.update_xaxes(linecolor='black', linewidth=6)
        fig.show()

        print(df_unstacked_money)


    # fig = px.line(df_unstacked, x="Index", y="Values", color="Payment Type", line_group=df_unstacked.groupby(['Payment Type', 'Event']).cumcount())
    # fig.show()
    #
    # print()
    #
    #
    # tickets_sold_df = stacked_data["Tickets in Order"]
    # for event in stacked_data.columns:
    #     fig = px.area(stacked_data_c, x="Date of Purchase", y="Total Tickets Sold", color="Event", line_group="Payment Type")
    #     fig.show()
    # fig.add_trace(go.Scatter(
    #         x=stacked_data.index,
    #         y=stacked_data[purchase_type],
    #         mode='lines',
    #         # stackgroup='one',  # Stack the traces
    #         name=purchase_type
    #     ))



    total_proceeds_df = stacked_data["Ticket Net Proceeds"]

    #print(tickets_sold_df)








    if False:

        grouped = df.groupby(["Date of Purchase",  "Event"])["Ticket Net Proceeds"].sum().reset_index()
        grouped_a = df.groupby(["Date of Purchase", "Event"])["Tickets in Order"].mean().reset_index()
        grouped_b = pd.concat([grouped, grouped_a["Tickets in Order"]], axis=1)
        #grouped["Total Earnings by Group"] = grouped.groupby("Event")["Ticket Net Proceeds"].cumsum()

        grouped_free = df["Payment Type" == "Free"].groupby(["Date of Purchase", "Event"])["Tickets in Order"].count().reset_index()
        pivot_df_free = grouped_free.pivot(index="Date of Purchase", columns=["Event", "Payment Type"], values="Tickets in Order")
        pivot_df_c = pivot_df_c.fillna(0)
        pivot_df_c = pivot_df_c.sort_index()


        pivot_df = grouped.pivot(index="Date of Purchase", columns="Event", values="Ticket Net Proceeds")

        pivot_df = pivot_df.fillna(0)
        pivot_df = pivot_df.sort_index()


        stacked_data_c = pivot_df_c.cumsum()
        print(px.data.gapminder())
        stacked_data = pivot_df.cumsum()
    # print(grouped)
    # fig = px.area(grouped,
    #               x="Date of Purchase",
    #               y="Total Earnings by Group",
    #               color='Event',
    #               line_group="Event",
    #               title='Total Sales by Purchase Type Over Time')

    # fig = px.area(stacked_data_c, x="Date of Purchase", y="Total Tickets Sold", color="Event", line_group="Payment Type")
    # fig.show()
    # fig = go.Figure()
    # for purchase_type in stacked_data_c.columns:
    #     fig.add_trace(go.Scatter(
    #         x=stacked_data.index,
    #         y=stacked_data[purchase_type],
    #         mode='lines',
    #         # stackgroup='one',  # Stack the traces
    #         name=purchase_type
    #     ))
    # fig.show()


    if False:
        fig = go.Figure()
        for concert_name in stacked_data.columns:
            fig.add_trace(go.Scatter(
                x=stacked_data.index,
                y=stacked_data[concert_name],
                mode='lines',
               # stackgroup='one',  # Stack the traces
                name=purchase_type
            ))
        fig.show()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
