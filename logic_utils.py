def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 50),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    text = str(raw).strip()
    if text == "":
        return False, None, "Enter a guess."

    try:
        if "." in text:
            value = int(float(text))
        else:
            value = int(text)
    except (TypeError, ValueError):
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Enter a number in the range {low} to {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    guess_number = int(guess)
    secret_number = int(secret)

    if guess_number == secret_number:
        return "Win", "🎉 Correct!"

    if guess_number > secret_number:
        return "Too High", "📉 Go LOWER!"

    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        return current_score + max(points, 10)

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def process_guess(
    raw_guess: str,
    secret,
    current_score: int,
    attempt_number: int,
    low: int,
    high: int,
    difficulty: str,
    history=None,
):
    """Process one guess and return UI-ready result data for the app and tests."""
    history_items = [] if history is None else list(history)

    ok, guess_int, error_message = parse_guess(raw_guess, low, high)
    if not ok:
        history_items.append(raw_guess)
        return {
            "ok": False,
            "error": error_message,
            "final_score": current_score,
            "debug_info": {
                "Secret": int(secret),
                "Attempts": attempt_number,
                "Score": current_score,
                "Difficulty": difficulty,
                "History": history_items,
            },
        }

    history_items.append(guess_int)
    outcome, message = check_guess(guess_int, secret)
    final_score = update_score(current_score, outcome, attempt_number)
    status = "won" if outcome == "Win" else "playing"
    final_message = None

    if outcome == "Win":
        final_message = (
            f"You won! The secret was {int(secret)}. Final score: {final_score}"
        )

    return {
        "ok": True,
        "guess": guess_int,
        "outcome": outcome,
        "message": message,
        "status": status,
        "final_score": final_score,
        "final_message": final_message,
        "debug_info": {
            "Secret": int(secret),
            "Attempts": attempt_number,
            "Score": final_score,
            "Difficulty": difficulty,
            "History": history_items,
        },
    }
