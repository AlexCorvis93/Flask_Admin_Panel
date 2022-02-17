from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from flask.cli import FlaskGroup
from auth.auth_config import auth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)
cli = FlaskGroup(app)


class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50))
    profiles = db.relationship('Profile', backref='position')

    def __init__(self, role):
        self.role = role

    def __repr__(self):
        return f"{self.name}"


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    pswd = db.Column(db.String(500), nullable=True)
    profiles = db.relationship('Profile', backref='users')

    def __init__(self, login, pswd):
        self.login = login
        self.pswd = pswd

    def __repr__(self):
        return f"{self.login}"


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id')) #должность с правами доступа к определенным действиям в админке
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"{self.name}:{self.last_name}"


@app.route('/user', methods=['POST', 'GET'])
def create_user():
    """функция создания пользователя в БД """
    login = request.form.get('login')
    password = request.form.get('pswd')
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    old = request.form.get('old')
    position = request.form.get('role')
    pos1 = Position.query.filter_by(id=1).all()
    pos2 = Position.query.filter_by(id=2).all()
    if request.method == 'POST':
        try:
            new_user = Users(login=login, pswd=generate_password_hash(password))
            db.session.add(new_user)
            new_profile = Profile(name=name, last_name=last_name, old=old, position=position)
            db.session.add(new_profile)
            db.session.commit()
            return redirect(url_for('.show_users_list'))#добавление изменений в бд
        except:
            db.session.rollback() #откат бд до первоначального состояния
            print('Error add into DB')
    return render_template('users/create.html', pos1=pos1, pos2=pos2)


@app.route('/list', methods=['GET', 'POST'])
def show_users_list():
    users_list = []
    try:
        users_list = Profile.query.all()
    except:
        print("ERROR READING DB")
    return render_template('users/list.html', list=users_list)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()