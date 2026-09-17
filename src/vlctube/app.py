from __future__ import annotations

import logging
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .config import HISTORY_LIMIT, load_settings, save_settings
from .formats import QUALITY_PRESETS
from .i18n import detect_language, tr
from .models import QueueItem
from .resolver import expand_playlist, resolve_stream
from .url_tools import normalize_url
from .vlc import find_vlc, launch_vlc

LANGUAGE_LABELS = {"Auto": "auto", "English": "en", "Polski": "pl", "Norsk": "no"}
LANGUAGE_REVERSE = {value: key for key, value in LANGUAGE_LABELS.items()}


class VLCTubeApp:
    def __init__(self, root: tk.Tk, logger: logging.Logger | None = None) -> None:
        self.root = root
        self.logger = logger or logging.getLogger("vlctube")
        self.settings = load_settings()
        configured_language = str(self.settings.get("language", "auto"))
        self.language = detect_language() if configured_language == "auto" else configured_language

        self.queue: list[QueueItem] = []
        self.history: list[str] = [str(value) for value in self.settings.get("history", []) if isinstance(value, str)]

        saved_vlc = str(self.settings.get("vlc_path", ""))
        if saved_vlc and Path(saved_vlc).is_file():
            self.vlc_path = saved_vlc
        else:
            self.vlc_path = find_vlc() or ""

        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar(value=str(self.settings.get("quality", "720p")))
        if self.quality_var.get() not in QUALITY_PRESETS:
            self.quality_var.set("720p")
        self.vlc_var = tk.StringVar(value=self.vlc_path)
        self.language_var = tk.StringVar(value=LANGUAGE_REVERSE.get(configured_language, "Auto"))
        self.status_var = tk.StringVar(value=tr(self.language, "status_ready"))

        self.root.title(tr(self.language, "title"))
        self.root.geometry("1180x760")
        self.root.minsize(900, 620)
        self.root.configure(bg="#060d18")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._configure_style()
        self._build_ui()
        self._apply_language()
        self._refresh_queue()
        self._refresh_history()
        self._set_vlc_status()

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("App.TFrame", background="#060d18")
        style.configure("Card.TFrame", background="#0b1828")
        style.configure("Header.TLabel", background="#060d18", foreground="#f1f7ff", font=("Segoe UI Semibold", 25))
        style.configure("Sub.TLabel", background="#060d18", foreground="#7fa5c7", font=("Segoe UI", 10))
        style.configure("Card.TLabel", background="#0b1828", foreground="#cde8ff", font=("Segoe UI", 10))
        style.configure("Hint.TLabel", background="#0b1828", foreground="#7294b1", font=("Segoe UI", 9))
        style.configure("Status.TLabel", background="#091727", foreground="#9bd5ff", padding=(12, 8), font=("Segoe UI", 9))
        style.configure("Accent.TButton", background="#197ed9", foreground="white", font=("Segoe UI Semibold", 10), padding=(12, 8))
        style.map("Accent.TButton", background=[("active", "#2a9cff"), ("disabled", "#32475a")])
        style.configure("Ghost.TButton", background="#122940", foreground="#d7efff", font=("Segoe UI", 9), padding=(10, 7))
        style.map("Ghost.TButton", background=[("active", "#1a3b5d")])
        style.configure("Danger.TButton", background="#3a1c28", foreground="#ffc7d3", font=("Segoe UI", 9), padding=(10, 7))
        style.map("Danger.TButton", background=[("active", "#5a2437")])
        style.configure("TEntry", fieldbackground="#10253b", foreground="#eef8ff", insertcolor="#eef8ff", padding=7)
        style.configure("TCombobox", fieldbackground="#10253b", foreground="#eef8ff", padding=5)
        style.configure("Treeview", background="#081522", fieldbackground="#081522", foreground="#d9efff", rowheight=28, borderwidth=0)
        style.configure("Treeview.Heading", background="#10253b", foreground="#abd9ff", relief="flat", font=("Segoe UI Semibold", 9))
        style.map("Treeview", background=[("selected", "#155f98")], foreground=[("selected", "white")])
        style.configure("Horizontal.TProgressbar", background="#2aa5ff", troughcolor="#10253b", borderwidth=0)

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, style="App.TFrame", padding=(22, 18))
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(2, weight=1)

        header = ttk.Frame(outer, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        header.columnconfigure(0, weight=1)
        self.title_label = ttk.Label(header, style="Header.TLabel")
        self.title_label.grid(row=0, column=0, sticky="w")
        self.subtitle_label = ttk.Label(header, style="Sub.TLabel")
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(3, 0))
        self.language_combo = ttk.Combobox(header, textvariable=self.language_var, values=list(LANGUAGE_LABELS), state="readonly", width=12)
        self.language_combo.grid(row=0, column=1, rowspan=2, sticky="e")
        self.language_combo.bind("<<ComboboxSelected>>", self._change_language)

        controls = ttk.Frame(outer, style="Card.TFrame", padding=16)
        controls.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        controls.columnconfigure(0, weight=1)

        self.url_label = ttk.Label(controls, style="Card.TLabel")
        self.url_label.grid(row=0, column=0, sticky="w")
        self.quality_label = ttk.Label(controls, style="Card.TLabel")
        self.quality_label.grid(row=0, column=3, sticky="w", padx=(12, 0))

        self.url_entry = ttk.Entry(controls, textvariable=self.url_var)
        self.url_entry.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        self.url_entry.bind("<Return>", lambda _event: self._add_to_queue())
        self.paste_button = ttk.Button(controls, style="Ghost.TButton", command=self._paste)
        self.paste_button.grid(row=1, column=1, padx=(8, 0), pady=(5, 0))
        self.add_button = ttk.Button(controls, style="Accent.TButton", command=self._add_to_queue)
        self.add_button.grid(row=1, column=2, padx=(8, 0), pady=(5, 0))
        self.quality_combo = ttk.Combobox(controls, textvariable=self.quality_var, values=list(QUALITY_PRESETS), state="readonly", width=10)
        self.quality_combo.grid(row=1, column=3, padx=(12, 0), pady=(5, 0), sticky="w")
        self.expand_button = ttk.Button(controls, style="Ghost.TButton", command=self._expand_playlist)
        self.expand_button.grid(row=1, column=4, padx=(8, 0), pady=(5, 0))

        self.vlc_label = ttk.Label(controls, style="Card.TLabel")
        self.vlc_label.grid(row=2, column=0, sticky="w", pady=(14, 0))
        self.vlc_entry = ttk.Entry(controls, textvariable=self.vlc_var, state="readonly")
        self.vlc_entry.grid(row=3, column=0, sticky="ew", pady=(5, 0))
        self.detect_button = ttk.Button(controls, style="Ghost.TButton", command=self._detect_vlc)
        self.detect_button.grid(row=3, column=1, padx=(8, 0), pady=(5, 0))
        self.browse_button = ttk.Button(controls, style="Ghost.TButton", command=self._browse_vlc)
        self.browse_button.grid(row=3, column=2, padx=(8, 0), pady=(5, 0))
        self.vlc_status_label = ttk.Label(controls, style="Hint.TLabel")
        self.vlc_status_label.grid(row=3, column=3, columnspan=2, sticky="w", padx=(12, 0), pady=(5, 0))
        self.about_label = ttk.Label(controls, style="Hint.TLabel", wraplength=1050)
        self.about_label.grid(row=4, column=0, columnspan=5, sticky="w", pady=(12, 0))
        self.progress = ttk.Progressbar(controls, mode="indeterminate")
        self.progress.grid(row=5, column=0, columnspan=5, sticky="ew", pady=(10, 0))

        content = ttk.Frame(outer, style="App.TFrame")
        content.grid(row=2, column=0, sticky="nsew")
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(1, weight=1)

        self.queue_label = ttk.Label(content, style="Sub.TLabel")
        self.queue_label.grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.history_label = ttk.Label(content, style="Sub.TLabel")
        self.history_label.grid(row=0, column=1, sticky="w", padx=(14, 0), pady=(0, 6))

        queue_frame = ttk.Frame(content, style="Card.TFrame", padding=8)
        queue_frame.grid(row=1, column=0, sticky="nsew")
        queue_frame.rowconfigure(0, weight=1)
        queue_frame.columnconfigure(0, weight=1)
        self.queue_tree = ttk.Treeview(queue_frame, columns=("title", "url", "status"), show="headings", selectmode="extended")
        self.queue_tree.heading("title", text="Title")
        self.queue_tree.heading("url", text="URL")
        self.queue_tree.heading("status", text="Status")
        self.queue_tree.column("title", width=230, anchor="w")
        self.queue_tree.column("url", width=360, anchor="w")
        self.queue_tree.column("status", width=110, anchor="center", stretch=False)
        self.queue_tree.grid(row=0, column=0, sticky="nsew")
        queue_scroll = ttk.Scrollbar(queue_frame, orient="vertical", command=self.queue_tree.yview)
        queue_scroll.grid(row=0, column=1, sticky="ns")
        self.queue_tree.configure(yscrollcommand=queue_scroll.set)
        self.queue_tree.bind("<Double-1>", lambda _event: self._play_selected())

        history_frame = ttk.Frame(content, style="Card.TFrame", padding=8)
        history_frame.grid(row=1, column=1, sticky="nsew", padx=(14, 0))
        history_frame.rowconfigure(0, weight=1)
        history_frame.columnconfigure(0, weight=1)
        self.history_list = tk.Listbox(
            history_frame,
            bg="#081522",
            fg="#cde8ff",
            selectbackground="#155f98",
            selectforeground="white",
            borderwidth=0,
            highlightthickness=0,
            font=("Segoe UI", 9),
        )
        self.history_list.grid(row=0, column=0, sticky="nsew")
        history_scroll = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_list.yview)
        history_scroll.grid(row=0, column=1, sticky="ns")
        self.history_list.configure(yscrollcommand=history_scroll.set)
        self.history_list.bind("<Double-Button-1>", self._history_to_queue)

        actions = ttk.Frame(outer, style="App.TFrame")
        actions.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        self.play_selected_button = ttk.Button(actions, style="Accent.TButton", command=self._play_selected)
        self.play_selected_button.pack(side="left")
        self.play_all_button = ttk.Button(actions, style="Ghost.TButton", command=self._play_all)
        self.play_all_button.pack(side="left", padx=(8, 0))
        self.remove_button = ttk.Button(actions, style="Ghost.TButton", command=self._remove_selected)
        self.remove_button.pack(side="left", padx=(8, 0))
        self.clear_button = ttk.Button(actions, style="Danger.TButton", command=self._clear_queue)
        self.clear_button.pack(side="left", padx=(8, 0))
        self.clear_history_button = ttk.Button(actions, style="Danger.TButton", command=self._clear_history)
        self.clear_history_button.pack(side="right")

        footer = ttk.Frame(outer, style="App.TFrame")
        footer.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        footer.columnconfigure(0, weight=1)
        ttk.Label(footer, textvariable=self.status_var, style="Status.TLabel").grid(row=0, column=0, sticky="ew")
        ttk.Label(footer, text="VLCTube v3.0.0  •  by Swir  •  github.com/Swir", style="Sub.TLabel").grid(row=0, column=1, padx=(12, 0))

    def _apply_language(self) -> None:
        self.root.title(tr(self.language, "title"))
        self.title_label.configure(text=tr(self.language, "title"))
        self.subtitle_label.configure(text=tr(self.language, "subtitle"))
        self.url_label.configure(text=tr(self.language, "url"))
        self.paste_button.configure(text=tr(self.language, "paste"))
        self.add_button.configure(text=tr(self.language, "add"))
        self.expand_button.configure(text=tr(self.language, "expand"))
        self.quality_label.configure(text=tr(self.language, "quality"))
        self.vlc_label.configure(text=tr(self.language, "vlc"))
        self.detect_button.configure(text=tr(self.language, "auto_detect"))
        self.browse_button.configure(text=tr(self.language, "browse"))
        self.queue_label.configure(text=tr(self.language, "queue"))
        self.history_label.configure(text=tr(self.language, "history"))
        self.play_selected_button.configure(text=tr(self.language, "play_selected"))
        self.play_all_button.configure(text=tr(self.language, "play_all"))
        self.remove_button.configure(text=tr(self.language, "remove"))
        self.clear_button.configure(text=tr(self.language, "clear"))
        self.clear_history_button.configure(text=tr(self.language, "clear_history"))
        self.about_label.configure(text=tr(self.language, "about"))
        self._set_vlc_status()
        self._refresh_queue()

    def _change_language(self, _event: object = None) -> None:
        selected = LANGUAGE_LABELS.get(self.language_var.get(), "auto")
        self.language = detect_language() if selected == "auto" else selected
        self._apply_language()
        self.status_var.set(tr(self.language, "status_ready"))

    def _paste(self) -> None:
        try:
            value = self.root.clipboard_get()
        except tk.TclError:
            return
        self.url_var.set(value.strip())

    def _add_to_queue(self) -> None:
        raw = self.url_var.get().strip()
        if not raw:
            messagebox.showwarning(tr(self.language, "title"), tr(self.language, "invalid_url"), parent=self.root)
            return
        added = 0
        for line in raw.splitlines():
            if not line.strip():
                continue
            try:
                url = normalize_url(line)
            except ValueError:
                continue
            if not any(item.url == url for item in self.queue):
                self.queue.append(QueueItem(url=url))
                added += 1
        if not added:
            messagebox.showwarning(tr(self.language, "title"), tr(self.language, "invalid_url"), parent=self.root)
            return
        self.url_var.set("")
        self._refresh_queue()
        self.status_var.set(tr(self.language, "added", count=added))

    def _expand_playlist(self) -> None:
        raw = self.url_var.get().strip()
        try:
            url = normalize_url(raw)
        except ValueError:
            messagebox.showwarning(tr(self.language, "title"), tr(self.language, "invalid_url"), parent=self.root)
            return
        self._busy(True, tr(self.language, "resolving"))

        def worker() -> None:
            try:
                items = expand_playlist(url, limit=100)
            except Exception as exc:
                self.logger.exception("Playlist expansion failed")
                self.root.after(0, lambda: self._operation_failed(str(exc)))
                return
            self.root.after(0, lambda: self._playlist_finished(items))

        threading.Thread(target=worker, daemon=True).start()

    def _playlist_finished(self, items: list[QueueItem]) -> None:
        existing = {item.url for item in self.queue}
        added = 0
        for item in items:
            if item.url not in existing:
                self.queue.append(item)
                existing.add(item.url)
                added += 1
        self.url_var.set("")
        self._busy(False)
        self._refresh_queue()
        self.status_var.set(tr(self.language, "expanded", count=added))

    def _detect_vlc(self) -> None:
        path = find_vlc()
        self.vlc_path = path or ""
        self.vlc_var.set(self.vlc_path)
        self._set_vlc_status()

    def _browse_vlc(self) -> None:
        filetypes = [("VLC executable", "vlc.exe"), ("Executable", "*.exe"), ("All", "*.*")] if Path().anchor or True else [("All", "*.*")]
        path = filedialog.askopenfilename(parent=self.root, filetypes=filetypes)
        if not path:
            return
        self.vlc_path = path
        self.vlc_var.set(path)
        self._set_vlc_status()

    def _set_vlc_status(self) -> None:
        if self.vlc_path and Path(self.vlc_path).is_file():
            self.vlc_status_label.configure(text=tr(self.language, "vlc_found", path=self.vlc_path))
        else:
            self.vlc_status_label.configure(text=tr(self.language, "vlc_missing"))

    def _selected_indices(self) -> list[int]:
        indices: list[int] = []
        for iid in self.queue_tree.selection():
            try:
                indices.append(int(iid))
            except ValueError:
                continue
        return sorted(set(index for index in indices if 0 <= index < len(self.queue)))

    def _play_selected(self) -> None:
        indices = self._selected_indices()
        if not indices:
            messagebox.showinfo(tr(self.language, "title"), tr(self.language, "no_selection"), parent=self.root)
            return
        self._play_indices(indices)

    def _play_all(self) -> None:
        if not self.queue:
            messagebox.showinfo(tr(self.language, "title"), tr(self.language, "no_selection"), parent=self.root)
            return
        self._play_indices(list(range(len(self.queue))))

    def _play_indices(self, indices: list[int]) -> None:
        if not self.vlc_path or not Path(self.vlc_path).is_file():
            detected = find_vlc()
            if detected:
                self.vlc_path = detected
                self.vlc_var.set(detected)
                self._set_vlc_status()
            else:
                messagebox.showwarning(tr(self.language, "title"), tr(self.language, "no_vlc"), parent=self.root)
                return

        quality = self.quality_var.get()
        vlc_path = self.vlc_path
        self._busy(True, tr(self.language, "resolving"))

        def worker() -> None:
            launched = 0
            last_title = ""
            for index in indices:
                if index >= len(self.queue):
                    continue
                item = self.queue[index]
                self.root.after(0, lambda idx=index: self._set_item_status(idx, "resolving"))
                try:
                    stream = resolve_stream(item.url, quality)
                    launch_vlc(vlc_path, stream, enqueue=launched > 0)
                except Exception as exc:
                    self.logger.exception("Playback failed for %s", item.url)
                    self.root.after(0, lambda idx=index: self._set_item_status(idx, "error"))
                    self.root.after(0, lambda msg=str(exc): self.status_var.set(tr(self.language, "failed", error=msg)))
                    continue
                launched += 1
                last_title = stream.title
                self.root.after(0, lambda idx=index, title=stream.title: self._mark_playing(idx, title))
                self._remember(item.url)
            self.root.after(0, lambda: self._playback_finished(launched, last_title))

        threading.Thread(target=worker, daemon=True).start()

    def _set_item_status(self, index: int, status: str) -> None:
        if 0 <= index < len(self.queue):
            self.queue[index].status = status
            self._refresh_queue()

    def _mark_playing(self, index: int, title: str) -> None:
        if 0 <= index < len(self.queue):
            self.queue[index].title = title
            self.queue[index].status = "playing"
            self._refresh_queue()
            self.status_var.set(tr(self.language, "launched", title=title))

    def _playback_finished(self, launched: int, last_title: str) -> None:
        self._busy(False)
        self._refresh_history()
        if launched and last_title:
            self.status_var.set(tr(self.language, "launched", title=last_title))

    def _remember(self, url: str) -> None:
        try:
            self.history.remove(url)
        except ValueError:
            pass
        self.history.insert(0, url)
        del self.history[HISTORY_LIMIT:]

    def _history_to_queue(self, _event: object = None) -> None:
        selection = self.history_list.curselection()
        if not selection:
            return
        url = self.history_list.get(selection[0])
        if not any(item.url == url for item in self.queue):
            self.queue.append(QueueItem(url=url))
            self._refresh_queue()

    def _remove_selected(self) -> None:
        for index in reversed(self._selected_indices()):
            self.queue.pop(index)
        self._refresh_queue()

    def _clear_queue(self) -> None:
        self.queue.clear()
        self._refresh_queue()
        self.status_var.set(tr(self.language, "status_ready"))

    def _clear_history(self) -> None:
        self.history.clear()
        self._refresh_history()

    def _refresh_queue(self) -> None:
        if not hasattr(self, "queue_tree"):
            return
        self.queue_tree.delete(*self.queue_tree.get_children())
        for index, item in enumerate(self.queue):
            status_key = item.status if item.status in {"queued", "playing", "error"} else "resolving"
            status = tr(self.language, status_key) if status_key in {"queued", "playing", "error"} else tr(self.language, "resolving")
            self.queue_tree.insert("", "end", iid=str(index), values=(item.title or "—", item.url, status))

    def _refresh_history(self) -> None:
        if not hasattr(self, "history_list"):
            return
        self.history_list.delete(0, tk.END)
        for url in self.history:
            self.history_list.insert(tk.END, url)

    def _busy(self, active: bool, message: str | None = None) -> None:
        widgets = (self.add_button, self.expand_button, self.play_selected_button, self.play_all_button)
        if active:
            self.progress.start(12)
            for widget in widgets:
                widget.state(["disabled"])
            if message:
                self.status_var.set(message)
        else:
            self.progress.stop()
            for widget in widgets:
                widget.state(["!disabled"])

    def _operation_failed(self, error: str) -> None:
        self._busy(False)
        self.status_var.set(tr(self.language, "failed", error=error))
        messagebox.showerror(tr(self.language, "title"), tr(self.language, "failed", error=error), parent=self.root)

    def _on_close(self) -> None:
        selected_language = LANGUAGE_LABELS.get(self.language_var.get(), "auto")
        try:
            save_settings(
                {
                    "language": selected_language,
                    "quality": self.quality_var.get(),
                    "vlc_path": self.vlc_path,
                    "history": self.history,
                }
            )
        except OSError:
            self.logger.exception("Could not save settings")
        self.root.destroy()


def run() -> None:
    from .logging_config import configure_logging

    root = tk.Tk()
    VLCTubeApp(root, configure_logging())
    root.mainloop()
