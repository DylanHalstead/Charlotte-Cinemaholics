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

def test_post_model():
    test_post = Post(title="Title", user_id=1, body="Body", post_time = '2021-05-01 12:00:00')
    assert test_post.title == "Title"
    assert test_post.user_id == 1
    assert test_post.body == "Body"
    assert test_post.post_time == '2021-05-01 12:00:00'


def test_reply_model():
    test_post = Reply(user_id=1, body="Body", post_time = '2021-05-01 12:00:00', post_id = 1)
    assert test_post.user_id == 1
    assert test_post.body == "Body"
    assert test_post.post_time == '2021-05-01 12:00:00'
    assert test_post.post_id == 1

def test_post_like_model():
    test_post = Post(title="Title", user_id=1, body="Body", post_time = '2021-05-01 12:00:00')
    test_user = User(email="test123@uncc.edu", username="test", passkey="12345", pfp="default_user.png")
    like = PostLike(user_id=test_user.user_id, post_id=test_post.post_id)
    assert like.user_id == test_user.user_id
    assert like.post_id == test_post.post_id

def test_reply_like_model():
    test_reply = Reply(user_id=1, body="Body", post_time = '2021-05-01 12:00:00', post_id = 1)
    test_user = User(email="test123@uncc.edu", username="test", passkey="12345", pfp="default_user.png")
    like = ReplyLike(user_id=test_user.user_id, reply_id=test_reply.reply_id)
    assert like.user_id == test_user.user_id
    assert like.reply_id == test_reply.reply_id

def test_reply_quote_model():
    test_post = Post(title="Title", user_id=1, body="Body", post_time = '2021-05-01 12:00:00')
    test_reply = Reply(user_id=1, body="Body", post_time = '2021-05-01 12:00:00', post_id = 1)
    quote_reply = Reply(user_id=1, body="Body", post_time = '2021-05-01 12:00:00', post_id = 1)
    quote = Reply_Quote(reply_id = quote_reply.reply_id, parent_id = test_reply.reply_id)
    assert quote.reply_id == quote_reply.reply_id
    assert quote.parent_id == test_reply.reply_id

def test_post_edit_model():
    test_post = Post(title="Title", user_id=1, body="Body", post_time = '2021-05-01 12:00:00')
    edit = Edits(user_id = test_post.user_id,post_id = test_post.post_id, reply_id = None, reason = "Typo", time = '2021-05-02 12:00:00')
    assert edit.user_id == test_post.user_id
    assert edit.post_id == test_post.post_id
    assert edit.reply_id == None
    assert edit.reason == "Typo"
    assert edit.time == '2021-05-02 12:00:00'

def test_reply_edit_model():
    test_reply = Reply(user_id=1, body="Body", post_time = '2021-05-01 12:00:00', post_id = 1)
    edit = Edits(user_id = test_reply.user_id,post_id = test_reply.post_id, reply_id = test_reply.reply_id, reason = "Typo", time = '2021-05-02 12:00:00')
    assert edit.user_id == test_reply.user_id
    assert edit.post_id == test_reply.post_id
    assert edit.reply_id == test_reply.reply_id
    assert edit.reason == "Typo"
    assert edit.time == '2021-05-02 12:00:00'