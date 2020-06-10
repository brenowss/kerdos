# from kerdos.blueprints.auth.auth import login_manager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from kerdos.app import db, login_manager
from werkzeug.security import check_password_hash


# @login_manager.user_loader
# def get_user(user_id):
#     return User.query.filter_by(id=user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(255))
    email = db.Column('email', db.String(255))
    senha = db.Column('senha', db.String(32))
    ind_ativo = db.Column('ind_ativo', db.Integer)
    cod_empresa = db.Column('cod_empresa', db.Integer)

    def __init__(self, nome, email, password, ind, c_empresa):
        self.nome = nome
        self.email = email
        self.password = password
        self.ind = ind
        self.c_empresa = c_empresa

    def verify_password(self, pwd):
        return check_password_hash(self.senha, pwd)


class Company(db.Model):
    __tablename__ = 'empresa'
    id = db.Column('codigo_empresa', db.Integer, primary_key=True)
    tipo_plano = db.Column('tipo_plano', db.Integer)
    nome_db = db.Column('nome_db', db.String(50))

    def __init__(self, tipo_plano, nome_db):
        self.tipo_plano = tipo_plano
        self.nome_db = nome_db
