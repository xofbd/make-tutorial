import os
import shutil

from dotenv import load_dotenv
import pandas as pd
import requests

load_dotenv()

API_KEY = os.getenv('API_KEY')

URL_BASE = "https://imdb-internet-movie-database-unofficial.p.rapidapi.com"
URL_SEARCH = URL_BASE + '/search/{}'
URL_FILM = URL_BASE + '/film/{}'

SLEEP_DURATION = 0
HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com"
}


def get_color_data(title, year, tol=2, verbose=True):
    """
    Return color data of the film, if available.

    Because several movies may share the same title, we need to check that the
    recorded date if only off by some tolerance.
    """
    if verbose:
        print(f"Processing {title} ({year})")

    time.sleep(SLEEP_DURATION)
    title_ids = search_film_ids(title)
    if title_ids is None:
        return None

    data_titles = [get_film_data(title_id) for title_id in title_ids]

    try:
        return [d['color'] for d in data_titles
                if d['year'] and abs(int(d['year']) - year) < tol][0]
    except IndexError:
        return None


def search_film_ids(title):
    """Return ids of all titles of a given name."""
    response = requests.get(URL_SEARCH.format(title), headers=HEADERS)

    if response.ok:
        return [title['id'] for title in response.json()['titles']]
    else:
        return None


def get_film_data(title_id):
    """Return color and year data for a given IMDB title ID."""
    response = requests.get(URL_FILM.format(title_id), headers=HEADERS)

    if response.ok:
        data = response.json()
        return {
            'year': data['year'],
            'color': dict(data['technical_specs']).get('Color')
        }
    else:
        return None


def simulate(path_output):
    """
    Simulate calling the API for the creation of the output file.

    The output file is created by simply copying over a file to the output
    path.
    """

    shutil.copyfile('.film_color_data.csv', path_output)


def main(path_input, path_output):
    df = pd.read_csv(path_input)
    color = [get_color_data(row.Film, row.Year) for row in df.itertuples()]

    df['Color'] = color
    df.to_csv(path_output, index=False)


if __name__ == '__main__':
    import argparse
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument('path_input', help='Path to input file')
    parser.add_argument('path_output', help='Path to output file')
    parser.add_argument('--simulate',
                        default=False,
                        action='store_true',
                        help='Whether to simulate the creation of the file')
    args = parser.parse_args()

    if args.simulate or API_KEY is None:
        simulate(args.path_output)
    else:
        t_0 = time.time()
        main(args.path_input, args.path_output)
        t_elapsed = time.time() - t_0
        print(f"Elapsed time: {t_elapsed :g} seconds")
