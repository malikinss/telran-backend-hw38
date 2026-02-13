# ./tests/test_ltr_evaluation.py

from unittest import TestCase
from src.tools.ltr import LtrCalculator


# --- Test Data ---

VALID_EXPRESSION_CASES = [
    (
        "(3 + (2 * 10 / (40 - 20))+(3 * 4)) * 10",
        160.0,
    ),
    (
        "((3.5 + (2 * 10.45 / (40.5 - 40))+(3 * 4)) * (10.2 ** 2)) / 2.55",
        ((3.5 + (2 * 10.45 / (40.5 - 40))+(3 * 4)) * (10.2 ** 2)) / 2.55,
    ),
]


class TestLtrEvaluation(TestCase):
    """
    Test suite for left-to-right arithmetic expression evaluation.

    These tests validate that `LtrCalculator` correctly evaluates
    syntactically valid arithmetic expressions and raises appropriate
    exceptions for invalid input or illegal operations.

    The calculator is expected to:
    - respect operator semantics as defined by the evaluation layer,
    - correctly handle nested parentheses,
    - fail fast on invalid syntax,
    - propagate runtime errors such as division by zero.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Initialize a shared calculator instance for all tests.

        LtrCalculator is stateless by design, so a single instance
        is safe to reuse across test cases.
        """
        cls.calculator = LtrCalculator()

    def test_valid_expressions(self) -> None:
        """
        Verify correct evaluation of valid arithmetic expressions.

        Ensures that:
        - nested parentheses are evaluated correctly,
        - floating-point arithmetic is handled consistently,
        - results are numerically close to Python's native evaluation.

        A tolerance is applied to account for floating-point precision.
        """
        for expr, expected in VALID_EXPRESSION_CASES:
            with self.subTest(expression=expr):
                self.assertAlmostEqual(
                    expected,
                    self.calculator.evaluate(expr),
                    places=1,
                )

    def test_invalid_syntax(self) -> None:
        """
        Verify that invalid expression syntax is rejected.

        Expressions containing malformed operand sequences or
        ambiguous token boundaries must raise ValueError instead
        of producing undefined results.
        """
        with self.assertRaises(ValueError):
            self.calculator.evaluate("4 + 2   5")

    def test_zero_division(self) -> None:
        """
        Verify correct handling of division by zero.

        The calculator must not suppress ZeroDivisionError and
        should propagate it to the caller unchanged.
        """
        with self.assertRaises(ZeroDivisionError):
            self.calculator.evaluate("4 + 2 / (20 / 20 - 1)")
