from logic_utils import check_guess

def test_high_low_string_comparison_bug():
    # BUG FIXED: The original check_guess had a dead try/except TypeError branch that
    # converted both values to strings and compared them lexicographically. This caused
    # check_guess(9, 10) to return "Too High" instead of "Too Low" because "9" > "10"
    # alphabetically (first character "9" > "1"). Claude Code removed the dead branch
    # so comparison is always numeric.
    outcome, _ = check_guess(9, 10)
    assert outcome == "Too Low", (
        f"Expected 'Too Low' for guess=9, secret=10 but got '{outcome}'. "
        "String comparison bug may have returned 'Too High' because '9' > '10' lexicographically."
    )

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"
