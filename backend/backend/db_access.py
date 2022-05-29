import psycopg2
from psycopg2.errors import SerializationFailure
import time


def get_conn():
    auth_key='postgresql://rayaq:J6qmyvR3OjIHYKixv3kIYQ@free-tier14.aws-us-east-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dtohacks22-2356'
    conn = psycopg2.connect(auth_key)
    return conn


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


def delete_tables(conn):
    with conn.cursor() as cur:
        cur.execute("DROP TABLE phrases;")
        cur.execute("DROP TABLE speech_segments;")
    conn.commit()


# value is an arr/tuple of 5 elements
def insert_into_speech_segments(conn, value):
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT segment_id FROM speech_segments ORDER BY segment_id DESC LIMIT 1")
        id = 1 if not cur.fetchall() else cur.fetchall()[0][0] + 1
        conn.commit()

        cur.execute("""INSERT INTO speech_segments \
            (segment_id, time_stamp, full_text, max_danger, min_danger, avg_danger) \
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (id, value[0], value[1], value[2], value[3], value[4]))
    conn.commit()


# value is an arr/tuple of 4 elements
def insert_into_phrases(conn, value):
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT phraseid FROM phrases ORDER BY phraseid DESC LIMIT 1")
        id = 1 if not cur.fetchall() else cur.fetchall()[0][0] + 1
        conn.commit()

        cur.execute("""INSERT INTO phrases \
            (phraseid, segment_id, phrase, danger, danger_precise) \
            VALUES (%s, %s, %s, %s, %s); \
        """, (id, value[0], value[1], value[2], value[3]))
    conn.commit()


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


# we are going to get access to all of the values in the database
def get_table_values(conn):
    with conn.cursor() as cur:
        cur.execute("""SELECT segment_id, time_stamp, full_text, min_danger, max_danger, avg_danger FROM (
                SELECT * FROM speech_segments
                ORDER BY segment_id DESC
            ) SQ
            ORDER BY segment_id ASC
        """)
        speech_segments = cur.fetchall()
        speech_segments = reversed(speech_segments)
        conn.commit()

        print(speech_segments)

        cur.execute("""SELECT * FROM (
                SELECT * FROM phrases
                ORDER BY phraseid DESC
            ) SQ
            ORDER BY phraseid ASC
        """)
        phrases = cur.fetchall()
        phrases = reversed(phrases)
        conn.commit()

    return speech_segments, phrases


def get_speech_segments(conn):
    with conn.cursor() as cur:
        cur.execute("""SELECT segment_id, time_stamp, full_text, min_danger, max_danger, avg_danger FROM (
                SELECT * FROM speech_segments
                ORDER BY segment_id DESC
            ) SQ
            ORDER BY segment_id ASC
        """)
        speech_segments = cur.fetchall()
        speech_segments = reversed(speech_segments)
        conn.commit()

    return speech_segments


def get_phrases(conn, pk):
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM (
                SELECT * FROM phrases
                ORDER BY phraseid DESC
            ) SQ
            WHERE segment_id = %s
            ORDER BY phraseid ASC
        """, (str(pk),))
        phrases = cur.fetchall()
        phrases = reversed(phrases)
        conn.commit()

    return phrases

