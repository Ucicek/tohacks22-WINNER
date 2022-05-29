import psycopg2
from psycopg2.errors import SerializationFailure
from env import auth_key


def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS speech_segments ( \
                    segment_id INT PRIMARY KEY NOT NULL, \
                    time_stamp TEXT, \
                    full_text TEXT, \
                    max_danger TEXT, \
                    min_danger TEXT, \
                    avg_danger TEXT \
                )
            """
        )
    conn.commit()

    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS phrases ( \
                    phraseid INT PRIMARY KEY NOT NULL, \
                    segment_id INT, \
                    phrase TEXT, \
                    danger TEXT, \
                    danger_precise DECIMAL, \
                    FOREIGN KEY (segment_id) REFERENCES speech_segments(segment_id) \
                )
            """
        )
    conn.commit()


# conn = psycopg2.connect(auth_key)
# create_tables(conn)
