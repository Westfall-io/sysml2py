"""Loss-minimizing IR for SysML text (issue #7).

The IR replaces the brace heuristic with a comment/string-aware parse:

  - `lexer.tokenize_sysml` tiles the input into tokens (100% coverage).
  - `statement_segments` splits the token stream into statements on
    `;` and brace boundaries, joining multi-line continuations into a
    single statement (so a 4-line transition is ONE statement, not four).
  - `parse_ir` builds a tree of `IRNode`s with kind/name/modifiers/
    type_refs/multiplicity/children/source_span/raw_text/fidelity.

Fidelity rules (loss-minimizing by design):
  - `modelled`   — the node's kind is known to the relationship model
                   (issue #6 children model) and its header decomposed.
  - `partial`    — the node's kind is known but the body/header could not
                   be fully decomposed (e.g. an unsupported construct).
  - `opaque`     — the node could not be classified (unknown construct).
At minimum it preserves the raw_text so nothing is silently dropped.

Comments are retained as IR nodes (kind `comment`).
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

from .lexer import (
    BLOCK_COMMENT,
    LBRACE,
    LINE_COMMENT,
    RBRACE,
    SEMI,
    STRING,
    SYMBOL,
    UNRESTRICTED_NAME,
    WHITESPACE,
    WORD,
    Token,
    tokenize_sysml,
)

# Node kinds
COMMENT = "comment"
PACKAGE = "package"
PART = "part"
ITEM = "item"
VALUE = "value"
ATTRIBUTE = "attribute"
CONNECTION = "connection"
PORT = "port"
STATE = "state"
TRANSITION = "transition"
ACTION = "action"
REQUIREMENT = "requirement"
USE_CASE = "use_case"

# Structural IR kinds that must never be produced by kind-derivation from the
# relationship model — the model vocab contains `comment`, and deriving it
# would collide with the structural comment node kind, turning a flagged loss
# into a clean `modelled` report (round-4 C1).
_RESERVED_KINDS = frozenset({"root", "brace_open", "brace_close", "block", "comment", "unknown"})
INTERFACE = "interface"
CONSTRAINT = "constraint"
OCCURRENCE = "occurrence"
IMPORT = "import"
UNKNOWN = "unknown"

# kind->"def" keyword that declares it (used for header classification)
_KIND_KEYWORDS = {
    "package": "package",
    "part": "part",
    "item": "item",
    "value": "value",
    "attribute": "attribute",
    "connection": "connection",
    "port": "port",
    "state": "state",
    "transition": "transition",
    "action": "action",
    "requirement": "requirement",
    "use_case": "use_case",
    "interface": "interface",
    "constraint": "constraint",
    "occurrence": "occurrence",
    "import": "import",
}

# No static keyword may be a reserved structural kind — if a future addition
# overlaps, the derivation guard (which runs first) still wins, but the
# contradiction is a bug worth failing fast on (round-5 W2).
assert not (_RESERVED_KINDS & set(_KIND_KEYWORDS)), \
    f"reserved structural kinds overlap static keywords: {sorted(_RESERVED_KINDS & set(_KIND_KEYWORDS))}"

# The full member-kind vocab derived from the issue-6 children model
# (`spec/relationships/children.json` in the lab).  It is EMBEDDED here so the
# IR classifies these kinds correctly whether the model file is reachable (the
# lab, where it sits at <root>/spec/relationships/children.json) or not (an
# installed wheel of the distributable, which has no spec/ dir).  Previously
# the fallback was an empty set, which silently degraded kinds like `actor`,
# `subject`, `flow`, `message`, `enumeration`, `allocation`, `view`, and
# `calculation` to `opaque` — real model kinds named by the `_is_kind_word`
# comment as "must not be downgraded".  The lookup below becomes an optional
# refinement; this embedded set is the always-available baseline.
_DERIVED_KIND_VOCAB = frozenset({
    "action", "actionnode", "actiontargetsuccession", "actor", "alias",
    "allocation", "analysiscase", "annotating", "assertconstraint",
    "association", "associationstructure", "attribute", "behavior",
    "behaviorusage", "bindingconnector", "booleanexpression", "calculation",
    "case", "class", "classifier", "comment", "concern",
    "conjugatedporttyping", "conjugation", "connection", "connector",
    "constraint", "datatype", "defaultinterfaceend", "defaultreference",
    "definition", "dependency", "disjoining", "doaction", "documentation",
    "elementfilter", "entryaction", "entrytransition", "enumeratedvalue",
    "enumeration", "enumerationusage", "eventoccurrence", "exhibitstate",
    "exitaction", "expose", "expression", "extended", "feature",
    "featureinverting", "flowconnection", "framedconcern", "function",
    "guardedsuccession", "guardedtargetsuccession", "import",
    "includeusecase", "individual", "initialnode", "interaction",
    "interface", "interfacenonoccurrenceusage", "interfaceoccurrenceusage",
    "invariant", "item", "itemflow", "librarypackage", "message",
    "metaclass", "metadata", "metadatabody", "metadatabodyusage",
    "multiplicityrange", "multiplicitysubset", "namespace", "nonfeature",
    "nonoccurrenceusage", "objective", "objectiverequirement", "occurrence",
    "occurrenceusage", "ownedexpression", "ownedfeaturetyping", "package",
    "part", "performaction", "port", "portion", "predicate", "redefinition",
    "reference", "rendering", "requirement", "requirementconstraint",
    "requirementverification", "resultexpression", "returnfeature",
    "returnparameter", "satisfyrequirement", "specialization",
    "stakeholder", "state", "stateaction", "step", "structure",
    "structureusage", "subclassification", "subject", "subsetting",
    "succession", "successionflowconnection", "successionitemflow",
    "targetsuccession", "targettransition", "targettransitionusage",
    "textualrepresentation", "transition", "transitionusage", "type",
    "typefeaturing", "usecase", "variantreference", "variantusage",
    "verificationcase", "view", "viewpoint", "viewrendering",
})


def _kind_vocab_from_model(model_path: str | None = None) -> set[str]:
    """Build the set of known member-kind stems from the issue-6 children
    model (`spec/relationships/children.json`).

    Returns the embedded ``_DERIVED_KIND_VOCAB`` when the model file is
    unavailable (an installed distributable), so classification stays complete
    with no filesystem dependency.  When the file IS reachable (the lab), it
    returns the file-derived set so the two stay in lockstep.
    """
    import json
    import re
    from pathlib import Path

    path = Path(model_path) if model_path else None
    if path is None:
        # look for the repo-relative default
        cand = Path(__file__).resolve().parents[2] / "spec" / "relationships" / "children.json"
        if cand.exists():
            path = cand
    if path is None or not path.exists():
        return set(_DERIVED_KIND_VOCAB)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set(_DERIVED_KIND_VOCAB)
    kinds: set[str] = set()
    for body_entries in data.get("bodies", {}).values():
        for entry in body_entries:
            for k in entry.get("kinds", []):
                stem = re.sub(r"(Member|Definition|Element|Usage)$", "", k).lower()
                kinds.add(stem)
            stem = re.sub(r"(Member|Definition|Element|Usage)$", "", entry.get("wrapper", "")).lower()
            kinds.add(stem)
    return kinds


@dataclass
class IRNode:
    kind: str
    name: str = ""
    short_name: str = ""
    modifiers: list[str] = field(default_factory=list)
    type_refs: list[str] = field(default_factory=list)
    multiplicity: str | None = None
    children: list[IRNode] = field(default_factory=list)
    source_span: tuple[int, int] = (0, 0)
    raw_text: str = ""
    fidelity: str = "modelled"

    def walk(self) -> Iterator[IRNode]:
        """Yield self and all descendants (preorder)."""
        yield self
        for c in self.children:
            yield from c.walk()

    def dump(self, indent: int = 0) -> str:
        pad = "  " * indent
        lines = [
            (
                f"{pad}{self.kind} name={self.name!r} mods={self.modifiers} "
                f"types={self.type_refs} mult={self.multiplicity} "
                f"fid={self.fidelity} span={self.source_span}"
            )
        ]
        for c in self.children:
            lines.append(c.dump(indent + 1))
        return "\n".join(lines)


# --------------------------------------------------------------------------
# Statement segmentation
# --------------------------------------------------------------------------

def statement_segments(text: str) -> list[str]:
    """Split `text` into statements (strings)."""
    return [text[s:e] for s, e in _statement_spans(text)]


def _statement_spans(text: str) -> list[tuple[int, int]]:
    """Split `text` into (start, end) statement spans.

    Segmentation boundaries: `;`, `{`, `}`.  Each terminator ends the
    current statement.  Multi-line continuations (a statement with no `;`
    that continues on the next line) are JOINED into a single span — so a
    4-line `transition ... first ... accept ... then ...;` is one segment.

    `{` and `}` each become their own span so the tree builder can place
    them, and the statement that opens a block (its header) is a separate
    span.  Comments are folded into their surrounding statement span
    (retained, never deleted) or become a comment-only span.
    """
    toks = tokenize_sysml(text)
    spans: list[tuple[int, int]] = []
    cur: list[tuple[int, int]] = []  # token spans of the current statement

    def flush():
        nonlocal cur
        if cur:
            s0 = min(s for s, _ in cur)
            e1 = max(e for _, e in cur)
            spans.append((s0, e1))
            cur = []

    for t in toks:
        if t.kind == WHITESPACE:
            continue
        if t.kind in (LINE_COMMENT, BLOCK_COMMENT):
            # A comment with no code yet in `cur` is a STANDALONE comment:
            # flush it as its own segment immediately (C1).  Otherwise it is
            # trailing trivia on the current statement — fold it in, so the
            # comment is retained with the statement it decorates.
            if not cur:
                cur.append((t.start, t.end))
                flush()
            else:
                cur.append((t.start, t.end))
            continue
        cur.append((t.start, t.end))
        if t.kind == SEMI:
            flush()
        elif t.kind == LBRACE:
            # close the header segment BEFORE the brace so `{` is its own span
            cur.pop()  # remove the brace from the header span
            flush()
            # reopen with just the brace
            cur.append((t.start, t.end))
            flush()
        elif t.kind == RBRACE:
            # close content, then `}` is its own span
            cur.pop()
            flush()
            cur.append((t.start, t.end))
            flush()
    flush()
    return spans


# --------------------------------------------------------------------------
# IR parsing
# --------------------------------------------------------------------------

def _parse_header(tokens: list[Token], vocab: set[str] | None = None) -> dict:
    """Decompose a statement's header token list into kind/name/modifiers/
    type_refs/multiplicity.

    `vocab` is the set of known member-kind stems from the issue-6 children
    model; when a leading keyword is in the vocabulary it classifies as
    `modelled` (the relationship model says that member kind is valid).
    """
    words = [t.text for t in tokens if t.kind in (WORD, UNRESTRICTED_NAME, SYMBOL, STRING)]
    # The derived vocabulary is the model's OWN stems, matched case-sensitively:
    # `_kind_vocab_from_model` already lowercases every stem, and the language is
    # case-sensitive — `Part`/`Actor` are CamelCase TYPE NAMES, not keywords.
    # Case-insensitive matching would over-classify identifiers as kinds and
    # suppress the parent's `partial`, hiding a loss (round-5 C1).  Quoted
    # names (`'Agree on adoption'`) retain their delimiters, so they cannot
    # collide with a bare vocab stem (round-5 W3).
    norm_vocab = set(vocab) if vocab else None

    def _is_kind_word(w: str) -> bool:
        # a kind token is either a static keyword OR a recognized stem from
        # the relationship-model vocabulary (round-3 C1: derive, don't just
        # validate — `actor`/`subject`/`message`/... are real model kinds
        # that must not be downgraded to opaque).
        # The reserved-structural guard runs FIRST so no future overlap with
        # _KIND_KEYWORDS can bypass it (round-5 W2).
        if w.lower() in _RESERVED_KINDS:
            return False
        if w in _KIND_KEYWORDS:
            return True
        return norm_vocab is not None and w in norm_vocab

    kind = None
    name = ""
    short_name = ""
    modifiers: list[str] = []
    type_refs: list[str] = []
    multiplicity: str | None = None
    # walk words.  Modifiers and operators may appear before the kind keyword
    # (C4) and the kind keyword may appear at any position; operators like
    # ':>' ':' denote type refs and are checked BEFORE the name branch so the
    # operator never becomes the name (C5).  `<shortName>` becomes short_name.
    i = 0
    while i < len(words):
        w = words[i]
        # two-word kind: 'use case'
        if w == "use" and i + 1 < len(words) and words[i + 1] == "case" and kind is None:
            kind = "use_case"
            i += 2
            continue
        if _is_kind_word(w) and kind is None:
            kind = w
            i += 1
            continue
        if kind is None and w in ("private", "public", "protected", "ref",
                                  "readonly", "derived", "end", "abstract",
                                  "variation", "in", "out", "inout",
                                  "individual", "snapshot", "timeslice"):
            modifiers.append(w)
            i += 1
            continue
        if w == "def":
            i += 1
            continue
        # short name <...> — becomes short_name, never name
        if w.startswith("<") and w.endswith(">") and not short_name:
            short_name = w.strip("<>")
            i += 1
            continue
        # operator / type-ref branch (C5: BEFORE name)
        if w in (":>", ":>>", ":", "=", ":=", "::>"):
            i += 1
            if i < len(words):
                type_refs.append(words[i])
                i += 1
            continue
        if w == "[":
            j = i + 1
            buf = []
            while j < len(words) and words[j] != "]":
                buf.append(words[j])
                j += 1
            multiplicity = "".join(buf) if buf else "*"
            i = j + 1
            continue
        if kind is None:
            kind = "unknown"
        # name token (first non-operator, non-keyword token)
        if not name and w != "def":
            name = w.strip("'\"")
            i += 1
            continue
        # any other token after name — skip
        i += 1

    if kind is None:
        kind = "unknown"
    if not short_name:
        short_name = name
    # fidelity: 'modelled' iff the kind is recognized.  kind is now DERIVED
    # from the relationship-model vocabulary (with _KIND_KEYWORDS as the
    # fallback), so every non-unknown kind is a genuine model kind — opaque
    # is then reserved strictly for "could not be classified" (round-3 C1).
    known = kind != "unknown"
    return {
        "kind": kind,
        "name": name,
        "short_name": short_name,
        "modifiers": modifiers,
        "type_refs": type_refs,
        "multiplicity": multiplicity,
        "known": known,
    }


def _classify_header(header_text: str, vocab: set[str] | None = None) -> dict:
    """Classify a header string into IR fields (used by parse_ir)."""
    toks = tokenize_sysml(header_text)
    return _parse_header(toks, vocab)


def parse_ir(text: str, model_path: str | None = None) -> IRNode:
    """Parse SysML text into an IR tree.

    Strategy: tokenize; segment into statements (; and brace aware);
    build a tree by walking statements and brace depth; classify each
    statement's header via `_parse_header`; attach statements as children of
    the current block.  Comments become `comment` IR nodes (not deleted).

    `model_path` optionally points at the issue-6 `children.json` used to
    classify `kind`/fidelity as modelled vs opaque rather than guessed.
    """
    vocab = _kind_vocab_from_model(model_path)
    segs = _statement_spans(text)
    root = IRNode(kind="root", source_span=(0, len(text)), raw_text="")
    stack: list[IRNode] = [root]
    depth = 0

    for (st, en) in segs:
        seg_text = text[st:en].strip()
        if not seg_text:
            continue
        parent = stack[-1] if stack else root

        # comment segments -> comment nodes
        if seg_text.lstrip().startswith("//") or seg_text.lstrip().startswith("/*"):
            node = IRNode(
                kind=COMMENT,
                raw_text=text[st:en],
                source_span=(st, en),
                fidelity="modelled",
            )
            parent.children.append(node)
            continue

        # `{` opens a block: the node we just created becomes the container
        if seg_text == "{":
            brace = IRNode(kind="brace_open", source_span=(st, en), raw_text="{")
            # W5 (r1) + W1 (r2) + W-A (r3): only treat the last child as a
            # real opener if it is a statement/kind node — never a comment, a
            # previous block's brace_close, a brace, an anonymous block, a
            # node that already owns a closed body, OR a `;`-terminated
            # statement (which cannot open a following block).
            opener = None
            if parent.children:
                cand = parent.children[-1]
                if cand.kind not in ("comment", "brace_close", "brace_open", "block") \
                        and not any(c.kind == "brace_close" for c in cand.children) \
                        and not cand.raw_text.rstrip().endswith(";"):
                    opener = cand
            if opener is not None:
                opener.children.append(brace)
                stack.append(opener)
            else:
                # anonymous block (W4: the brace child carries the byte, so
                # blk itself has NO raw_text — and no span to avoid a
                # double-count in tiling checks, r2 W2)
                blk = IRNode(kind="block", source_span=(st, st), raw_text="")
                parent.children.append(blk)
                blk.children.append(brace)
                stack.append(blk)
            depth += 1
            continue
        # `}` closes a block: brace_close goes inside the block we're closing
        if seg_text == "}":
            brace = IRNode(kind="brace_close", source_span=(st, en), raw_text="}")
            if len(stack) > 1:
                stack[-1].children.append(brace)
                stack.pop()
            else:
                stack[-1].children.append(brace)
            depth = max(0, depth - 1)
            continue

        # ordinary statement
        hdr = _classify_header(seg_text, vocab)
        node = IRNode(
            kind=hdr["kind"],
            name=hdr["name"],
            short_name=hdr["short_name"],
            modifiers=hdr["modifiers"],
            type_refs=hdr["type_refs"],
            multiplicity=hdr["multiplicity"],
            source_span=(st, en),
            raw_text=text[st:en],
            fidelity="modelled" if hdr["known"] else "opaque",
        )
        parent.children.append(node)

    # W2: assign `partial` — a known-kind node whose body contains opaque
    # regions is not fully modelled.  Walk bottom-up: a node is `partial` if
    # it (or any descendant) is opaque; remaining known kinds stay `modelled`.
    def _mark_partial(n: IRNode) -> bool:
        has_opaque = n.fidelity == "opaque"
        for c in n.children:
            has_opaque = _mark_partial(c) or has_opaque
        if has_opaque and n.fidelity == "modelled" and n.kind not in (
                "root", "brace_open", "brace_close", "comment", "block"):
            n.fidelity = "partial"
        return has_opaque

    _mark_partial(root)

    # root range is whole text (nodes may have overlaps with whitespace but
    # raw_text coverage assertion is on texts, not spans)
    return root


def render_ir(root: IRNode, indent: int = 0) -> str:
    """Render an IR tree back to text.

    The IR is loss-minimizing: every node's raw_text tiles the source in
    source order (preorder == source order for statements), so rendering is
    simply concatenating raw_text in preorder.  Inter-statement whitespace
    (not owned by any node) is not reproduced — the issue's acceptance
    criterion is round-trip under normalization, which collapses whitespace
    anyway.

    LINE-COMMENT TERMINATION (issue #8 corpus casting): a `//` line comment's
    lexical effect runs to end-of-line.  Because nodes concatenate without
    newlines (inter-statement whitespace is not owned by nodes), a `//`
    comment node whose raw_text does not end in a newline would swallow every
    following statement on re-parse.  To keep the round-trip faithful, emit a
    newline after any rendered `//` comment that is not already newline-
    terminated.  (Block comments `/* */` terminate themselves.)
    """
    out: list[str] = []
    for n in root.walk():
        raw = n.raw_text
        out.append(raw)
        if n.kind == "comment" and raw.lstrip().startswith("//") \
                and not raw.endswith("\n"):
            out.append("\n")
    return "".join(out)


def ir_fidelity_summary(root: IRNode, source: str | None = None) -> dict:
    """Per-file fidelity summary: counts of modelled/partial/opaque nodes
    plus byte coverage of each fidelity class (issue #7: fidelity reported
    per file so opaque regions are visible, not lost).

    When `source` is given, the report also includes a coverage ratio and
    an `uncovered_non_whitespace_bytes` count so a reader can distinguish
    "N bytes of dropped whitespace" from "N bytes of dropped code" (W7/W9).
    """
    counts = {"modelled": 0, "partial": 0, "opaque": 0}
    bytes_by_fid = {"modelled": 0, "partial": 0, "opaque": 0}
    covered = 0
    for n in root.walk():
        f = n.fidelity if n.fidelity in counts else "opaque"
        counts[f] += 1
        bytes_by_fid[f] += len(n.raw_text)
        covered += len(n.raw_text)
    out = {
        "node_counts": counts,
        "raw_text_bytes": bytes_by_fid,
        "total_raw_bytes": covered,
    }
    if source is not None:
        nws = sum(1 for ch in source if not ch.isspace())
        out["source_bytes"] = len(source)
        out["covered_non_whitespace_bytes"] = sum(
            1 for n in root.walk() for ch in n.raw_text if not ch.isspace())
        out["uncovered_non_whitespace_bytes"] = nws - out["covered_non_whitespace_bytes"]
        out["coverage_ratio"] = covered / len(source) if source else 0.0
    return out


def ir_to_json(root: IRNode) -> dict:
    """Serialize an IR tree to a JSON-friendly dict (issue #7 deliverable).

    NOTE (W10): `source_span` is stored as a list in JSON (its natural JSON
    shape) and restored as a `tuple[int, int]` by `ir_from_json`; the
    round-trip is stable (ir_to_json(ir_from_json(x)) == ir_to_json(x)).
    """
    return {
        "kind": root.kind,
        "name": root.name,
        "short_name": root.short_name,
        "modifiers": list(root.modifiers),
        "type_refs": list(root.type_refs),
        "multiplicity": root.multiplicity,
        "source_span": list(root.source_span),
        "raw_text": root.raw_text,
        "fidelity": root.fidelity,
        "children": [ir_to_json(c) for c in root.children],
    }


def ir_from_json(d: dict) -> IRNode:
    """Reconstruct an IRNode tree from `ir_to_json` output."""
    return IRNode(
        kind=d.get("kind", "root"),
        name=d.get("name", ""),
        short_name=d.get("short_name", ""),
        modifiers=list(d.get("modifiers", [])),
        type_refs=list(d.get("type_refs", [])),
        multiplicity=d.get("multiplicity"),
        source_span=tuple(d.get("source_span", (0, 0))),
        raw_text=d.get("raw_text", ""),
        fidelity=d.get("fidelity", "modelled"),
        children=[ir_from_json(c) for c in d.get("children", [])],
    )
