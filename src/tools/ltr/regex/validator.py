# ./src/tools/ltr/regex/validator.py

import re

from .patterns import RegexPatterns
from ..evaluation import OperatorRegistry
from ..utils import ParenthesesChecker


class ExpressionValidator:
    """
    Validates arithmetic expression syntax using regular expressions.

    This class acts as a syntax validation gate before expression evaluation.
    It ensures that an expression:
    - consists only of valid numeric operands,
    - uses supported arithmetic operators,
    - follows a structurally correct arithmetic form.

    The validator does not evaluate expressions, resolve parentheses,
    or check semantic correctness of operations.
    """

    def __init__(self, operators: OperatorRegistry) -> None:
        """
        Initialize the validator with a set of supported operators.

        Args:
            operators: Registry defining supported arithmetic operators.
        """
        self._parentheses_checker = ParenthesesChecker()

        pattern: str = RegexPatterns.expression(operators)
        self._expression_pattern: re.Pattern[str] = re.compile(
            pattern, re.ASCII
        )

    def validate(self, expression: str) -> None:
        """
        Validate the syntax of an arithmetic expression.

        The expression must fully match the arithmetic expression pattern.
        Partial matches or malformed structures are considered invalid.

        Args:
            expression: Arithmetic expression to validate.

        Raises:
            ValueError: If the expression does not conform to the
                        supported arithmetic syntax.
        """
        if not self._expression_pattern.fullmatch(expression):
            raise ValueError(
                f"Syntax error in expression: {expression}"
            )

    def validate_full(self, expression: str) -> None:
        """
        Perform full syntax validation for an arithmetic expression.

        This includes:
        1. Parentheses pairing validation (only round brackets are checked).
        2. Regex-based arithmetic syntax validation.

        Args:
            expression: Arithmetic expression to validate.

        Raises:
            ValueError: If parentheses are unbalanced or if the syntax
                        is invalid.
        """
        self._parentheses_checker.check(
            expression, pairs={"(": ")"}
        )
        self.validate(expression)
