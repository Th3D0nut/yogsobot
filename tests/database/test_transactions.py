import os
from os.path import join, dirname
import sqlite3

import pytest

from yogsobot.database.transactions import DatabaseActor


PATH_TO_DB = join(dirname(__file__), "test.db")


@pytest.fixture()
def db():
    # Setup
    db = DatabaseActor(PATH_TO_DB)
    yield db
    # Teardown
    db.cursor.close()
    db.connection.close()
    testdb = join(PATH_TO_DB)
    os.remove(testdb)


# init_tables tests
def test_init_tables_creates_user_and_roll_alias_tables(db):
    db.init_tables()

    table_names = db.cursor.execute("""
        SELECT name FROM sqlite_master
            WHERE name = 'user' OR name = 'roll_alias'
    """)
    assert len(table_names.fetchall()) == 2


# save_user tests
def test_does_not_save_user_that_already_exist(db):
    db.init_tables()
    db.save_user(discord_id="12345678")

    with pytest.raises(sqlite3.IntegrityError):
        db.save_user(discord_id="12345678")


# tests
def test_find_roll_in_db_after_saving_it(db):
    db.init_tables()
    db.save_user(discord_id="12345678")
    db.save_roll(discord_id="12345678", alias="fireball", roll_expression="2d8 d10")

    discord_id = db.cursor.execute("""SELECT user_id, alias FROM roll_alias
        WHERE user_id = 12345678 AND alias = 'fireball';
    """)
    assert discord_id.fetchone() == ("12345678", "fireball")
