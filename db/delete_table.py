import psycopg2
from psycopg2.errors import SerializationFailure
from env import auth_key


def delete_tables(conn):
    with conn.cursor() as cur:
        cur.execute("DROP TABLE phrases;")
        cur.execute("DROP TABLE speech_segments;")
    conn.commit()


# conn = psycopg2.connect(auth_key)
# delete_tables(conn)
