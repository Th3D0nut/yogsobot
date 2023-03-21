import sqlite3


class DatabaseActor:
    def __init__(self, path_to_db):
        self.connection = sqlite3.connect(path_to_db)
        self.cursor = self.connection.cursor()

    def init_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user(
                id INTEGER PRIMARY KEY,
                discord_id TEXT NOT NULL UNIQUE
                );
            """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS roll_alias(
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                roll TEXT
                );
            """)

    def save_user(self, discord_id):
        self.cursor.execute(
            "INSERT INTO user (discord_id) VALUES (?);",
            (discord_id,)
            )
        self.connection.commit()
