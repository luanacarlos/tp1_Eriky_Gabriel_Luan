import psycopg2
from utils import Produto, Grupo, Categoria, CategoriaProduto, Review, Reviews, Similar, Parser
import time
import psycopg2.extras

comeco = time.time() 
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

cursor.execute('''CREATE TABLE categoria (
                  id INTEGER PRIMARY KEY,
                  nome VARCHAR(155),
                  id_pai INTEGER);''') 

cursor.execute('''CREATE TABLE review (
                  id SERIAL PRIMARY KEY,
                  assin VARCHAR(20),
                  data DATE,
                  user_id VARCHAR(20),
                  nota INTEGER,
                  votos INTEGER,
                  uteis INTEGER); ''')

cursor.execute('''CREATE TABLE produto (
                  id INTEGER PRIMARY KEY,
                  assin VARCHAR(20) UNIQUE,
                  titulo TEXT,
                  grupo VARCHAR(20),
                  rank INTEGER);''') 

cursor.execute('''CREATE TABLE cat_produto (
                  assin VARCHAR(10),
                  codigo INTEGER,
                  FOREIGN KEY (assin) REFERENCES produto(assin),
                  FOREIGN KEY (codigo) REFERENCES categoria(id));''')

cursor.execute('''CREATE TABLE similars (
                  assin VARCHAR(20),
                  assin_sim VARCHAR(20),
                  FOREIGN KEY (assin) REFERENCES produto(assin));''') 

conector.commit()
cursor.close()
conector.close()

'''
Leitura do arquivo

'''
path = '/home/luan/BD/amazon-meta.txt'

produtos = []
similares = []
categorias = []
cat_produtos = []
reviews = []
cat_ids = []


with open(path, 'r', encoding='utf-8') as arquivo:
    linha = arquivo.readline()
    
    soma = 0
    while linha:  
        linha = linha.strip()
        if linha.startswith('Id:'):
            id = Parser.id(linha)
        
        elif linha.startswith('ASIN:'):
            assin = Parser.assin(linha)
            
        #Produto completo    
        elif not linha.startswith('discontinued product'):
            if linha.startswith('title:'):
                title = Parser.title(linha)
            
            elif linha.startswith('group:'):
               grupo = Parser.group(linha)
          
            elif linha.startswith('salesrank:'):
                rank = Parser.salesrank(linha)
                tupla = (id, assin, title, grupo, rank)
                produtos.append(tupla)
                               
            elif linha.startswith('similar:'):
                similar = Parser.similar(linha)
                if similar is not None:
                    for item in similar:
                        similares.append((assin, item))

            elif linha.startswith('categories:'):
                cats = None
                hierarquia = None
                cats, hierarquia = Parser.categories(linha, arquivo)
                if cats is not None:
                    for cat in cats:
                        cat_produtos.append((assin, cat))
                if hierarquia is not None:
                    for categoria in hierarquia:
                        if categoria[0] not in cat_ids:
                            categorias.append(categoria)
                            cat_ids.append(categoria[0])
                
                
            elif linha.startswith('reviews:'):
                rev_list = Parser.reviews(linha, arquivo)
                if rev_list is not None:
                    for review in rev_list:
                        reviews.append((assin ,review[0], review[1], review[2], review[3], review[4]))
                
        #Produto descontinuado                           
        else:
            tupla = (id, assin, None, None, None)
            produtos.append(tupla)
                  
        linha = arquivo.readline()
                 
    arquivo.close()
    
"""

Inserção dos dados no banco de dados

"""
print(f'Tamanho da lista profuto {len(produtos)}')
print(f'Tamanho da lista similares {len(similares)}')
print(f'Tamanho da lista categorias {len(categorias)}')
print(f'Tamanho da lista cat_produtos {len(cat_produtos)}')
print(f'Tamanho da lista reviews {len(reviews)}')
conector = psycopg2.connect("host=" + host + " dbname=" + database + 
                            " user=" + usuario + " password=" + senha)
cursor = conector.cursor()

#Inserção na tabela Produto
query_produto = """INSERT INTO produto (id, assin, titulo, grupo, rank)
                    VALUES (%s, %s, %s, %s, %s)"""          
start_time = time.time()           
psycopg2.extras.execute_batch(cursor, query_produto, produtos)
end_time = time.time()
print(f"Tempo de inserção Produto: {end_time - start_time:.2f} segundos")  


#Inserção na tabela Similares 
query_similares = """INSERT INTO similars (assin, assin_sim)
                     VALUES (%s, %s)"""
start_time = time.time() 
psycopg2.extras.execute_batch(cursor, query_similares, similares)
end_time = time.time()
print(f"Tempo de inserção Similares: {end_time - start_time:.2f} segundos")  


#Inserção na tabela Categoria
query_categoria = """INSERT INTO categoria (id, nome, id_pai)
                          VALUES (%s, %s, %s)"""
start_time = time.time() 
psycopg2.extras.execute_batch(cursor, query_categoria, categorias)
end_time = time.time()
print(f"Tempo de inserção Categoria: {end_time - start_time:.2f} segundos") 


#Insersão na tabela Cat_Produto
query_cat_produto = """INSERT INTO cat_produto (assin, codigo)
                        VALUES (%s, %s)"""  
start_time = time.time() 
psycopg2.extras.execute_batch(cursor, query_similares, cat_produtos)
end_time = time.time()
print(f"Tempo de inserção Cat_produtos: {end_time - start_time:.2f} segundos")        
     
     
#Insersão na tabela Reviews
query_reviews = """INSERT INTO review (assin, data, user_id, nota, votos, uteis)
                     VALUES (%s, %s, %s, %s, %s, %s)"""  
start_time = time.time() 
psycopg2.extras.execute_batch(cursor, query_reviews, reviews)
end_time = time.time()
print(f"Tempo de inserção Reviews: {end_time - start_time:.2f} segundos")   

conector.commit()
cursor.close()
conector.close()
fim = time.time()
print(f"Tempo total de execução: {fim - comeco:.2f} segundos")
