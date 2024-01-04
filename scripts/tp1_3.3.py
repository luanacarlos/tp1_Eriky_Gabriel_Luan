import psycopg2
import time
from utils import Query
    
#Conectando ao banco de dados    
host="localhost"
database="tp1"
usuario="postgres"
senha="12345"
conector = psycopg2.connect("host=" + host + " dbname=" + database + 
                            " user=" + usuario + " password=" + senha)
cursor = conector.cursor()

#Criação do arquivo de saída
nome_arquivo = 'Queries.txt'
with open(nome_arquivo, 'w') as arquivo:       
    assin = 1885408749
    alternativas = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    for alternativa in alternativas:
        instancia = Query(alternativa, cursor)
        if alternativa in ['A', 'B', 'C']:
            resposta = instancia.query(assin)
            instancia.tabulate_print(resposta, nome_arquivo)
        
        else:
            resposta = instancia.query()
            instancia.tabulate_print(resposta, nome_arquivo)

print('Arquivo Queries.txt criado com sucesso.')

#Dashboard do usuário
escolha = None
while escolha != 'EXIT':
    for query in Query.descricoes:
        print(f'\033[93m{query}) {Query.descricoes[query]}\033[0m\n')
    
    print('\033[93mEXIT ou exit) Sair\033[0m\n')
    
    escolha = input('\nEscolha uma opção:').upper()
    if len(escolha) == 1:
        if escolha in Query.descricoes:
            query = Query(escolha, cursor)
            if escolha in ['A', 'B', 'C']:
                codigo = input('Digite o código do produto: ')
                if len(codigo) != 10:
                    print('Código inválido.')
                    
                else :
                    resusltado = query.query(codigo)
                    query.tabulate_print(resusltado)
          
            else:
                resultado = query.query()
                query.tabulate_print(resultado)  
   
        else:
            print('Opção inválida.')
            
        escolha= input('\nDigite qualquer tecla para continuar ou EXIT para sair: ').upper()
    
    elif escolha != 'EXIT':
        print('Opção inválida.')
        escolha= input('\nDigite qualquer tecla para continuar ou EXIT para sair: ').upper()
    