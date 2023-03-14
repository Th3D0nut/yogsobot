import os
from os.path import join, dirname
import sqlite3

import pytest

from yogsobot.database.utills import init_tables


DIR = dirname(__file__)
PATH_TO_DB = join(DIR, "test.db")


@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup
    db_connection = sqlite3.connect(PATH_TO_DB)
    db_curs = db_connection.cursor()
    yield db_curs
    # Teardown
    db_curs.close()
    db_connection.close()
    testdb = join(DIR, "test.db")
    os.remove(testdb)


def test_add_tables_when_tables_not_present(run_around_tests):
    db_curs = run_around_tests
    init_tables(db_curs)
    res = db_curs.execute("SELECT name FROM sqlite_master")
    assert res.fetchone() is not None
