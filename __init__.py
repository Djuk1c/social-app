from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import datetime, timeago
import ast

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    from .models import User
    from .models import Posts
    from .models import Comments

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.template_filter('fromnow')
    def fromnow(date):
        return timeago.format(date, datetime.datetime.utcnow())

    @app.template_filter('likesCount')
    def likesCount(likeList):
        likeList = ast.literal_eval(likeList)
        return len(likeList)

    @app.template_filter('retList')
    def retList(list):
        list = ast.literal_eval(list)
        return list

    @app.template_filter('commentsCount')
    def commentsCount(comments):
        return len(comments)

    return app