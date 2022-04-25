from ctypes.wintypes import PWIN32_FIND_DATAA
from flask import Blueprint, abort, redirect, render_template, request, session
from src.models import db, Movie
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
from imdb import Cinemagoer

router = Blueprint('movie_router', __name__, url_prefix='/movies')

# Pre-Load imdb & popular movie dictionairy
imdbpy = Cinemagoer()
top_films = imdbpy.get_top250_movies()
popular_films = imdbpy.get_popular100_movies()
worst_films = imdbpy.get_bottom100_movies()

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

# Routers
@router.get('/top-films')
def all_movies():
    parseMovieDict(top_films)
    return render_template('top_250.html', top_films=top_films)


def parseMovieDict(movieDict): 
    print('Grabbing films, this can take a while')
    for movie in movieDict: # Very slow to load all 250 url's, just grabbing first 25 for now
        print(movie.movieID)
        if len(Movie.query.filter_by(movie_id=movie.movieID).all()) == 0:
            # Add poster to each film, format movieID with 'tt' in front
            movie['cover url'] = imdb_scrape_poster(f'tt{movie.movieID}')
            id = int(movie.movieID)
            top_25 = Movie(movie_id=id, poster_url=movie['cover url'])
            db.session.add(top_25)
            db.session.commit()
        else:
            movie['cover url'] = Movie.query.filter_by(movie_id=movie.movieID).first().poster_url

@router.post('/search/')
def search_movie():
    searched = request.form.get('search')
    movies = imdbpy.search_movie(searched)
    parseMovieDict(movies)
    return render_template('search.html', searched=searched, movies = movies)