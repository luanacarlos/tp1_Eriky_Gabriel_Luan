import psycopg2
from utils import Produto, Grupo, Categoria, CategoriaProduto, Review, Reviews, Similar, Parser
import time

start_time = time.time()

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
                  id_pai INTEGER);''') #ok

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
                  rank INTEGER);''') #ok

cursor.execute('''CREATE TABLE cat_produto (
                  assin VARCHAR(10),
                  codigo INTEGER,
                  FOREIGN KEY (assin) REFERENCES produto(assin),
                  FOREIGN KEY (codigo) REFERENCES categoria(id));''') #ok

cursor.execute('''CREATE TABLE similars (
                  assin VARCHAR(20),
                  assin_sim VARCHAR(20),
                  FOREIGN KEY (assin) REFERENCES produto(assin));''') #ok

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
                produtos.append(Produto(id, assin, title, grupo, rank))
                               
            elif linha.startswith('similar:'):
                similar = Parser.similar(linha)
                if similar is not None:
                    similares.append(Similar(assin, similar))

            elif linha.startswith('categories:'):
                cats = None
                hierarquia = None
                cats, hierarquia = Parser.categories(linha, arquivo)
                cat_produtos.append(CategoriaProduto(assin, cats)) if cats is not None else None 
                if hierarquia is not None:
                    for categoria in hierarquia:
                        if categoria.id not in cat_ids:
                            categorias.append(categoria)
                            cat_ids.append(categoria.id)
                
                
            elif linha.startswith('reviews:'):
                rev_list = Parser.reviews(linha, arquivo)
                if rev_list is not None:
                    for review in rev_list:
                        reviews.append(Review(assin ,review[0], review[1], review[2], review[3], review[4]))
                
        #Produto descontinuado                           
        else:
            produtos.append(Produto(id, assin, None, None, None))
                  
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

print('Preenchenco tabela Produto...')
for produto in produtos:
    cursor.execute("""INSERT INTO produto (id, assin, titulo, grupo, rank)
                      VALUES (%s, %s, %s, %s, %s)""", 
                      (produto.id ,produto.assin, produto.titulo, produto.grupo, produto.rank))

print('Tabela Produto preenchida com sucesso.')

print('Preenchenco tabela Categoria...')
for categoria in categorias:
    cursor.execute("SELECT 1 FROM categoria WHERE id = %s", (categoria.id,))
    existe = cursor.fetchone()

    if not existe:
        cursor.execute("""INSERT INTO categoria (id, nome, id_pai)
                          VALUES (%s, %s, %s)""",
                          (categoria.id, categoria.nome, categoria.id_pai))
 
print('Tabela Categoria preenchida com sucesso.') 
    
print('Preenchenco tabela Similares...')    
for similar in similares:
    for element in similar.similars_asin:
        cursor.execute("""INSERT INTO similars (assin, assin_sim)
                        VALUES (%s, %s)""",
                        (similar.Assin, element))
        
print('Tabela Similares preenchida com sucesso.')        
        
print('Preenchenco tabela Cat_Produto...')        
for cat_produto in cat_produtos:
    for element in cat_produto.lista_cat:
        cursor.execute("""INSERT INTO cat_produto (assin, codigo)
                        VALUES (%s, %s)""",
                        (cat_produto.assin, element))
        
print('Tabela Cat_Produto preenchida com sucesso.')       
        
print('Preenchenco tabela Review...')      
for review in reviews:
    cursor.execute("""INSERT INTO review (assin, data, user_id, nota, votos, uteis)
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (review.assin, review.data, review.user_id, review.nota, review.votos, review.votos_util))

print('Tabela Review preenchida com sucesso.')

conector.commit()
cursor.close()
conector.close()

end_time = time.time()
execution_time = end_time - start_time

print(f"Tempo de execução: {execution_time:.2f} segundos")
