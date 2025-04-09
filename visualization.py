import plotly.express as px
import plotly.graph_objects as go

class TicketVisualizer:
    """Class for creating visualizations of ticket sales data."""
    def __init__(self):
        """Initialize the visualizer."""
        self.layout_settings = {
            'xaxis': {'tickfont_size': 20, "gridcolor": "gainsboro"},
            'yaxis': {'tickfont_size': 20, "gridcolor": "lightgray"},
            'xaxis_title': dict(font=dict(size=30)),
            'yaxis_title': dict(font=dict(size=30)),
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'legend': dict(font=dict(size=30)),
            'legend_title_text': ''
            }


    def plot_pwyc_by_source(self, heard_about_df):
        heard_about_df_PWYC = heard_about_df[
            heard_about_df["Ticket Type"] == "Pay What You Can"
        ].sort_values("Average Ticket Price", ascending=False)

        fig = px.bar(
            heard_about_df_PWYC,
            x="How did you hear about this event? (Buyer)",
            y="Average Ticket Price",
            labels={
                 "How did you hear about this event? (Buyer)": "How did you hear about this event?",
            },
            )


        tick_labels = {"Word of Mouth": "Word of Mouth",
                       "Social Media": "Social Media",
                       "Other": "Other",
                       "Online Events Calendar (The Boston Calendar, ArtsBoston, etc.)": "Events Calendar",
                       "Previous BFO Event": "Previous BFO Event",
                       "BFO Newsletter": "BFO Newsletter",
                       "Flyer/Poster": "Flyer",
                       "Advertisement": "Advertisement",
                       "Newspaper": "Newspaper"
        }
        tick_vals = list(tick_labels.keys())
        tick_text = list(tick_labels.values())

        fig.update_layout(**self.layout_settings,
                          xaxis_tickangle=45,
                          xaxis_tickvals=tick_vals,
                          xaxis_ticktext=tick_text,
                          yaxis_tickprefix='$',
                          yaxis_tickformat=',.2f',  # Set to dollars
                          )

        return fig

    def plot_by_source(self, heard_about_df):
        fig = px.bar(heard_about_df,
                     x="How did you hear about this event? (Buyer)",
                     y="Order ID",
                     color="Ticket Type",
                     barmode="group",
                     labels={
                         "How did you hear about this event? (Buyer)": "How did you hear about this event?",
                         "Order ID": "Total Number of Tickets",
                     },
                     )

        tick_labels = {"Word of Mouth": "Word of Mouth",
                       "Social Media": "Social Media",
                       "Other": "Other",
                       "Online Events Calendar (The Boston Calendar, ArtsBoston, etc.)": "Events Calendar",
                       "Previous BFO Event": "Previous BFO Event",
                       "BFO Newsletter": "BFO Newsletter",
                       "Flyer/Poster": "Flyer",
                       "Advertisement": "Advertisement",
                       "Newspaper": "Newspaper"
        }
        tick_vals = list(tick_labels.keys())
        tick_text = list(tick_labels.values())

        fig.update_layout(
            **self.layout_settings,
                          xaxis_tickvals=tick_vals,
                          xaxis_ticktext=tick_text,
                          )

        return fig

    def plot_by_city(self, city_df_top):
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

        fig.update_layout(**self.layout_settings)

        return fig

    def plot_orders_on_map(self, zip_orders_df, geojson,exclude_pwyc=True):

        fig = go.Figure()

        all_guests_df = {"All Guests": zip_orders_df}
        paying_guests_df = {"Paying Guests": zip_orders_df[zip_orders_df["Ticket Type"] != "Pay What You Can"]}
        pwyc_guests_df = {"Pay-What-You-Can Guests": zip_orders_df[zip_orders_df["Ticket Type"] == "Pay What You Can"]}
        menu_data_dict = {**all_guests_df, **paying_guests_df, **pwyc_guests_df}

        menu_list = []
        j = 0
        for category, df in menu_data_dict.items():

            fig.add_trace(go.Choroplethmapbox(
                geojson=geojson,
                locations=df["Buyer Postal Code"],
                z=df["count"],
                colorscale="Viridis",
                zmin=0,
                zmax=df["count"].max(),
                featureidkey="properties.ZCTA5CE10",
                marker_opacity=0.5,
                marker_line_width=0,
            )
            )
            menu_list.append(dict(label=category,
                         method="update",
                         args=[{"visible": [True if i == j else False for i in range(len(menu_data_dict))]}]),
                             )


            j+=1


        fig.update_layout(mapbox_style="carto-positron",
                          mapbox_zoom=8,
                          mapbox_center={"lat": 42.363075, "lon": -71.058690},
                          margin={"r": 0, "t": 0, "l": 0, "b": 0})

        fig.update_layout(
            updatemenus=[
                dict(buttons=menu_list,
                    direction="down"
                         )
                ]
        )


        return fig

    def plot_weekly(self, weekly_df):


        fig = px.line(weekly_df,
                      x="Date of Purchase",
                      y="Ticket Net Proceeds",
                      color="Event",

                      labels={
                          "Date of Purchase": "Date of Purchase",
                          "Ticket Net Proceeds": "Weekly Ticket Proceeds ($)",
                      },
                      )

        fig.update_layout(**self.layout_settings)
        fig.update_traces(line=dict(width=5))
        fig.update_yaxes(range=[0, 6000], linecolor='black', linewidth=6)
        fig.update_xaxes(linecolor='black', linewidth=6, dtick=86400000.0 * 7)  # Set x-axis by week

        return fig

    def plot_cumulative_sales(self, df_cumulative):
        df_sampled = df_cumulative.sample(frac=0.2).sort_index()  # Reduce points so dotted lines don't look janky
        fig = px.line(df_sampled,
                      x="Date of Purchase",
                      y="Values",
                      color="Event",
                      line_dash="Payment Type",
                      category_orders={"Payment Type": ["Purchased", "Free"]},
                      labels={
                          "Date of Purchase": "Date of Purchase",
                          "Purchased": "Total Tickets Sold",
                      },
                      )

        fig.update_layout(**self.layout_settings)
        fig.update_traces(line=dict(width=5))
        fig.update_yaxes(range=[0, 550], linecolor='black', linewidth=6)
        fig.update_xaxes(linecolor='black', linewidth=6)

        # Set line styles alternating between solid and dotted
        line_styles = ['solid', 'dot', 'solid', 'dot']
        for i, d in enumerate(fig.data):
            d.line["dash"] = line_styles[i % len(line_styles)]

        return fig

    def plot_cumulative_income(self, cumulative_income_df):
        # Cumulative income over the season
        fig = px.line(cumulative_income_df,
                      x="Date of Purchase",
                      y="Purchased",
                      color="Event",
                      labels={
                          "Date of Purchase": "Date of Purchase",
                          "Purchased": "Total Income ($)",
                      },

                      )

        fig.update_layout(**self.layout_settings)

        fig.update_traces(line=dict(width=5))
        fig.update_yaxes(range=[0, 13000], linecolor='black', linewidth=6)
        fig.update_xaxes(linecolor='black', linewidth=6)

        return fig