import os
import psycopg2

# from tests.db.celery.tasks import fetch_json
from dotenv import load_dotenv

load_dotenv()


# def test_celery_task(test_json_urls):
#     try:
#         for url in test_json_urls:
#             assert fetch_json.delay(url).get(timeout=30)
#     except Exception as e:  # noqa
#         pass

#     assert False


# def test_create_task(test_json_urls, celery_app, celery_worker):
#     for url in test_json_urls:
#         assert fetch_json.delay(url).get(timeout=30)


def test_create_task(celery_app, celery_worker):
    @celery_app.task
    def mul(x, y):
        return x * y

    assert mul.delay(4, 4).get(timeout=10) == 16


def test_create_table(create_test_table_sql, get_test_table_sql):
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

        if len(curs.fetchall()) > 0:  # verify it exists
            assert True

    except Exception as e:  # noqa
        pass

    assert False
