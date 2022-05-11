from typing import List
from flask import Blueprint, abort, jsonify, redirect, render_template, request, session
from src.models import db, Movie, User, UserRating
import requests
from bs4 import BeautifulSoup
import json
from imdb import Cinemagoer

router = Blueprint('movie_router', __name__, url_prefix='/movies')

# Pre-Load imdb & movie lists
imdbpy = Cinemagoer()
top_films = imdbpy.get_top250_movies()
trending = imdbpy.get_popular100_movies()
worst_films = imdbpy.get_bottom100_movies()

# Scrapes IMDb using IMDb ID, like 'tt0107290', to find movie's poster.
# Function modified and based on https://github.com/tomkeith/imdb-scraper
def scrape_poster(imdb_id: str) -> str:
    # Build URL and soup content
    imdb_base_url = 'https://www.imdb.com/title/'
    imdb_full_url = imdb_base_url + imdb_id
    r = requests.get(imdb_full_url).content
    soup = BeautifulSoup(r, 'html.parser')

    # Grab JSON data
    json_dict = json.loads(str(soup.findAll('script', {'type':'application/ld+json'})[0].text))
    if 'image' not in json_dict:
        return '/static/unknown-film.jpg'
    imdb_img_url = json_dict['image']
    return imdb_img_url

# Take a movie from cinemagoer/imdbpy and import it into db 
def add_movie(movie) -> None: 
    # Make sure movie isn't arleady in db
    doesExist = len(Movie.query.filter_by(movie_id=movie.movieID).all())
    if doesExist == 0:
        movie = imdbpy.get_movie(movie.movieID)
        poster_url = scrape_poster(f'tt{movie.movieID}')
        # Grab longer, user review if it exists
        if 'plot' in movie:
            if len(movie['plot']) > 1:
                about = movie['plot'][1][:movie['plot'][1].find('::')]
            else:
                about = movie['plot'][0]
        else:
            about = ''
        
        if 'director' in movie:
            director = movie['director'][0]['name']
        else:
            director = 'Not Known'

        if 'rating' in movie:
            imdb_rating = movie['rating']
        else:
            imdb_rating = 0
        if 'votes' in movie:
            imdb_votes = movie['votes']
        else:
            imdb_votes = 0

        movie = Movie(movie_id=movie.movieID, title=movie['title'], director=director, about=about, poster_url=poster_url, imdb_rating=imdb_rating, imdb_votes=imdb_votes)
        db.session.add(movie)
        db.session.commit()

# Routers
@router.get('/')
def all_movies():
    ratedMovies = get_rated_IDs()
    return render_template('all_movies.html', ratedMovies=ratedMovies)

@router.get('/<movie_id>')
def movie_page(movie_id):
    single_movie = imdbpy.get_movie(movie_id)
    add_movie(single_movie)
    single_movie = Movie.query.get_or_404(movie_id).to_dict()
    return render_template('movie.html', single_movie=single_movie)

@router.post('/<movie_id>')
def post_rating(movie_id):
    # Grab and check rating from user
    if 'user' in session:
        user_rating = float(request.form.get('rating', -1))
        if user_rating < 0 or user_rating > 10:
            abort(400)

        # Add review to user_rating table
        reviee = User.query.get_or_404(session['user']['user_id'])
        movie = Movie.query.get_or_404(movie_id)
        new_review = UserRating(movie_rating=user_rating)
        new_review.user = reviee
        new_review.movie = movie
        movie.user_rating.append(new_review)
        db.session.add(new_review)
        db.session.commit()
        return redirect(f'/movies/{movie_id}')
    else:
        return abort(403)

@router.post('/search')
def search_movie():
    searched = request.form.get('search')
    movies = imdbpy.search_movie(searched)
    for movie in range(10):
        add_movie(movies[movie])
        movies[movie] = Movie.query.get_or_404(movies[movie].movieID).to_dict()
    ratedMovies = get_rated_IDs()
    return render_template('search.html', searched=searched, movies = movies, ratedMovies=ratedMovies)

@router.post('/<movie_id>/watchlist')
def watchlisting(movie_id):
    if 'user' in session:
        user = User.query.get_or_404(session['user']['user_id'])
        movie = Movie.query.get_or_404(movie_id)
        # Check to see if user is adding or removing from his watchlist
        if(movie not in user.watchlistMovies):
            user.watchlistMovies.append(movie)
        else:
            user.watchlistMovies.remove(movie)
        db.session.commit()
        return redirect(f'/filter/watchlist')
    return abort(403)

# JSON
@router.get('/top-250')
def get_top_movies():
    for movie in range(len(top_films)):
        if not isinstance(top_films[movie], dict):
            add_movie(top_films[movie])
            top_films[movie] = Movie.query.get_or_404(top_films[movie].movieID).to_dict()
        else:
            top_films[movie] = Movie.query.get_or_404(top_films[movie]['movie_id']).to_dict()
    return jsonify(top_films)

@router.get('/bottom-100')
def get_worst_movies():
    for movie in range(len(worst_films)):
        if not isinstance(worst_films[movie], dict):
            add_movie(worst_films[movie])
            worst_films[movie] = Movie.query.get_or_404(worst_films[movie].movieID).to_dict()
        else:
            worst_films[movie] = Movie.query.get_or_404(worst_films[movie]['movie_id']).to_dict()
    return jsonify(worst_films)

@router.get('/trending')
def get_trending_movies():
    for movie in range(len(trending)):
        if not isinstance(trending[movie], dict):
            add_movie(trending[movie])
            trending[movie] = Movie.query.get_or_404(trending[movie].movieID).to_dict()
        else:
            trending[movie] = Movie.query.get_or_404(trending[movie]['movie_id']).to_dict()
    return jsonify(trending)

# Used for checking if user has rated film, returns the movie ID of user rated films
def get_rated_IDs() -> List[str]:
    ratedFilms = []
    if 'user' in session:
        user = User.query.get_or_404(session['user']['user_id'])
        for rating in user.movie_rating:
            ratedFilms.append(rating.movie_id)
    return ratedFilms