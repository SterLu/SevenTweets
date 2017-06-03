import os
import functools
import pg8000
import requests
import json


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
    def search(self, cursor, query, search_external=False):
        cursor.execute("SELECT * FROM tweets WHERE text LIKE '%%{query}%%' \
                        AND tweet_type='regular' ".format(query=query))
        # TODO: Possible SQL injection vulnerability
        results = [row_to_tweet(row) for row in cursor.fetchall()]
        if search_external:
            from seventweets import nodes
            Nodes = nodes.Nodes()
            nodes = Nodes.get_all()
            print(nodes)
            for node in nodes:
                print(node)
                try:
                    address = node['address'] + '/search/?content=' + query
                    if address[:4] != "http":
                        address = "http://" + address
                    print(address)
                    res = requests.get(address)
                    returned_tweets = json.loads(res.text)
                    print(returned_tweets)
                    results.append(returned_tweets)
                except requests.exceptions.RequestException as e:
                    print(e)
                except json.decoder.JSONDecodeError as e:
                    print(e)
        return results

    @uses_db
    def get_all_keys(self, cursor):
        cursor.execute("SELECT * FROM api_keys")
        return [row[1] for row in cursor.fetchall()]
