import os

port = 8888
debug = True
db_host= '127.0.0.1'
db_port =3306
db_user='root'
db_password='123456'
db_database='blog'
page_size=10
template_path = os.path.join(os.path.dirname(__file__), 'templates')
static_path = os.path.join(os.path.dirname(__file__), 'static')


