import psycopg2
from utils import Produto, Grupo, Categoria, CategoriaProduto, Review, Reviews, Similar, Parser

host="localhost"
database="tp1"
usuario="postgres"
senha="12345"
"""
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
"""

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

id = 0
asin = 0
title = ''
group = ''
salesrank = 0
similar = []
categories = 0
reviews = 0
total = 0
downloaded = 0
avg_rating = 0


with open(path, 'r', encoding='utf-8') as arquivo:
    linha = arquivo.readline().strip()

    soma = 0
    while soma < 50:  
        if linha.startswith('Id:'):
            print(f'ID DO PRODUTO ->{Parser.id(linha)}')
        
        elif linha.startswith('ASIN:'):
            print(f'ASIN DO PRODUTO ->{Parser.assin(linha)}')
            
        elif not linha.startswith('discontinued product'):
            if linha.startswith('title:'):
                print(f'TITULO DO PRODUTO ->{Parser.title(linha)}')
            
            elif linha.startswith('group:'):
                print(f'GRUPO DO PRODUTO ->{Parser.group(linha)}')
                
            elif linha.startswith('salesrank:'):
                print(f'RANK DO PRODUTO ->{Parser.salesrank(linha)}')
                
            elif linha.startswith('similar:'):
                print(f'SIMILARES DO PRODUTO ->{Parser.similar(linha)}')
                
            elif linha.startswith('categories:'):
                print(f'CATEGORIAS DO PRODUTO ->{Parser.categories(linha, arquivo)}')
            
            elif linha.startswith('reviews:'):
                print(f'REVIEWS DO PRODUTO ->{Parser.reviews(linha, arquivo)}')
        
        
        else:
            print('descontinuado')
            #tratamento pra produto descontinuado
            
        linha = arquivo.readline().strip()
        soma += 1
    
    print(soma)


    arquivo.close()