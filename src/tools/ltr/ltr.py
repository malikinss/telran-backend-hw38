# ./src/tools/ltr/ltr.py

import re
from .evaluation import LeftToRightEvaluator, OperatorRegistry
from .regex import ExpressionValidator


class LtrCalculator:
    """
    Left-to-right arithmetic expression calculator.

    Evaluates arithmetic expressions strictly from left to right,
    ignoring standard operator precedence, while correctly handling
    parentheses via recursive reduction.

    Responsibilities:
        - Validate parentheses pairing.
        - Validate expression syntax against supported operators.
        - Delegate actual arithmetic computation to LeftToRightEvaluator.

    Notes:
        - Whitespace is ignored.
        - Parentheses are processed from innermost to outermost.
        - Only round brackets () are checked.
    """

    def __init__(self) -> None:
        """
        Initialize the calculator with operator registry, syntax validator,
        and left-to-right evaluator.
        """
        self._operators = OperatorRegistry()
        self._validator = ExpressionValidator(self._operators)
        self._evaluator = LeftToRightEvaluator(self._operators)

    def _remove_spaces(self, expression: str) -> str:
        """
        Remove all whitespace characters from the expression.

        Args:
            expression: Original arithmetic expression.

        Returns:
            Expression with all whitespace removed.
        """
        return re.sub(r"\s+", "", expression)

    def _replace(
        self,
        expression: str,
        start: int,
        end: int,
        value: float,
    ) -> str:
        """
        Replace a slice of the expression with a computed numeric value.

        Args:
            expression: Original expression string.
            start: Start index of the slice to replace.
            end: End index of the slice to replace.
            value: Computed value to insert.

        Returns:
            Updated expression string with the slice replaced.
        """
        return expression[:start] + str(value) + expression[end:]

    def evaluate(self, expression: str) -> float:
        """
        Evaluate an arithmetic expression.

        Evaluation steps:
            1. Validate parentheses pairing (only round brackets are checked).
            2. Validate expression syntax against supported operands/operators.
            3. Remove all whitespace.
            4. Recursively evaluate innermost parenthesized subexpressions.
            5. Evaluate final flat expression strictly left-to-right.

        Args:
            expression: Arithmetic expression to evaluate.

        Returns:
            Computed numeric result of the expression.

        Raises:
            ValueError: If the expression is syntactically invalid.
            ZeroDivisionError: If division by zero occurs during evaluation.
        """
        # Step 1 & 2: Validate parentheses and syntax
        self._validator.validate_full(expression)

        # Step 3: Normalize expression
        expression = self._remove_spaces(expression)

        # Step 4: Recursively evaluate parenthesized subexpressions
        while match := re.search(r"\([^()]+\)", expression):
            inner_expression = match.group()[1:-1]
            value = self._evaluator.evaluate(inner_expression)

            expression = self._replace(
                expression=expression,
                start=match.start(),
                end=match.end(),
                value=value,
            )

        # Step 5: Evaluate the final flat expression left-to-right
        return self._evaluator.evaluate(expression)
