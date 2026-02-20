from decimal import Decimal

import pytest

from .money import Money


class TestMoney:
    def test_init(self) -> None:
        money1 = Money("100.00", "EUR")
        assert money1.amount == Decimal("100.00")
        assert money1.currency == "EUR"

        money2 = Money(Decimal("100.00"), "EUR")
        assert money2.amount == Decimal("100.00")
        assert money2.currency == "EUR"

        assert money1 == money2

    def test_eq(self) -> None:
        assert Money("100.00", "EUR") == Money("100.00", "EUR")
        assert Money("100.00", "EUR") == Money(Decimal("100.00"), "EUR")
        assert Money("100.00", "EUR") == Money("100", "EUR")
        assert Money("100.00", "EUR") != Money("100.00", "USD")
        assert Money("100.00", "EUR") != Money("200.00", "EUR")
        assert Money("100.12", "EUR") != Money("100", "EUR")

    @pytest.mark.parametrize(
        "initial, multiplier, expected",
        [
            ("100.00", "0", "0.00"),
            ("100.00", "0.3333333", "33.33"),
            ("100.00", "0.6666666", "66.67"),
            ("100.00", "0.5", "50.00"),
            ("100.00", "1", "100.00"),
            ("100.00", "1.5", "150.00"),
            ("100.00", "-1", "-100.00"),
            ("-100.00", "0.5", "-50.00"),
            ("100.00", "-0.3333333", "-33.33"),
            ("100.00", "-0.6666666", "-66.67"),
            ("89.50", "0.19", "17.01"),  # commercial rounding
            ("-89.50", "0.19", "-17.01"),  # commercial rounding
        ],
    )
    def test_mul(self, initial: str, multiplier: str, expected: str) -> None:
        money = Money(initial, "EUR")
        result = money * Decimal(multiplier)
        assert result == Money(expected, "EUR")

    @pytest.mark.parametrize(
        "initial, divisor, expected",
        [
            ("100.00", "1", "100.00"),
            ("100.00", "3", "33.33"),
            ("100.00", "6", "16.67"),
            ("100.00", "2", "50.00"),
            ("100.00", "0.5", "200.00"),
            ("100.00", "-1", "-100.00"),
            ("-100.00", "1", "-100.00"),
            ("-100.00", "-1", "100.00"),
            ("-100.00", "2", "-50.00"),
            ("100.00", "-3", "-33.33"),
            ("100.00", "-6", "-16.67"),
            ("100.01", "2", "50.01"),  # commercial rounding
            ("-100.01", "2", "-50.01"),  # commercial rounding
        ],
    )
    def test_truediv(self, initial: str, divisor: str, expected: str) -> None:
        money = Money(initial, "EUR")
        result = money / Decimal(divisor)
        assert result == Money(expected, "EUR")
