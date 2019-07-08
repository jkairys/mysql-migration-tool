import pytest
from package.migration_tool.model.migration_file import SemVer


def test_semver_parse():
    v = SemVer.from_string("1.3.0")
    assert v.major == 1
    assert v.minor == 3
    assert v.patch == 0

    v = SemVer.from_string("0.0.1")
    assert v.major == 0
    assert v.minor == 0
    assert v.patch == 1

    with pytest.raises(ValueError):
        SemVer.from_string("1.0")

    with pytest.raises(ValueError):
        SemVer.from_string("apples.0.0")


def test_semver_comparison():
    assert SemVer.from_string("1.2.0").is_greater_than(SemVer.from_string("1.1.0"))
    assert not SemVer.from_string("1.2.0").is_greater_than(SemVer.from_string("1.2.0"))
    assert not SemVer.from_string("1.2.0").is_greater_than(SemVer.from_string("3.10.0"))
    assert SemVer.from_string("0.2.10").is_greater_than(SemVer.from_string("0.2.1"))
