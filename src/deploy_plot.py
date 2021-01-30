"""
Deploy plot of the fraction of color movies for each year of data available.
"""
from bokeh.plotting import figure, show

from color_films_by_year import count_color_data


def main(path_data):
    pct_series = count_color_data(path_data)

    p = figure(title='Percentage of color movies through the years',
               x_axis_label='Year',
               y_axis_label='Percentage')
    p.line(pct_series.index, pct_series.values, line_width=2)

    show(p)


if __name__ == '__main__':
    import sys

    path_data = sys.argv[1]
    main(path_data)
