import pytest

from vlctube.formats import QUALITY_PRESETS, format_selector


def test_all_presets_have_selectors():
    assert set(QUALITY_PRESETS) == {"best", "1080p", "720p", "480p", "360p", "audio"}
    assert all(format_selector(name) for name in QUALITY_PRESETS)


def test_unknown_preset():
    with pytest.raises(ValueError):
        format_selector("8k")
