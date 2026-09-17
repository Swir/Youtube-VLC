from __future__ import annotations

QUALITY_PRESETS: dict[str, str] = {
    "best": "bv*+ba/b",
    "1080p": "bv*[height<=1080]+ba/b[height<=1080]/b",
    "720p": "bv*[height<=720]+ba/b[height<=720]/b",
    "480p": "bv*[height<=480]+ba/b[height<=480]/b",
    "360p": "bv*[height<=360]+ba/b[height<=360]/b",
    "audio": "ba/b",
}


def format_selector(preset: str) -> str:
    try:
        return QUALITY_PRESETS[preset]
    except KeyError as exc:
        raise ValueError(f"Unknown quality preset: {preset}") from exc
