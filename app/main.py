from typing import Union # une duas informações
import sqlite3 
from fastapi import FastAPI, HTTPException
from model import Database # importa a classe Database do arquivo model/database.py

app = FastAPI() # instancia a aplicação

# DATABASE = 'app/database.db' # define o banco de dados

@app.get('/') # define a rota raiz
def read_hello():
    return {"Series": "Must Watch"} # retorna um dicionário com a mensagem "Must " -> json

# @app.get('/items/{item_id}/{query}') # define a rota com um parâmetro item_id
# def read_item(item_id: int, query: Union[str, None] = None):
#     return {"item_id": item_id, "query": query}

# @app.get('/series/{series_id}') # define a rota com um parâmetro series_id
# def read_series(series_id:int, query: Union[str, None] = None):
#     return {"series_id": series_id, "query": query}

# @app.get('/series/{series_id}/{query}')  # Define a rota com um parâmetro series_id
# def read_series(series_id: int, query: Union[str, None] = None):

#     # Conecta ao banco de dados usando a função do arquivo database
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()

#     # Executa a consulta SQL para buscar a série pelo ID
#     cursor.execute("SELECT * FROM serie WHERE id = ?", (series_id,))
#     row = cursor.fetchone()

#     # Fecha a conexão
#     conn.close()

#     # Verifica se a série foi encontrada
#     if row is None:
#         raise HTTPException(status_code=404, detail="Série não encontrada")

#     # Retorna os dados da série como um dicionário
#     return {"id": row[0], "titulo": row[1], "desc": row[2], "ano": row[3], "categoria": row[4]}

@app.get('/series/{series_id}')
def read_series(series_id: int):
    db = Database()
    db.conectar()

    # Consulta a série pelo ID
    sql = "SELECT * FROM serie WHERE id = %s"
    params = (series_id,)
    resultado = db.consultar(sql, params)

    db.desconectar()

    if not resultado:
        raise HTTPException(status_code=404, detail="Série não encontrada")

    return resultado[0]  # Retorna o primeiro resultado como JSON