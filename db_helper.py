import psycopg2
from psycopg2 import OperationalError


# Connexion à la bdd
def create_connection(db_name, db_user, db_password, db_host, db_port):
    conn = None
    try:
        conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
    except OperationalError as e:
        print(f"L'erreur '{e}' est survenue !")

    return conn


# Exécution de la requête
def exec_read_query(conn, query):
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"L'erreur '{e}' est survenue !")
