from src.models import * 

def test_user_model():
    test_user = User(user_id=1, username='Test', email='dhalstea@uncc.edu', passkey='password123', pfp='defaultuser.png')
    assert test_user.username == 'Test'
    assert test_user.email == 'dhalstea@uncc.edu'
    assert test_user.passkey == 'password123'
    assert test_user.pfp == 'defaultuser.png'
    assert test_user.about == None

    test_user.username = 'NewTest'
    test_user.email = 'dillybags@uncc.edu'
    test_user.passkey = 'passkey1234'
    test_user.pfp = 'epicpic.jpg'
    test_user.about = 'This is an about.'
    assert test_user.username == 'NewTest'
    assert test_user.email == 'dillybags@uncc.edu'
    assert test_user.passkey == 'passkey1234'
    assert test_user.pfp == 'epicpic.jpg'
    assert test_user.about == 'This is an about.'
    assert test_user.about == 'This is an about.'

def test_admin_model():
    assert(True)

def test_movie_model():
    test_movie = Movie(movie_id='0029364', title='Shawshank Titration', director='Brayden Pitts', about='2018 extra credit for MHS Chemestry', poster_url='testurl.com', imdb_rating=9.4, imdb_votes=93237)
    assert test_movie.movie_id == '0029364'
    assert test_movie.title == 'Shawshank Titration'
    assert test_movie.director == 'Brayden Pitts'
    assert test_movie.about == '2018 extra credit for MHS Chemestry'
    assert test_movie.poster_url == 'testurl.com'
    assert test_movie.imdb_rating == 9.4
    assert test_movie.imdb_votes == 93237

def test_user_rating_model():
    test_user = User(user_id=1, username='Test', email='dhalstea@uncc.edu', passkey='password123', pfp='defaultuser.png')
    test_movie = Movie(movie_id='0029364', title='Shawshank Titration', director='Brayden Pitts', about='2018 extra credit for MHS Chemestry', poster_url='testurl.com', imdb_rating=9.4, imdb_votes=93237)
    test_user_rating = UserRating(movie_rating=8.2)
    test_user_rating.user = test_user
    test_user_rating.movie = test_movie
    assert test_user_rating.movie == test_movie
    assert test_user_rating.user == test_user
    assert test_user_rating.movie_rating == 8.2



def test_watchlist_model():
    assert(True)

# Encomposes likes & edits
def test_post_model():
    assert(True)

# Encomposes likes, qu & edits
def test_reply_model():
    assert(True)

