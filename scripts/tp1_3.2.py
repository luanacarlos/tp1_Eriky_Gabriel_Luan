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


cursor.execute('''CREATE TABLE categoria (
                  id INTEGER PRIMARY KEY,
                  nome VARCHAR(155),
                  id_pai INTEGER);''')

cursor.execute('''CREATE TABLE review (
                  id SERIAL PRIMARY KEY,
                  data TIMESTAMP,
                  user_id INTEGER,
                  nota INTEGER,
                  votos INTEGER); ''')

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
similar = []
categorias = []
cat_produtos = []
reviews = []



with open(path, 'r', encoding='utf-8') as arquivo:
    linha = arquivo.readline()
    
    soma = 0
    while linha:  
        linha = linha.strip()
        #print(linha)
        if linha.startswith('Id:'):
            id = Parser.id(linha)
            ###
        
        elif linha.startswith('ASIN:'):
            assin = Parser.assin(linha)
            ###
            
        elif not linha.startswith('discontinued product'):
            if linha.startswith('title:'):
                title = Parser.title(linha)
                ###
            
            elif linha.startswith('group:'):
               grupo = Parser.group(linha)
               ###
                                   
            elif linha.startswith('salesrank:'):
                rank = Parser.salesrank(linha)
                produtos.append(Produto(id, assin, title, grupo, rank))
                ###
                
                
            elif linha.startswith('similar:'):
                if Parser.similar(linha) is not None:
                    similares.append(Similar(assin, Parser.similar(linha)))
                    ###

            
            elif linha.startswith('categories:'):
                cats = None
                hierarquia = None
                cats, hierarquia = Parser.categories(linha, arquivo)
                cat_produtos.append(CategoriaProduto(assin, cats))
                if hierarquia is not None:
                    for categoria in hierarquia:
                        categorias.append(categoria)
                
                
            
            
            elif linha.startswith('reviews:'):
                rev_list = Parser.reviews(linha, arquivo)
                if rev_list is not None:
                    for review in rev_list:
                        reviews.append(Review(assin ,review[0], review[1], review[2], review[3], review[4]))
                    
                
        else:
            #print('descontinuado')
            produtos.append(Produto(id, assin, None, None, None))
            #linha = arquivo.readline().strip()
                  
        soma += 1
        if soma%1000000 == 0:
            print(soma)
        linha = arquivo.readline()
                 
    arquivo.close()
    print('done!')
    

    
"""

Inserção dos dados no banco de dados

"""


conector = psycopg2.connect("host=" + host + " dbname=" + database + 
                            " user=" + usuario + " password=" + senha)

cursor = conector.cursor()

for produto in produtos:
    print(produto.id)
    cursor.execute("""INSERT INTO produto (id, assin, titulo, grupo, rank)
                      VALUES (%s, %s, %s, %s, %s)""", 
                      (produto.id ,produto.assin, produto.titulo, produto.grupo, produto.rank))
'''
for categoria in categorias:
    cursor.execute("""INSERT INTO categoria (id, nome, id_pai)
                      VALUES (%s %s, %s)""",
                      (categoria.id, categoria.nome, categoria.id_pai))'''
    
for similar in similares:
    for element in similar.similars_asin:
        cursor.execute("""INSERT INTO similars (assin, assin_sim)
                        VALUES (%s, %s)""",
                        (similar.Assin, element))

conector.commit()
cursor.close()
conector.close()
