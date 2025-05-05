from model.database import Database
from fastapi import HTTPException
from typing import Optional, List, Tuple, Any 

tabelas_permitidas = {
        'serie' : 'idserie',
        'categoria' : 'idcategoria',
        'ator' : 'idator',
        'motivo_assistir' : 'idmotivo_assistir',
        'avaliacao_serie' : 'idavaliacao_serie',
        'ator_serie' : 'idator_serie',
}

db = Database()

class MustWatch:
    def __init__(self, table_name: str, item: dict, item_id: int = None):
        """Construtor da classe Serie."""
        self.table_name = table_name
        self.item = item
        self.item_id = item_id
        self.coluna_id = tabelas_permitidas.get(table_name)

    def consultarTabela(self):
        """Consulta uma tabela específica no banco de dados pelo ID."""
        try:
            if self.item_id is None:
                sql = f"SELECT * FROM {self.table_name}"
                params = ()
            else:
                sql = f"SELECT * FROM {self.table_name} WHERE {self.coluna_id} = %s"
                params = (self.item_id,)

            resultado = db.consultar(sql, params)
            db.desconectar()
            
            if not resultado:
                raise HTTPException(status_code=404, detail="Item não encontrado")

            return resultado
        except Exception as e:
            db.desconectar()
            raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")
    

    @staticmethod # decorador -> não precisa instanciar a classe para usar o método
    def listarTarefas():
        """Retornar uma lista com todas as tarefas já cadastradas."""
        db = Database()
        db.conectar()

        sql = 'SELECT id, titulo, data_conclusao FROM tarefa'
        tarefas = db.consultar(sql)
        db.desconectar()
        return tarefas if tarefas else [] # Se tarefas for None, retorna uma lista vazia -> moderna, só funciona em Python
    
    @staticmethod
    def apagarTarefa(idTarefa):
        """Apaga uma tarefa cadastrada no banco de dados."""
        db = Database()
        db.conectar()

        sql = 'DELETE FROM tarefa WHERE id = %s'
        params = (idTarefa,) # Precisa passar como tupla? SIM! -> espera 1 ou mais valores
        db.executar(sql, params)
        db.desconectar()

    @staticmethod
    def buscarTarefa(idTarefa):
        """Busca uma tarefa pelo ID no banco de dados."""
        db = Database()
        db.conectar()
        sql = 'SELECT id, titulo, data_conclusao FROM tarefa WHERE id = %s'
        params = (idTarefa,)
        resultado = db.consultar(sql, params)
        db.desconectar()
        return resultado if resultado else None
        

    def editarTarefa(idTarefa, titulo, data_conclusao):
        """Editar uma tarefa cadastrada no banco de dados."""
        db = Database()
        db.conectar()

        sql = 'UPDATE tarefa SET titulo = %s, data_conclusao = %s WHERE id = %s'
        params = (titulo, data_conclusao, idTarefa) # Precisa passar como tupla? SIM! -> espera 1 ou mais valores
        db.executar(sql, params)
        db.desconectar()