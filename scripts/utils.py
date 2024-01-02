import re
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
    def __init__(self, id, nome, id_pai):
        self.id = id
        self.nome = nome
        self.id_pai = id_pai
    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id):
        self.__id = id
    
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome):
        self.__nome = nome
        
    @property
    def id_pai(self):
        return self.__id_pai
    
    @id_pai.setter
    def id_pai(self, id_pai):
        self.__id_pai = id_pai
    
    
class CategoriaProduto:
    def __init__(self, assin, lista_cat):
        self.assin = assin
        self.lista_cat = lista_cat  

    @property
    def assin(self):
        return self.__assin
    
    @assin.setter
    def assin(self, assin):
        self.__assin = assin
    
    @property
    def lista_cat(self):
        return self.__lista_cat

    @lista_cat.setter
    def lista_cat(self, lista_cat):
        self.__lista_cat = lista_cat
    
        

class Review:
    def __init__(self, assin, data, user_id, nota, votos, votos_util):
        self.assin = assin
        self.data = data
        self.user_id = user_id
        self.nota = nota
        self.votos = votos
        self.votos_util = votos_util
    
    @property
    def assin(self):
        return self.__assin
    
    @assin.setter
    def assin(self, assin):
        self.__assin = assin
        
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
    def __init__(self, Assin, similars_asin):
        self.Assin = Assin
        self.similars_asin = similars_asin
        
    @property
    def Assin(self):
        return self.__Assin
    
    @Assin.setter
    def Assin(self, Assin):
        self.__Assin = Assin
    
    @property
    def similars_asin(self):
        return self.__similars_asin
    
    @similars_asin.setter
    def similars_asin(self, similars_asin):
        self.__similars_asin = similars_asin
        

        
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
                #print(Parser.gera_hierarquia(linha.split('|')[1:]))
                for categoria in Parser.gera_hierarquia(linha.split('|')[1:]):
                        hierarquia.append(categoria)
                        
            codes = Parser.extract_codes(cats)
            #print(codes)
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
        """
        Extrai códigos de strings no formato "texto[code]" ou "texto".

        Args:
            strings: Uma lista de strings.

        Returns:
            Uma lista contendo os códigos extraídos ou None se a string não tiver um código.
        """

        codes = []
        for string in strings:
            # Encontra os índices de início e fim da seção de código mais à direita
            start_index = string.rfind("[")
            end_index = string.rfind("]")

            # Verifica se há uma seção de código
            if start_index != -1 and end_index != -1:
                try:
                    # Tenta converter o código para inteiro
                    code = int(string[start_index + 1:end_index])
                    codes.append(code)
                except ValueError:
                    # Se a conversão falhar, assume que não há código e adiciona None
                    codes.append(None)
            else:
                # Não há seção de código na string, então adiciona None
                codes.append(None)

        return codes
    
    def extract_names(strings):
        names = []
        for string in strings:
            start_index = 0  # Índice de início do texto
            end_index = string.find("[")  # Índice de fechamento do colchete
            name = string[:end_index]  # Extrai o texto
            names.append(name)  # Adiciona o nome à lista de nomes

        return names
    
