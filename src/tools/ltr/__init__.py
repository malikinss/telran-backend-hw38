# ./src/tools/ltr/__init__.py

"""
Left-to-right arithmetic evaluation package.

Exports:
    - LtrCalculator: High-level calculator for LTR arithmetic expressions.
    - RegexPatterns: Factory for arithmetic validation regex patterns.
    - ExpressionValidator: Syntax validator for arithmetic expressions.
    - ParenthesesChecker: Utility for validating paired brackets.
    - PAIRS, PAIRING_ERROR: Constants for bracket checking.
    - LeftToRightEvaluator: Core evaluator for expressions without parentheses.
    - BinaryOperator, OperatorRegistry: Operator definitions and registry.
"""

from .ltr import LtrCalculator
from .regex import RegexPatterns, ExpressionValidator
from .utils import ParenthesesChecker, PAIRS, PAIRING_ERROR
from .evaluation import LeftToRightEvaluator, BinaryOperator, OperatorRegistry

__all__ = [
    "LtrCalculator",
    "RegexPatterns",
    "ExpressionValidator",
    "ParenthesesChecker",
    "PAIRS",
    "PAIRING_ERROR",
    "LeftToRightEvaluator",
    "BinaryOperator",
    "OperatorRegistry",
]
