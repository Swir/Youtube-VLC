# YouTube VLC Player

A lightweight Python desktop application that opens YouTube videos directly in VLC Media Player. It uses `yt-dlp` to resolve the playable stream URL and launches the selected VLC executable from a simple Tkinter GUI.

## Features

- Paste a YouTube video URL
- Resolve the playable stream with `yt-dlp`
- Open the stream directly in VLC Media Player
- Select VLC from common Windows installation paths
- Choose a custom `vlc.exe` location
- Simple Tkinter desktop interface
- No browser playback required

## Requirements

- Python 3
- VLC Media Player
- `yt-dlp`

Install the Python dependency:

```bash
pip install yt-dlp
```

To update `yt-dlp` later:

```bash
pip install --upgrade yt-dlp
```

Tkinter is included with most standard Windows Python installations, so a separate `pip install ttk` is normally not required.

## Run

```bash
python main.py
```

Then:

1. Paste a YouTube URL.
2. Select the VLC executable path.
3. Click **Open in VLC**.

Common VLC paths supported by the interface include:

```text
C:\Program Files\VideoLAN\VLC\vlc.exe
C:\Program Files (x86)\VideoLAN\VLC\vlc.exe
```

## How it works

The app uses `yt-dlp` to extract a direct stream URL without downloading the video, then passes that stream to VLC for playback.

## Screenshot

![YouTube VLC Player](https://images89.fotosik.pl/704/ba6025affcfcd098gen.png)

## Search keywords

`youtube vlc` `youtube to vlc` `play youtube in vlc` `python vlc youtube` `yt-dlp vlc` `youtube stream player` `tkinter youtube player` `vlc media player python` `open youtube link in vlc` `youtube desktop player`

## Author

Created by Swir.

## Note

Use the application only with content you are authorized to access and in accordance with the relevant platform terms and applicable law.
