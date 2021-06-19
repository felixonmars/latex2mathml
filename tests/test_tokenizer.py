import string

import pytest

from latex2mathml.tokenizer import tokenize


@pytest.mark.parametrize(
    "latex, expected",
    [
        pytest.param("\\", ["\\"], id="single-backslash"),
        pytest.param(string.ascii_letters, list(string.ascii_letters), id="alphabets"),
        pytest.param(string.digits, [string.digits], id="numbers"),
        pytest.param("123\\", ["123", "\\"], id="backslash-after-number"),
        pytest.param(r"123\\", ["123", r"\\"], id="double-backslash-after-number"),
        pytest.param("12.56", ["12.56"], id="decimal"),
        pytest.param(r"12.\\", ["12", ".", r"\\"], id="incomplete-decimal"),
        pytest.param("5x", list("5x"), id="numbers-and-alphabets"),
        pytest.param("5.8x", ["5.8", "x"], id="decimals-and-alphabets"),
        pytest.param("3 x", ["3", "x"], id="string-with-spaces"),
        pytest.param("+-*/=()[]_^{}", list("+-*/=()[]_^{}"), id="operators"),
        pytest.param(
            "3 + 5x - 5y = 7", ["3", "+", "5", "x", "-", "5", "y", "=", "7"], id="numbers-alphabets-and-operators"
        ),
        pytest.param(r"\alpha\beta", [r"\alpha", r"\beta"], id="symbols"),
        pytest.param(r"\frac2x", [r"\frac", "2", "x"], id="symbols-appended-with-number"),
        pytest.param(
            r"\begin{matrix}a & b \\ c & d \end{matrix}",
            [r"\begin{matrix}", "a", "&", "b", r"\\", "c", "&", "d", r"\end{matrix}"],
            id="matrix",
        ),
        pytest.param(
            r"\begin{matrix*}[r]a & b \\ c & d \end{matrix*}",
            [
                r"\begin{matrix*}",
                "[",
                "r",
                "]",
                "a",
                "&",
                "b",
                r"\\",
                "c",
                "&",
                "d",
                r"\end{matrix*}",
            ],
            id="matrix-with-alignment",
        ),
        pytest.param(
            r"\begin{matrix}-a & b \\ c & d \end{matrix}",
            [r"\begin{matrix}", "-", "a", "&", "b", r"\\", "c", "&", "d", r"\end{matrix}"],
            id="matrix-with-negative-sign",
        ),
        pytest.param(
            r"\begin{array}{cc} 1 & 2 \\ 3 & 4 \end{array}",
            [
                r"\begin{array}",
                "{",
                "c",
                "c",
                "}",
                "1",
                "&",
                "2",
                r"\\",
                "3",
                "&",
                "4",
                r"\end{array}",
            ],
            id="simple-array",
        ),
        pytest.param("a_{2,n}", ["a", "_", "{", "2", ",", "n", "}"], id="subscript"),
        pytest.param("a^{i+1}_3", ["a", "^", "{", "i", "+", "1", "}", "_", "3"], id="superscript-with-curly-braces"),
        pytest.param(
            r"""\begin{bmatrix}
             a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
             a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
             \vdots  & \vdots  & \ddots & \vdots  \\
             a_{m,1} & a_{m,2} & \cdots & a_{m,n}
            \end{bmatrix}""",
            [
                r"\begin{bmatrix}",
                "a",
                "_",
                "{",
                "1",
                ",",
                "1",
                "}",
                "&",
                "a",
                "_",
                "{",
                "1",
                ",",
                "2",
                "}",
                "&",
                r"\cdots",
                "&",
                "a",
                "_",
                "{",
                "1",
                ",",
                "n",
                "}",
                r"\\",
                "a",
                "_",
                "{",
                "2",
                ",",
                "1",
                "}",
                "&",
                "a",
                "_",
                "{",
                "2",
                ",",
                "2",
                "}",
                "&",
                r"\cdots",
                "&",
                "a",
                "_",
                "{",
                "2",
                ",",
                "n",
                "}",
                r"\\",
                r"\vdots",
                "&",
                r"\vdots",
                "&",
                r"\ddots",
                "&",
                r"\vdots",
                r"\\",
                "a",
                "_",
                "{",
                "m",
                ",",
                "1",
                "}",
                "&",
                "a",
                "_",
                "{",
                "m",
                ",",
                "2",
                "}",
                "&",
                r"\cdots",
                "&",
                "a",
                "_",
                "{",
                "m",
                ",",
                "n",
                "}",
                r"\end{bmatrix}",
            ],
            id="issue-33",
        ),
        pytest.param(r"\mathbb{R}", ["&#x0211D;"], id="issue-51"),
        pytest.param(
            r"\begin{array}{rcl}ABC&=&a\\A&=&abc\end{array}",
            [
                r"\begin{array}",
                "{",
                "r",
                "c",
                "l",
                "}",
                "A",
                "B",
                "C",
                "&",
                "=",
                "&",
                "a",
                r"\\",
                "A",
                "&",
                "=",
                "&",
                "a",
                "b",
                "c",
                r"\end{array}",
            ],
            id="issue-55",
        ),
        pytest.param(r"\mathrm{...}", [r"\mathrm", "{", ".", ".", ".", "}"], id="issue-60"),
        pytest.param(
            r"\frac{x + 4}{x + \frac{123 \left(\sqrt{x} + 5\right)}{x + 4} - 8}",
            [
                r"\frac",
                "{",
                "x",
                "+",
                "4",
                "}",
                "{",
                "x",
                "+",
                r"\frac",
                "{",
                "123",
                r"\left",
                "(",
                r"\sqrt",
                "{",
                "x",
                "}",
                "+",
                "5",
                r"\right",
                ")",
                "}",
                "{",
                "x",
                "+",
                "4",
                "}",
                "-",
                "8",
                "}",
            ],
            id="issue-61",
        ),
        pytest.param(
            r"\sqrt {\sqrt {\left( x^{3}\right) + v}}",
            [
                r"\sqrt",
                "{",
                r"\sqrt",
                "{",
                r"\left",
                "(",
                "x",
                "^",
                "{",
                "3",
                "}",
                r"\right",
                ")",
                "+",
                "v",
                "}",
                "}",
            ],
            id="issue-63",
        ),
        pytest.param(
            r"\left[\begin{matrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 1 & 0\\0 & 0 & 0 & 1\end{matrix}\right]",
            [
                r"\left",
                "[",
                r"\begin{matrix}",
                "1",
                "&",
                "0",
                "&",
                "0",
                "&",
                "0",
                r"\\",
                "0",
                "&",
                "1",
                "&",
                "0",
                "&",
                "0",
                r"\\",
                "0",
                "&",
                "0",
                "&",
                "1",
                "&",
                "0",
                r"\\",
                "0",
                "&",
                "0",
                "&",
                "0",
                "&",
                "1",
                r"\end{matrix}",
                r"\right",
                "]",
            ],
            id="issue-77",
        ),
        pytest.param(
            r"x^{x^{x^{x}}} \left(x^{x^{x}} \left(x^{x} \left(\log{\left(x \right)} + 1\right) \log{\left(x \right)} + "
            r"\frac{x^{x}}{x}\right) \log{\left(x \right)} + \frac{x^{x^{x}}}{x}\right)",
            [
                "x",
                "^",
                "{",
                "x",
                "^",
                "{",
                "x",
                "^",
                "{",
                "x",
                "}",
                "}",
                "}",
                r"\left",
                "(",
                "x",
                "^",
                "{",
                "x",
                "^",
                "{",
                "x",
                "}",
                "}",
                r"\left",
                "(",
                "x",
                "^",
                "{",
                "x",
                "}",
                r"\left",
                "(",
                r"\log",
                "{",
                r"\left",
                "(",
                "x",
                r"\right",
                ")",
                "}",
                "+",
                "1",
                r"\right",
                ")",
                r"\log",
                "{",
                r"\left",
                "(",
                "x",
                r"\right",
                ")",
                "}",
                "+",
                r"\frac",
                "{",
                "x",
                "^",
                "{",
                "x",
                "}",
                "}",
                "{",
                "x",
                "}",
                r"\right",
                ")",
                r"\log",
                "{",
                r"\left",
                "(",
                "x",
                r"\right",
                ")",
                "}",
                "+",
                r"\frac",
                "{",
                "x",
                "^",
                "{",
                "x",
                "^",
                "{",
                "x",
                "}",
                "}",
                "}",
                "{",
                "x",
                "}",
                r"\right",
                ")",
            ],
            id="issue-78",
        ),
        pytest.param(
            r"\max_{x \in \[a,b\]}f(x)",
            [
                r"\max",
                "_",
                "{",
                "x",
                r"\in",
                r"\[",
                "a",
                ",",
                "b",
                r"\]",
                "}",
                "f",
                "(",
                "x",
                ")",
            ],
            id="max",
        ),
        pytest.param(r"\max \{a, b, c\}", [r"\max", r"\{", "a", ",", "b", ",", "c", r"\}"], id="issue-108-1"),
        pytest.param(r"\operatorname{sn}x", [r"\operatorname{sn}", "x"], id="issue-109"),
        pytest.param(
            r"\text{Let}\ x=\text{number of cats}.",
            [r"\text", "Let", r"\ ", "x", "=", r"\text", "number of cats", "."],
            id="issue-109",
        ),
        pytest.param(
            r"x = {-b \pm \sqrt{b^2-4ac} \over 2a}",
            [
                "x",
                "=",
                "{",
                "-",
                "b",
                r"\pm",
                r"\sqrt",
                "{",
                "b",
                "^",
                "2",
                "-",
                "4",
                "a",
                "c",
                "}",
                r"\over",
                "2",
                "a",
                "}",
            ],
            id="quadratic-equation",
        ),
        pytest.param(
            r"a\,\overset{?}{=}\,b", ["a", "\\,", r"\overset", "{", "?", "}", "{", "=", "}", "\\,", "b"], id="issue-125"
        ),
        pytest.param(
            r"|\hspace1em|\hspace 1.2em|\hspace{1.5ex}|\hspace {2ex}|",
            [
                "|",
                r"\hspace",
                "1em",
                "|",
                r"\hspace",
                "1.2em",
                "|",
                r"\hspace",
                "{",
                "1.5ex",
                "}",
                "|",
                r"\hspace",
                "{",
                "2ex",
                "}",
                "|",
            ],
            id="issue-129",
        ),
        pytest.param(r"\text{Hello~World}", [r"\text", "Hello~World"], id="tilde-in-text"),
        pytest.param(
            r"""% this is hidden
            100\%! 100% this is hidden, too
            \test% this is another hidden line""",
            ["100", r"\%", "!", "100", r"\test"],
            id="comments",
        ),
        pytest.param(
            r"{a \above 1pt b} + {c \above { 1.5 pt } d}",
            ["{", "a", r"\above", "1pt", "b", "}", "+", "{", "c", r"\above", "{", "1.5pt", "}", "d", "}"],
            id="above",
        ),
        pytest.param(
            r"\mathop{x}\limits_0^1",
            [r"\mathop", "{", "x", "}", r"\limits", "_", "0", "^", "1"],
            id="issue-125",
        ),
        pytest.param(r"\fbox{E=mc^2}", [r"\fbox", "E=mc^2"], id="fbox"),
        pytest.param("X_123", ["X", "_", "1", "23"], id="issue-203-1"),
        pytest.param("X_1.23", ["X", "_", "1", ".23"], id="issue-203-2"),
        pytest.param("X^123", ["X", "^", "1", "23"], id="issue-203-3"),
        pytest.param("X^1.23", ["X", "^", "1", ".23"], id="issue-203-4"),
        pytest.param(r"X_\mathrm{min}", ["X", "_", r"\mathrm", "{", "m", "i", "n", "}"], id="issue-203-5"),
        pytest.param(r"\hbox{E=mc^2}", [r"\hbox", "E=mc^2"], id="hbox"),
    ],
)
def test_tokenize(latex: str, expected: list) -> None:
    assert list(tokenize(latex)) == expected
