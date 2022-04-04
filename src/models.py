from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# It is fine to break up your models into different files, just watch out for any import cycles