"""

Representação das tabelas do esquema em classes

"""

class Produto:
    def __init__(self, Id, Assin, Titulo, Grupo, Rank):
        self.id = Id
        self.assin = Assin
        self.titulo = Titulo
        self.grupo = Grupo
        self.rank = Rank
        
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, Id):
        self.__id = Id
    
    @property
    def ASSIN(self):
        return self.__ASSIN
    
    @ASSIN.setter
    def ASSIN(self, ASSIN):
        self.__ASSIN = ASSIN
        
    @property
    def titulo(self):
        return self.__titulo
    
    @titulo.setter
    def titulo(self, titulo):
        self.__titulo = titulo
    
    @property
    def grupo(self):
        return self.__grupo
    
    @grupo.setter
    def grupo(self, grupo):
        self.__grupo = grupo
    
    @property
    def rank(self):
        return self.__rank
    
    @rank.setter
    def rank(self, rank):
        self.__rank = rank
        

class Grupo:
    def __init__(self, cod_grupo, nome_grupo):
        self.cod_grupo = cod_grupo
        self.nome_grupo = nome_grupo
    
    @property
    def cod_grupo(self):
        return self.__cod_grupo
    
    @cod_grupo.setter
    def cod_grupo(self, cod_grupo):
        self.__cod_grupo = cod_grupo
    
    @property
    def nome_grupo(self):
        return self.__nome_grupo
    

class Categoria:
    def __init__(self, categoria_id, categoria_nome, categoria_pai_id):
        self.categoria_id = categoria_id
        self.categoria_nome = categoria_nome
        self.categoria_pai_id = categoria_pai_id
    
    @property
    def categoria_id(self):
        return self.__categoria_id
    
    @categoria_id.setter
    def categoria_id(self, categoria_id):
        self.__categoria_id = categoria_id
    
    @property
    def categoria_nome(self):
        return self.__categoria_nome
    
    @categoria_nome.setter
    def categoria_nome(self, categoria_nome):
        self.__categoria_nome = categoria_nome
        
    @property
    def categoria_pai_id(self):
        return self.__categoria_pai_id
    
    @categoria_pai_id.setter
    def categoria_pai_id(self, categoria_pai_id):
        self.__categoria_pai_id = categoria_pai_id
        

class CategoriaProduto:
    def __init__(self, asin, categoria_id):
        self.asin = asin
        self.categoria_id = categoria_id
        

class Review:
    def __init__(self, review_id, data, user_id, nota, votos, votos_util):
        self.review_id = review_id
        self.data = data
        self.user_id = user_id
        self.nota = nota
        self.votos = votos
        self.votos_util = votos_util
        
    @property
    def review_id(self):
        return self.__review_id
    
    @review_id.setter
    def review_id(self, review_id):
        self.__review_id = review_id
        
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, data):
        self.__data = data
    
    @property
    def user_id(self):
        return self.__user_id
    
    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id
    
    @property
    def nota(self):
        return self.__nota
    
    @nota.setter
    def nota(self, nota):
        self.__nota = nota
    
    @property
    def votos(self):
        return self.__votos
    
    @votos.setter
    def votos(self, votos):
        self.__votos = votos
    
    @property
    def votos_util(self):
        return self.__votos_util
    
    @votos_util.setter
    def votos_util(self, votos_util):
        self.__votos_util = votos_util
    

class Reviews:
    def __init__(self, asin, id_review):
        self.asin = asin
        self.id_review = id_review
        
    @property
    def asin(self):
        return self.__asin
    
    @asin.setter
    def asin(self, asin):
        self.__asin = asin
    
    @property
    def id_review(self):
        return self.__id_review
    
    @id_review.setter
    def id_review(self, id_review):
        self.__id_review = id_review
    

class Similar:
    def __init__(self, asin, similars_asin):
        self.asin = asin
        self.similars_asin = similars_asin
        
    @property
    def asin(self):
        return self.__asin
    
    @asin.setter
    def asin(self, asin):
        self.__asin = asin
    
    @property
    def similar_asin(self):
        return self.__similar_asin
    
    @similar_asin.setter
    def similar_asin(self, similar_asin):
        self.__similar_asin = similar_asin
        
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
            return None
        else:
            categorias = []
        
            for i in range(0, int(quantity)):
                linha = arquivo.readline().strip()
                categorias.append(linha.split('|')[1:])              
            return categorias

    def reviews(linha, arquivo):
        quantity = linha.split('reviews: ')[1].split(' ')[1]
        reviews = []
        for review in range(0, int(quantity)):
            linha = arquivo.readline().strip()
            dados = linha.split()
            dados.remove('cutomer:')
            dados.remove('rating:')
            dados.remove('votes:')
            dados.remove('helpful:')
            reviews.append(dados)
        return reviews
            


