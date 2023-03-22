import sqlite3


class DatabaseActor:
    def __init__(self, path_to_db: str):
        self.connection = sqlite3.connect(path_to_db)
        self.cursor = self.connection.cursor()

    def init_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user(
                discord_id TEXT NOT NULL UNIQUE
                );
            """)  # discord_id replaces the need for a primary key
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS roll_alias(
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                alias TEXT NOT NULL,
                roll_expression TEXT
                );
            """)

    def save_user(self, discord_id: str):
        self.cursor.execute(
            "INSERT INTO user (discord_id) VALUES (?);",
            (discord_id,)
            )
        self.connection.commit()

    def save_roll(self, discord_id: str, alias: str, roll_expression: str):
        self.cursor.execute("""
            INSERT INTO roll_alias (user_id, alias, roll_expression)
                VALUES (?, ?, ?);
            """,
            (discord_id, alias, roll_expression)
            )
        self.connection.commit()
