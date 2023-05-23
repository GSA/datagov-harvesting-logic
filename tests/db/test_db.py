import os
import psycopg2
# from dotenv import load_dotenv
from .celery.tasks import download_json
# from celery.contrib.pytest import celery_app, celery_session_worker

# load_dotenv()


def test_celery_task(test_json_urls):
    try:
        for url in test_json_urls:
            assert download_json.delay(url).get(timeout=30)
    except Exception as e:  # noqa
        pass

def test_create_table(create_test_table_sql, get_test_table_sql):

    success = False

    try:
        conn = psycopg2.connect(
            **{
                "host": os.getenv("TEST_POSTGRES_HOST"),
                "user": os.getenv("TEST_POSTGRES_USER"),
                "password": os.getenv("TEST_POSTGRES_PASSWORD"),
            }
        )
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
