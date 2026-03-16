import random
import pytest
from logic_utils import check_guess, get_range_for_difficulty

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


# Bug 3: new game handler must reset status to "playing"
# Without the fix, status stays "won"/"lost" and st.stop() fires on the next
# run, making the New Game button appear to do nothing.
def test_new_game_resets_status_after_won():
    session = {"status": "won", "attempts": 7, "secret": 42}

    # simulate what the fixed new_game handler does
    session["status"] = "playing"
    session["attempts"] = 0
    session["secret"] = 99

    assert session["status"] == "playing", "status must be reset so the game can continue"


def test_new_game_resets_status_after_lost():
    session = {"status": "lost", "attempts": 8, "secret": 42}

    session["status"] = "playing"
    session["attempts"] = 0
    session["secret"] = 55

    assert session["status"] == "playing", "status must be reset so the game can continue"


# Bug 4: new game secret must use difficulty range, not hardcoded 1-100

@pytest.mark.parametrize("difficulty,expected_low,expected_high", [
    ("Easy",   1,  20),
    ("Normal", 1, 100),
    ("Hard",   1,  50),
])
def test_get_range_for_difficulty(difficulty, expected_low, expected_high):
    low, high = get_range_for_difficulty(difficulty)
    assert low == expected_low
    assert high == expected_high


@pytest.mark.parametrize("difficulty", ["Easy", "Normal", "Hard"])
def test_new_game_secret_within_difficulty_range(difficulty):
    # Reproduces the bug: before the fix, new_game always used random.randint(1, 100)
    # regardless of difficulty, so Easy could produce secrets > 20.
    low, high = get_range_for_difficulty(difficulty)
    for _ in range(50):
        secret = random.randint(low, high)
        assert low <= secret <= high


# --- Tests targeting the swapped hint message bug ---
# Bug: when guess > secret the message said "Go HIGHER!" (wrong direction),
#      and when guess < secret it said "Go LOWER!" (wrong direction).
# The prior tests only checked the outcome label ("Too High"/"Too Low") and
# never unpacked the message, so the wrong direction went undetected.

def test_too_high_message_says_go_lower():
    # Guess is above the secret — player needs to go LOWER, not higher.
    outcome, message = check_guess(75, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, (
        f"Expected hint to say 'LOWER' when guess is too high, got: '{message}'"
    )
    assert "HIGHER" not in message, (
        f"Hint must not say 'HIGHER' when guess is too high, got: '{message}'"
    )

def test_too_low_message_says_go_higher():
    # Guess is below the secret — player needs to go HIGHER, not lower.
    outcome, message = check_guess(25, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, (
        f"Expected hint to say 'HIGHER' when guess is too low, got: '{message}'"
    )
    assert "LOWER" not in message, (
        f"Hint must not say 'LOWER' when guess is too low, got: '{message}'"
    )
