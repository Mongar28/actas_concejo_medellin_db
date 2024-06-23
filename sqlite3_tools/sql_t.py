import sqlite3 as sql


def create_inteventions_db():
    conection = sql.connect("interventions_concejo_med.db")
    conection.commit()
    conection.close()


def create_authors_table():
    connection = sql.connect("interventions_concejo_med.db")
    cursor = connection.cursor()
    instruction = """
    CREATE TABLE IF NOT EXISTS authors (
        author_id INTEGER PRIMARY KEY AUTOINCREMENT,
        author VARCHAR(50) NOT NULL
    )
    """
    cursor.execute(instruction)
    connection.commit()
    connection.close()


def create_inteventions_table():
    conection = sql.connect("interventions_concejo_med.db")
    cursor = conection.cursor()
    instruction: str = """
    CREATE TABLE IF NOT EXISTS interventions (
            interventions_id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_id INTEGER,
            acta VARCHAR(50) NOT NULL,
            date TEXT NOT NULL,
            intervention TEXT NOT NULL
    )
    """
    cursor.execute(instruction)
    conection.commit()
    conection.close()


def insert_rows_authors(authors_tuples: list):
    conection = sql.connect("interventions_concejo_med.db")
    cursor = conection.cursor()
    instruction: str = """
    INSERT INTO authors VALUES (?, ?)
    """
    cursor.executemany(instruction, authors_tuples)
    conection.commit()
    conection.close()


def insert_rows_interventions(interventions_tuples: list):
    conection = sql.connect("interventions_concejo_med.db")
    cursor = conection.cursor()
    instruction: str = """
    INSERT INTO interventions VALUES (?, ?, ?, ?, ?)

    """
    cursor.executemany(instruction, interventions_tuples)
    conection.commit()
    conection.close()
