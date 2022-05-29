import psycopg2
from psycopg2.errors import SerializationFailure
# import logging


def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS speech_segments ( \
                segment_id INT PRIMARY KEY, \
                time_stamp DATE, \
                full_text TEXT, \
                max_danger TEXT, \
                min_danger TEXT, \
                avg_danger TEXT \
            )"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS phrases ( \
                phraseid INT PRIMARY KEY, \
                segment_id INT, \
                phrase TEXT, \
                danger TEXT, \
                danger_precise DECIMAL \
            )"
        )
        # logging.debug("create_accounts(): status message: %s",
        #               cur.statusmessage)
    conn.commit()


db_url = ''
conn = psycopg2.connect(db_url)

create_tables(conn)
