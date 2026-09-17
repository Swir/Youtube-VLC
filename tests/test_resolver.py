import pytest

from vlctube.resolver import stream_from_info


def test_stream_from_separate_av_formats():
    source = "https://example.com/watch?v=1"
    info = {
        "title": "Example",
        "duration": 123,
        "extractor_key": "Generic",
        "requested_formats": [
            {"url": "https://cdn.example/video", "vcodec": "avc1", "acodec": "none"},
            {"url": "https://cdn.example/audio", "vcodec": "none", "acodec": "mp4a"},
        ],
    }
    stream = stream_from_info(source, info)
    assert stream.title == "Example"
    assert stream.video_url == "https://cdn.example/video"
    assert stream.audio_url == "https://cdn.example/audio"
    assert stream.duration == 123
    assert stream.has_separate_audio


def test_stream_from_single_url():
    stream = stream_from_info("https://example.com/video", {"title": "Single", "url": "https://cdn.example/stream"})
    assert stream.video_url == "https://cdn.example/stream"
    assert stream.audio_url is None
    assert not stream.has_separate_audio


def test_missing_playable_url():
    with pytest.raises(ValueError):
        stream_from_info("https://example.com/video", {"title": "Broken"})
