import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def normalize_youtube_url(url: str) -> str:
    """
    Normalize YouTube URLs while preserving playlist information.
    Converts short and shorts URLs into watch URLs.
    Keeps ?list= and other useful query parameters.
    """

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parse_qs(parsed.query)

    # Handle youtu.be short links
    match = re.match(r"^/([A-Za-z0-9_-]{11})$", path)
    if "youtu.be" in hostname and match:
        video_id = match.group(1)
        new_query = {'v': video_id}
        # Keep playlist if present
        if 'list' in query:
            new_query['list'] = query['list']
        return f"https://www.youtube.com/watch?{urlencode(new_query, doseq=True)}"

    # Handle shorts
    match = re.match(r"^/shorts/([A-Za-z0-9_-]{11})$", path)
    if "youtube.com" in hostname and match:
        video_id = match.group(1)
        new_query = {'v': video_id}
        if 'list' in query:
            new_query['list'] = query['list']
        return f"https://www.youtube.com/watch?{urlencode(new_query, doseq=True)}"

    # Default — return normalized base URL
    return url