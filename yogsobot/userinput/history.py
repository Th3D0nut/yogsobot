def update_roll_history(
        history: dict[dict],
        discord_id: str,
        nickname: str,
        expression: str
    ) -> dict[dict]:
    """Update the input history in this function and return it."""
    history[discord_id] = {
        "nickname": nickname,
        "expression": expression,
    }
    return history
