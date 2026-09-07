<div align="center">

# 🎬 YouTube VLC Player

### Play YouTube videos directly in VLC Media Player with Python & yt-dlp

**Simple • Lightweight • Windows-friendly • Open Source**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![VLC](https://img.shields.io/badge/VLC-Media%20Player-orange)
![yt-dlp](https://img.shields.io/badge/yt--dlp-supported-red)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)

</div>

---

## 🚀 About

**YouTube VLC Player** is a lightweight Python desktop application that lets you open and play **YouTube videos directly in VLC Media Player**.

Paste a YouTube link, select your VLC installation and the program uses **yt-dlp** to resolve the playable video stream before launching it in VLC.

No browser playback. No complicated commands. Just paste the link and play.

This project is useful for people looking for a **YouTube to VLC player**, **yt-dlp VLC GUI**, **Python YouTube player**, **YouTube external player for Windows**, or a simple way to **open YouTube links in VLC Media Player**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎬 YouTube playback | Open YouTube videos directly in VLC |
| 🔗 Simple URL input | Paste a YouTube link into the desktop GUI |
| ⚡ yt-dlp integration | Resolves the playable stream URL automatically |
| 📺 VLC integration | Sends the resolved stream to VLC Media Player |
| 🪟 Windows support | Includes common Windows VLC installation paths |
| 📂 Custom VLC path | Select `vlc.exe` manually when installed elsewhere |
| 🖥️ Desktop GUI | Lightweight interface built with Tkinter |
| 🪶 Minimal setup | Only a small Python dependency set is required |

---

## 🖼️ Preview

<div align="center">

![YouTube VLC Player Screenshot](https://images89.fotosik.pl/704/ba6025affcfcd098gen.png)

</div>

---

## ⚙️ How It Works

```text
YouTube URL
     │
     ▼
 Python GUI
     │
     ▼
   yt-dlp
     │
     ▼
Playable Stream URL
     │
     ▼
VLC Media Player
```

The application uses **yt-dlp** to obtain a playable stream URL without downloading the complete video. The resulting stream is then passed to **VLC Media Player** for playback.

---

## 📋 Requirements

### Python

Python **3.10+** is recommended.

```bash
python --version
```

### VLC Media Player

Install VLC Media Player. Typical Windows locations are:

```text
C:\Program Files\VideoLAN\VLC\vlc.exe
C:\Program Files (x86)\VideoLAN\VLC\vlc.exe
```

### yt-dlp

```bash
pip install yt-dlp
```

Keep it updated with:

```bash
pip install --upgrade yt-dlp
```

> Tkinter is normally included with standard Windows Python installations and does not usually require a separate `pip` package.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Swir/Youtube-VLC.git
```

### 2. Open the project folder

```bash
cd Youtube-VLC
```

### 3. Install the dependency

```bash
pip install -U yt-dlp
```

### 4. Start the application

```bash
python main.py
```

---

## ▶️ Usage

1. Start the application with `python main.py`.
2. Paste a YouTube video URL.
3. Select the VLC Media Player executable.
4. Click **Open in VLC**.
5. The application resolves the stream with yt-dlp and opens it in VLC.

---

## 🧩 Project Structure

```text
Youtube-VLC/
│
├── main.py      # GUI, yt-dlp integration and VLC launcher
└── README.md    # Project documentation
```

---

## 🔧 Troubleshooting

### VLC does not start

Make sure the selected path points directly to `vlc.exe`, for example:

```text
C:\Program Files\VideoLAN\VLC\vlc.exe
```

### A YouTube link stops working

YouTube changes frequently, so first update yt-dlp:

```bash
pip install -U yt-dlp
```

### `ModuleNotFoundError: No module named 'yt_dlp'`

```bash
pip install yt-dlp
```

### `python` command is not recognized

On Windows, try:

```bash
py main.py
```

---

## 💡 Why YouTube + VLC?

VLC provides useful local playback features such as playback-speed control, audio and video filters, equalizer controls, subtitles, fullscreen playback and hardware-accelerated video output.

**YouTube VLC Player** provides a simple bridge between **YouTube, Python, yt-dlp and VLC Media Player** from one lightweight desktop interface.

---

## 🔍 Discoverability

Common terms related to this project:

`youtube vlc player` • `youtube to vlc` • `play youtube in vlc` • `youtube vlc python` • `yt-dlp vlc` • `youtube external player` • `youtube stream vlc` • `python vlc gui` • `open youtube link in vlc` • `youtube player python` • `vlc youtube launcher`

---

## 🛠️ Built With

- **Python**
- **Tkinter**
- **yt-dlp**
- **VLC Media Player**
- Python `subprocess`

---

## 🤝 Contributing

Bug reports, improvements and pull requests are welcome. If you find a problem, open an Issue with information about your Python version, VLC version and yt-dlp version.

---

## ⭐ Support

If **YouTube VLC Player** is useful to you, consider giving the repository a **Star ⭐**. It helps other users discover the project.

---

## ⚖️ Disclaimer

Use this application only with content you are authorized to access and in accordance with applicable platform terms and law.

YouTube, VLC and yt-dlp belong to their respective owners/projects. This repository is not affiliated with or endorsed by YouTube, Google, VideoLAN or the yt-dlp developers.

---

## 👨‍💻 Author

Developed by **Swir** — [@Swir](https://github.com/Swir)

---

<div align="center">

### 🎬 YouTube + Python + yt-dlp + VLC

**Paste • Open • Watch**

⭐ **Star the repository if you find it useful!**

</div>
