from __future__ import annotations

import argparse

from .formats import format_selector
from .resolver import direct_stream, is_direct_media_url, stream_from_info
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
        direct_url = "https://cdn.example/live/channel.m3u8?token=smoke"
        if not is_direct_media_url(direct_url) or direct_stream(direct_url).video_url != direct_url:
            return 5
    except Exception:
        return 6
    return 0


def gui_smoke_test() -> int:
    import tkinter as tk

    from .app import VLCTubeApp
    from .logging_config import configure_logging
    from .resources import apply_window_icon

    root = tk.Tk()
    root.withdraw()
    try:
        apply_window_icon(root)
        VLCTubeApp(root, configure_logging())
        root.update_idletasks()
        root.update()
    finally:
        try:
            root.destroy()
        except tk.TclError:
            pass
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="VLCTube — resolve online video streams and play them in VLC")
    parser.add_argument("--smoke-test", action="store_true", help="run a non-GUI packaged-app self test")
    parser.add_argument("--smoke-gui", action="store_true", help="construct and process the real GUI once, then exit")
    args = parser.parse_args()
    if args.smoke_test:
        return smoke_test()
    if args.smoke_gui:
        return gui_smoke_test()

    import tkinter as tk

    from .app import VLCTubeApp
    from .logging_config import configure_logging
    from .resources import apply_window_icon

    root = tk.Tk()
    apply_window_icon(root)
    VLCTubeApp(root, configure_logging())
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
