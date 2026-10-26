# Contributing to sysml2py

This project is the **generation distributable** in the Westfall SysMLv2 stack: it
is the generated Python library (AST classes + builder API + printer) that
Vesara and Brella author their models with, and the counterpart to the
`sysml2py-lab` factory that generates it and the `windtrader` validator that
reads/validates it. This page sets the contribution and release conventions so
the generation pipeline stays predictable.

## The house rule (feature flow)

Every change — feature, fix, or docs — ships the same way:

1. Create a feature branch off `main` (`feat/…`, `fix/…`, `docs/…`,
   `release/vX.Y.Z`).
2. Commit gitmoji-conventional messages (e.g. `✨ feat: …`, `🐛 fix: …`,
   `📝 docs: …`).
3. Open a PR → Claude Code review → address findings → **merge only after the
   reviewer passes** (or explicit direction from the owner).
4. Merge with `--no-ff` and a `🔀 merge(pr#N): …` commit; delete the branch.

**Never commit to `main` directly.** `main` must stay **always deployable** —
the CI gate (tests + ruff + casting/round-trip + windtrader validation) is what
keeps that true, and it runs on every PR.

## Release cadence (trunk accumulation + release-train batching)

`main` *is* the dev line — work merges to it continuously, per the house rule.
Releases are cut at **chosen batch points**, not per-PR.

- **Minor releases** (`1.x`) happen when a coherent batch is on `main` —
  roughly two or more feature PRs merged, or a named milestone complete.
  The batch is defined by *what has already merged to main*; it is never built
  by holding PRs open or running a long-lived `dev` branch.
- **Patch releases** (`1.x.y`) are **immediate** — a packaging break, a docs
  fix, or a validation regression ships on its own and does **not** wait for a
  feature batch. Patch releases never queue behind the train.
- **Cutting a release** is a `release/vX.Y.Z` branch off `main` that bumps the
  four version-stamp files in lockstep (`pyproject.toml`, `__init__.py`,
  `provenance.py`, README example), updates the CHANGELOG, gets its own review,
  then merges and tags `vX.Y.Z`. Pushing the tag drives the automated release
  pipeline (PyPI publish + GitHub Release with wheel/sdist attached).

Rationale: per-feature releases create version churn and meaningless ceremony
(e.g. a docs-only `1.0.1`). Batching keeps semver honest — minor per
feature-batch, patch per fix — and keeps the release pipeline exercised on a
regular cadence, without the two-long-lived-branches cost of a `dev` branch
that this repo consciously abandoned at the 1.0.0 rewrite.

## Coordinate before you change the surface

- **Generation behavior** (builder API, emitted SysML syntax, casting): this is
  Jasper's anvil — involve the generation owner before a render path changes
  how a model is expressed.
- **Parsing / reading / validating**: the `windtrader` team reads what this
  library emits. Before any emitted-syntax or structure change, coordinate so
  the text we write and the tools that read it stay in agreement.
- **Model authors** (Vesara, Brella): a change that alters how their models are
  expressed needs their sign-off before shipping.

## The casting standard

Before output ships, prove **The Casting**: Python model → emit textual
`.sysml` → parse back → re-parsed structure equals the original model,
element-for-element — no loss, no drift, no invented syntax. A generator path
that cannot round-trip its own output does not ship.
