# ./src/tools/ltr/evaluation/operators.py

import operator as op
from typing import Callable

BinaryOperator = Callable[[float, float], float]


class OperatorRegistry:
    """
    Registry of supported binary arithmetic operators.

    This class serves as a single source of truth for all binary operators
    supported by the evaluation layer. It maps operator symbols to their
    corresponding callable implementations and provides a uniform interface
    for operator lookup and execution.

    Responsibility:
    - define which operators are supported,
    - expose operator symbols for parsing,
    - delegate execution of binary operations.

    Non-responsibility:
    - expression parsing,
    - validation of operator placement,
    - handling of operator precedence.
    """

    def __init__(self) -> None:
        """
        Initialize the operator registry with supported operators.

        Each operator is represented by a symbol mapped to a callable
        accepting two float operands and returning a float result.
        """
        self._operators: dict[str, BinaryOperator] = {
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            "**": op.pow,
            "%": op.mod,
            # Custom percentage operator:
            # Computes what percentage `part` is of `whole`
            "%%": lambda whole, part: part * 100 / whole,
        }

    def get(self, symbol: str) -> BinaryOperator:
        """
        Retrieve a binary operator implementation by its symbol.

        Args:
            symbol: Operator symbol (e.g. '+', '-', '*', '/', '**').

        Returns:
            Callable implementing the binary operation.

        Raises:
            ValueError: If the operator symbol is not registered.
        """
        try:
            return self._operators[symbol]
        except KeyError as exc:
            raise ValueError(f"Unknown operator '{symbol}'") from exc

    def symbols(self) -> list[str]:
        """
        Return supported operator symbols ordered by matching priority.

        Symbols are sorted by length in descending order to ensure correct
        regex matching of multi-character operators (e.g. '**' before '*').
        """
        return sorted(self._operators.keys(), key=len, reverse=True)

    def compute(self, left: float, right: float, symbol: str) -> float:
        """
        Compute the result of a binary operation.

        Args:
            left: Left-hand operand.
            right: Right-hand operand.
            symbol: Operator symbol.

        Returns:
            Result of applying the operator to the operands.

        Raises:
            ValueError: If the operator symbol is not supported.
            ZeroDivisionError: If the underlying operator raises it.
        """
        return self.get(symbol)(left, right)
