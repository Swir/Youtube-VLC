from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from .models import ResolvedStream


def _registry_candidates() -> list[Path]:
    if os.name != "nt":
        return []
    try:
        import winreg
    except ImportError:
        return []
    candidates: list[Path] = []
    for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        for key_name in (r"SOFTWARE\VideoLAN\VLC", r"SOFTWARE\WOW6432Node\VideoLAN\VLC"):
            try:
                with winreg.OpenKey(hive, key_name) as key:
                    install_dir, _ = winreg.QueryValueEx(key, "InstallDir")
                candidates.append(Path(install_dir) / "vlc.exe")
            except OSError:
                continue
    return candidates


def find_vlc() -> str | None:
    configured = os.environ.get("VLCTUBE_VLC")
    if configured and Path(configured).is_file():
        return str(Path(configured))

    in_path = shutil.which("vlc") or shutil.which("vlc.exe")
    if in_path:
        return in_path

    candidates: list[Path] = []
    for env_name in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
        root = os.environ.get(env_name)
        if not root:
            continue
        base = Path(root)
        candidates.extend(
            [
                base / "VideoLAN" / "VLC" / "vlc.exe",
                base / "Programs" / "VideoLAN" / "VLC" / "vlc.exe",
            ]
        )
    candidates.extend(_registry_candidates())

    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return None


def build_vlc_command(vlc_path: str, stream: ResolvedStream, *, enqueue: bool = False) -> list[str]:
    executable = Path(vlc_path)
    if not executable.is_file() and not shutil.which(vlc_path):
        raise FileNotFoundError(f"VLC executable not found: {vlc_path}")

    # Classic Youtube-VLC always used --playlist-enqueue so launching a URL did
    # not unexpectedly replace the user's current VLC playlist. Preserve that
    # behavior for the first item as well as subsequent queue items.
    command = [str(vlc_path), "--one-instance", "--playlist-enqueue", "--no-video-title-show"]
    if stream.audio_url:
        command.append(f"--input-slave={stream.audio_url}")
    command.append(stream.video_url)
    return command


def launch_vlc(vlc_path: str, stream: ResolvedStream, *, enqueue: bool = False) -> subprocess.Popen[bytes]:
    command = build_vlc_command(vlc_path, stream, enqueue=enqueue)
    creationflags = 0
    if os.name == "nt":
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    return subprocess.Popen(command, shell=False, creationflags=creationflags)
