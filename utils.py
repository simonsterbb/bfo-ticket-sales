import pandas as pd
import os
import json

def ensure_dir_exists(directory):
    """Ensure that a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_figure(fig, filename, directory='figures', format='html'):
    ensure_dir_exists(directory)
    file_path = os.path.join(directory, filename)
    # To fix .png: https://community.plotly.com/t/static-image-export-hangs-using-kaleido/61519/3
    if format =='html':
        fig.write_html(f"{file_path}.html")
        print(f"Saved figure to {file_path}.html")
    elif format.lower() == 'png':
        fig.write_image(f"{file_path}",format='png')
        print(f"Saved figure to {file_path}.png")
    elif format.lower() == 'json':
        with open(f"{file_path}.json", 'w') as f:
            f.write(json.dumps(fig.to_dict()))
        print(f"Saved figure data to {file_path}.json")
    else:
        raise ValueError(f"Unsupported format: {format}")

def save_dataframe(df, filename,directory='output'):
    ensure_dir_exists(directory)
    file_path = os.path.join(directory, filename)
    df.to_csv(file_path, index=False)
    print(f'Saved dataframe to {file_path}')

def print_analysis_summary(data_dict, title="Analysis Summary"):
    """Print a formatted summary of analysis results."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)