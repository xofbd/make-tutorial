"""
Scrape Wikipedia article of Academy Award nominees for Best Picture.
"""
import os

import pandas as pd


def get_nominees_per_year(df):
    """Return data frame of movie title and year."""
    year = df['Year'].str.extract(r'(\d{4})')
    df['Year'] = year

    # Some tables use "film" while others use "films"
    if 'Films' in df.columns:
        df = df.rename({'Films': 'Film'}, axis=1)

    return df.dropna()[['Year', 'Film']]


def main(url, path_csv):
    """Create CSV file of Oscar Best Picture nominees across the year."""
    df_tables = pd.read_html(url)[2:10]  # all films before 2000
    df_all = pd.concat([get_nominees_per_year(df) for df in df_tables])

    df_all.to_csv(path_csv, index=False)


if __name__ == '__main__':
    import sys

    path_csv = sys.argv[1]
    url = 'https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture'
    main(url, path_csv)
