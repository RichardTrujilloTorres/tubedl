import os
import pytest
from click.testing import CliRunner
from tubedl.cli import main  # 👈 changed from cli → main
from unittest.mock import patch


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_help(runner):
    """Ensure the CLI displays help and exits cleanly."""
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "tubedl" in result.output


def test_cli_url_normalization_youtube(runner, tmp_path):
    """Ensure short youtu.be URLs are normalized correctly."""
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    with patch("tubedl.cli.yt_dlp.YoutubeDL") as mock_dl:
        mock_instance = mock_dl.return_value.__enter__.return_value
        mock_instance.download.return_value = 0

        result = runner.invoke(
            main,
            [
                "https://youtu.be/dQw4w9WgXcQ",
                "-f", "mp4",
                "-o", str(output_dir),
            ],
        )

        assert result.exit_code == 0
        # Assert yt_dlp was called with the normalized URL
        called_args = mock_instance.download.call_args[0][0]
        assert called_args[0] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

def test_cli_playlist_flag(runner, tmp_path):
    """Verify the playlist flag triggers playlist handling and runs cleanly."""
    output_dir = tmp_path / "music"
    output_dir.mkdir()

    result = runner.invoke(
        main,
        [
            "https://www.youtube.com/watch?v=abc123&list=PL123",
            "-f", "mp3",
            "-o", str(output_dir),
            "--playlist",
        ],
    )

    # Should exit successfully
    assert result.exit_code == 0

    # Verify CLI output reflects playlist detection
    assert "Detected playlist URL" in result.output
    assert "Playlist flag: True" in result.output
    assert "noplaylist" in result.output

def test_cli_accepts_cookies_file(runner, tmp_path):
    """Ensure --cookies flag is accepted and handled properly."""
    # Create a fake cookies.txt file
    cookies_file = tmp_path / "cookies.txt"
    cookies_file.write_text("# Netscape HTTP Cookie File\n")

    output_dir = tmp_path / "downloads"
    output_dir.mkdir()

    result = runner.invoke(
        main,
        [
            "https://youtu.be/dQw4w9WgXcQ",
            "-f", "mp4",
            "-o", str(output_dir),
            "--cookies", str(cookies_file),
        ],
    )

    # Verify CLI runs successfully
    assert result.exit_code == 0
    # The output should show cookies file being used
    assert "Using cookies from" in result.output


def test_cli_accepts_cookies_from_browser(runner, tmp_path):
    """Ensure --cookies-from-browser flag is accepted."""
    output_dir = tmp_path / "downloads"
    output_dir.mkdir()

    result = runner.invoke(
        main,
        [
            "https://youtu.be/dQw4w9WgXcQ",
            "-f", "mp4",
            "-o", str(output_dir),
            "--cookies-from-browser", "chrome",
        ],
    )

    assert result.exit_code == 0
    assert "Loaded cookies from browser" in result.output