from __future__ import annotations

from typing import Any

from yt_dlp import YoutubeDL

from .formats import format_selector
from .models import QueueItem, ResolvedStream
from .url_tools import normalize_url


def stream_from_info(source_url: str, info: dict[str, Any]) -> ResolvedStream:
    title = str(info.get("title") or info.get("id") or "Online video")
    requested = info.get("requested_formats") or []

    video_url: str | None = None
    audio_url: str | None = None
    if isinstance(requested, list):
        for item in requested:
            if not isinstance(item, dict) or not item.get("url"):
                continue
            vcodec = item.get("vcodec")
            acodec = item.get("acodec")
            if vcodec and vcodec != "none" and video_url is None:
                video_url = str(item["url"])
            if acodec and acodec != "none" and (not vcodec or vcodec == "none") and audio_url is None:
                audio_url = str(item["url"])

    if not video_url:
        raw_url = info.get("url")
        if not raw_url:
            raise ValueError("yt-dlp did not return a playable stream URL")
        video_url = str(raw_url)

    return ResolvedStream(
        source_url=source_url,
        title=title,
        video_url=video_url,
        audio_url=audio_url,
        webpage_url=str(info.get("webpage_url") or source_url),
        duration=int(info["duration"]) if isinstance(info.get("duration"), (int, float)) else None,
        extractor=str(info.get("extractor_key") or info.get("extractor") or "") or None,
    )


def resolve_stream(url: str, quality: str = "best") -> ResolvedStream:
    source = normalize_url(url)
    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
        "format": format_selector(quality),
        "socket_timeout": 20,
        "retries": 3,
        "fragment_retries": 3,
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(source, download=False)
    if not isinstance(info, dict):
        raise ValueError("yt-dlp returned an unexpected response")
    return stream_from_info(source, info)


def expand_playlist(url: str, limit: int = 100) -> list[QueueItem]:
    source = normalize_url(url)
    if not 1 <= limit <= 500:
        raise ValueError("Playlist limit must be between 1 and 500")
    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": "in_playlist",
        "playlistend": limit,
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(source, download=False)
    if not isinstance(info, dict):
        return [QueueItem(source)]
    entries = info.get("entries")
    if not entries:
        return [QueueItem(source, str(info.get("title") or ""))]

    items: list[QueueItem] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        candidate = entry.get("webpage_url") or entry.get("original_url") or entry.get("url")
        if not isinstance(candidate, str) or not candidate.startswith(("http://", "https://")):
            continue
        items.append(QueueItem(candidate, str(entry.get("title") or "")))
    return items or [QueueItem(source)]
