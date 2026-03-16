# FIX: Refactored all game logic into logic_utils.py using Claude Code to separate
# concerns — game logic here, UI in app.py. Claude Code also fixed the high/low bug
# where a dead try/except TypeError branch compared values as strings, causing
# lexicographic ordering (e.g. "9" > "10") to return wrong Too High / Too Low results.

# FIX: Moved from app.py into logic_utils.py using Claude Code to keep all game
# logic in one place and out of the UI layer.
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


# FIX: Moved from app.py into logic_utils.py using Claude Code. Handles float
# input (e.g. "3.7") by truncating to int so the game accepts decimal entries.
def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: Removed dead try/except TypeError fallback that compared values as strings,
    # which could produce wrong results (e.g. "9" > "10"). Claude Code identified the
    # branch was unreachable since both inputs are always int.
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📈 Go LOWER!"
    else:
        return "Too Low", "📉 Go HIGHER!"


# FIX: Moved from app.py into logic_utils.py using Claude Code. Win awards
# decreasing points per attempt (min 10); Too High and Too Low each deduct 5.
# Score is clamped to 0 to prevent negative values.
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    result = current_score

    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        result = current_score + points
    elif outcome == "Too High":
        # Consistently penalize a Too High guess by subtracting points
        result = current_score - 5
    elif outcome == "Too Low":
        result = current_score - 5

    # Ensure score never goes below zero
    if result < 0:
        result = 0

    return result
