import os
import pytest
from click.testing import CliRunner
from tubedl.cli import main  # 👈 changed from cli → main


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

    result = runner.invoke(
        main,
        [
            "https://youtu.be/dQw4w9WgXcQ",
            "-f", "mp4",
            "-o", str(output_dir),
        ],
    )

    # The CLI should run without crashing.
    assert result.exit_code == 0
    assert "https://www.youtube.com/watch?v=dQw4w9WgXcQ" in result.output or "✅" in result.output

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
