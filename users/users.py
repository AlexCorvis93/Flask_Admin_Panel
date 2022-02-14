from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from database import Users, Profile, Position, db

users = Blueprint('users', __name__, template_folder='templates', static_folder='static')


@users.route('/', methods=['POST', 'GET'])
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
            new_profile = Profile(name=name, last_name=last_name, old=old, position_id=position)
            db.session.add(new_profile)
            db.session.commit()
            return redirect(url_for('.show_users_list'))#добавление изменений в бд
        except:
            db.session.rollback() #откат бд до первоначального состояния
            print('Error add into DB')
    return render_template('users/create.html', pos1=pos1, pos2=pos2)


@users.route('/list', methods=['GET', 'POST'])
def show_users_list():
    users_list = []
    try:
        users_list = Profile.query.all()
    except:
        print("ERROR READING DB")
    return render_template('users/list.html', list=users_list)