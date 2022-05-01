from flask import Blueprint, abort, redirect, render_template, request, session
from src.models import db, Movie, User, UserRating
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
from imdb import Cinemagoer
import unicodedata

router = Blueprint('movie_router', __name__, url_prefix='/movies')

# Pre-Load imdb & movie lists
imdbpy = Cinemagoer()
top_films = imdbpy.get_top250_movies()
popular_films = imdbpy.get_popular100_movies()
worst_films = imdbpy.get_bottom100_movies()

# Function scrapes IMDb using IMDb ID 'tt0107290' to find movie's poser.
# Function modified and based on https://github.com/tomkeith/imdb-scraper
def scrape_poster(imdb_id):
    # build URL and soup content
    imdb_base_url = 'https://www.imdb.com/title/'
    imdb_full_url = imdb_base_url + imdb_id
    r = requests.get(imdb_full_url).content
    soup = BeautifulSoup(r, 'html.parser')

    # Grab JSON data
    json_dict = json.loads( str( soup.findAll('script', {'type':'application/ld+json'})[0].text ))
    imdb_img_url = json_dict['image']
    
    return imdb_img_url

# Take a movie from cinemagoer and import it into db 
def addMovie(movie): 
    # Make sure movie isn't arleady in db
    if len(Movie.query.filter_by(movie_id=movie.movieID).all()) == 0:
        movie = imdbpy.get_movie(movie.movieID)
        poster_url = scrape_poster(f'tt{movie.movieID}')
        # Grab longer, user review if it exists
        if len(movie['plot']) > 1:
            about = movie['plot'][1][:movie['plot'][1].find('::')]
        else:
            about = movie['plot'][0]
        
        if 'director' in movie:
            director = ascii(movie['director'][0]['name'])
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

        movie = Movie(movie_id=movie.movieID, title=movie['title'], director=director, about=about, poster_url=poster_url, imdb_rating=imdb_rating, imdb_votes=imdb_votes, uncc_rating=0, uncc_votes=0)
        print(movie)
        db.session.add(movie)
        db.session.commit()

# Grabs votes and review average from list of ratings for specific movie
def grabUNCCRatings(movieRatings):
    total_ratings = 0
    rating_sum = 0
    for rating in movieRatings:
        total_ratings += 1
        rating_sum += rating.movie_rating
    rating_average = rating_sum/total_ratings
    rating_info = {
        'votes': total_ratings,
        'average': rating_average
    }
    return rating_info

# Routers
@router.get('/top-films')
def all_movies():
    # Grab all films
    for movie in range(len(top_films)):
        if not isinstance(movie, dict):
            addMovie(top_films[movie])
            top_films[movie] = Movie.query.filter_by(movie_id=top_films[movie].movieID).first().to_dict()
    for movie in range(len(popular_films)):
        if not isinstance(movie, dict):
            addMovie(popular_films[movie])
            popular_films[movie] = Movie.query.filter_by(movie_id=popular_films[movie].movieID).first().to_dict()
    for movie in range(len(worst_films)):
        if not isinstance(movie, dict):
            addMovie(worst_films[movie])
            worst_films[movie] = Movie.query.filter_by(movie_id=worst_films[movie].movieID).first().to_dict()
    print(top_films[0]['poster_url'])
    return render_template('top_250.html', top_films=top_films)

@router.get('/<movie_id>')
def movie_page(movie_id):
    single_movie = imdbpy.get_movie(movie_id)
    addMovie(single_movie)
    single_movie = Movie.query.filter_by(movie_id=movie_id).first().to_dict()
    return render_template('movie.html', single_movie=single_movie)

@router.post('/<movie_id>')
def post_rating(movie_id):
    user_rating = float(request.form.get('rating', -1))
    if user_rating == -1:
        abort(400)

    # Add review to user_rating table
    reviee = User.query.filter_by(user_id=session['user']['user_id']).first()
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    new_review = UserRating(movie_rating=user_rating)
    new_review.user = reviee
    new_review.movie = movie
    movie.user_rating.append(new_review)
    db.session.add(new_review)
    uncc_info = grabUNCCRatings(UserRating.query.filter_by(movie_id=movie_id).all())
    movie.uncc_rating = uncc_info['average']
    movie.uncc_votes = uncc_info['votes']
    db.session.commit()
    return redirect(f'/movies/{movie_id}')

@router.post('/search')
def search_movie():
    searched = request.form.get('search')
    movies = imdbpy.search_movie(searched)
    for movie in movies:
        addMovie(movie)
        movie = Movie.query.filter_by(movie_id=movie.movieID).first().to_dict()
    return render_template('search.html', searched=searched, movies = movies)
