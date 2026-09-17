from __future__ import annotations

import argparse

from .formats import format_selector
from .resolver import stream_from_info
from .url_tools import normalize_url


def smoke_test() -> int:
    try:
        source = normalize_url("https://example.com/watch?v=test")
        if format_selector("720p") == "":
            return 2
        fake_info = {
            "title": "Smoke Test",
            "webpage_url": source,
            "duration": 42,
            "extractor_key": "Generic",
            "requested_formats": [
                {"url": "https://cdn.example/video", "vcodec": "h264", "acodec": "none"},
                {"url": "https://cdn.example/audio", "vcodec": "none", "acodec": "aac"},
            ],
        }
        stream = stream_from_info(source, fake_info)
        if stream.video_url != "https://cdn.example/video":
            return 3
        if stream.audio_url != "https://cdn.example/audio" or not stream.has_separate_audio:
            return 4
    except Exception:
        return 5
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="VLCTube — resolve online video streams and play them in VLC")
    parser.add_argument("--smoke-test", action="store_true", help="run a non-GUI packaged-app self test")
    args = parser.parse_args()
    if args.smoke_test:
        return smoke_test()

    from .app import run

    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
