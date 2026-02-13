# ./src/tools/ltr/utils/parentheses.py

PAIRING_ERROR = "Parentheses Pairing Error"

PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
}


class ParenthesesChecker:
    """
    Validates correct pairing and ordering of parentheses and brackets.

    This class checks that all supported bracket types are:
    - properly opened and closed,
    - correctly nested,
    - closed in the correct order.

    Supported bracket types:
    - round brackets: ()
    - square brackets: []
    - curly brackets: {}
    """

    def check(
        self, expression: str, pairs: dict[str, str] | None = None
    ) -> None:
        """
        Validate bracket pairing in the given expression.

        The method uses a stack-based approach to ensure that every opening
        bracket is closed by the correct corresponding closing bracket and
        that brackets are properly nested.

        Args:
            expression: String expression to validate.
            pairs: Optional dict of brackets to check (default all PAIRS).

        Raises:
            ValueError: If brackets are unbalanced, mismatched, or incorrectly
                        nested.
        """
        stack: list[str] = []
        pairs = pairs or PAIRS
        closing = set(pairs.values())

        for ch in expression:
            if ch in pairs:
                # Opening bracket
                stack.append(ch)

            elif ch in closing:
                # Closing bracket
                if not stack:
                    raise ValueError(PAIRING_ERROR)

                last_open = stack.pop()
                if pairs[last_open] != ch:
                    raise ValueError(PAIRING_ERROR)

        if stack:
            # Unclosed opening brackets remain
            raise ValueError(PAIRING_ERROR)
