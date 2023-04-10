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


def get_last_roll(roll_history: dict[str, dict[str, str]], discord_id: str) -> str:
    try:
        return roll_history[discord_id]["expression"]
    except KeyError:
        return ""