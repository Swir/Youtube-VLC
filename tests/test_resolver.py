import pytest

from vlctube.resolver import direct_stream, is_direct_media_url, stream_from_info


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


def test_direct_media_url_passthrough_preserves_query_string():
    url = "https://cdn.example/live/channel.m3u8?token=abc123"
    assert is_direct_media_url(url)
    stream = direct_stream(url)
    assert stream.video_url == url
    assert stream.source_url == url
    assert stream.extractor == "Direct"


@pytest.mark.parametrize("url", [
    "https://cdn.example/movie.mp4",
    "https://cdn.example/audio.mp3?key=1",
    "https://cdn.example/live/stream.ts",
])
def test_direct_media_extensions(url):
    assert is_direct_media_url(url)


def test_normal_webpage_is_not_classified_as_direct_media():
    assert not is_direct_media_url("https://example.com/watch?v=1")


def test_missing_playable_url():
    with pytest.raises(ValueError):
        stream_from_info("https://example.com/video", {"title": "Broken"})
