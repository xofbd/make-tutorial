import json
import os
from unittest.mock import patch

import pytest

from src.film_color import search_film_ids

DATA_DIR = os.path.join('tests', 'data')


@pytest.fixture
def mock_get():
    """Fixture that mocks requests.get that returns a JSON."""
    with patch('src.film_color.requests.get') as mock_get:
        with open(os.path.join(DATA_DIR, 'search_response.json'), 'r') as f:
            mock_get.return_value.json.return_value = json.load(f)
        yield mock_get


def test_search_film_ids(mock_get):
    """
    GIVEN a search term of Little Women
    WHEN the search_film_ids is called which uses the IMDB API
    THEN four titles IDs are returned
    """
    title_ids = search_film_ids('Little Women')

    assert title_ids == ['tt3281548', 'tt0110367', 'tt6853528', 'tt0041594']
    mock_get.assert_called_once()
