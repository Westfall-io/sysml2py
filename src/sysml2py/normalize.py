"""Canonical SysMLv2 normalizer (issue #8).

Resolves the normalization conflict described in issue #8.  Two incompatible
definitions existed:

- Lab `normalize_text` (this module, pre-#8): collapses whitespace only.
- `sysml2py/tests/functions.py::strip_ws`: removes comments, rewrites
  `specializes`/`subsets` -> `:>` and `redefines` -> `:>>`, then DELETES all
  whitespace.  Deleting whitespace makes `part x` and `partx` compare equal
  and silently launders keyword-vs-symbol differences — a lossy comparison
  that can pass two models that are not equivalent.

The canonical normalizer is a TOKEN-STREAM comparison:

- significant tokens (words, unrestricted names, strings, symbols, braces,
  semicolons) are compared in order;
- whitespace and comments are trivia and are dropped (comments are NOT
  semantic in SysMLv2 comparison);
- an explicit, OPT-IN alias table resolves the keyword-vs-symbol spellings
  the SysMLv2 grammar treats as synonyms (`specializes` == `:>`,
  `subsets` == `:>`, `redefines` == `:>>`).  No other rewriting happens;
- `part x` and `partx` remain different, because the token stream keeps
  token boundaries — this is the property `strip_ws` violated.

This module is deliberately SELF-CONTAINED (no lab imports): the codegen
pipeline ships it verbatim into the generated `sysml2py` package so the lab
and the generated library use ONE canonical normalizer (issue #8 acceptance
criterion).  The tokenizer here is a minimal, comment/string-aware splitter
that mirrors the lexer's significant-token categories; the full lexer (with
spans and 100% byte coverage) remains the property of the IR layer.
"""

from __future__ import annotations

import re

_ws = re.compile(r"\s+")

ALIASES = {
    "specializes": ":>",
    "subsets": ":>",
    "redefines": ":>>",
}

# leading whitespace (to compute a line's indent) — not used by canonical
# comparison, kept for the legacy text normalizer
_LEAD = re.compile(r"^[ \t]+")


def normalize_text(text: str) -> str:
    """
    Legacy text-level normalizer (MVP equivalence).

    Rules:
      - Trim each line
      - Drop fully-empty lines
      - Collapse internal whitespace runs to a single space
      - Keep braces and semicolons as-is

    This collapses whitespace ONLY — it never merges or renames tokens, so
    `part x` and `partx` stay different.  It is superseded for corpus
    comparison by :func:`canonical_equals` (token-stream, alias-aware), but
    is kept for existing callers (generated `dump()` etc.).
    """
    out_lines: list[str] = []
    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            continue
        s = _ws.sub(" ", s)
        out_lines.append(s)
    return "\n".join(out_lines) + ("\n" if out_lines else "")


# ---------------------------------------------------------------------------
# Canonical token-stream normalizer
# ---------------------------------------------------------------------------

_WORD = re.compile(r"[A-Za-z0-9_]+")

# Multi-char symbols that must stay a single token (longest first).
_MULTI_SYMS = (
    "::>", ":>>", "::", ":>", "**", "&&", "||", "<<", ">>",
    "=>", ":=", "==", "->", "<=", ">=", "!=", "..",
)


def _split_significant(text: str) -> list[str]:
    """Split `text` into significant SysML tokens (no whitespace/comments).

    Minimal, self-contained, comment/string-aware splitter.  It mirrors the
    full lexer's significant categories: words/identifiers, unrestricted
    names (`'...'`), string literals (`"..."`), multi-char symbols (`:>`,
    `:>>`, `=>`, ...), single symbols, braces, and semicolons.

    Comments are skipped: line comments (`//` to EOL) and block comments
    (`/* ... */`).  This means a `{` or `;` inside a comment is never a
    significant token — same guarantee the IR lexer provides.
    """
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if ch in ("'", '"'):
            # quoted name or string literal: consume until matching quote,
            # honouring backslash escapes
            j = i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == ch:
                    break
                j += 1
            out.append(text[i : j + 1 if j < n else n])
            i = j + 1 if j < n else n
            continue
        if ch in "{};":
            out.append(ch)
            i += 1
            continue
        # multi-char symbols first (longest match)
        matched = False
        for sym in _MULTI_SYMS:
            if text.startswith(sym, i):
                out.append(sym)
                i += len(sym)
                matched = True
                break
        if matched:
            continue
        m = _WORD.match(text, i)
        if m:
            out.append(m.group(0))
            i = m.end()
            continue
        # single symbol / stray char (kept verbatim so the stream is lossless
        # for comparison purposes)
        out.append(ch)
        i += 1
    return out


def canonical_tokens(text: str, aliases: dict[str, str] | None = None) -> list[str]:
    """Return the canonical significant-token stream for `text`.

    `aliases` is the OPT-IN alias table (default: :data:`ALIASES`, resolving
    `specializes`/`subsets` -> `:>` and `redefines` -> `:>>`).  Pass
    ``aliases={}`` to disable synonym resolution entirely.
    """
    aliases = ALIASES if aliases is None else aliases
    out: list[str] = []
    for tok in _split_significant(text):
        if aliases and tok in aliases:
            out.append(aliases[tok])
        else:
            out.append(tok)
    return out


def canonical_equals(
    a: str, b: str, aliases: dict[str, str] | None = None
) -> bool:
    """Canonical equivalence: ``a`` and ``b`` have identical significant
    token streams (after optional alias resolution).  Whitespace and comments
    are ignored; token boundaries are NOT (``part x`` != ``partx``)."""
    return canonical_tokens(a, aliases) == canonical_tokens(b, aliases)


def canonicalize(text: str, aliases: dict[str, str] | None = None) -> str:
    """Return a stable, canonical textual form of `text`: significant tokens
    joined by single spaces (comments and whitespace dropped, aliases
    applied).  Two texts are canonically equal iff
    ``canonicalize(a) == canonicalize(b)``."""
    return " ".join(canonical_tokens(text, aliases))
