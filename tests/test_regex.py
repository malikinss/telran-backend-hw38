# ./tests/test_regex.py

import re
from typing import Callable, Dict, List
from unittest import TestCase

from src.tools.ltr import OperatorRegistry
from src.tools.ltr import RegexPatterns, ExpressionValidator


# --- Test Data ---

OPERAND_CASES = {
    "true": ["42", " 42 ", "(42)", "42.5", "42.555"],
    "false": ["42 5", "", "()", ")42.5", "42&5", "42.555("],
}

OPERATOR_CASES = {
    "true": ["**", "+", "-", "*", "/"],
    "false": ["++", "//"],
}

EXPRESSION_CASES = {
    "true": [
        "3+4-7",
        "3 + 4 - 7.5",
        "10",
        "3+(4-7)",
        "(3 + (2 * 10 / (40 - 20))+(3 * 4)) * 10",
        "(3 ** (2.3 * 10.8 / (40 - 20))+(3 * 4)) * (10/3)",
    ],
    "false": [
        "(3 ** (2.3 * 1 0.8 / (40 - 20)) +(3 * 4)) * (10/3)",
        "(3 ** (2.3 * 10.8 & (40 - 20))+(3 * 4)) * (10/3)",
    ],
}

PARENTHESES_CASES = {
    'valid':  [
        "3 + (4 * 5)",
        "(10 + 20)",
        "((3+2)) + 1",
    ],
    'invalid': [
        "(10 + 20))))",
        "((3 + 4) + 2)))",
    ]
}


class TestRegEx(TestCase):
    """
    Test suite validating correctness of arithmetic-related regular
    expressions.

    This test class verifies that regex patterns produced by `RegexPatterns`
    correctly recognize valid and invalid:
    - numeric operands,
    - arithmetic operators,
    - full arithmetic expressions with nested parentheses.

    The tests ensure that regex validation logic remains consistent with
    supported operators defined in `OperatorRegistry` and rejects malformed
    or ambiguous input early, before evaluation.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Initialize shared dependencies for all regex tests.

        OperatorRegistry defines the set of supported arithmetic operators,
        while RegexPatterns generates regex patterns based on those operators.
        """
        cls.ops = OperatorRegistry()
        cls.patterns = RegexPatterns()
        cls.validator = ExpressionValidator(cls.ops)

    # --- Helper methods ---

    def _assert_match(self, pattern: str, value: str) -> None:
        """
        Assert that a value fully matches a given regex pattern.

        This method enforces *full* string validation using `re.fullmatch`,
        ensuring that partial matches are not considered valid.
        """
        self.assertIsNotNone(re.fullmatch(pattern, value))

    def _assert_no_match(self, pattern: str, value: str) -> None:
        """
        Assert that a value does not fully match a given regex pattern.

        Used to confirm that malformed or unsupported input is correctly
        rejected by the regex.
        """
        self.assertIsNone(re.fullmatch(pattern, value))

    def _run_test_cases(
        self,
        test_cases: Dict[str, List[str]],
        pattern: str,
    ) -> None:
        """
        Execute grouped regex test cases against a single pattern.

        Each test case is executed as a subtest to improve failure diagnostics
        and isolate individual invalid or unexpected matches.

        Args:
            test_cases: Mapping of expected result ("true" or "false")
                to a list of input strings.
            pattern: Regex pattern to validate against.
        """
        assertions: Dict[str, Callable[[str, str], None]] = {
            "true": self._assert_match,
            "false": self._assert_no_match,
        }

        for expected, cases in test_cases.items():
            for case in cases:
                with self.subTest(expected=expected, value=case):
                    assertions[expected](pattern, case)

    # --- Actual tests ---

    def test_arithmetic_operand(self) -> None:
        """
        Verify operand regex matches valid numeric literals only.

        Ensures support for:
        - integers and floating-point numbers,
        - optional surrounding whitespace,
        - optional single-level parentheses.

        Invalid formats, malformed numbers, or unexpected symbols
        must be rejected.
        """
        self._run_test_cases(OPERAND_CASES, self.patterns.operand())

    def test_arithmetic_operator(self) -> None:
        """
        Verify operator regex matches only supported arithmetic operators.

        The set of valid operators is defined exclusively by OperatorRegistry.
        Any operator not explicitly registered must be rejected.
        """
        self._run_test_cases(OPERATOR_CASES, self.patterns.operator(self.ops))

    def test_arithmetic_expression(self) -> None:
        """
        Verify full arithmetic expression regex validation.

        Confirms that expressions consisting of valid operands, operators,
        and properly balanced parentheses are accepted, while expressions
        containing invalid tokens or malformed structure are rejected.

        This test acts as the final validation gate before expression
        evaluation.
        """
        self._run_test_cases(
            EXPRESSION_CASES, self.patterns.expression(self.ops)
        )

    def test_check_arithmetic_expr_parentheses_only(self) -> None:
        """
        Test that ExpressionValidator correctly checks parentheses pairing.

        Valid expressions should pass.
        Invalid expressions with mismatched or extra brackets should
        raise ValueError.
        """
        test_cases = {
            True: PARENTHESES_CASES["valid"],
            False: PARENTHESES_CASES["invalid"],
        }

        for should_pass, expressions in test_cases.items():
            for expr in expressions:
                with self.subTest(expr=expr):
                    if should_pass:
                        self.validator.validate_full(expr)
                    else:
                        with self.assertRaises(ValueError):
                            self.validator.validate_full(expr)
