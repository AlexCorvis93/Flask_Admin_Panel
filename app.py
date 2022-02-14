from flask import Flask
from auth.auth_config import auth
from users.users import users
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from database import Users, Profile, Position
import os
from dotenv import load_dotenv

"""FOR LOADING environment variables"""
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(users, url_prefix='/users')
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)
db = SQLAlchemy(app)


if __name__ == "__main__":
    app.run(debug=True)