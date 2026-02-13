# ./src/tools/ltr/regex/patterns.py

import re
from ..evaluation import OperatorRegistry


class RegexPatterns:
    """
    Factory for regular expressions used to validate arithmetic syntax.

    This class generates regex patterns for validating:
    - numeric operands,
    - supported arithmetic operators,
    - full arithmetic expressions.

    The produced patterns are intended for *validation only* and do not
    perform parsing or evaluation. All operator knowledge is sourced
    exclusively from OperatorRegistry.
    """

    @staticmethod
    def operand() -> str:
        """
        Build a regex pattern matching a numeric arithmetic operand.

        Supported numeric formats:
        - Integers: `10`, `-3`
        - Floating-point numbers: `10.5`, `10.`, `.5`
        - Scientific notation: `1e3`, `1.2E-4`

        Additional allowances:
        - optional leading sign,
        - optional surrounding whitespace,
        - optional wrapping parentheses (single-level).

        Returns:
            Regex pattern matching a valid numeric operand.
        """
        # Optional leading sign
        sign = r"[+-]?"

        # Core numeric formats:
        # - digits with optional decimal part
        # - decimal starting with dot
        number_body = r"(\d+(\.\d*)?|\.\d+)"

        # Optional scientific notation exponent
        exponent_part = r"([eE][+-]?\d+)?"

        # Full number pattern with optional whitespace after sign
        number = rf"{sign}\s*{number_body}{exponent_part}"

        # Allow surrounding whitespace and optional parentheses
        return rf"\s*\(*\s*{number}\s*\)*\s*"

    @staticmethod
    def operator(operators: OperatorRegistry) -> str:
        """
        Build a regex pattern matching supported arithmetic operators.

        Operator symbols are obtained from OperatorRegistry and escaped
        to ensure correct regex interpretation. Symbols are ordered by
        descending length to guarantee correct matching of multi-character
        operators (e.g. '**' before '*').

        Args:
            operators: Registry defining supported operator symbols.

        Returns:
            Regex pattern matching a single supported operator.
        """
        symbols = sorted(
            operators.symbols(),
            key=len,
            reverse=True,
        )

        escaped_operators = map(
            re.escape,
            symbols,
        )

        return rf"(?:{'|'.join(escaped_operators)})"

    @classmethod
    def expression(cls, operators: OperatorRegistry) -> str:
        """
        Build a regex pattern matching a full arithmetic expression.

        Expression grammar (simplified):
            operand (operator operand)*

        The pattern validates structural correctness only and assumes that:
        - operands are valid numeric literals,
        - operators are supported by OperatorRegistry,
        - parentheses are syntactically balanced at the operand level.

        Args:
            operators: Registry defining supported operators.

        Returns:
            Regex pattern matching a full arithmetic expression.
        """
        operand = cls.operand()
        operator = cls.operator(operators)

        return rf"{operand}({operator}{operand})*"
