from flask import Blueprint, render_template, request, redirect, url_for, flash, session


auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


def login_admin():
    """if admin login"""
    session['admin_logged'] = 1


def is_logged():
    """if admin in session"""
    return True if session.get("admin_logged") else False


def logout():
    """if admin is logout"""
    session.pop('admin_logged', None)


@auth.route('/', methods=['POST', 'GET'])
def index():
    if is_logged():
        return redirect(url_for('.admin'))

    if request.method == 'POST':
        if request.form['login'] == 'Admin' and request.form['pswd'] == 'admin123':
            login_admin()
            return redirect(url_for('.admin'))
        else:
            flash('Неверный логин или пароль')
    return render_template('auth/auth.html')


menu = [{'url': '.logout_admin', 'title': 'Выход'}]


@auth.route('/admin', methods=['GET'])
def admin():
    if not is_logged():
        return redirect(url_for('.index'))
    return render_template('auth/admin.html', menu=menu)


@auth.route('/logout', methods=['POST', 'GET'])
def logout_admin():
    if not logout():
        return redirect(url_for('.index'))