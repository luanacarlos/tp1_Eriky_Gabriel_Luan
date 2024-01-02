import psycopg2

host = "localhost"
database = "tp1"
usuario = "postgres"
senha = "12345"

# Conectar ao banco de dados
conector = psycopg2.connect(host=host, dbname=database, user=usuario, password=senha)
cursor = conector.cursor()

# Lista das tabelas na ordem inversa de dependência
tabelas = ['similars', 'cat_produto', 'produto', 'review', 'categoria']

# Desativa a verificação de chaves estrangeiras temporariamente para evitar erros de dependência
cursor.execute('SET session_replication_role = replica;')

# Exclui as tabelas
for tabela in tabelas:
    cursor.execute(f'DROP TABLE IF EXISTS {tabela} CASCADE;')

# Ativa novamente a verificação de chaves estrangeiras
cursor.execute('SET session_replication_role = DEFAULT;')

# Confirma as alterações e fecha a conexão
conector.commit()
conector.close()

print("Tabelas excluídas com sucesso.")