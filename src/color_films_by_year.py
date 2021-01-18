"""
Create figure of the fraction of color movies for each year of data available.
"""
import matplotlib.pyplot as plt
import pandas as pd


def count_color_data(path_data):
    """Return data frame of color type per year."""
    df = pd.read_csv(path_data).dropna()
    ind_color = df['Color'].str.contains('Color')
    ind_b_and_w = df['Color'].str.contains('Black and White')

    df['color_cleaned'] = None
    df.loc[ind_color, 'color_cleaned'] = 'Color'
    df.loc[ind_b_and_w & ~ind_color, 'color_cleaned'] = 'Black and White'

    denom = df.dropna()['Year'].value_counts()
    num = df.query('color_cleaned == "Color"')['Year'].value_counts()

    return 100 * (num / denom).fillna(0).rename('ratio')


def create_figure(data, path_figure):
    """Create figure of percentage of black and white movies for each year."""

    plt.plot(data, '-o')
    plt.hlines(50, data.index.min(), data.index.max(),
               color='red',
               linestyles='dashed')
    plt.xlabel('Year')
    plt.ylabel('Percentage')
    plt.savefig(path_figure, dpi=600)


def main(path_data, path_figure):
    pct_series = count_color_data(path_data)
    create_figure(pct_series, path_figure)


if __name__ == '__main__':
    import sys

    path_data = sys.argv[1]
    path_figure = sys.argv[2]
    main(path_data, path_figure)
