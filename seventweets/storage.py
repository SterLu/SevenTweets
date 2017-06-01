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


def row_to_tweet(row):
    if not row:
        return False
    if row[2] == 'regular':
        return {
            "id": row[0],
            "tweet": row[1],
            "created": str(row[3])[:16]
        }
    else:
        return {
            "id": row[0],
            "tweet": "Retweet: " + row[1],
            "created": str(row[3])[:16]
        }


class Storage:
    @uses_db
    def __init__(self, cursor):
        pass

    @uses_db
    def bootstrap(self, cursor):
        cursor.execute("CREATE TABLE IF NOT EXISTS tweets (id SERIAL, text TEXT, tweet_type TEXT, \
                                      created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        cursor.execute("CREATE TABLE IF NOT EXISTS api_keys (id SERIAL, key TEXT)")

    @uses_db
    def add_api_key(self, cursor, key):
        cursor.execute("INSERT INTO api_keys (key) VALUES (%s)", (key, ))

    @uses_db
    def get_all(self, cursor):
        cursor.execute("SELECT * FROM tweets WHERE tweet_type='regular'")
        return [row_to_tweet(row) for row in cursor.fetchall()]

    @uses_db
    def get_by_id(self, cursor, tweet_id):
        cursor.execute("SELECT * FROM tweets WHERE id=%s", (tweet_id,))
        return row_to_tweet(cursor.fetchone())

    @uses_db
    def save_tweet(self, cursor, tweet_text):
        cursor.execute("INSERT INTO tweets (text, tweet_type) VALUES (%s, 'regular') \
                        RETURNING id, text, tweet_type, created", (tweet_text,))
        return row_to_tweet(cursor.fetchone())

    @uses_db
    def delete_tweet(self, cursor, tweet_id):
        cursor.execute("DELETE FROM tweets WHERE id=%s", (tweet_id,))

    @uses_db
    def search(self, cursor, query):
        cursor.execute("SELECT * FROM tweets WHERE text LIKE '%%{query}%%' \
                        AND tweet_type='regular' ".format(query=query))
        # TODO: Possible SQL injection vulnerability
        return [row_to_tweet(row) for row in cursor.fetchall()]

    @uses_db
    def get_all_keys(self, cursor):
        cursor.execute("SELECT * FROM api_keys")
        return [row[1] for row in cursor.fetchall()]


def row_to_node(row, show_type=False):
    if not row:
        return False
    returns = {
        "name": row[0],
        "address": row[1]
    }
    if show_type:
        returns['type'] = row[2]
    return returns


class Nodes:
    @uses_db
    def __init__(self, cursor):
        cursor.execute("DROP TABLE IF EXISTS nodes")
        cursor.execute("CREATE TABLE IF NOT EXISTS nodes (name TEXT, address TEXT, node_type TEXT)")

    @uses_db
    def set_self(self, cursor, name, address):
        cursor.execute("DELETE FROM nodes WHERE node_type ='self'")
        cursor.execute("INSERT INTO nodes (name, address, node_type) VALUES (%s, %s, 'self')", (name, address))

    @uses_db
    def get_self(self, cursor):
        cursor.execute("SELECT * FROM nodes WHERE node_type='self'")
        return row_to_node(cursor.fetchone())

    @uses_db
    def get_all(self, cursor):
        cursor.execute("SELECT * FROM nodes")
        return [row_to_node(row, True) for row in cursor.fetchall()]

    @uses_db
    def register_node(self, cursor, name, address):
        # TODO: Check if node with given name or address exists, update if exists, else insert
        cursor.execute("INSERT INTO nodes (name, address, node_type) VALUES (%s, %s, 'external')", (name, address))

    @uses_db
    def get_all_external(self, cursor):
        cursor.execute("SELECT * FROM nodes WHERE node_type='external'")
        return [row_to_node(row) for row in cursor.fetchall()]

    @uses_db
    def delete_node(self, cursor, name):
        cursor.execute("DELETE FROM nodes WHERE name=%s AND node_type='external'", (name, ))
