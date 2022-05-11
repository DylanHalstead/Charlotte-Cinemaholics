from src.blueprints.movie_blueprint import scrape_poster, add_movie, get_rated_IDs
from src.models import Movie, User, UserRating
from imdb import Cinemagoer

def test_scrape_poster():
    pulp_fiction_url = scrape_poster('tt0110912')
    the_batman_url = scrape_poster('tt1877830')
    # this is the if for Pulp Fiction
    assert pulp_fiction_url == 'https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg'
    # this is the if for The Batman
    assert the_batman_url == 'https://m.media-amazon.com/images/M/MV5BMDdmMTBiNTYtMDIzNi00NGVlLWIzMDYtZTk3MTQ3NGQxZGEwXkEyXkFqcGdeQXVyMzMwOTU5MDk@._V1_.jpg'