import os
from datagovharvester.utils.celery import fetch_url
from datagovharvester.utils.db_utilities import get_db_conn, get_cursor, execute_sql
from dotenv import load_dotenv

load_dotenv()


def test_celery_task():
    try:
        resp = fetch_url()
        assert resp.status_code == 200
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
        conn = get_db_conn(connect_props)
        curs = get_cursor(conn)
        execute_sql(curs, create_test_table_sql)  # create the table
        execute_sql(curs, get_test_table_sql)

        if len(curs.fetchall()) > 0:  # verify it exists
            success = True

    except Exception as e:
        e = e  # to pass ruff
        # print(e)

    assert success
