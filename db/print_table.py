import psycopg2
from psycopg2.errors import SerializationFailure
import time
from env import auth_key


def print_tables(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM speech_segments")
        rows = cur.fetchall()
        conn.commit()

        print(f"Speech Segment at {time.asctime()}:")
        for row in rows:
            print(row)

        cur.execute("SELECT * FROM phrases")
        rows = cur.fetchall()
        conn.commit()

        print(f"Phrases at {time.asctime()}:")
        for row in rows:
            print(row)


def print_speech_segments(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM speech_segments")
        rows = cur.fetchall()
        conn.commit()

        print(f"Speech Segment at {time.asctime()}:")
        for row in rows:
            print(row)


def print_phrases(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM phrases")
        rows = cur.fetchall()
        conn.commit()

        print(f"Phrases at {time.asctime()}:")
        for row in rows:
            print(row)


conn = psycopg2.connect(auth_key)
print_tables(conn)