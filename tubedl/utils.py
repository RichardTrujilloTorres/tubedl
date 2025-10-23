import re
from urllib.parse import urlparse, parse_qs

def normalize_youtube_url(url: str) -> str:
    """
    Normalize YouTube URLs to a canonical form.
    Handles shortlinks, shorts, watch links, and playlists.
    """

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parse_qs(parsed.query)

    # 🎬 Case 1: youtu.be short links
    match = re.match(r"^/([A-Za-z0-9_-]{11})$", path)
    if "youtu.be" in hostname and match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"

    # 🎥 Case 2: Shorts links
    match = re.match(r"^/shorts/([A-Za-z0-9_-]{11})$", path)
    if "youtube.com" in hostname and match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"

    # ▶️ Case 3: Standard watch URLs (normalize params)
    if "youtube.com" in hostname and path == "/watch" and "v" in query:
        video_id = query["v"][0]
        return f"https://www.youtube.com/watch?v={video_id}"

    # 📃 Case 4: Playlist URLs (keep as-is)
    if "youtube.com" in hostname and "list" in query:
        playlist_id = query["list"][0]
        return f"https://www.youtube.com/playlist?list={playlist_id}"

    # 🔄 Default: leave untouched (yt-dlp can handle many exotic cases)
    return url