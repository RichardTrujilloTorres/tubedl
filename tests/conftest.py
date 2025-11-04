import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def mock_youtube_dl():
    """Automatically mock yt_dlp.YoutubeDL for all tests."""
    with patch("tubedl.cli.yt_dlp.YoutubeDL") as mock_dl:
        mock_instance = MagicMock()
        mock_instance.download.return_value = 0  # simulate success
        mock_dl.return_value.__enter__.return_value = mock_instance
        yield mock_dl