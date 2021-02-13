# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 14:35:28 2021

@author: Pedro
"""

# 1. Criar o script de coleta dos dados (se atentar aos tratamentos de erros)
# Json parser
import json
from urllib.request import urlopen

def queroQuero():
    response = urlopen("http://dataeng.quero.com:5000/caged-data").read().decode('utf-8')
    responseJson = json.loads(response)
    return responseJson.get("caged")

import ujson
quero = ujson.dumps(queroQuero())
print(quero)

# 2. Tratar os dados que foram coletados
# Json to Pandas Dataframe
import pandas as pd

data = pd.read_json(quero)
data.info() # Não precisa de muito tratamento aparentemente

# 3. Criar o banco relacional na sua máquina com a tabela para receber os dados
# Database criado manualmente no MySQL, com o nome 'querosql'
# Este processo de criação do database poderia ser automatizado aqui mesmo no Python, mas não o fiz

# 4. Inserir os dados tratados na tabela criada

# Import dataframe into MySQL
import sqlalchemy

database_username = 'root'
database_password = '******'
database_ip       = 'localhost'
database_name     = 'querosql'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))
data.to_sql(con=database_connection, name='tablesql', if_exists='replace')

# 5. Criar índices na tabela para facilitar a consulta
# Índices já haviam sido criados na transformação do Json em Dataframe
# Logo, não foi necessária a criação de índices nesse passo