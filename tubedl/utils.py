import re

def normalize_youtube_url(url: str) -> str:
    """
    Normalize YouTube URLs to a canonical 'https://www.youtube.com/watch?v=...' form.
    Handles shortlinks, missing protocols, and extra query parameters.
    """

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Match youtu.be short link
    match = re.match(r"https?://(?:www\.)?youtu\.be/([A-Za-z0-9_-]{11})", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"

    # Match standard YouTube link
    match = re.match(r"https?://(?:www\.)?youtube\.com/watch\?v=([A-Za-z0-9_-]{11})", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"

    # If already valid or yt-dlp-compatible, just return as-is
    return url