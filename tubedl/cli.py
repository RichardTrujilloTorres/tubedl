import os
import sys
import yt_dlp
import click
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
def main(url, format, output, playlist, quiet, cookies, cookies_from_browser):
    """tubedl — simple YouTube video & audio downloader with restricted video support."""

    os.makedirs(output, exist_ok=True)
    url = normalize_youtube_url(url)
    is_playlist = is_playlist_url(url)

    # Configure yt-dlp options
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

    # Add cookie support
    if cookies:
        ydl_opts["cookiefile"] = cookies
    elif cookies_from_browser:
        ydl_opts["cookiesfrombrowser"] = (cookies_from_browser,)

    # Add MP3 audio extraction
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