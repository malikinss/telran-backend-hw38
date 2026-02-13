# ./src/tools/ltr/evaluation/evaluator.py

import re
from .operators import OperatorRegistry


class LeftToRightEvaluator:
    """
    Evaluates arithmetic expressions strictly from left to right.

    This evaluator intentionally ignores operator precedence and does not
    support parentheses. It assumes that the input expression is already
    syntactically valid and consists only of numeric operands and supported
    binary operators.

    Responsibility:
    - orchestrate evaluation order,
    - delegate actual computation to OperatorRegistry.

    Non-responsibility:
    - syntax validation,
    - parentheses handling,
    - operator precedence resolution.
    """

    def __init__(self, operators: OperatorRegistry) -> None:
        """
        Initialize evaluator with a registry of supported operators.

        Args:
            operators: Registry providing available operator symbols
                and their corresponding computation logic.
        """
        self._operators = operators

        # Matches any supported operator symbol (e.g. +, -, *, /, **)
        self._operator_pattern = re.compile(
            "|".join(map(re.escape, operators.symbols()))
        )

        # Matches integer and floating-point numeric literals
        self._operand_pattern = re.compile(r"\d+(?:\.\d+)?|\.\d+")

    def evaluate(self, expr: str) -> float:
        """
        Evaluate an arithmetic expression from left to right.

        The expression is evaluated sequentially in the order operators
        appear, without considering operator precedence. Parentheses are
        explicitly not supported and must be resolved beforehand.

        Args:
            expr: Arithmetic expression without parentheses.

        Returns:
            The numeric result of the evaluation.

        Raises:
            ValueError: If operator lookup fails or operands cannot be parsed.
            ZeroDivisionError: If a division by zero occurs during evaluation.
        """
        operands = re.split(self._operator_pattern, expr)
        operators = re.split(self._operand_pattern, expr)

        result = float(operands[0])

        for i in range(1, len(operands)):
            result = self._operators.compute(
                left=result,
                right=float(operands[i]),
                symbol=operators[i],
            )

        return result
