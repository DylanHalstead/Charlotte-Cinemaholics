from flask import Blueprint, abort, redirect, render_template, request, session
from models import db
from datetime import datetime

from imdb import Cinemagoer
imdb = Cinemagoer()
import requests
from bs4 import BeautifulSoup
import json

router = Blueprint('movie_router', __name__, url_prefix='/movies')

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
# # Very slow to load all 250 url's, just grabbing first 25 for now
# for movie in range(25):
#     # Add poster to each film, format movieID with 'tt' in front
#     top_films[movie]['cover url'] = imdb_scrape_poster(f'tt{top_films[movie].movieID}')

popular_films = imdb.get_popular100_movies()
worst_films = imdb.get_bottom100_movies()
# Add when database is built
community_films = {}

# Routers
@router.get('/top-films')
def all_movies():
    return render_template('top_250.html', top_films=top_films)