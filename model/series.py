from datetime import date
from xml.dom.expatbuilder import Rejecter
from model.database import Database
from fastapi import HTTPException
from pydantic import BaseModel, ValidationError
from typing import Optional

tabelas_permitidas = {
        'serie' : 'idserie',
        'categoria' : 'idcategoria',
        'ator' : 'idator',
        'motivo_assistir' : 'idmotivo_assistir',
        'avaliacao_serie' : 'idavaliacao_serie',
        'ator_serie' : 'idator_serie',
}

db = Database()

class Serie(BaseModel):
    idserie: Optional[int] = None
    idcategoria: Optional[int] = None
    idator: Optional[int]  = None
    idmotivo_assistir: Optional[int] = None
    idavaliacao_serie: Optional[int] = None
    idator_serie: Optional[int] = None

    titulo: Optional[str] = None
    descricao: Optional[str] = None
    ano_lancamento: Optional[int] = None
    
    nome: Optional[str] = None
    motivo: Optional[str] = None
    nota: Optional[int] = None
    comentario: Optional[str] = None
    data_avaliacao: Optional[date] = None
    
    personagem: Optional[str] = None

class MustWatch:
    def __init__(self, table_name: str, item: dict, item_id: int = None):
        """Construtor da classe MustWatch."""
        self.table_name = table_name
        self.item = item
        self.item_id = item_id
        self.coluna_id = tabelas_permitidas.get(table_name)
        
    def consultarSerie(self):
        """Consulta uma tabela específica no banco de dados pelo ID."""
        db.conectar()

        try:
            if self.table_name not in tabelas_permitidas:
                raise HTTPException(status_code=406, detail="Tabela não encontrada")
                # Erro 406: Not Acceptable 

            if self.item_id is None:
                sql = f"SELECT * FROM {self.table_name}"
                params = ()

            else:
                sql = f"SELECT * FROM {self.table_name} WHERE {self.coluna_id} = %s"
                params = (self.item_id,)

            resultado = db.executar_consulta(sql, params, fetch=True)

            if not resultado:
                raise HTTPException(status_code=404, detail="Item não encontrado")
                # Erro 404: Not Found

            if resultado and isinstance(resultado, list): # Verifica se o resultado é uma lista
                return resultado
            
            else:
                raise HTTPException(status_code=406, detail="Erro de formato na resposta")
                # Erro 406: Not Acceptable
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")
            # Erro 500: Internal Server Error
        
        finally:
            db.desconectar()

    def inserirSerie(self):
        """Adiciona um item a uma tabela específica no banco de dados."""
        db.conectar()

        try:
            if not self.item:
                raise HTTPException(status_code=400, detail="Nenhum dado fornecido para adicionar.")
            # Erro 400: Bad Request

            colunas = ', '.join(self.item.keys()) # para cada chave do dicionário, cria uma string no formato "chave", separando por vírgula
            valores = ', '.join(['%s'] * len(self.item)) # para cada valor do dicionário, cria uma string no formato "%s", separando por vírgula
            sql = f"INSERT INTO {self.table_name} ({colunas}) VALUES ({valores})"
            params = tuple(self.item.values())
            
            try:
                validacao = Serie(**self.item) # Valida os dados do dicionário
                db.executar_consulta(sql, params)
                db.desconectar()
                return validacao
            except ValidationError:
                raise HTTPException(status_code=406, detail="Erro de validação na tipagem. Tente inserir valores de outros tipos.")
                # Erro 406: Not Acceptable

        except Exception as e:
            db.desconectar()
            raise HTTPException(status_code=500, detail=f"Erro ao adicionar o item: {str(e)}")
            # Erro 500: Internal Server Error
        
    def removerSerie(self):
        '''Remove um item de alguma lista do banco de dados'''
        db.conectar()

        try:
            if self.coluna_id is None:
                raise HTTPException(status_code=406, detail="Mudança não permitida (Não foi atribuído um ID)")
                # Erro 406: Not Acceptable
            sql = f"DELETE FROM {self.table_name} WHERE {self.coluna_id} = %s"
            params = (self.item_id,)

            db.executar_consulta(sql, params)
            db.desconectar()

        except Exception as e:
            db.desconectar()
            raise HTTPException(status_code=500, detail=f"Erro ao remover o item: {str(e)}")
        
    def atualizarSerie(self):
        '''Atualiza um item de alguma lista do banco de dados'''
        db.conectar()

        try:
            if self.coluna_id is None:
                raise HTTPException(status_code=406, detail="Mudança não permitida (Não foi atribuído um ID)")
                # Erro 406: Not Acceptable
            if not self.item:
                raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")
                # Erro 400: Bad Request
            
            atualizacao = ", ".join([f"{key} = %s" for key in self.item.keys()]) # para cada chave do dicionário, cria uma string no formato "chave = %s", separando por vírgula
            sql = f"UPDATE {self.table_name} SET {atualizacao} WHERE {self.coluna_id} = %s"
            params = tuple(self.item.values()) + (self.item_id,)

            try:
                validacao = Serie(**self.item) # Valida os dados do dicionário
                db.executar_consulta(sql, params)
                db.desconectar()
                return validacao
            except ValidationError:
                raise HTTPException(status_code=406, detail="Erro de validação na tipagem. Tente inserir valores de outros tipos.")
                # Erro 406: Not Acceptable

        except Exception as e:
            db.desconectar()
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar o item: {str(e)}")