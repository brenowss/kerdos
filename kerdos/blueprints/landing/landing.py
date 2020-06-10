from flask import Blueprint, render_template

landing = Blueprint('landing', __name__, template_folder='templates', static_folder='static', static_url_path='/landing/static')


@landing.route('/', methods=['GET', 'POST'])
def login():
    return render_template('landing-page.html')


def init_app(app):
    app.register_blueprint(landing)
    