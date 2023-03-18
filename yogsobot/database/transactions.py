def init_tables(db_curs):
    db_curs.execute("""
        CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY,
            discord_id TEXT NOT NULL UNIQUE,
            nickname VARCHAR(30)
            );
        """)
    db_curs.execute("""
        CREATE TABLE IF NOT EXISTS alias(
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            roll_expression TEXT
            );
        """)


def save_user(db_curs, discord_id, nickname):
    user = db_curs.execute(
        "SELECT discord_id FROM user WHERE discord_id = ?;",
        discord_id
        )
    if not user.fetchone():
        db_curs.execute(
            "INSERT INTO user (discord_id, nick) VALUES (?, ?);",
            discord_id, nickname
            )
