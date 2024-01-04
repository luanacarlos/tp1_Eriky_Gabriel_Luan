# Integrantes 
Eriky Rodrigues de Souza - 21950630

Gabriel César Tavares Ferreira - 21854868

Luan Carlos Cunha Loureiro de Alencar - 22051002

# Instalação das dependências

Para instalar as dependências desse projeto basta executar o arquivo `packs.sh` da seguinte forma:
```bash
chmod +x packs.sh
./packs.sh
```

# Como executar o arquivo tp1_3.2.py

Antes de executar esse arquivo é preciso que sejam feitas duas mudanças nesse arquivo

## 1. Editar as variáveis de conexão com o banco de dados
Para fazer isso basta adicionar as informações do postgres que está na máquina que irá rodar o projeto:
```bash
host="localhost"
database="tp1"
usuario="postgres"
senha="12345"
```
## 2. Editar o caminho do arquivo `amazon-meta.txt`
```bash
#Path do arquivo, OBS: mudar o path para o caminho do arquivo amazon-meta.txt da máquina que está rodando o código
path = '../../amazon-meta.txt'
```

## 3. Executar
```bash
python3 tp1_3.2.py
```

# Como executar o arquivo tp1_3.2.py
```bash
python3 tp1_3.3.py
```

