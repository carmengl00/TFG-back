import psycopg2
import pytest
from django.db import connections
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def run_sql(sql):
    conn = psycopg2.connect(database="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings

    settings.DATABASES["default"]["NAME"] = "backend"
    run_sql("DROP DATABASE IF EXISTS backend-test")
    run_sql("CREATE DATABASE backend-test TEMPLATE backend")
    yield
    for connection in connections.all():
        connection.close()
    run_sql("DROP DATABASE backend-test")
