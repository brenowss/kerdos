import pymysql
from datetime import date, timedelta
from flask_login import current_user


class Database:
    def __init__(self):
        __host = "127.0.0.1"
        __host = "localhost"
        __user = "kerdos"
        __password = "123"
        __db = f"{current_user.nome}"
        # print(__db)
        self.con = pymysql.connect(host=__host, user=__user, password=__password, db=__db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    # def login(self, login, password):
    #     self.cur.execute(f"""select*from usuarios where nome = '{login}' and senha = '{password}'""")
    #     result = self.cur.fetchall()
    #     if not result:
    #         self.cur.execute(f"""select*from usuarios where email = '{login}' and senha = '{password}'""")
    #         result = self.cur.fetchall()
    #         return result
    #     return result

    def open_order_sql(self):
        self.cur.execute("""select pi.vlt_total, pb.cod_cliente, pb.nm_cliente
                            from pedido_base pb 
                              join ped_item pi on pi.key_pedido = pb.key_pedido
                              join clientes c on c.cod_cliente = pb.cod_cliente
                            where  pb.status_ped = 'A';""")
        result = self.cur.fetchall()
        return result

    def open_bills_sql(self):
        a = date.today() - timedelta(days=365)
        a = str(a)
        # print(a)
        self.cur.execute(
            f"""select nb.num_documento as num_documento, ni.vlt_total as vlt_total, nb.data_docto from nota_item ni join nota_base nb on 
                            nb.key_nota = ni.key_nota where nb.status_nota = 'A' and nb.data_docto IS NOT NULL and data_docto > '{a}';""")
        result = self.cur.fetchall()
        return result

    def top_seller_sql(self):
        self.cur.execute("""select pb.cod_vendedor, rep.nm_representante, pi.vlt_total
                                        from pedido_base pb 
                                        join ped_item pi on pi.key_pedido = pb.key_pedido
                                        join representantes rep on rep.cod_representante =  pb.cod_vendedor;""")
        result = self.cur.fetchall()
        return result

    def top_products_sql(self):
        self.cur.execute("""select ni.vlt_total, ni.nm_produto
                                from nota_base nb join nota_item ni on ni.key_nota = nb.key_nota
                                where nb.status_nota = 'F'
                            LIMIT 10;""")
        result = self.cur.fetchall()

        return result

    def last_30_months_sql(self):
        a = date.today() - timedelta(days=60)
        a = str(a)
        print(a)
        self.cur.execute(f"""select nsi.vlt_total, data_docto 
                                from nota_item nsi join nota_base nb on nb.key_nota = nsi.key_nota 
                                where data_docto > '{a}';""")
        result = self.cur.fetchall()
        print(result)
        return result


