<div align="center">

<img src="assets/vlctube_icon.png" alt="VLCTube icon" width="140" />

# ▶ VLCTube 3

### Resolve online video streams with yt-dlp and play them directly in VLC

**Queue • Quality presets • Playlists • History • EN/PL/NO • Windows EXE**

[![CI](https://github.com/Swir/Youtube-VLC/actions/workflows/ci.yml/badge.svg)](https://github.com/Swir/Youtube-VLC/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10--3.14-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D4?logo=windows11&logoColor=white)
![Version](https://img.shields.io/badge/version-3.1.0-2aa5ff)

</div>

---

## v3.1 regression audit

VLCTube 3.1 was compared against the original 2024 `main.py` launcher. The simple classic workflow is still present — paste a URL, select or auto-detect VLC and open the media — while the modern queue, quality presets, playlist expansion, history and multilingual interface remain intact.

Two classic behaviors that could be lost in the v3 rebuild are explicitly restored and covered by tests:

- **VLC playlist enqueue:** launched media uses `--playlist-enqueue`, matching the original application so opening a new item does not unexpectedly replace an existing VLC playlist.
- **Direct media URL passthrough:** direct HTTP/HTTPS media links such as M3U8, MP4, WebM, MP3 and similar resources can be sent straight to VLC without requiring yt-dlp page extraction.

The custom VLCTube icon is now displayed in this README, applied to the running Tk window, generated as a multi-size Windows ICO and bundled into the packaged EXE. Windows CI now constructs the real GUI, and the release pipeline smoke-tests both the source GUI and packaged GUI before publishing.

VLCTube is a **stream launcher, not a downloader**. It does not save media files, bypass DRM, or provide access to content that the source does not expose to the user.

## Classic-to-modern feature map

| Original Youtube VLC | VLCTube 3.1 |
|---|---|
| Paste one media URL | Preserved; also supports multiple queue entries |
| YouTube resolution with yt-dlp | Preserved and expanded with quality presets/current format handling |
| Non-YouTube URL passed to VLC | Restored for direct media URLs |
| Standard Program Files VLC locations | Preserved and expanded with PATH/registry/LocalAppData detection |
| Manual `vlc.exe` selection | Preserved |
| `--playlist-enqueue` playback | Restored for launched media |
| Error/warning dialogs | Preserved with diagnostics logging |
| Author credit | Preserved as `by Swir` |

## Highlights

| Feature | VLCTube 3.1 |
|---|---|
| Stream resolving | Current `yt-dlp` integration with retries and timeout handling |
| Direct media | M3U8/MP4/WebM/MKV/MOV/AVI/TS and common audio URLs can pass directly to VLC |
| Quality presets | Best, 1080p, 720p, 480p, 360p and audio-only |
| Modern A/V formats | Supports separate video + audio streams through VLC `--input-slave` |
| VLC queue compatibility | Uses `--one-instance` + `--playlist-enqueue` |
| Queue | Add one or many URLs and play selected items or the whole queue |
| Playlist expansion | Expand supported public playlists into queue items |
| VLC integration | Auto-detect from PATH, common Windows locations and registry |
| History | Remembers up to 50 recently launched URLs |
| Languages | English, Polish and Norwegian with system-language detection |
| UI | Modern responsive dark-blue Tkinter/ttk interface |
| Settings | Remembers quality, language, VLC path and history |
| Diagnostics | Rotating local application log |
| App icon | PNG at runtime/README + generated multi-size Windows ICO |
| Safety | Only HTTP/HTTPS URLs; embedded URL credentials are rejected |
| Releases | Windows EXE + portable ZIP + SHA256 checksums |
| CI | Python 3.10-3.14 plus real Windows GUI startup smoke test |

## Requirements

- Windows 10 or 11 for the packaged EXE
- VLC Media Player installed locally
- Internet access for online stream resolution and playback

The source version also runs on other platforms where Python, Tkinter, VLC and the dependencies are available.

## Run from source

```bash
git clone https://github.com/Swir/Youtube-VLC.git
cd Youtube-VLC
python -m pip install -e ".[test]"
python run.py
```

Non-GUI self-test:

```bash
python -m vlctube --smoke-test
```

Real GUI startup smoke test:

```bash
python -m vlctube --smoke-gui
```

Run tests:

```bash
pytest
```

## How playback works

1. VLCTube validates the URL.
2. A clearly direct media URL is passed through unchanged; other supported pages are resolved with `yt-dlp` at the selected quality.
3. For combined streams, VLC receives one stream URL.
4. For separate modern video/audio formats, video is passed to VLC and audio is attached with `--input-slave`.
5. VLC runs in one-instance/enqueue mode to preserve the classic queue behavior.

Direct stream URLs can expire; for page-based sources VLCTube resolves a fresh stream each time an item is launched.

## VLC detection

VLCTube checks `VLCTUBE_VLC`, PATH, common Program Files/LocalAppData locations and standard VideoLAN registry entries on Windows. You can always choose `vlc.exe` manually from the interface.

## Windows release

A validated release contains:

```text
VLCTube.exe
VLCTube.exe.sha256
VLCTube-vX.Y.Z-Windows-x64.zip
VLCTube-vX.Y.Z-Windows-x64.zip.sha256
```

Before publication GitHub Actions runs unit tests, builds the icon, starts the real source GUI, builds the EXE, runs the non-GUI packaged self-test and starts the packaged GUI once.

## Project layout

```text
Youtube-VLC/
├─ assets/
│  ├─ vlctube_icon.svg
│  └─ vlctube_icon.png
├─ src/vlctube/
│  ├─ app.py
│  ├─ config.py
│  ├─ formats.py
│  ├─ i18n.py
│  ├─ logging_config.py
│  ├─ models.py
│  ├─ resolver.py
│  ├─ resources.py
│  ├─ url_tools.py
│  └─ vlc.py
├─ tests/
├─ tools/build_icon.py
├─ run.py
└─ pyproject.toml
```

## Privacy

Preferences, history and logs are stored locally in the normal per-user application/configuration directory. VLCTube does not run its own analytics service. URLs necessarily reach the source service through `yt-dlp` and VLC when you resolve or play them.

## Responsible use

Use VLCTube only for media you are permitted to access and play. Respect the source website's terms, regional restrictions and content rights. This project intentionally does not include DRM circumvention, authentication bypass or automated bulk downloading.

## Author

Developed by **Swir** — [github.com/Swir](https://github.com/Swir)

<div align="center">

**VLCTube 3.1 — classic playback behavior, modern stream handling.**

</div>
