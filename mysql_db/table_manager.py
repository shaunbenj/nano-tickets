from mysql_db.cursor import Cursor

TABLE_CREATION = {
    "Users": '''CREATE TABLE IF NOT EXISTS Users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password BINARY(60) NOT NULL
            );''',
    "Events":  '''CREATE TABLE IF NOT EXISTS Events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL,
                time DATETIME NOT NULL,
                description VARCHAR(255) NOT NULL,
                creator_id INT NOT NULL
            );''',
    "Tickets": '''CREATE TABLE IF NOT EXISTS Tickets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                description VARCHAR(255) NOT NULL,
                price DECIMAL(12, 2) NOT NULL,
                event_id INT NOT NULL
            );''',
}

# Used to build and delete tables.
class TableManager:
    def __init__(self) -> None:
        self.mysql_db = Cursor()

    def build_all(self):
        for table in TABLE_CREATION:
            try:
                self.mysql_db.execute(TABLE_CREATION[table])
            except ValueError as e:
                next

    def delete_all(self):
        for table in TABLE_CREATION:
            self.mysql_db.execute(f"DROP TABLE {table};")

    def delete_table(self, table):
        if table not in TABLE_CREATION:
            raise ValueError(f"Invalid table f{table}")
        self.mysql_db.execute("DROP TABLE %s;", table)

    def rebuild_all(self):
        self.delete_all()
        self.build_all()