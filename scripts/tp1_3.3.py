import psycopg2
from utils import Query
    
host="localhost"
database="tp1"
usuario="postgres"
senha="12345"
conector = psycopg2.connect("host=" + host + " dbname=" + database + 
                            " user=" + usuario + " password=" + senha)
cursor = conector.cursor()
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
                if escolha == 'A':
                    query1, query2 = query.query(codigo)
                    print('\033[92m5 reviews mais úteis:\033[0m')
                    query.tabulate_print(['Assinatura', 'Nota', 'Úteis', 'Total'], query1)
                

            
            else:
                query.query()
      
        else:
            print('Opção inválida.')
    
    elif escolha != 'EXIT':
        print('Opção inválida.')
