import psycopg2
from psycopg2.errors import SerializationFailure
from datetime import datetime
from env import auth_key


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

conn = psycopg2.connect(auth_key)

# insert_into_speech_segments(conn, [str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")), "This is going to be the full text", "VERY MUCH DANGEROUS", "NOT VERY MUCH SO", "AVERAGE DANGER"])
# insert_into_phrases(conn, [1, "some phrase", "HIGHHHH", 1.23])