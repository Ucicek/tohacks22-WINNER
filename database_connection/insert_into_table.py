import psycopg2
from psycopg2.errors import SerializationFailure
from datetime import datetime


# value is an arr/tuple of 5 elements
def insert_into_speech_segments(conn, value):
    with conn.cursor() as cur:
        columns = "(time_stamp, full_text, max_danger, min_danger, avg_danger)"
        vals = f"({value[0]}, {value[1]}, {value[2]}, {value[3]}, {value[4]})"
        cur.execute(f"INSERT INTO speech_segments {columns} VALUES {vals};")
    conn.commit()


# value is an arr/tuple of 4 elements
def insert_into_phrases(conn, value):
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO speech_segments \
            (segment_id, phrase, danger, danger_precise) \
            VALUES ({value[0]}, {value[1]}, {value[2]}, {value[3]}); \
        ")
    conn.commit()

db_url = 'postgresql://rayaq:J6qmyvR3OjIHYKixv3kIYQ@free-tier14.aws-us-east-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dtohacks22-2356'
conn = psycopg2.connect(db_url)

insert_into_speech_segments(conn, [datetime.now(), "This is going to be the full text", "VERY MUCH DANGEROUS", "NOT VERY MUCH SO", "AVERAGE DANGER"])
# insert_into_phrases(conn, [])