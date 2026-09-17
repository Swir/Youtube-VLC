from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path


def asset_path(name: str) -> Path:
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root:
        return Path(bundle_root) / "assets" / name
    return Path(__file__).resolve().parents[2] / "assets" / name


def apply_window_icon(root: tk.Tk) -> None:
    path = asset_path("vlctube_icon.png")
    if not path.exists():
        return
    try:
        icon = tk.PhotoImage(file=str(path))
        root.iconphoto(True, icon)
        root._vlctube_icon = icon  # type: ignore[attr-defined]
    except tk.TclError:
        return
