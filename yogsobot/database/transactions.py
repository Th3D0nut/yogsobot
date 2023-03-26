import sqlite3


class DatabaseActor:
    def __init__(self, path_to_db: str):
        """Creates a connection and cursor from a path to the database"""
        self.connection = sqlite3.connect(path_to_db)
        self.cursor = self.connection.cursor()

    def init_tables(self):
        """Creates the initial tables necessary for the database."""
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
        """Saves user to the database"""
        self.cursor.execute(
            "INSERT INTO user (discord_id) VALUES (?);",
            (discord_id,)
        )
        self.connection.commit()

    def save_roll(self, discord_id: str, alias: str, roll_expression: str):
        """Save a roll expression into the database"""
        self.cursor.execute("""
            INSERT INTO roll_alias (user_id, alias, roll_expression)
                VALUES (?, ?, ?);
            """,
            (discord_id, alias, roll_expression)
        )
        self.connection.commit()

    def get_roll(self, discord_id: str, alias: str):
        """Retrieve a saved roll expression from the database"""
        roll_expression = self.cursor.execute("""
            SELECT roll_expression FROM roll_alias
            WHERE user_id = ? AND alias = ?;
            """,
            (discord_id, alias)
        ).fetchone()[0]
        return roll_expression
