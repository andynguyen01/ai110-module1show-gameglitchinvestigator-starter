from logic_utils import check_guess, process_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_check_guess_tells_player_to_go_higher_or_lower():
    low_outcome, low_message = check_guess(40, 50)
    high_outcome, high_message = check_guess(60, 50)

    assert low_outcome == "Too Low"
    assert "HIGHER" in low_message
    assert high_outcome == "Too High"
    assert "LOWER" in high_message


def test_winning_guess_keeps_final_score_equal_to_debug_score():
    result = process_guess(
        raw_guess="50",
        secret=50,
        current_score=0,
        attempt_number=1,
        low=1,
        high=100,
        difficulty="Normal",
        history=[],
    )

    assert result["ok"] is True
    assert result["outcome"] == "Win"
    assert result["final_score"] == result["debug_info"]["Score"]
    assert str(result["final_score"]) in result["final_message"]


def test_guess_outside_1_to_100_returns_range_error_message():
    low_result = process_guess(
        raw_guess="0",
        secret=50,
        current_score=0,
        attempt_number=1,
        low=1,
        high=100,
        difficulty="Normal",
        history=[],
    )
    high_result = process_guess(
        raw_guess="101",
        secret=50,
        current_score=0,
        attempt_number=1,
        low=1,
        high=100,
        difficulty="Normal",
        history=[],
    )

    assert low_result["ok"] is False
    assert high_result["ok"] is False
    assert low_result["error"] == "Enter a number in the range 1 to 100."
    assert high_result["error"] == "Enter a number in the range 1 to 100."

