"""Comment/string-aware lexer for SysML text (issue #7).

The lexer tiles the whole input into tokens — every byte belongs to exactly
one token (100% coverage by construction).  It understands:
  - line comments  `// ...`
  - block comments `/* ... */`
  - unrestricted names `'text with spaces'` (''-quoted)
  - string literals `"text"` with backslash escapes
  - everything else as punctuation / symbol / word / whitespace

Whitespace is emitted as its own token kind so that round-tripping the token
stream reproduces the input exactly when needed; the IR layer decides whether
whitespace belongs to a node's raw_text or is inter-node trivia.
"""

from __future__ import annotations

from dataclasses import dataclass

# Token kinds (constants, module-level — matching the grammar/lexer convention)
WORD = "WORD"
WHITESPACE = "WHITESPACE"
LINE_COMMENT = "LINE_COMMENT"
BLOCK_COMMENT = "BLOCK_COMMENT"
UNRESTRICTED_NAME = "UNRESTRICTED_NAME"
STRING = "STRING"
SYMBOL = "SYMBOL"
LBRACE = "LBRACE"
RBRACE = "RBRACE"
SEMI = "SEMI"
EOF = "EOF"


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    start: int
    end: int


def token_kinds() -> list[str]:
    """All token kinds the lexer can emit (helpful for tests/tooling)."""
    return [
        WORD, WHITESPACE, LINE_COMMENT, BLOCK_COMMENT,
        UNRESTRICTED_NAME, STRING, SYMBOL, LBRACE, RBRACE, SEMI, EOF,
    ]


def _is_word_char(ch: str) -> bool:
    return ch.isalnum() or ch in "_$:-><~+*/%&|!=^?." or ch == "\\"


def tokenize_sysml(text: str) -> list[Token]:
    """Tokenize `text` with 100% byte coverage.

    Every character is consumed into exactly one token (coverage by
    construction — no gaps, no overlaps).  Braces inside comments or
    strings never become LBRACE/RBRACE.
    """
    toks: list[Token] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]

        # whitespace run
        if ch.isspace():
            j = i
            while j < n and text[j].isspace():
                j += 1
            toks.append(Token(WHITESPACE, text[i:j], i, j))
            i = j
            continue

        # line comment //
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            j = i + 2
            while j < n and text[j] not in "\r\n":
                j += 1
            toks.append(Token(LINE_COMMENT, text[i:j], i, j))
            i = j
            continue

        # block comment /* ... */ (multi-line; never split)
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            j = i + 2
            while j < n and not (text[j] == "*" and j + 1 < n and text[j + 1] == "/"):
                j += 1
            # j is at closing or EOF
            if j + 1 < n:
                j += 2  # consume '*'
            else:
                j = n  # unterminated — consume to EOF
            toks.append(Token(BLOCK_COMMENT, text[i:j], i, j))
            i = j
            continue

        # unrestricted name '...' (may contain spaces; '' = empty name)
        if ch == "'":
            j = i + 1
            while j < n and text[j] != "'":
                if text[j] == "\\":
                    j += 2  # skip escaped char (over \\' )
                    continue
                j += 1
            if j < n:
                j += 1  # closing quote
            else:
                j = n
            toks.append(Token(UNRESTRICTED_NAME, text[i:j], i, j))
            i = j
            continue

        # string literal "..." with backslash escapes
        if ch == '"':
            j = i + 1
            while j < n and text[j] != '"':
                if text[j] == "\\":
                    j += 2
                    continue
                j += 1
            if j < n:
                j += 1
            else:
                j = n
            toks.append(Token(STRING, text[i:j], i, j))
            i = j
            continue

        # single-char punctuation / braces / semicolon
        if ch == "{":
            toks.append(Token(LBRACE, ch, i, i + 1))
            i += 1
            continue
        if ch == "}":
            toks.append(Token(RBRACE, ch, i, i + 1))
            i += 1
            continue
        if ch == ";":
            toks.append(Token(SEMI, ch, i, i + 1))
            i += 1
            continue

        # word run (keywords, identifiers, numbers, multi-char operators like
        # `:>`; but stop BEFORE a comment opener `//` or `/*` glued to the
        # word — C3: `/` is a word char, so without this guard `1/* { */`
        # would lex as WORD('1/*') and the `{` inside the comment would emit
        # LBRACE)
        if _is_word_char(ch):
            j = i
            while j < n and _is_word_char(text[j]) and not (
                    text[j] == "/" and j + 1 < n and text[j + 1] in "/*"):
                j += 1
            toks.append(Token(WORD, text[i:j], i, j))
            i = j
            continue

        # any other symbol (single char, or run of symbols like :>, ::>, =>
        # that round-trip as a unit).  `;` is ALWAYS its own token (C2) so
        # statement segmentation sees every terminator.
        j = i
        while j < n and not text[j].isspace() and not _is_word_char(text[j]) \
                and text[j] not in "{}'\";" and not (
                    text[j] == "/" and j + 1 < n and text[j + 1] in "/*"):
            j += 1
        toks.append(Token(SYMBOL, text[i:j], i, j))
        i = j

    return toks
