import psycopg2
from utils import Produto, Grupo, Categoria, CategoriaProduto, Review, Reviews, Similar, Parser

host="localhost"
database="tp1"
usuario="postgres"
senha="12345"

conector = psycopg2.connect("host=" + host + " dbname=" + database + 
                            " user=" + usuario + " password=" + senha)

cursor = conector.cursor()

'''

Criação das tabelas

'''
cursor.execute('''CREATE TABLE grupo (
                  codigo INTEGER PRIMARY KEY,
                  nome VARCHAR(255));''')

cursor.execute('''CREATE TABLE categoria (
                  id SERIAL PRIMARY KEY,
                  id_pai INTEGER,
                  nome VARCHAR(155));''')

cursor.execute('''CREATE TABLE review (
                  id SERIAL PRIMARY KEY,
                  data TIMESTAMP,
                  user_id INTEGER,
                  nota INTEGER,
                  votos INTEGER); ''')

cursor.execute('''CREATE TABLE produto (
                  id SERIAL PRIMARY KEY,
                  asin VARCHAR(20) UNIQUE,
                  titulo VARCHAR(255),
                  cod_grupo INTEGER,
                  rank INTEGER,
                  id_categoria INTEGER,
                  FOREIGN KEY (cod_grupo) REFERENCES grupo(codigo));''')

cursor.execute('''CREATE TABLE cat_produto (
                  asin VARCHAR(10),
                  codigo INTEGER,
                  FOREIGN KEY (asin) REFERENCES produto(asin),
                  FOREIGN KEY (codigo) REFERENCES categoria(id));''')

cursor.execute('''CREATE TABLE reviews (
                  asin VARCHAR(10),
                  review_id INTEGER,
                  FOREIGN KEY (review_id) REFERENCES review(id),
                  FOREIGN KEY (asin) REFERENCES produto(asin));''')

cursor.execute('''CREATE TABLE similars (
                  asin VARCHAR(20),
                  asin_sim VARCHAR(20),
                  FOREIGN KEY (asin) REFERENCES produto(asin));''')

conector.commit()
cursor.close()
conector.close()


'''

Leitura do arquivo

'''
path = '/home/luan/BD/amazon-meta.txt'

grupo = []
categoria = []
review = []
produto = []
cat_produto = []
reviews = []
similars = []

with open(path, 'r', encoding='utf-8') as arquivo:
    linhas = arquivo.readlines().strip()
    
for linha in range(0, 5):
    print (linhas[linha])
    