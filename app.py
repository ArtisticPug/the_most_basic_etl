from flask import Flask, request
from flask.helpers import safe_join
import psycopg2


app = Flask(__name__)


@app.route("/")
def db_func():
    conn = psycopg2.connect(dbname='postgres', user='postgres',
                            password='password', host='localhost')
    cursor = conn.cursor()
    item = str(request.args.get("word"))
    item = item.encode('l1').decode()
    query = f'''
        SELECT word FROM 
                    (
                    SELECT word, similarity('{item}', word) AS sml
                    FROM the_database.the_table
                    ORDER BY sml DESC
                    LIMIT 10
                    ) AS the_select;
    '''
    cursor.execute(query)
    the_list = []
    for row in cursor:
        the_list.append(f'{row[0]}\n')

    return f"{''.join(the_list)}"
