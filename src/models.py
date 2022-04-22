from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    post_time = db.Column(db.String, nullable=False)
    likes = db.relationship('PostLike', backref='posts', lazy='dynamic')
    def __repr__(self):
        return f'Post({self.post_id}, {self.title}, {self.user_id}, {self.body}, {self.post_time}, {self.likes})'

class Reply(db.Model):
    __tablename__ = 'replies'
    reply_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id')) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    body = db.Column(db.String, nullable=False)
    post_time = db.Column(db.String, nullable=False)
    likes = db.relationship('ReplyLike', backref='replies', lazy='dynamic')
    
    def __repr__(self):
        return f'Reply({self.reply_id}, {self.post_id}, {self.user_id}, {self.body}, {self.post_time}, {self.likes})'

user_playlist = db.Table(
    'user_playlist',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.playlist_id'),primary_key=True)
)

user_ratings = db.Table(
    'user_ratings',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True),
    db.Column('user_rating', db.Float, nullable = False)
)

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

    movie_rating = db.relationship('Movie', secondary=user_ratings, backref='user_rating')
    users_playlist = db.relationship('Playlist', secondary=user_playlist, backref='users_playlist')
    
    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='users', lazy='dynamic')

    def like_post(self, post):
        if not self.has_liked_post(post):
            print(self.username + " liked " + str(post.post_id))
            like = PostLike(user_id=self.user_id, post_id=post.post_id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            print(self.username + " unliked " + str(post.post_id))
            PostLike.query.filter_by(
                user_id=self.user_id,
                post_id=post.post_id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.user_id,
            PostLike.post_id == post.post_id).count() > 0

    def like_reply(self, reply):
        if not self.has_liked_reply(reply):
            like = ReplyLike(user_id=self.user_id, reply_id=reply.reply_id)
            db.session.add(like)

    def unlike_reply(self, reply):
        
        if self.has_liked_reply(reply):
            print(self.username + " unliked " + str(reply.reply_id))
            ReplyLike.query.filter_by(
                user_id=self.user_id,
                reply_id=reply.reply_id).delete()

    def has_liked_reply(self, reply):
        
        return ReplyLike.query.filter(
            ReplyLike.user_id == self.user_id,
            ReplyLike.reply_id == reply.reply_id).count() > 0
    
    def get_posts_count(self):
        return Post.query.filter(Post.user_id == self.user_id).count()

    def get_reply_count(self):
        return Reply.query.filter(Reply.user_id == self.user_id).count()
    
    def get_posts_and_reply_count(self):
        return self.get_reply_count() + self.get_posts_count()

    def get_reputation(self):
        reputation = 0
        user_posts = Post.query.filter(Post.user_id == self.user_id)
        user_replies = Reply.query.filter(Reply.user_id == self.user_id)
        for p in user_posts:
            reputation += p.likes.count()
        for r in user_replies:
            reputation += r.likes.count()
        return reputation

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

    def __repr__(self):
        return f'Movie({self.movie_id}, {self.poster_url})'

class Edits(db.Model):
    __tablename__ = 'edits'
    edit_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id', ondelete='CASCADE'), nullable = True)
    reply_id = db.Column(db.Integer, db.ForeignKey('replies.reply_id', ondelete='CASCADE'), nullable = True)
    reason = db.Column(db.String, nullable=True)
    time = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'Edits({self.post_id}, {self.user_id}, {self.post_id}, {self.reply_id}, {self.reason}, {self.time})'

    
class PostLike(db.Model):
    __tablename__ = 'post_like'
    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id', ondelete='CASCADE'))

class ReplyLike(db.Model):
    __tablename__ = 'reply_like'
    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    reply_id = db.Column(db.Integer, db.ForeignKey('replies.reply_id', ondelete='CASCADE'))