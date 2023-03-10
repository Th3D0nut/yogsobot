def init_tables(db_curs):
    if not db_curs.execute("SELECT name FROM sqlite_master").fetchone():
        db_curs.execute(
            "create table user(id int, discord_id varchar(30), nickname varchar(30));"
            )
        db_curs.execute(
            "create table alias(id int, user_id int, name varchar(30), roll_expression varchar(200));"
            )
