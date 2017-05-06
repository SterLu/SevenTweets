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
        db_name = os.environ['POSTGRES_NAME'] if 'POSTGRES_NAME' in os.environ else 'radionica'
        conn = pg8000.connect(user=db_user, password=db_pass, host=db_host, database=db_name, port=db_port)
        cursor = conn.cursor()

        returns = f(cls, cursor, *args, **kwargs)

        cursor.close()
        conn.commit()
        return returns
    return inner_f


def row_to_tweet(row):
    if not row:
        return False
    return {
        "id": row[0],
        "tweet": row[1]
    }


class Storage:
    @uses_db
    def __init__(self, cursor):
        pass

    @uses_db
    def bootstrap(self, cursor):
        cursor.execute("CREATE TABLE tweets (id SERIAL, text TEXT)")
        cursor.execute("INSERT INTO tweets (text) VALUES (%s), (%s), (%s)", (
            "Test tweet 1",
            "Test tweet 2",
            "Test tweet 3"
        ))

    @uses_db
    def get_all(self, cursor):
        cursor.execute("SELECT * FROM tweets")
        return [row_to_tweet(row) for row in cursor.fetchall()]

    @uses_db
    def get_by_id(self, cursor, tweet_id):
        cursor.execute("SELECT * FROM tweets WHERE id=%s", (tweet_id,))
        return row_to_tweet(cursor.fetchone())

    @uses_db
    def save_tweet(self, cursor, tweet_text):
        cursor.execute("INSERT INTO tweets (text) VALUES (%s) RETURNING id, text", (tweet_text,))
        return row_to_tweet(cursor.fetchone())

    @uses_db
    def delete_tweet(self, cursor, tweet_id):
        cursor.execute("DELETE FROM tweets WHERE id=%s", (tweet_id,))
