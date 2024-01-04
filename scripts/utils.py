from tabulate import tabulate

class Query:
    descricoes = {'A':'Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação',
                        'B':'Dado um produto, listar os produtos similares com maiores vendas do que ele',
                        'C':'Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada',
                        'D':'Listar os 10 produtos lideres de venda em cada grupo de produtos',
                        'E':'Listar os 10 produtos com a maior média de avaliações úteis positivas por produto',
                        'F':'Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto',
                        'G':'Listar os 10 clientes que mais fizeram comentários por grupo de produto'}
    
    
    
    def __init__(self, query, cursor):
        self.funcoes = {'A':self.a, 'B':self.b, 'C':self.c, 'D':self.d, 'E':self.e, 'F':self.f, 'G':self.g}
        self.query = self.funcoes[query]
        self.cursor = cursor
    
    def a(self, cod):
        query1 = f'''(SELECT * 
                    FROM review 
                    WHERE assin='{cod}'
                    ORDER BY nota DESC, uteis DESC limit 5);'''
        
        query2 = f'''(SELECT * 
                    FROM review 
                    WHERE assin='{cod}' 
                    ORDER BY nota ASC, uteis DESC limit 5);'''
        
        self.cursor.execute(query1)
        query1 = self.cursor.fetchall()
        self.cursor.execute(query2)
        query2 = self.cursor.fetchall()

        return query1, query2
    
    def b(self, cod):
        query = f'''SELECT p.assin, p.rank
                   FROM produto p
                   WHERE p.assin IN 
                   (SELECT s.assin_sim
                    FROM similars s
                    WHERE s.assin = '{cod}')
                    AND p.rank < (SELECT rank
                                  FROM produto
                                  WHERE assin = '{cod}')
                    ORDER BY p.rank ASC;'''
        
        self.cursor.execute(query)
        query = self.cursor.fetchall()
        self.tabulate_print(['Assin', 'Rank'], query)
    
    def c(self, cod):
        query = f'''SELECT DISTINCT data, AVG(nota) OVER (ORDER BY data) AS media
                    FROM review
                    WHERE assin = '{cod}'
                    ORDER BY data;'''
        
        self.cursor.execute(query)
        query = self.cursor.fetchall()
        self.tabulate_print(['Data', 'Média'], query)
        
    def d(self):
        query = '''SELECT assin, grupo, MIN(rank) AS rank
                   FROM (SELECT assin, grupo, rank, ROW_NUMBER() 
                   OVER (PARTITION BY grupo ORDER BY rank ASC) AS rnk
                   FROM produto
                   WHERE grupo IS NOT NULL AND rank != -1 AND rank != 0) 
                   AS ranked_products
                   WHERE rnk <= 10
                   GROUP BY assin, grupo
                   ORDER BY grupo, MIN(rank) ASC;'''
                   
        self.cursor.execute(query)
        query = self.cursor.fetchall()
        self.tabulate_print(['Assin', 'Grupo', 'Rank'], query)
    
    def e(self):
        query = '''SELECT p.assin, p.titulo, AVG(r.uteis) AS media
                   FROM produto p
                   JOIN review r ON p.assin = r.assin
                   WHERE r.uteis >0 AND r.nota >3
                   GROUP BY p.assin, p.titulo
                   ORDER BY media DESC
                   LIMIT 10;'''
        
        self.cursor.execute(query)
        query = self.cursor.fetchall()
        self.tabulate_print(['Assin', 'Titulo', 'Média'], query)
    
    def f(self):
        query = '''SELECT c.id, c.nome, AVG(r.uteis) AS media
                   FROM categoria c
                   JOIN cat_produto cp ON c.id = cp.codigo
                   JOIN produto p ON cp.assin = p.assin
                   JOIN review r ON p.assin = r.assin
                   WHERE r.nota > 3 AND r.uteis >0
                   GROUP BY c.id, c.nome
                   ORDER BY media DESC
                   LIMIT 5;'''
                   
        self.cursor.execute(query)
        query = self.cursor.fetchall()
        self.tabulate_print(['Id', 'Nome', 'Média'], query)
                   
    def g(self):
        query = '''SELECT r.User_ID, p.Grupo, COUNT(r.id) AS total_comentarios
                   FROM REVIEW r
                   JOIN PRODUTO p ON r.assin = p.assin
                   WHERE r.User_ID IS NOT NULL
                   GROUP BY r.User_ID, p.Grupo
                   ORDER BY total_comentarios DESC
                   LIMIT 10;'''
                   
        self.cursor.execute(query)
        query = self.cursor.fetchall()
        self.tabulate_print(['User_ID', 'Grupo', 'Total de Comentários'], query)
    
    
    def tabulate_print(self, cabecalho, tabela):
        tabela_formatada = tabulate(tabela, headers=cabecalho, tablefmt='grid')
        print(tabela_formatada, '\n')
        
        
"""

Classe do parser

"""

class Parser:
        
    def id(linha):
        id = linha.split(':')[1][3:]
        return id
    
    def assin(linha):
        assin = linha.split(':')[1][1:]
        return assin

    def title(linha):
        title = linha.split('title: ')[1]
        return title

    def group(linha):
        group = linha.split(':')[1][1:]
        return group

    def salesrank(linha):
        salesrank = linha.split(':')[1][1:]
        return int(salesrank)

    def similar(linha):
        quantity = linha.split(':')[1][1:2]
        if quantity == '0':
            return None
        else:
            similar = linha.split(':')[1][1:].split()[1:]
            return similar
            
    def categories(linha, arquivo):
        quantity = linha.split(':')[1][1:2]
        if quantity == '0':
            return None, None
        else:
            cats = []
            hierarquia = []
            for i in range(0, int(quantity)):
                linha = arquivo.readline().strip() 
                cats.append(linha.split('|')[1:][-1])
                for categoria in Parser.gera_hierarquia(linha.split('|')[1:]):
                        hierarquia.append(categoria)
                        
            codes = Parser.extract_codes(cats)
            return codes, hierarquia

    def reviews(linha, arquivo):
        quantity = linha.split('reviews: ')[1].split(' ')[4]
        reviews = []
        if quantity == '0':
            return None
        else:
            for review in range(0, int(quantity)):
                linha = arquivo.readline().strip()
                dados = linha.split()
                dados.remove('cutomer:')
                dados.remove('rating:')
                dados.remove('votes:')
                dados.remove('helpful:')
                reviews.append(dados)
            return reviews
            

    def gera_hierarquia(lista):
        categorias = []
        codigos = Parser.extract_codes(lista)
        nomes = Parser.extract_names(lista)
        ultima = len(lista) - 1
        while ultima != -1:
            categorias.append((codigos[ultima], nomes[ultima], codigos[ultima-1]) if ultima != 0 else (codigos[ultima], nomes[ultima], None))
            ultima -= 1
        return categorias
    
    def extract_codes(strings):
        codes = []
        for string in strings:
            start_index = string.rfind("[")
            end_index = string.rfind("]")
            if start_index != -1 and end_index != -1:
                try:
                    code = int(string[start_index + 1:end_index])
                    codes.append(code)
                except ValueError:
                    codes.append(None)
            else:
                codes.append(None)

        return codes
    
    def extract_names(strings):
        names = []
        for string in strings:
            start_index = 0
            end_index = string.find("[")
            name = string[:end_index]  
            names.append(name) 

        return names
    