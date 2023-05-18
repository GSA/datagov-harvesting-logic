import psycopg2


def get_db_conn(connect_props):
    return psycopg2.connect(**connect_props)


def get_cursor(conn):
    return conn.cursor()


def execute_sql(cursor, sql):
    cursor.execute(sql)
    return cursor
