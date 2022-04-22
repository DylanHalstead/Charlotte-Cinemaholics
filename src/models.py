from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    post_time = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, nullable = False)
    
    def __repr__(self):
        return f'Post({self.post_id}, {self.title}, {self.user_id}, {self.body}, {self.post_time}, {self.likes})'

class Reply(db.Model):
    __tablename__ = 'replies'
    reply_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id')) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    body = db.Column(db.String, nullable=False)
    post_time = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, nullable = False)
    
    def __repr__(self):
        return f'Reply({self.reply_id}, {self.post_id}, {self.user_id}, {self.body}, {self.post_time}, {self.likes})'

user_playlist = db.Table(
    'user_playlist',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.playlist_id'),primary_key=True)
)

class UserRating(db.Model):
    __tablename__ = 'user_ratings'
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    movie_id = db.Column('movie_id', db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    movie_rating = db.Column('user_rating', db.Float, nullable = False)
    user = db.relationship('User', back_populates='movie_rating')
    movie = db.relationship('Movie', back_populates='user_rating')

playlist_movie = db.Table(
    'playlist_movie',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.playlist_id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True),
    db.Column('movie_rank', db.Integer, nullable = False)
)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    passkey = db.Column(db.String, nullable=False)
    pfp = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=True)

    movie_rating = db.relationship("UserRating", back_populates="user")
    users_playlist = db.relationship('Playlist', secondary=user_playlist, backref='users_playlist')

    def __repr__(self):
        return f'User({self.user_id}, {self.username}, {self.email}, {self.pfp}, {self.about})'


class User_Playlist(db.Model):
    __tablename__ = 'users_playlist'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.playlist_id'),primary_key=True)

    def __repr__(self):
        return f'User_Playlist({self.user_id}, {self.playlist_id})'

class Playlist(db.Model):
    __tablename__ = 'playlist'
    playlist_id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String, nullable = False)

    playlist_movie = db.relationship('Movie', secondary=playlist_movie, backref='playlist_movie')

    def __repr__(self):
        return f'Playlist({self.playlist_id}, {self.playlist_name})'

class Movie(db.Model):
    __tablename__ = 'movie'
    movie_id = db.Column(db.Integer, primary_key=True)
    poster_url = db.Column(db.String, nullable=True)

    user_rating = db.relationship("UserRating", back_populates="movie")

    def __repr__(self):
        return f'Movie({self.movie_id}, {self.poster_url})'