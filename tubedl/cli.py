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
@click.argument('url')
@click.option('-f', '--format', default='best', help='Video format (mp4, mp3, best, worst)')
@click.option('-o', '--output', default='.', help='Output directory')
@click.option('-p', '--playlist', is_flag=True, help='Download full playlist if URL includes one')
@click.option('-q', '--quiet', is_flag=True, help='Suppress output')
def main(url, format, output, playlist, quiet):
    """tubedl — simple YouTube video & audio downloader."""

    os.makedirs(output, exist_ok=True)
    url = normalize_youtube_url(url)

    # Detect if URL includes a playlist
    is_playlist = is_playlist_url(url)

    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best' if format == 'mp3' else format,
        'outtmpl': os.path.join(
            output,
            '%(playlist_title)s/%(title)s.%(ext)s' if playlist or is_playlist else '%(title)s.%(ext)s'
        ),
        'quiet': quiet,
        'noprogress': True,
        'postprocessors': [],
        'ignoreerrors': True,
        # 👇 Correct way to handle playlists
        'noplaylist': not playlist,
    }

    if format == 'mp3':
        ydl_opts['postprocessors'].append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        })

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=console,
            disable=quiet
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
    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()