<div align="center">

# ▶ VLCTube 3

### Resolve online video streams with yt-dlp and play them directly in VLC

**Queue • Quality presets • Playlists • History • EN/PL/NO • Windows EXE**

[![CI](https://github.com/Swir/Youtube-VLC/actions/workflows/ci.yml/badge.svg)](https://github.com/Swir/Youtube-VLC/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10--3.14-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D4?logo=windows11&logoColor=white)
![Version](https://img.shields.io/badge/version-3.0.0-2aa5ff)

</div>

---

## About

**VLCTube 3** is a complete rebuild of the old YouTube-to-VLC launcher. Paste a supported public media URL, let `yt-dlp` resolve a playable stream, and VLCTube sends that stream directly to VLC.

VLCTube is a **stream launcher, not a downloader**. It does not save media files, bypass DRM, or provide access to content that the source does not expose to `yt-dlp`.

## Highlights

| Feature | VLCTube 3 |
|---|---|
| Stream resolving | Current `yt-dlp` integration with retries and timeout handling |
| Quality presets | Best, 1080p, 720p, 480p, 360p and audio-only |
| Modern A/V formats | Supports separate video + audio streams through VLC `--input-slave` |
| Queue | Add one or many URLs and play selected items or the whole queue |
| Playlist expansion | Expand supported public playlists into queue items |
| VLC integration | Auto-detect from PATH, common Windows locations and registry |
| History | Remembers up to 50 recently launched URLs |
| Languages | English, Polish and Norwegian with system-language detection |
| UI | Modern responsive dark-blue Tkinter/ttk interface |
| Settings | Remembers quality, language, VLC path and history |
| Diagnostics | Rotating local application log |
| Safety | Only HTTP/HTTPS URLs; embedded URL credentials are rejected |
| Releases | Windows EXE + portable ZIP + SHA256 checksums |
| CI | Python 3.10-3.14 plus Windows smoke test |

## Requirements

- Windows 10 or 11 for the packaged EXE
- VLC Media Player installed locally
- Internet access for stream resolution and playback

The source version also runs on other platforms where Python, Tkinter, VLC and the dependencies are available.

## Run from source

```bash
git clone https://github.com/Swir/Youtube-VLC.git
cd Youtube-VLC
python -m pip install -e ".[test]"
python run.py
```

Run the non-GUI self-test:

```bash
python -m vlctube --smoke-test
```

Run tests:

```bash
pytest
```

## How playback works

1. VLCTube validates the URL.
2. `yt-dlp` resolves the selected quality without downloading the media file.
3. For combined streams, VLC receives one stream URL.
4. For separate modern video/audio formats, the video is passed to VLC and audio is attached with `--input-slave`.
5. Additional queue items are enqueued into the existing VLC instance.

Direct stream URLs can expire; VLCTube resolves a fresh URL each time an item is launched.

## VLC detection

VLCTube checks, in order:

- `VLCTUBE_VLC` environment variable,
- `vlc` / `vlc.exe` available on PATH,
- common Program Files / LocalAppData locations,
- standard VideoLAN VLC registry entries on Windows.

You can always choose `vlc.exe` manually from the interface.

## Windows release

Validated releases contain:

```text
VLCTube.exe
VLCTube.exe.sha256
VLCTube-vX.Y.Z-Windows-x64.zip
VLCTube-vX.Y.Z-Windows-x64.zip.sha256
```

The packaged executable must pass the same non-GUI smoke test before GitHub Actions publishes the release.

## Project layout

```text
Youtube-VLC/
├─ assets/
│  └─ vlctube_icon.svg
├─ src/vlctube/
│  ├─ app.py
│  ├─ config.py
│  ├─ formats.py
│  ├─ i18n.py
│  ├─ logging_config.py
│  ├─ models.py
│  ├─ resolver.py
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

**VLCTube 3 — resolve once, play in VLC.**

</div>
