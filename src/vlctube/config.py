from __future__ import annotations

import json
import os
from pathlib import Path

DEFAULTS: dict[str, object] = {
    "language": "auto",
    "quality": "720p",
    "vlc_path": "",
    "history": [],
}
HISTORY_LIMIT = 50


def app_dir() -> Path:
    if os.name == "nt":
        root = Path(os.environ.get("LOCALAPPDATA", Path.home()))
        path = root / "VLCTube"
    else:
        root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        path = root / "vlctube"
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_settings() -> dict[str, object]:
    path = app_dir() / "settings.json"
    result = dict(DEFAULTS)
    if not path.exists():
        return result
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return result
    if not isinstance(payload, dict):
        return result
    for key in DEFAULTS:
        if key in payload:
            result[key] = payload[key]
    if not isinstance(result.get("history"), list):
        result["history"] = []
    result["history"] = [str(item) for item in result["history"][:HISTORY_LIMIT]]
    return result


def save_settings(settings: dict[str, object]) -> None:
    history = settings.get("history", [])
    if not isinstance(history, list):
        history = []
    payload = {
        "language": settings.get("language", "auto"),
        "quality": settings.get("quality", "720p"),
        "vlc_path": settings.get("vlc_path", ""),
        "history": [str(item) for item in history[:HISTORY_LIMIT]],
    }
    (app_dir() / "settings.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
