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

## Configurando

### Pacotes
```bash
chmod +x packs.sh
```
### Docker e Docker Compose

Instalando o [docker desktop e docker compose (Windows, Linux e Mac)](https://www.docker.com/products/docker-desktop/)

Instalando na linha de comando

[Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-pt) e [Docker Compose Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-pt)

#### Como funciona o docker compose

[Docker Compose - Explicado](https://blog.4linux.com.br/docker-compose-explicado/)

### Postgres

Criar pasta `postgres-data` na raiz do projeto. Essa pasta **não deve ser enviada** para o github.

Depois você deve subir o docker-compose com o postgres. Da primeira vez vai demorar um pouco, e fique de olho nos logs para qualquer erro.

```bash
docker-compose up -d
```

### Python

Criar o ambiente virtual

```bash
python3 -m venv .tp1
```

Ativar o ambiente virtual

```bash
source .tp1/bin/activate
```

## Usando o postgres na sua maquina

Após subir, você conseguirá conectar no banco. Ele vem vazio e você terá que preencher ele com o que o trabalho pede.

```bash
psql -h localhost -U postgres
```

As credenciais são:

```yaml
username: postgres
password: postgres
```

## Usando Python

Para instalar bibliotecas necessarias para o trabalho, use o pip [DEPOIS de ativar o ambiente](#python) virtual.

```bash
pip install <biblioteca>
```
