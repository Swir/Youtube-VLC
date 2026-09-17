import pytest

from vlctube.url_tools import is_supported_url, normalize_url


def test_valid_https_url():
    value = "https://example.com/watch?v=123"
    assert normalize_url(value) == value
    assert is_supported_url(value)


@pytest.mark.parametrize("value", ["", "ftp://example.com/video", "example.com/video", "https://user:pass@example.com/video"])
def test_invalid_urls(value):
    assert not is_supported_url(value)
    with pytest.raises(ValueError):
        normalize_url(value)
