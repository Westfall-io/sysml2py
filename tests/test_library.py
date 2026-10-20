"""Self-contained tests for the generated sysml2py library.

This suite tests the COMMITTED generated library directly (no sysml2py-lab
dependency at runtime — AC8 of the generation epic: the distributed library
must not import lab code or the corpus).

The deep emit -> parse-back casting lives in the lab's suite
(sysml2py-lab tests/test_ast_codegen.py, 268 tests + regress harness).
Here we verify the shipped guarantees:
  - friendly builder API (issue #27)
  - import visibility emission (KERML-74, issue #23)
  - value-bearing attributes / units (issue #26)
  - provenance stamp (issue #13)
  - pure-stdlib runtime (no textx/astropy/yaml/lab)
"""

import re
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

PKG_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PKG_ROOT / "src"))


def _package():
    import sysml2py

    return sysml2py


# ---------------------------------------------------------------------------
# Friendly builder API (issue #27)
# ---------------------------------------------------------------------------


def test_friendly_names_emit_expected_keyword():
    """Issue #27: friendly names exist and emit the correct SysML keyword.
    This catches the `use_case S;` class of bug (wrong keyword for the kind).
    """
    sysml2py = _package()
    expected = {
        "Part": "part",
        "Attribute": "attribute",
        "Item": "item",
        "Port": "port",
        "Requirement": "requirement",
        "Reference": "reference",
    }
    for name, keyword in expected.items():
        cls = getattr(sysml2py, name)
        assert issubclass(cls, sysml2py.Builder), f"{name} not a Builder"
        assert (
            cls("S").dump().lstrip().startswith(keyword)
        ), f"{name} emitted wrong keyword: {cls('S').dump()!r}"


def test_kind_selection_usage_vs_definition():
    sysml2py = _package()
    assert sysml2py.Part("S").dump().strip() == "part S;"
    assert sysml2py.Part("S", kind="definition").dump().strip() == "part def S;"
    assert sysml2py.Part("S", kind="def").dump().strip() == "part def S;"
    assert sysml2py.Part("S", kind="part").dump().strip() == "part S;"
    for bad in ("PartDefinition", "PartUsage", "bogus"):
        with pytest.raises(ValueError):
            sysml2py.Part("S", kind=bad)


def test_add_appends_children_and_dumps_nested_package():
    sysml2py = _package()
    pkg = sysml2py.PackageBuilder("MyModel")
    stage = sysml2py.Part("Stage_1")
    stage.add(sysml2py.Attribute("mass"))
    stage.add(sysml2py.Attribute("thrust"))
    pkg.add(stage)
    out = pkg.dump()
    assert "package MyModel" in out
    assert "part Stage_1" in out
    assert "attribute mass" in out
    assert "attribute thrust" in out


# ---------------------------------------------------------------------------
# Import visibility (KERML-74, issue #23)
# ---------------------------------------------------------------------------


def test_import_defaults_to_public():
    sysml2py = _package()
    assert "public import SI::kg;" in sysml2py.ImportBuilder("SI::kg").dump()


def test_import_explicit_private_and_protected():
    sysml2py = _package()
    imp = sysml2py.ImportBuilder("SI::m")
    imp._set_visibility("private")
    assert "private import SI::m;" in imp.dump()
    imp2 = sysml2py.ImportBuilder("SI::s")
    imp2._set_visibility("protected")
    assert "protected import SI::s;" in imp2.dump()


def test_import_never_bare():
    sysml2py = _package()
    for mod in (None, "private", "protected"):
        imp = sysml2py.ImportBuilder("SI::kg")
        if mod is not None:
            imp._set_visibility(mod)
        txt = imp.dump()
        assert re.search(r"^\s*import SI::kg;$", txt, re.MULTILINE) is None, txt
        assert re.search(r"(public|private|protected) import SI::kg;", txt), txt


def test_import_invalid_visibility_fails_loud():
    sysml2py = _package()
    with pytest.raises(ValueError):
        sysml2py.ImportBuilder("SI::kg")._set_visibility("secret")


# ---------------------------------------------------------------------------
# Units / value-bearing attributes (issue #26)
# ---------------------------------------------------------------------------


def test_attribute_value_unit_auto_imports():
    sysml2py = _package()
    pkg = sysml2py.PackageBuilder("MyModel")
    stage = sysml2py.Part("Stage_1")
    stage.add(sysml2py.Attribute("mass", value=1000, unit="kg"))
    pkg.add(stage)
    out = pkg.dump()
    assert "attribute mass = 1000[kg];" in out
    # unit import is emitted exactly once, with explicit public visibility
    assert out.count("public import SI::kg;") == 1


def test_attribute_value_unit_derived_from_quantity():
    """astropy Quantity support: unit derived from the quantity object."""
    pytest.importorskip("astropy")
    import astropy.units as u

    sysml2py = _package()
    p = sysml2py.Part("S")
    a = sysml2py.Attribute("mass", value=1000 * u.kg)
    p.add(a)
    out = p.dump()
    assert "attribute mass = 1000[kg];" in out


