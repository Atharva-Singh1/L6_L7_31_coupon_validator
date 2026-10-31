import pytest

from coupon_validator import best_discount, coupon_discount, is_expired


@pytest.mark.parametrize(
    ("code", "cart_total", "is_new_user", "day", "expected"),
    [
        ("WELCOME10", 200, True, "mon", 20),
        ("WELCOME10", 200, False, "mon", 0),
        ("WEEKEND20", 500, True, "sat", 100),
        ("WEEKEND20", 500, True, "sun", 100),
        ("WEEKEND20", 400, False, "sat", 50),
        ("WEEKEND20", 499, False, "sun", 50),
        ("WEEKEND20", 500, True, "mon", 0),
        ("WEEKEND20", 200, True, "fri", 0),
        ("FLAT100", 301, False, "mon", 100),
        ("FLAT100", 300, False, "mon", 0),
        ("FLAT100", 299, False, "mon", 0),
        ("UNKNOWN", 200, False, "mon", 0),
    ],
)
def test_coupon_discount_scenarios(code, cart_total, is_new_user, day, expected):
    assert coupon_discount(code, cart_total, is_new_user, day) == expected


@pytest.mark.parametrize("cart_total", [0, -1])
def test_coupon_discount_rejects_empty_or_negative_cart(cart_total):
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", cart_total, True, "mon")


@pytest.mark.parametrize(
    ("codes", "cart_total", "is_new_user", "day", "expected"),
    [
        ([], 500, False, "mon", 0),
        (["UNKNOWN"], 500, False, "mon", 0),
        (["WELCOME10"], 200, True, "mon", 20),
        (["WELCOME10", "FLAT100"], 1000, False, "mon", 100),
        (["WELCOME10", "WEEKEND20"], 500, True, "sat", 100),
        (["WEEKEND20"], 100, False, "sat", 40),
        (["WELCOME10"], 1000, True, "mon", 100),
        (["WELCOME10"], 100, True, "mon", 10),
    ],
)
def test_best_discount_scenarios(codes, cart_total, is_new_user, day, expected):
    assert best_discount(codes, cart_total, is_new_user, day) == expected


@pytest.mark.parametrize(
    ("today", "start", "days_valid", "expected"),
    [
        (10, 5, 0, True),
        (10, 5, -1, True),
        (5, 5, 1, False),
        (6, 5, 1, False),
        (7, 5, 1, True),
    ],
)
def test_is_expired_scenarios(today, start, days_valid, expected):
    assert is_expired(today, start, days_valid) is expected
