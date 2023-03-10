import os
from os.path import join, dirname
import sqlite3

import pytest

from yogsobot.database.utills import init_tables


DIR = dirname(__file__)
PATH_TO_DB = join(DIR, "test.db")
db_connection = sqlite3.connect(PATH_TO_DB)
db_curs = db_connection.cursor()

def test_add_tables_when_tables_not_present():
    init_tables(db_curs)
    res = db_curs.execute("SELECT name FROM sqlite_master")
    assert res.fetchone() is not None
    db_curs.close()
    db_connection.close()
    try:
        testdb = join(DIR, "test.db")
        os.remove(testdb)
    except OSError as e:
        raise OSError(f"File: {e.filename} not found, therefore can't remove. {e.strerror}")


def test_does_not_add_tables_when_present():
    # TODO: implement
    pass