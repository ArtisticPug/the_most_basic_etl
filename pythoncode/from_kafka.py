import io, chardet, os, codecs, re, json, psycopg2
from kafka import KafkaConsumer
from time import sleep

conn = psycopg2.connect(dbname='postgres', user='postgres',
                        password='password', host='localhost')
cursor = conn.cursor()

consumer = KafkaConsumer(
    'test',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for message in consumer:
    message = message.value
    query = f'''
        INSERT INTO the_database.the_table
        (word)
        VALUES('{message}');

    '''
    try:
        cursor.execute(query)
    except:
        pass
    conn.commit()
