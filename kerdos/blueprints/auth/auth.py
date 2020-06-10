from flask import Blueprint, render_template, request, url_for, redirect, flash, current_app
from flask_login import login_user, logout_user, current_user, login_required
# from flask_sqlalchemy import SQLAlchemy
from kerdos.models import User
from kerdos.app import login_manager

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static', static_url_path='/auth/static')
# auth.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://kerdos:123@localhost/kerdos_admin'
# auth.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(auth)
# login_manager = LoginManager(auth)


@auth.route('/kerdos/', methods=['GET', 'POST'])
def login_auth():
    if not current_user.is_authenticated:
        if request.method == 'POST':
            login = request.form['login']
            password = request.form['password']
            remember_me = request.form.getlist("keep_login")
            user = User.query.filter_by(email=login).first()
            if not user:
                user = User.query.filter_by(nome=login).first()
                if not user:
                    flash(True)
                    return redirect(url_for('auth.login_auth'))
                login_user(user, remember=remember_me)
                return redirect(url_for('charts.home'))
            login_user(user, remember=remember_me)
            return redirect(url_for('charts.home'))
        return render_template('login.html')
    return redirect(url_for('charts.home'))


@auth.route('/kerdos/logout/')
@login_required
def logout_auth():
    logout_user()
    return redirect(url_for('auth.login_auth'))



@login_manager.user_loader
def get_user(id):
    return User.query.filter_by(id=id).first()


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return redirect(url_for('auth.login_auth'))


def init_app(app):
    app.register_blueprint(auth)
