from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):

    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False) #need to make it a foreign key, just mocking it up for now
    body = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    

    def __repr__(self):
        return f'Post({self.post_id}, {self.title}, {self.username}, {self.body}, {self.time})'