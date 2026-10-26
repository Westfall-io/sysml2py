"""read_model: load a .sysml file, edit it, emit lossless SysML.

This is the read side of the read-modify-write loop.  A user script does::

    from sysml2py_lab import read_model
    from sysml2py import PackageBuilder

    model = read_model("file.sysml")        # -> an editable model (ReadModel)
    model.add(PackageBuilder("C"))          # edit with the normal builder API
    open("out.sysml", "w").write(model.dump())

The parser lives HERE (the lab), per the agreed design (B): the distributable
``sysml2py`` stays builder-only.

Fidelity (cast-true): ``dump()`` is LOSSLESS at the *model* level.  The model
wraps the parsed IR tree, and ``dump()`` renders it via ``render_ir`` — which
is canonical-equal on 62/62 corpus files (100%): same elements, kinds, names,
modifiers, children, order, values/units — nothing is dropped, reordered, or
invented.  Edits via ``model.add(builder)`` are appended; the builder renders
faithfully for authored content, so an injected package survives.

Note on layout: the model-level round-trip is structural, NOT byte-identical.
``render_ir`` concatenates each statement's raw text and discards inter-
statement whitespace (blank lines / indentation), so a hand-formatted file is
re-emitted in a compact single-flow form.  That is expected: the contract is
that the *model* survives unchanged, not the formatting.  See the spec.
"""

from __future__ import annotations

from pathlib import Path

from .ir import IRNode, parse_ir, render_ir


def _chunk(text: str) -> str:
    """Terminate a `//` line comment so later chunks aren't swallowed.

    Mirrors ``render_ir``'s guard: a ``//`` comment's lexical effect runs to
    end-of-line, so a chunk that ends in ``// note`` would comment out the
    next chunk if no newline is emitted.  Block comments ``/* */`` terminate
    themselves.
    """
    if text.lstrip().startswith("//") and not text.endswith("\n"):
        return text + "\n"
    return text


# ---------------------------------------------------------------------------
# The editable, lossless model
# ---------------------------------------------------------------------------


class ReadModel:
    """Editable wrapper over the lossless IR tree of a parsed .sysml file.

    ``dump()`` renders the IR tree losslessly via ``render_ir`` (canonical-
    equal on the whole corpus).  ``add()`` appends a builder-authored element
    (or a raw text string) to the output, spliced after the original content.

    Untouched source content is preserved at the model level: only what a
    script explicitly ``add``s is rendered fresh; the rest re-emits the
    original statement text.  (Inter-statement whitespace is normalized — see
    module docstring.)
    """

    def __init__(self, root: IRNode):
        self._root = root
        self._added: list[str] = []

    @property
    def children(self):
        """The parsed structure of the original model (read-only snapshot)."""
        return tuple(self._root.children)

    def add(self, builder_or_raw) -> ReadModel:
        """Append content to the emitted model.

        Accepts a ``sysml2py`` Builder (rendered faithfully via its
        ``dump()``) or a string of raw SysML text.  Appends at the end of the
        output.  Returns self for chaining.

        Note: for a file whose root is ``package 'X' { ... }``, ``add()``
        produces a *second* top-level element, not a member of package X.
        """
        if isinstance(builder_or_raw, str):
            text = builder_or_raw
        elif hasattr(builder_or_raw, "dump"):
            text = builder_or_raw.dump()
        else:
            raise TypeError(
                "add() expects a sysml2py Builder or a raw text string, "
                f"got {type(builder_or_raw).__name__}"
            )
        self._added.append(text)
        return self

    def dump(self) -> str:
        """Emit the model as SysML text (structural round-trip)."""
        body = render_ir(self._root)
        added = _render_added(self._added)
        if not added:
            return body
        # N6: a separator between the original body and the added block, so a
        # final `;`/`}`-unterminated statement with a trailing `//` comment
        # cannot swallow the added content.
        if body and not body.endswith("\n"):
            body += "\n"
        return body + added


def _render_added(chunks: list[str]) -> str:
    if not chunks:
        return ""
    out = [_chunk(c) for c in chunks]
    text = "\n".join(out)
    return text + ("\n" if not text.endswith("\n") else "")


# ---------------------------------------------------------------------------
# read_model entry point
# ---------------------------------------------------------------------------


def read_model(
    file: str | Path,
    *,
    model_path: str | None = None,
) -> ReadModel:
    """Load a ``.sysml`` text file into an editable, lossless model.

    Args:
        file: Path to the ``.sysml`` file to read.
        model_path: Optional path to the issue-6 ``children.json`` used to
            classify kind/fidelity (default: repo spec relationships model).

    Returns:
        A ``ReadModel`` whose ``dump()`` emits the lossless SysML text and
        whose ``add()`` appends builder-authored elements.
    """
    src_str = Path(file).read_text(encoding="utf-8")
    root = parse_ir(src_str, model_path=model_path)
    return ReadModel(root)
