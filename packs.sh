#!/bin/bash

# Instalação das bibliotecas Python
pip install tabulate psycopg2

# Instalação da biblioteca libpq-dev 
sudo apt-get install --reinstall libpq-dev

# Instalação do psycopg-extra 
pip install psycopg2[extras]

echo "Instalação concluída."
