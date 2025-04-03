import argparse
import os
from data_loader import TicketDataLoader
from data_analysis import TicketAnalyzer
from visualization import TicketVisualizer
from config import DATA_PATH_2024, DATA_PATH_2025 #MASS_ZIP_CODE_URL, NY_ZIPCODE_URL
from utils import  save_figure, save_dataframe

def parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description="Analyze ticket sales data.")

    parser.add_argument('--data', type=str, default=DATA_PATH_2025,#'S4 Ticket Data COMPLETE.csv',
                        help='Path to the ticket data CSV file')
    parser.add_argument('--output-dir', type=str, default='output',
                        help='Directory to save output files')
    parser.add_argument('--figures-dir', type=str, default='figures',
                        help='Directory to save figures')
    parser.add_argument('--analyses', type=str, nargs='+',
                        default=['all'],
                        choices=['all', 'source', 'city', 'order_map', 'weekly', 'cumulative', 'cum_income'],
                        help='Analyses to run')
    parser.add_argument('--show-plots', action='store_true',
                        help='Show plots interactively')
    parser.add_argument('--save-plots', action='store_true',
                        help='Save plots to files')
    parser.add_argument('--plot-format', type=str, default='html',
                        choices=['html','png','json'],
                        help='Format to save plots')
    return parser.parse_args()


def main():

    args = parse_args()

    # Create output directors if they don't exist
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.figures_dir, exist_ok=True)

    # Initialize the data loader and load data
    print(f"Loading data from {args.data}...")
    loader = TicketDataLoader(args.data)
    data = loader.clean_data()
    print(f"Loaded {len(data)} records")

    # Initialize analyzer and visualizer
    analyzer = TicketAnalyzer(data)
    visualizer = TicketVisualizer()

    # Determine which analyses to run
    analyses_to_run = args.analyses
    run_all = "all" in analyses_to_run

    if run_all or "source" in analyses_to_run:
        print('\nAnalyzing ticket sources...')
        heard_about_df = analyzer.analyze_by_source()
        save_dataframe(heard_about_df, 'source_analysis.csv', args.output_dir)

        # Create visualizations for where people found out about BFO analysis
        pwyc_source_fig = visualizer.plot_pwyc_by_source(heard_about_df)
        source_fig = visualizer.plot_by_source(heard_about_df)

        if args.save_plots:
            save_figure(pwyc_source_fig, 'pwyc_by_source', args.figures_dir, args.plot_format)
            save_figure(source_fig, 'by_source', args.figures_dir, args.plot_format)

        if args.show_plots:
            pwyc_source_fig.show()
            source_fig.show()

    if run_all or "city" in analyses_to_run:
        print('\nAnalyzing ticket sales by city...')
        city_df_top = analyzer.analyze_by_city(select_top=10)
        save_dataframe(city_df_top, 'city_analysis.csv', args.output_dir)

        # Create visualizations for city analysis
        city_fig = visualizer.plot_by_city(city_df_top)


        if args.save_plots:
            save_figure(city_fig,'by_city', args.figures_dir, args.plot_format)

        if args.show_plots:
            city_fig.show()


    if run_all or "order_map" in analyses_to_run:
        print('\nAnalyzing ticket sales by zip code...')
        zip_orders_df = analyzer.analyze_zipcode_map(exclude_pwyc=True)
        save_dataframe(zip_orders_df,'zipcode_analysis_map.csv', args.output_dir)

        # Load geographic data
        state_list = ["MA",
                      "NY",
                      "VT",
                      "NH",
                      "ME",
                      "CT",
                      "RI",
                      "NJ"]

        dcombined_geojson = loader.combine_geo_data(state_list)

        #combined_geojson = loader.load_and_combine(state_list)

        zip_order_fig = visualizer.plot_orders_on_map(zip_orders_df, dcombined_geojson)

        if args.save_plots:
            save_figure(zip_order_fig, 'tickets_by_zipcode_map', args.figures_dir, args.plot_format)

        if args.show_plots:
            zip_order_fig.show()

    if run_all or "weekly" in analyses_to_run:
        print('\nAnalyzing ticket sales by week...')
        weekly_df = analyzer.analyze_weekly()
        save_dataframe(weekly_df, 'weekly_proceeds.csv', args.output_dir)

        weekly_fig = visualizer.plot_weekly(weekly_df)

        if args.save_plots:
            save_figure(weekly_fig, 'weekly_proceeds', args.figures_dir, args.plot_format)

        if args.show_plots:
            weekly_fig.show()

    if run_all or "cumulative" in analyses_to_run:
        print('\nAnalyzing cumulative ticket sales...')
        cumulative_df, timing_stats = analyzer.analyze_cumulative_sales(loader.concert_dates)
        save_dataframe(cumulative_df, 'weekly_proceeds.csv', args.output_dir)

        cumulative_fig = visualizer.plot_cumulative_sales(cumulative_df)


        if args.save_plots:
            save_figure(cumulative_fig, 'cumulative_sales', args.figures_dir, args.plot_format)

        if args.show_plots:
            cumulative_fig.show()

    if run_all or "cum_income" in analyses_to_run:
        print('\nAnalyzing cumulative income...')
        cumulative_income_df = analyzer.analyze_cumulative_income(loader.concert_dates)
        save_dataframe(cumulative_income_df, 'cumulative_income.csv', args.output_dir)

        cum_income_fig = visualizer.plot_cumulative_income(cumulative_income_df)

        if args.save_plots:
            save_figure(cum_income_fig, 'cumulative_income', args.figures_dir, args.plot_format)

        if args.show_plots:
            cum_income_fig.show()


if __name__ == '__main__':

    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/