import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import parse_guess


# --- Bug 2: range validation ---
# Before the fix, parse_guess accepted any valid integer regardless of the
# game range. Negative numbers and values above the upper bound were silently
# treated as valid guesses.

class TestParseGuessBug2RangeValidation:
    """parse_guess must reject values outside [low, high] when a range is given."""

    def test_negative_number_rejected(self):
        ok, value, err = parse_guess("-5", low=1, high=20)
        assert not ok
        assert value is None
        assert "1" in err and "20" in err

    def test_zero_rejected_when_range_starts_at_one(self):
        ok, value, err = parse_guess("0", low=1, high=100)
        assert not ok

    def test_above_upper_bound_rejected(self):
        ok, value, err = parse_guess("101", low=1, high=100)
        assert not ok
        assert value is None
        assert "100" in err

    def test_boundary_low_accepted(self):
        ok, value, err = parse_guess("1", low=1, high=20)
        assert ok
        assert value == 1
        assert err is None

    def test_boundary_high_accepted(self):
        ok, value, err = parse_guess("20", low=1, high=20)
        assert ok
        assert value == 20
        assert err is None

    def test_valid_mid_range_accepted(self):
        ok, value, err = parse_guess("10", low=1, high=20)
        assert ok
        assert value == 10

    def test_no_range_args_skips_range_check(self):
        """Calling without low/high should still parse normally (backwards compat)."""
        ok, value, err = parse_guess("999")
        assert ok
        assert value == 999
