from flask import Flask
from kerdos.ext import configuration
# from flask_sqlalchemy import SQLAlchemy
# from dynaconf import FlaskDynaconf
from kerdos.ext import configuration
from kerdos.ext import database
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kerdos:123@localhost/kerdos_admin'
app.config['SECRET_KEY'] = 'aaa'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


from kerdos.blueprints.charts import charts
from kerdos.blueprints.auth import auth
from kerdos.blueprints.landing import landing
charts.init_app(app)
auth.init_app(app)
landing.init_app(app)
