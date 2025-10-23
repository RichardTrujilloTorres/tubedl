import re

def normalize_youtube_url(url: str) -> str:
    """
    Normalize YouTube URLs to a canonical 'https://www.youtube.com/watch?v=...' form.
    Handles shortlinks, shorts, missing protocols, and extra query parameters.
    """

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # youtu.be short links
    match = re.match(r"https?://(?:www\.)?youtu\.be/([A-Za-z0-9_-]{11})", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"

    # shorts links
    match = re.match(r"https?://(?:www\.)?youtube\.com/shorts/([A-Za-z0-9_-]{11})", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"

    # standard YouTube links (watch?v=)
    match = re.match(r"https?://(?:www\.)?youtube\.com/watch\?v=([A-Za-z0-9_-]{11})", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"

    # Already a supported URL (like playlist or mix)
    return url