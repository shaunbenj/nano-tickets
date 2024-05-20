import mysql.connector
import os

class Cursor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        db_host = os.getenv('DATABASE_HOST', 'localhost') 
        db_port = os.getenv('DATABASE_PORT', '3306')   
        db_user = os.getenv('DATABASE_USER', 'root')     
        db_password = os.getenv('DATABASE_PASSWORD', 'password')  
        db_name = os.getenv('DATABASE_NAME', 'mydatabase')   
        self._connection = mysql.connector.connect(
            host = db_host,
            user = db_user,
            password = db_password,
            port = db_port,
            database = db_name,
            autocommit=True,
        )
        print("[Cursor] MySQL connected")
        self._cursor = self._connection.cursor(dictionary=True)

    def insert(self, table_name, params):
        col_names = ", ".join(params)
        values = ")s, %(".join(params)
        print(f"values {values}")
        query = f"INSERT INTO {table_name} (" + col_names + ") VALUES (%(" + values + ")s);"
        return self.execute(query, params)
        

    def execute(self, query, params = {}):
        print(f"[Cursor] MySQL Execute {query} {params}")
        try:
            self._cursor.execute(query, params)
        except mysql.connector.Error as e:
            if e.errno == 1051:
                print("[Cursor] MySQL table or index does not exist")
                return ValueError("MySQL table or index does not exist")
            else:
                print(f"[Cursor] Error {e}")
                return e
        if query.startswith("SELECT"):
            return self._cursor.fetchall()
        else:
            return self._cursor.lastrowid
        
    def transaction(self):
        print("[Cursor] Starting MySQL transaction")
        return TransactionManager(self._connection)

class TransactionManager:
    def __init__(self, connection):
        self._connection = connection

    def __enter__(self):
        print("[TransactionManager] Starting MySQL transaction")
        self._connection.autocommit = False
        self._connection.start_transaction()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            print("[TransactionManager] Committing MySQL transaction")
            self._connection.commit()
            return True
        else:
            print(f"[TransactionManager] MySQL transaction failed: {exc_type}, {exc_value}")
            self._connection.rollback()
            self._connection.autocommit = True
            print("[TransactionManager] MySQL transaction rolled back")
            return False


            
