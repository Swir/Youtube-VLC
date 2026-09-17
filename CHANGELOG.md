# Changelog

All notable changes to VLCTube are documented here.

## [3.0.0] - 2026-09-17

### Added
- Complete package-based architecture under `src/vlctube`.
- Modern responsive dark-blue Tkinter/ttk desktop UI.
- URL queue with play-selected and play-all actions.
- Public playlist expansion into the queue.
- Quality presets: Best, 1080p, 720p, 480p, 360p and audio-only.
- Separate video/audio stream support through VLC `--input-slave`.
- VLC auto-detection from PATH, common Windows install locations and registry entries.
- Up to 50 locally stored recent URLs.
- English, Polish and Norwegian UI with system-language detection.
- Persistent per-user settings and rotating application logs.
- Original VLCTube SVG icon and Windows ICO build tool.
- URL validation that permits only HTTP/HTTPS and rejects embedded credentials.
- Python 3.10-3.14 CI plus Windows smoke testing.
- Automated Windows EXE, portable ZIP and SHA256 release workflow.
- Packaged-app smoke test before release publication.

### Changed
- Updated the yt-dlp integration for current format-selection behavior and resilient stream resolution.
- VLC receives stream URLs directly; temporary playlist files are no longer created.
- Replaced the old single-file UI with maintainable modules and tests.

### Removed
- Removed the legacy `main.py` implementation.
- Removed the old fixed `best`-only playback path.

## [2.0.0] - 2024-11-28

Legacy `VLCTube 2.0` Windows release.

## [1.0.0] - 2024-01-26

Original YouTube VLC Windows release.