def test_attribute_value_unit_derived_from_pint_quantity():
    """pint Quantity support (parallel to astropy): unit derived from pint."""
    pytest.importorskip("pint")
    import pint

    ureg = pint.UnitRegistry()
    sysml2py = _package()

    # simple SI unit
    p = sysml2py.PackageBuilder("R")
    p.add(sysml2py.Attribute("mass", value=1000 * ureg.kg))
    out = p.dump()
    assert "attribute mass = 1000[kg];" in out
    assert "public import SI::kg;" in out

    # composite unit (m/s**2) — pint folds scale into magnitude
    p2 = sysml2py.PackageBuilder("R2")
    p2.add(sysml2py.Attribute("accel", value=9.8 * ureg.m / ureg.s**2))
    out2 = p2.dump()
    assert "attribute accel = 9.8[m/s**2];" in out2

    # imperial unit namespacing
    p3 = sysml2py.PackageBuilder("R3")
    p3.add(sysml2py.Attribute("vol", value=2 * ureg.gallon))
    out3 = p3.dump()
    assert "attribute vol = 2[gal];" in out3
    assert "public import USCustomaryUnits::gal;" in out3

    # dimensionless pint Quantity carries no unit
    a = sysml2py.Attribute("cnt", value=3 * ureg.dimensionless)
    assert a.dump() == "attribute cnt = 3;"


def test_pint_quantity_matches_explicit_unit():
    """pint Quantity + matching explicit unit= is accepted (no conflict)."""
    pytest.importorskip("pint")
    import pint

    ureg = pint.UnitRegistry()
    sysml2py = _package()
    a = sysml2py.Attribute("x", value=5 * ureg.m, unit="m")
    assert a.dump() == "attribute x = 5[m];"


# ---------------------------------------------------------------------------
# Provenance + self-containment (issue #13, AC8)
# ---------------------------------------------------------------------------


def test_provenance_present_and_deterministic_keys():
    from sysml2py import provenance

    for key in (
        "children_sha256",
        "corpus_manifest_sha256",
        "generated_at",
        "generator_version",
        "grammar_sha256",
        "modifiers_sha256",
        "spec_sha256",
    ):
        assert key in provenance.PROVENANCE, f"missing provenance key {key}"
    assert provenance.PROVENANCE["generator_version"] == sysml2py_version()


def sysml2py_version():
    import sysml2py

    return sysml2py.__version__


def test_version_matches_metadata():
    # derive from the packaged metadata, not a hard-coded string, so a v1.1.0
    # tag doesn't fail the release suite.  When the dist isn't installed
    # (plain `pytest tests/` via pythonpath), skip honestly rather than
    # tautologically comparing the module version to itself.
    from importlib.metadata import PackageNotFoundError, version

    try:
        installed = version("sysml2py")
    except PackageNotFoundError:
        pytest.skip("sysml2py distribution not installed")
    else:
        assert sysml2py_version() == installed


def test_import_graph_has_no_forbidden_runtime_deps():
    """AC8: the generated library must not pull textx/astropy/yaml/lab."""
    code = (
        "import sys\n"
        "import sysml2py\n"
        "loaded = {m.split('.')[0] for m in sys.modules}\n"
        "forbidden = {'textx', 'astropy', 'yaml', 'sysml2py_lab'}\n"
        "bad = sorted(forbidden & loaded)\n"
        "assert not bad, f'forbidden runtime deps: {bad}'\n"
        "print('OK', sysml2py.__version__)\n"
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        check=False,
        text=True,
        env={"PYTHONPATH": str(PKG_ROOT / "src"), "PATH": "/usr/bin:/bin"},
        cwd=PKG_ROOT,
    )
    assert proc.returncode == 0, proc.stderr
    assert f"OK {sysml2py_version()}" in proc.stdout


def test_wheel_ships_provenance_only():
    """A built wheel must carry provenance (and no dead .tx grammar).

    Run with SYML2PY_DIST_DIR set (CI builds to a temp dir); point the
    workflow at the built artifacts so THIS assertion is the single source
    of truth for wheel contents, rather than a YAML copy.
    """
    import glob
    import os

    dist_dir = os.environ.get("SYML2PY_DIST_DIR", str(PKG_ROOT / "dist"))
    wheels = glob.glob(os.path.join(dist_dir, "*.whl"))
    if not wheels:
        pytest.skip(f"no wheel in {dist_dir}")
    names = set(zipfile.ZipFile(wheels[0]).namelist())
    assert any(n.endswith("provenance.py") for n in names), "provenance missing"
    assert all(not n.endswith(".tx") for n in names), "unexpected .tx in wheel"


# ---------------------------------------------------------------------------
# Emission sanity — classic README example
# ---------------------------------------------------------------------------


def test_readme_example_casts_syntactically():
    sysml2py = _package()
    pkg = sysml2py.PackageBuilder("MyModel")
    stage = sysml2py.Part("Stage_1")
    stage.add(sysml2py.Attribute("mass"))
    stage.add(sysml2py.Attribute("thrust"))
    pkg.add(stage)
    out = pkg.dump()
    # the actual emission: braces on their own line, 3-space indent
    assert "package MyModel\n{" in out, out
    assert "part Stage_1" in out
    assert "attribute mass;" in out
    assert "attribute thrust;" in out
