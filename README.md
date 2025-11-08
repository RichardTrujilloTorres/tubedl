# 🎬 tubedl

`tubedl` is a simple yet powerful **command-line YouTube downloader** built with Python and [yt-dlp](https://github.com/yt-dlp/yt-dlp).  
It supports videos, shorts, playlists, and now thumbnails — with clean CLI options, progress indicators, audio conversion via FFmpeg, and authentication for age-restricted or private videos.

---

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)
![Build Status](https://github.com/RichardTrujilloTorres/tubedl/actions/workflows/ci.yml/badge.svg)

---

## 🚀 Features

✅ Download single YouTube videos in MP4 or MP3  
✅ Download **full playlists** (or just a single video from one)  
✅ Supports short links (`youtu.be/...`) and Shorts (`/shorts/...`)  
✅ Automatic URL normalization and error handling  
✅ Clean terminal interface with [Rich](https://github.com/Textualize/rich)  
✅ Cross-platform (macOS, Linux, Windows)  
✅ 🔐 **Download age-restricted or private videos** using cookies or browser session  
✅ 🖼️ **Download high-resolution video thumbnails** with `--thumbnail`  

---

## 🧰 Installation

### 1️⃣ Clone the repo

```bash
git clone https://github.com/RichardTrujilloTorres/tubedl.git
cd tubedl
```

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# OR
.venv\Scripts\activate        # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Install `tubedl` as a CLI command (editable mode)

```bash
pip install -e .
```

✅ Now you can run `tubedl` directly from your terminal.

---

## 🖥️ Usage

### 🎬 Download a single video

```bash
tubedl "https://youtu.be/dQw4w9WgXcQ" -f mp4 -o ~/Videos
```

### 🎧 Download as MP3

```bash
tubedl "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -f mp3 -o ~/Music
```

### 📃 Download a full playlist

```bash
tubedl "https://www.youtube.com/playlist?list=PLhit70zW35SEyhtF0zE7UTDPB9VGM4ngN" --playlist -f mp4 -o ~/Videos
```

### 🎯 Download a single video from a playlist

```bash
tubedl "https://www.youtube.com/watch?v=xjiJYT8Uu38&list=PLhit70zW35SEyhtF0zE7UTDPB9VGM4ngN" -f mp4 -o ~/Videos
```

### 🔐 Download age-restricted or private videos

`tubedl` supports **authenticated downloads** via:
- A `cookies.txt` file exported from your logged-in browser  
- Your existing browser session (no manual export required)

#### Using a cookies file
```bash
tubedl "https://www.youtube.com/watch?v=VIDEO_ID"   --cookies ~/Downloads/youtube_cookies.txt -o ~/Videos
```

#### Using your browser session directly
```bash
tubedl "https://www.youtube.com/watch?v=VIDEO_ID"   --cookies-from-browser chrome -o ~/Videos
```

Supported browsers: `chrome`, `brave`, `firefox`, `edge`, `safari`

### 🖼️ Download a video thumbnail only

```bash
tubedl "https://www.youtube.com/watch?v=VIDEO_ID" --thumbnail -o ~/Pictures
```

This will save the thumbnail as `<VIDEO_ID>_thumbnail.jpg`.

---

## ⚙️ Options

| Flag | Description |
|------|--------------|
| `-f, --format` | Output format (`mp4`, `mp3`, `best`, `worst`) |
| `-o, --output` | Output directory |
| `-p, --playlist` | Download the full playlist (if URL includes `list=`) |
| `-q, --quiet` | Suppress progress output |
| `--cookies PATH` | Path to cookies.txt for age-restricted/private videos |
| `--cookies-from-browser [chrome\|brave\|firefox\|edge\|safari]` | Load cookies from a local browser session |
| `--thumbnail` | Download only the video thumbnail |
| `--help` | Show CLI help |

---

## 🧩 Development

### Run locally

```bash
python -m tubedl.cli "https://youtu.be/dQw4w9WgXcQ" -f mp3
```

### Run from CLI (after install)

```bash
tubedl "https://youtu.be/dQw4w9WgXcQ" -f mp3
```

### Rebuild for release

```bash
rm -rf build dist *.egg-info
python -m build
```

---

## 🧾 Versioning & Releases

This project follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) and uses [Commitizen](https://commitizen-tools.github.io/commitizen/) for:

- Automated version bumps  
- Tagged releases (`v0.x.x`)  
- Auto-generated changelogs (`CHANGELOG.md`)

```bash
cz bump
cz changelog
```

---

## ⚡ Requirements

- Python 3.9+  
- FFmpeg (for MP3 conversion)  
  - macOS: `brew install ffmpeg`  
  - Ubuntu: `sudo apt install ffmpeg`  
  - Windows: [Download here](https://ffmpeg.org/download.html)

---

## 🧑‍💻 Contributing

1. Fork the repo  
2. Create a feature branch (`git checkout -b feat/my-feature`)  
3. Commit changes using Conventional Commits  
4. Submit a PR 🚀

---

## 🧱 Continuous Integration

`GitHub Actions` is used for:
- Testing builds and dependency installs  
- Ensuring consistent packaging  
- Auto-generating changelogs on release

A sample workflow is located at:
```
.github/workflows/ci.yml
```

Badge at the top of this README shows current CI status.

---

## 📜 License

MIT License © 2025 [Richard Trujillo Torres](https://github.com/RichardTrujilloTorres)

---

## 🌟 Acknowledgements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — core download engine  
- [Click](https://click.palletsprojects.com/) — elegant CLI framework  
- [Rich](https://github.com/Textualize/rich) — beautiful terminal output  
- [Requests](https://docs.python-requests.org/) — simple HTTP for Python

---
