import mysql.connector as mc # Importando a biblioteca do conector do MYSQL
from mysql.connector import Error, MySQLConnection # Importando a classe Error para tratar as mensagens de erro do código
from dotenv import load_dotenv # Importando a função load_dotenv
from os import getenv # Importando a função getenv
from typing import Optional, Any, Tuple, List # Importando as funções Optional, Any, Tuple e List para trabalhar com tipos de dados

class Database:
    def __init__(self) -> None: # método construtor. retorna None (nada)
        load_dotenv()
        self.host: str = getenv('DB_HOST') # Declaração de variáveis que se referem a própria classe (variáveis de ambiente)
        self.username: str = getenv('DB_USER')
        self.password: str = getenv('DB_PSWD')
        self.database: str = getenv('DB_NAME')
        self.connection: Optional[MySQLConnection] = None # Inicialização da conexão -> variavel connection existe, mas não tem nada ainda. Conexão é uma ponte entre o programa e o banco de dados
        self.cursor: Optional[List[dict]] = None # Inicialização do cursor. É o mensageiro entre o programa e o banco de dados. Ele é quem executa as instruções SQL. 

    def conectar(self) -> None:
        """Estabelece uma conexão com o banco de dados."""
        try:
            self.connection = mc.connect( # conecta a variavel da classe com o método do MYSQL.connector
                host = self.host, # self = atributo do objeto. Faz com que o objeto execute algo com ele mesmo
                database = self.database,
                user = self.username,
                password = self.password
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary = True)
                print("Conexão ao banco de dados realizada com sucesso!")
        except Error as e:
            print(f'Erro de conexão: {e}')
            self.connection = None
            self.cursor = None

    def desconectar(self) -> None:
        """Encerra a conexão com o banco de dados e o cursor, se existirem."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Conexão com o banco de dados encerrada com sucesso!")

    def executar(self, sql: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[List[dict]]: # variável parametros existe para que as pessoas não façam destruam a dayabase. '...' aplica a todos os elementos da tupla
        """Executa uma instrução no banco de dados"""
        if self.connection is None and self.cursor is None:
            print('Conexão ao banco de dados não estabelecida!')
            return None
        
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            return self.cursor
        except Error as e:
            print(f'Erro de execução: {e}')
            return None
        
    def consultar(self, sql: str, params: Optional[Tuple[Any,...]] = None) -> Optional[List[dict]]: # variável parametros existe para que as pessoas não façam destruam a database -> proteção de MySQL Injection
        """Executa uma consulta no banco de dados"""
        if self.connection is None and self.cursor is None:
            print('Conexão ao banco de dados não estabelecida!')
            return None
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f'Erro de execução: {e}')
            return None