# ./src/tools/ltr/evaluation/__init__.py

"""
Left-to-right expression evaluation package.

Exports:
    - LeftToRightEvaluator: Core evaluator implementation.
    - BinaryOperator: Representation of binary operator.
    - OperatorRegistry: Registry of supported operators.
"""

from .evaluator import LeftToRightEvaluator
from .operators import BinaryOperator, OperatorRegistry

__all__ = [
    "LeftToRightEvaluator",
    "BinaryOperator",
    "OperatorRegistry",
]
