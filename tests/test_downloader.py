import unittest
from unittest.mock import MagicMock, patch
from src.downloader import download_youtube_video, reset_download_ui

class TestDownloader(unittest.TestCase):
    @patch('src.downloader.yt_dlp.YoutubeDL')
    def test_download_youtube_video(self, MockYoutubeDL):
        MockYoutubeDL.return_value.__enter__.return_value.download.return_value = None
        
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        quality = "best"
        output_format = "mp4"
        progress_bar = MagicMock()
        status_label = MagicMock()
        progress = MagicMock()
        messagebox = MagicMock()
        root = MagicMock()
        update_downloaded_files_list = MagicMock()
        
        download_youtube_video(url, quality, output_format, progress_bar, status_label, progress, messagebox, root, update_downloaded_files_list)
        
        MockYoutubeDL.return_value.__enter__.return_value.download.assert_called_once_with([url])
        update_downloaded_files_list.assert_called_once()

    def test_reset_download_ui(self):
        progress_bar = MagicMock()
        status_label = MagicMock()
        progress = MagicMock()
        root = MagicMock()
        
        reset_download_ui(progress_bar, status_label, progress, root)
        
        progress_bar.__setitem__.assert_called_with('value', 0)
        status_label.config.assert_called_with(text="")
        progress.set.assert_called_with("")

if __name__ == '__main__':
    unittest.main()
