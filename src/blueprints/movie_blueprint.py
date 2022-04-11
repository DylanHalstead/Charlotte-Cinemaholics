from flask import Blueprint, abort, redirect, render_template, request, session
from src.models import db, Movie
from datetime import datetime

from imdb import Cinemagoer
import requests
from bs4 import BeautifulSoup
import json

router = Blueprint('movie_router', __name__, url_prefix='/movies')

imdb = Cinemagoer()

# Function scrapes IMDb using IMDb ID 'tt0107290' to find movie's poser.
# Function modified and based on https://github.com/tomkeith/imdb-scraper
def imdb_scrape_poster(imdb_id):
    imdb_base_url = 'https://www.imdb.com/title/'
    # Main content - build URL, and soup content
    imdb_full_url = imdb_base_url + imdb_id
    r = requests.get(imdb_full_url).content
    soup = BeautifulSoup(r, 'html.parser')
    
    # Code from js section has json variables
    json_dict = json.loads( str( soup.findAll('script', {'type':'application/ld+json'})[0].text ))

    # Grab movie poster url
    imdb_img_url = json_dict['image']
    
    return imdb_img_url

# Pre-Load movie dictionairy
top_films = imdb.get_top250_movies()
popular_films = imdb.get_popular100_movies()
worst_films = imdb.get_bottom100_movies()
# Routers
@router.get('/top-films')
def all_movies():
    getTopMovies()
    return render_template('top_250.html', top_films=top_films)


def getTopMovies(): 
    for movie in range(25): # Very slow to load all 250 url's, just grabbing first 25 for now
        if movie not in Movie.query.all():
            # Add poster to each film, format movieID with 'tt' in front
            top_films[movie]['cover url'] = imdb_scrape_poster(f'tt{top_films[movie].movieID}')
            id = int(top_films[movie].movieID)
            top_25 = Movie(movie_id=id, poster_url=top_films[movie]['cover url'])
            db.session.add(top_25)
            db.session.commit()