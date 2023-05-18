import os
import psycopg2
from tests.db.celery.tasks import fetch_url
from dotenv import load_dotenv

load_dotenv()


def test_celery_task(test_json_urls):
    try:
        for url in test_json_urls:
            assert len(fetch_url.delay(url).get(timeout=30)) > 0
    except Exception as e:
        e = e
        assert False


def test_create_table(create_test_table_sql, get_test_table_sql):
    success = False

    connect_props = {
        "host": os.getenv("TEST_POSTGRES_HOST"),
        "user": os.getenv("TEST_POSTGRES_USER"),
        "password": os.getenv("TEST_POSTGRES_PASSWORD"),
    }

    try:
        conn = psycopg2.connect(**connect_props)
        curs = conn.cursor()
        curs.execute(create_test_table_sql)  # create the table
        curs.execute(get_test_table_sql)

        if len(curs.fetchall()) > 0:  # verify it exists
            success = True

    except Exception as e:
        print(e)

    assert success
