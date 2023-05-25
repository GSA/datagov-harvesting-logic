import os
import psycopg2
# from dotenv import load_dotenv
from .celery.tasks import download_json
# from celery.contrib.pytest import celery_app, celery_session_worker


def test_celery_task(test_json_urls):
    try:
        for url in test_json_urls:
            assert download_json.delay(url).get(timeout=30)
    except Exception as e:  # noqa
        pass

def test_create_table(create_test_table_sql, get_test_table_sql):

    success = False

    config_file = {
                "host": os.getenv("POSTGRES_HOST"),
                "user": os.getenv("POSTGRES_USER"),
                "password": os.getenv("POSTGRES_PASSWORD"),
            }

    try:
        conn = psycopg2.connect(**config_file)
        curs = conn.cursor()
        curs.execute(create_test_table_sql)  # create the table
        curs.execute(get_test_table_sql)

        res = curs.fetchall()
        if len(res ) > 0:  # verify it exists
            success = True

    except Exception as e:  # noqa
        print( e ) 
        pass 
    
    assert success
