import os
import functools
import pg8000


def uses_db(f):
    @functools.wraps(f)
    def inner_f(cls, *args, **kwargs):
        db_host = os.environ['POSTGRES_HOST'] if 'POSTGRES_HOST' in os.environ else 'localhost'
        db_user = os.environ['POSTGRES_USER'] if 'POSTGRES_USER' in os.environ else 'radionica'
        db_port = int(os.environ['POSTGRES_PORT']) if 'POSTGRES_PORT' in os.environ else 5432
        db_pass = os.environ['POSTGRES_PASS'] if 'POSTGRES_PASS' in os.environ else 'P4ss'
        conn = pg8000.connect(user=db_user, password=db_pass, host=db_host, database=db_user, port=db_port)
        cursor = conn.cursor()

        returns = f(cls, cursor, *args, **kwargs)

        cursor.close()
        conn.commit()
        return returns
    return inner_f


def row_to_node(row, show_status=False):
    if not row:
        return False
    returns = {
        "name": row[0],
        "address": row[1]
    }
    if show_status:
        returns['status'] = row[2]
    return returns


class Nodes:
    @uses_db
    def __init__(self, cursor):
        pass

    @uses_db
    def bootstrap(self, cursor):
        cursor.execute("DROP TABLE IF EXISTS nodes")
        cursor.execute("CREATE TABLE IF NOT EXISTS nodes \
                      (name TEXT, address TEXT, status TEXT)")

    @uses_db
    def get_all(self, cursor, show_status=False):
        cursor.execute("SELECT * FROM nodes")
        return [row_to_node(row, show_status) for row in cursor.fetchall()]

    @uses_db
    def get_new(self, cursor):
        cursor.execute("SELECT * FROM nodes WHERE status='new'")
        return row_to_node(cursor.fetchone())

    @uses_db
    def register_node(self, cursor, name, address):
        cursor.execute("SELECT * FROM nodes WHERE name=%s AND address=%s", (name, address))
        if len(cursor.fetchall()):
            print("Node already registered")
            return

        cursor.execute("SELECT * FROM nodes WHERE name=%s", (name, ))
        if len(cursor.fetchall()):
            print("Node with same name already registered")
            cursor.execute("UPDATE nodes SET status='new', address=%s WHERE name=%s", (address, name))
            return

        cursor.execute("SELECT * FROM nodes WHERE address=%s", (address, ))
        if len(cursor.fetchall()):
            print("Node with same address already registered")
            cursor.execute("UPDATE nodes SET status='new', name=%s WHERE address=%s", (name, address))
            return

        cursor.execute("INSERT INTO nodes (name, address, status) VALUES (%s, %s, 'new')", (name, address))
        print("Node registered")

    @uses_db
    def mark_as_checked(self, cursor, name, address):
        cursor.execute("UPDATE nodes SET status='checked' WHERE name=%s AND address=%s", (name, address))

    @uses_db
    def delete_node(self, cursor, name):
        cursor.execute("DELETE FROM nodes WHERE name=%s AND node_type='external'", (name, ))
