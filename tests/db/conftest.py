import pytest
from celery.contrib.pytest import celery_app, celery_worker


@pytest.fixture
def test_json_urls():
    return [
        "https://project-open-data.cio.gov/v1.1/schema/catalog.json",
        "https://data.wa.gov/api/views/f6w7-q2d2/columns.json",
        "https://project-open-data.cio.gov/v1.1/schema/catalog.json",
        "https://healthdata.gov/data.json",
    ]


@pytest.fixture
def test_table_name():
    return "test_table"


@pytest.fixture
def create_test_table_sql(test_table_name):
    return f"""DROP TABLE IF EXISTS {test_table_name}; 
	CREATE TABLE {test_table_name} (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	created_on TIMESTAMP NOT NULL,
    last_login TIMESTAMP );"""


@pytest.fixture
def get_test_table_sql(test_table_name):
    return f"""SELECT * 
	FROM pg_catalog.pg_tables
	WHERE tablename = '{test_table_name}';"""
