import os
import sys
import yt_dlp
import click
import requests
from urllib.parse import urlparse, parse_qs
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from tubedl.utils import normalize_youtube_url

console = Console()


def is_playlist_url(url: str) -> bool:
    """Check if the URL contains a playlist parameter."""
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    return "list" in query


@click.command()
@click.argument("url")
@click.option("-f", "--format", default="best", help="Video format (mp4, mp3, best, worst)")
@click.option("-o", "--output", default=".", help="Output directory")
@click.option("-p", "--playlist", is_flag=True, help="Download full playlist if URL includes one")
@click.option("-q", "--quiet", is_flag=True, help="Suppress output")
@click.option(
    "--cookies",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to cookies.txt for age-restricted/private videos",
)
@click.option(
    "--cookies-from-browser",
    type=click.Choice(["chrome", "firefox", "edge", "safari", "brave"]),
    help="Load cookies automatically from a local browser session",
)
@click.option("--thumbnail", is_flag=True, help="Download only the video thumbnail (no video/audio)")
def main(url, format, output, playlist, quiet, cookies, cookies_from_browser, thumbnail):
    """tubedl — simple YouTube video & audio downloader with restricted video and thumbnail support."""

    os.makedirs(output, exist_ok=True)
    url = normalize_youtube_url(url)
    is_playlist = is_playlist_url(url)

    # 🔹 Handle thumbnail-only mode
    if thumbnail:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        video_id = query.get("v", [None])[0]

        if not video_id:
            console.print("[red]❌ Could not extract video ID from URL.[/red]")
            sys.exit(1)

        thumb_urls = [
            f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
        ]
        thumb_path = os.path.join(output, f"{video_id}_thumbnail.jpg")

        try:
            for thumb_url in thumb_urls:
                r = requests.get(thumb_url, stream=True)
                if r.status_code == 200:
                    with open(thumb_path, "wb") as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
                    console.print(f"[green]✅ Thumbnail downloaded:[/green] {thumb_path}")
                    sys.exit(0)
            console.print("[red]❌ No thumbnail found for this video.[/red]")
        except Exception as e:
            console.print(f"[bold red]❌ Error downloading thumbnail:[/bold red] {e}")
        sys.exit(1)

    # 🔹 Configure yt-dlp options
    ydl_opts = {
        "format": "bestaudio/best" if format == "mp3" else format,
        "outtmpl": os.path.join(
            output,
            "%(playlist_title)s/%(title)s.%(ext)s"
            if playlist or is_playlist
            else "%(title)s.%(ext)s"
        ),
        "quiet": quiet,
        "noprogress": True,
        "postprocessors": [],
        "ignoreerrors": True,
        "noplaylist": not playlist,
    }

    # 🔹 Add cookie support
    if cookies:
        ydl_opts["cookiefile"] = cookies
    elif cookies_from_browser:
        ydl_opts["cookiesfrombrowser"] = (cookies_from_browser,)

    # 🔹 Add MP3 audio extraction
    if format == "mp3":
        ydl_opts["postprocessors"].append(
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        )

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=console,
            disable=quiet,
        ) as progress:
            desc = "Downloading playlist..." if playlist and is_playlist else "Downloading video..."
            task = progress.add_task(desc, start=False)

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                progress.start_task(task)
                ydl.download([url])

        if not quiet:
            console.print(f"[cyan]Detected playlist URL:[/cyan] {is_playlist}")
            console.print(f"[cyan]Playlist flag:[/cyan] {playlist}")
            console.print(f"[cyan]noplaylist setting:[/cyan] {ydl_opts['noplaylist']}")
            if cookies:
                console.print(f"[green]Using cookies from:[/green] {cookies}")
            elif cookies_from_browser:
                console.print(f"[green]Loaded cookies from browser:[/green] {cookies_from_browser}")

    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()