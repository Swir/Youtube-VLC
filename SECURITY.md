# Security Policy

## Supported version

Security and reliability fixes are applied to the current 3.x line.

## Scope

VLCTube validates user-supplied media URLs, asks `yt-dlp` to resolve playable streams and launches the local VLC executable. It does not implement DRM circumvention, authentication bypass or hidden downloading.

## Reporting

Please use GitHub's private security reporting features when available. Include the affected version, operating system, reproduction steps, expected behavior and actual behavior. Avoid publishing sensitive exploit details in a public issue before a fix is available.

## URL and process safety

- Only `http://` and `https://` media URLs are accepted.
- URLs containing embedded credentials are rejected.
- VLC is launched with an argument list and `shell=False`.
- No shell command is constructed from a media URL.
- User settings and logs are stored locally in the per-user application directory.

## Third-party components

VLCTube depends on `yt-dlp` for media extraction and on a locally installed VLC Player for playback. Keep both current and obtain them from their official distribution channels.
