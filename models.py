from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    body = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, nullable = False)
    

    def __repr__(self):
        return f'Post({self.post_id}, {self.title}, {self.user_id}, {self.body}, {self.time}, {self.likes})'

class Reply(db.Model):
    __tablename__ = 'reply'
    reply_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id')) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    body = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, nullable = False)
    

    def __repr__(self):
        return f'Reply({self.reply_id}, {self.post_id}, {self.user_id}, {self.body}, {self.time}, {self.likes})'


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    pfp = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=True)
    rated_id = db.Column(db.Integer, db.ForeignKey('rated_films.rated_id')) 
    watchlist_id = db.Column(db.Integer, db.ForeignKey('watchlist_films.watchlist_id')) 

    def __repr__(self):
        return f'User({self.user_id}, {self.username}, {self.email}, {self.about}, {self.rated_id}, {self.watchlist_id})'


class Rated_Films(db.Model):
    __tablename__ = 'rated_films'
    rated_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movies.movie_id'))

    def __repr__(self):
        return f'Rated Flims({self.rated_id}, {self.movie_id})'


class Watchlist_Films(db.Model):
    __tablename__ = 'watchlist_films'

    watchlist_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movies.movie_id'))

    def __repr__(self):
        return f'Rated Flims({self.watchlist_id}, {self.movie_id})'


class Movie(db.Model):
    __tablename__ = 'movie'
    movie_id = db.Column(db.Integer, primary_key=True)
    poster_url = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    IMDB_rating = db.Column(db.Integer, nullable=False)
    UNCC_rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'User({self.movie_id}, {self.poster_url}, {self.title}, {self.IMDB_rating}, {self.UNCC_rating})'