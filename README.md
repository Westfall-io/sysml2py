# sysml2py

**A pure-Python library for building SysML v2 models — generated, not handcrafted.**

`sysml2py` is a drop-in Python API for constructing SysML v2 textual models.
You write Python; it emits spec-correct `.sysml` notation. Its AST node
classes, builder API, and printer are **deterministically generated** from the
SysML v2 grammar by a companion project (`sysml2py-lab`) — so the library
stays in lockstep with the language instead of drifting behind a hand-written
parser.

```python
from sysml2py import PackageBuilder, Part, Attribute

pkg = PackageBuilder('MyModel')
stage = Part('Stage_1')
stage.add(Attribute('mass'))
stage.add(Attribute('thrust'))
pkg.add(stage)
print(pkg.dump())
```

```sysml
package MyModel
{
   part Stage_1
   {
      attribute mass;
      attribute thrust;
   }
}
```

---

## Why a full overhaul? What happened before 1.0.0

The 0.5.x line was a **hand-maintained parser** built on textX, astropy, and
PyYAML (`grammar/SysML_compiled.tx` + hand-written classes) that loaded slow,
dragged in heavy runtime dependencies, and covered only a sliver of SysML v2.
Maintaining it meant hand-editing parser code every time the language moved.

**1.0.0 is a ground-up rewrite with a different philosophy.** We no longer
handcraft the implementation. Instead, `sysml2py-lab` — the generation
factory — consumes:

1. the **SysML v2 grammar** (the authoritative syntax + relationships),
2. a **relationship model** of which modifiers and children each element
   allows, and
3. a growing **corpus** of real models as usage evidence,

…and **deterministically generates** the entire `sysml2py` library from
those inputs. No growing pile of hand-written classes to maintain — when the
language or the corpus changes, we regenerate.

### What that buys you

- **Pure standard library at runtime.** `pip install sysml2py` now pulls
  *nothing* beyond the stdlib — no textX, no astropy, no yaml. (The old 0.5.x
  line shipped a textX-backed parser with astropy as a runtime dependency.)
- **Broad AST coverage with an honest fallback.** Hundreds of generated node
  classes mirror the grammar rules. Constructs not yet structurally
  represented are preserved as `Unsupported` nodes carrying their raw text —
  **zero `NotImplementedError`**; nothing is silently dropped.
- **Reproducible provenance.** Every install records the exact grammar, spec,
  relationship-model, and corpus SHAs plus the generator version that
  produced the wheel — you can always prove *which* inputs your library came
  from.
- **A cast that stays true.** Generated output is re-parsed and compared
  element-for-element against the model that produced it, and validated
  against an independent SysML v2 oracle — **if it doesn't round-trip, it
  doesn't ship.**

### Why generate instead of handcrafting it ourselves?

Two words: **drift and scale.**

Hand-written parsers drift. They accumulate special cases, silently diverge
from the spec, and every grammar adjustment becomes a manual archaeology
project. Generation inverts that: the *grammar is the source of truth*, and
the implementation is derived from it mechanically. When SysML v2 evolves or
the corpus reveals a new construct, we update the inputs and regenerate —
the whole library stays consistent by construction, and a regression that
breaks an earlier model is caught the same way it was introduced.

This is the same reason we validate the output against an external oracle
rather than our own assumptions: the generator never gets to grade its own
homework.

---

## Building a model (friendly builder API)

Friendly names drop the `Builder`/`Usage`/`Definition` suffixes — `Part`,
`Attribute`, `Item`, `Port`, `Requirement`, `Reference`, ... are builders.
Usage vs. definition is chosen at creation via `kind=`; `add()` appends
children so a full package dumps from nested composition.

```python
from sysml2py import PackageBuilder, Part

pkg = PackageBuilder('Rocket')
pkg.add(Part('Stage_1'))
pkg.add(Part('Stage_2'))
print(pkg.dump())
```

```sysml
package Rocket
{
   part Stage_1;
   part Stage_2;
}
```

A *definition* is the same class with `kind=` at creation:

```python
>>> Part('Stage_1', kind='definition').dump()
'part def Stage_1;'
```

Kinds without a definition form (`Package`, `Comment`, `Actor`,
`Reference`, `Transition`, `Import`, `Message`, `Succession`,
`AliasMember`, `Subject`, `ObjectiveRequirement`) reject
`kind='definition'` with a `ValueError` — the generator never emits a
definition it cannot cast back, and a class-name kind like
`'PartDefinition'` raises too, since it would print invalid SysML.

Container names that collide with AST node classes (`Package`, `Comment`,
`Import`, `Message`, `Succession`, `AliasMember`) keep the `*Builder`
suffix — use `PackageBuilder`, `ImportBuilder`, etc. The classic `*Builder`
names (`PartUsageBuilder`, ...) remain available if you prefer them.

## Units

Value-bearing attributes are first-class. Pass a value and a unit and the
unit is imported automatically as a `public import` (KERML-74 requires an
explicit visibility modifier):

```python
>>> Attribute('mass', value=1000, unit='kg').dump()
'attribute mass = 1000[kg];'
```

```sysml
public import SI::kg;
attribute mass = 1000[kg];
```

You can also pass an astropy `Quantity` and the unit is derived from it:

```python
import astropy.units as u
Attribute('mass', value=1000 * u.kg)
```

Since the runtime itself stays pure-stdlib, astropy is **not** bundled — add
`import astropy.units as u` yourself if you use this form.

## Provenance & reproducibility

Check which exact inputs produced an install:

```python
from sysml2py import provenance
print(provenance.PROVENANCE)
```

```python
{'grammar_sha256': '...', 'spec_sha256': '...',
 'children_sha256': '...', 'modifiers_sha256': '...',
 'corpus_manifest_sha256': '...', 'generator_version': '1.0.0'}
```

## Also in the package

The generated AST classes and helpers are all public: `Node` and its
hundreds of subclasses, `walk` / `walk_preorder` / `walk_postorder` /
`find_all` traversal, `printer` / `beautify`, `normalize_text`,
`canonical_equals` for structure-aware comparison, and the `*Builder`
classes. See the [wiki](https://github.com/Westfall-io/sysml2py/wiki) for
tutorials and deeper examples.

## Compatibility & migrating from 0.5.x

This is the **1.x** line. The builder API *shape* you remember is preserved
(`Part`, `Attribute`, `Item`, `Port`, `_set_name`, `_set_child`,
`get_definition`, `dump()`), but there are deliberate breaking changes:

- **No runtime deps** — 0.5.x bundled astropy; 1.0.0 does not. Add
  `import astropy.units as u` yourself where you use units.
- **Usage vs. definition chosen at creation** via `kind=` (0.5.x inferred it
  differently); friendly names drop the `Builder`/`Usage`/`Definition`
  suffixes.
- `set_value` is gone — pass `value=` / `unit=` to the builder constructor.

For the full step-by-step migration guide, see
[**migration-0.5-to-1.0.md**](https://github.com/Westfall-io/sysml2py-lab/blob/main/docs/migration-0.5-to-1.0.md)
in the `sysml2py-lab` repo.

---

## Background

- **`sysml2py`** (this repo) — the generated, distributable library on PyPI.
- **`sysml2py-lab`** — the generation factory that produces this library from
  the SysML v2 grammar, relationship model, and corpus. Grammar and corpus
  content, and bug reports against generated behavior, live there.
- **Windtrader** — the independent SysML v2 validator used as the
  correctness oracle during generation.

## License

MIT.
