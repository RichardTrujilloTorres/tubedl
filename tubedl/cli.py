import os
import sys
import yt_dlp
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from tubedl.utils import normalize_youtube_url

console = Console()

@click.command()
@click.argument('url')
@click.option('-f', '--format', default='best', help='Video format (mp4, mp3, best, worst)')
@click.option('-o', '--output', default='.', help='Output directory')
@click.option('-q', '--quiet', is_flag=True, help='Suppress output')
def main(url, format, output, quiet):
    """tubedl — simple YouTube video & audio downloader."""

    os.makedirs(output, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best' if format == 'mp3' else format,
        'outtmpl': os.path.join(output, '%(title)s.%(ext)s'),
        'quiet': quiet,
        'noprogress': True,
        'postprocessors': []
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
            task = progress.add_task("Downloading...", start=False)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                progress.start_task(task)
                url = normalize_youtube_url(url)
                ydl.download([url])

        if not quiet:
            console.print("[bold green]✅ Download complete![/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()