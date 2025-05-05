from fastapi import FastAPI, HTTPException
from model.database import Database
from model.series import MustWatch

app = FastAPI()

db = Database()

@app.get('/')
def read_root():
    return {"Series": "Must Watch"}

@app.get("/{table_name}/{item_id}")
@app.get("/{table_name}")
def read_item(table_name: str, item_id: int = None):
    """
    Consulta uma tabela específica no banco de dados pelo ID.
    """
    db.conectar()

    tabelas_permitidas = {
        'serie' : 'idserie',
        'categoria' : 'idcategoria',
        'ator' : 'idator',
        'motivo_assistir' : 'idmotivo_assistir',
        'avaliacao_serie' : 'idavaliacao_serie',
        'ator_serie' : 'idator_serie',
    }

    coluna_id = tabelas_permitidas.get(table_name)

    try:
        if item_id is None:
            sql = f"SELECT * FROM {table_name}"
            params = ()
        else:
            sql = f"SELECT * FROM {table_name} WHERE {coluna_id} = %s"
            params = (item_id,)

        resultado = db.consultar(sql, params)
        db.desconectar()
        
        if not resultado:
            raise HTTPException(status_code=404, detail="Item não encontrado")

        return resultado
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")
    
@app.post("/{table_name}")
def create_item(table_name: str, item: dict):
    '''Adiciona um item a uma tabela específica no banco de dados'''
    db.conectar()

    try:
        if table_name == 'serie':
            sql = "INSERT INTO serie (titulo, descricao, ano_lancamento, idcategoria) VALUES (%s, %s, %s, %s)"
            params = (item["titulo"], item["descricao"], item["ano_lancamento"], item["idcategoria"])
        elif table_name == 'categoria':
            sql = "INSERT INTO categoria (nome) VALUES (%s)"
            params = (item['nome'],)
        elif table_name == 'ator':
            sql = "INSERT INTO ator (nome) VALUES (%s)"
            params = (item['nome'],)
        elif table_name == 'motivo_assistir':
            sql = "INSERT INTO motivo_assistir (idserie, motivo) VALUES (%s, %s)"
            params = (item['idserie'], item['motivo'])
        elif table_name == 'avaliacao_serie':
            sql = "INSERT INTO avaliacao_serie (idserie, nota, comentario, data_avaliacao) VALUES (%s, %s, %s, %s)"
            params = (item['idserie'], item['nota'], item['comentario'], item['data_avaliacao'])
        elif table_name == 'ator_serie':
            sql = "INSERT INTO ator_serie (idator, idserie, personagem) VALUES (%s, %s, %s)"
            params = (item['idator'], ['idserie'], item['personagem'])
        else:
            raise HTTPException(status_code=400, detail="Tabela não permitida")

        db.executar(sql, params)
        db.desconectar()

        return {"message": "Item adicionado com sucesso!"}
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar o item: {str(e)}")
    
@app.delete("/{table_name}/{item_id}")
def delete_item(table_name: str, item_id: int):

    '''Remove um item de uma tabela específica no banco de dados'''
    db.conectar()

    try:
        tabelas_permitidas = {
            'serie' : 'idserie',
            'categoria' : 'idcategoria',
            'ator' : 'idator',
            'motivo_assistir' : 'idmotivo_assistir',
        }

        coluna_id = tabelas_permitidas.get(table_name)

        if coluna_id is None:
            raise HTTPException(status_code=400, detail="Tabela não permitida")

        sql = f"DELETE FROM {table_name} WHERE {coluna_id} = %s"
        params = (item_id,)

        db.executar(sql, params)
        db.desconectar()

        return {"message": "Item removido com sucesso!"}
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=f"Erro ao remover o item: {str(e)}")

@app.put("/{table_name}/{item_id}")
def update_item(table_name: str, item_id: int, item: dict):
    """
    Atualiza um item em uma tabela específica no banco de dados.
    """
    db.conectar()

    try:
        # Tabelas permitidas e suas colunas de ID
        tabelas_permitidas = {
            'serie': 'idserie',
            'categoria': 'idcategoria',
            'ator': 'idator',
            'motivo_assistir': 'idmotivo_assistir',
            'avaliacao_serie': 'idavaliacao_serie',
            'ator_serie': 'idator_serie',
        }

        # Verifica se a tabela é permitida
        coluna_id = tabelas_permitidas.get(table_name)
        if coluna_id is None:
            raise HTTPException(status_code=400, detail="Tabela não permitida")

        # Verifica se o dicionário `item` não está vazio
        if not item:
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")

        # Monta a consulta SQL dinamicamente
        set_clause = ", ".join([f"{key} = %s" for key in item.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {coluna_id} = %s"
        params = tuple(item.values()) + (item_id,)

        # Executa a consulta
        db.executar(sql, params)
        db.desconectar()

        return {"message": "Item atualizado com sucesso!", "data": item}
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar o item: {str(e)}")