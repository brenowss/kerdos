from flask import Blueprint, render_template, url_for, flash
# from kerdos.db import Database
from jinja2 import TemplateNotFound
from werkzeug.exceptions import abort
# from app.models.charts_sql import Database
import pandas as pd
from pprint import pprint
from flask_login import login_required, current_user


charts = Blueprint('charts', __name__, template_folder='templates', url_prefix='/kerdos/',  static_folder='static', static_url_path='/charts/static')


def date_format(data):
    for i in data:
        # print(list(i.keys()))
        b = str(i['data_docto'])
        b = b.replace('-', ' ')
        i['data_docto'] = tuple(b.split())
    return data


def decimal_format(data):
    for i in data:
        i['vlt_total'] = int(i['vlt_total'])
    return data


def order_by_vlt_total(data):
    data = sorted(data, key=lambda f_data: f_data['vlt_total'])
    return data


class DataProcessing:

    def __init__(self, data):
        self.data = data
        # print(self.data)

    def open_orders(self):
        decimal_format(self.data)
        df = pd.DataFrame(self.data)
        # print(self.data)
        self.data = df.groupby(['cod_cliente', 'nm_cliente'], as_index=False).sum()
        self.data = self.data.to_dict('records')
        self.data = order_by_vlt_total(self.data)
        self.data = self.data[len(self.data) - 20:]
        return self.data

    def open_bills(self):
        date_format(self.data)
        decimal_format(self.data)
        df = pd.DataFrame(self.data)
        # print(self.data)
        # a = pd.to_datetime(df['data_docto_old'])
        # df['Semana'] = a.dt.to_period('W')
        # self.data = df.groupby(['Semana', 'num_documento', 'data_docto'], as_index=False).sum()
        self.data = df.groupby(['num_documento', 'data_docto'], as_index=False).sum()
        self.data = self.data.to_dict('records')
        return self.data

    def top_sellers(self):
        decimal_format(self.data)
        df = pd.DataFrame(self.data)
        self.data = df.groupby(['nm_representante', 'cod_vendedor'], as_index=False).sum()
        self.data = self.data.to_dict('records')
        self.data = order_by_vlt_total(self.data)
        # print(self.data)
        return self.data

    def last_30_months(self):
        date_format(self.data)
        decimal_format(self.data)
        return self.data

    def top_products(self):
        decimal_format(self.data)
        # print(self.data)
        return self.data


@charts.route('/home/')
@login_required
def home():
    from kerdos.db import Database
    dp = DataProcessing
    db = Database()
    try:
        open_order = dp(db.open_order_sql()).open_orders()
        open_bill = dp(db.open_bills_sql()).open_bills()
        top_seller = dp(db.top_seller_sql()).top_sellers()
        last_30_month = dp(db.last_30_months_sql()).last_30_months()
        # print(last_30_month)
        top_product = dp(db.top_products_sql()).top_products()
        # print(current_user.id)
        return render_template('index.html', open_order=open_order, open_bill=open_bill, top_seller=top_seller,
                               last_30_month=last_30_month, top_product=top_product)
    except TemplateNotFound:
        abort(404)


def init_app(app):
    app.register_blueprint(charts)