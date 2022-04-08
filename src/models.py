from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Users(db.model):
    __tablename__ = 'app_user'
    user_id = db.column(db.Integer, nullable=False)
    username = db.column(db.String, nullable=False)
    user_email = db.column(db.String, nullable=False)
    user_password = db.column(db.String, nullable=False)
    user_pfp = db.column(db.String, nullable=False)
    user_about = db.column(db.String, nullable=False)
    def __repr__(self):
        return f'Users({self.user_id}, {self.username}, {self.user_email}, {self.user_password}, {self.user_pfp}, {self.user_about})'

class Posts(db.Model):
    post_id = db.column(db.Integer, nullable=False)
    user_id = db.column(db.Integer, nullable=False)
    title = db.column(db.String, nullable=False)
    body = db.column(db.String, nullable=False)
    post_time = db.column(db.String, nullable=False)
    likes = db.column(db.Integer, nullable=False)
    def __repr__(self):
            return f'Users({self.post_id}, {self.user_id}, {self.title}, {self.body}, {self.post_time}, {self.likes})'

class Replies(db.Model):
    reply_id = db.column(db.Integer, nullable=False)
    post_id = db.column(db.Integer, nullable=False)
    user_id = db.column(db.Integer, nullable=False)
    body = db.column(db.String, nullable=False)
    post_time = db.column(db.String, nullable=False)
    likes = db.column(db.Integer, nullable=False)
    def __repr__(self):
        return f'Users({self.reply_id}, {self.post_id}, {self.user_id}, {self.body}, {self.post_time}, {self.likes})'