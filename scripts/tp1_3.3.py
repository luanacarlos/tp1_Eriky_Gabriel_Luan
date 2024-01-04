import psycopg2
import time
from utils import Query
    
host="localhost"
database="tp1"
usuario="postgres"
senha="12345"
conector = psycopg2.connect("host=" + host + " dbname=" + database + 
                            " user=" + usuario + " password=" + senha)
cursor = conector.cursor()

nome_arquivo = 'Queries.txt'

with open(nome_arquivo, 'w') as arquivo:       
    assin = input('\033[95mDigite o codigo Assin para gerar as queryes A, B e C que necesitam de Assin: \033[0m')
    alternativas = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    for alternativa in alternativas:
        instancia = Query(alternativa, cursor)
        if alternativa == 'A':
            resposta1, resposta2 = instancia.query(assin)
            instancia.tabulate_print(resposta1, nome_arquivo, flag=True)
            instancia.tabulate_print(resposta2, nome_arquivo, flag=False)
            
        elif alternativa == 'B' or alternativa == 'C':
            resposta = instancia.query(assin)
            instancia.tabulate_print(resposta, nome_arquivo)
        
        else:
            resposta = instancia.query()
            instancia.tabulate_print(resposta, nome_arquivo)


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
                    if escolha == 'A':
                        resultado1, resultado2 = query.query(codigo)
                        print('\033[92m5 reviews mais úteis:\033[0m')
                        query.tabulate_print(resultado1)
                        print('\n\033[92m5 reviews menos úteis:\033[0m')
                        query.tabulate_print(resultado2)                      
                    
                    else:
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
    