import unittest
from unittest.mock import MagicMock, patch
from src.gui import on_enter, on_leave, play_click_sound
import pygame

class TestGui(unittest.TestCase):
    def setUp(self):
        pygame.mixer.init()

    def tearDown(self):
        pygame.mixer.quit()

    @patch('src.gui.play_click_sound')
    def test_on_enter(self, mock_play_click_sound):
        event = MagicMock()
        path = "test_path"
        
        on_enter(event, path)
        
        event.widget.config.assert_called_with(font=('Helvetica', 10, 'underline'))
        mock_play_click_sound.assert_called_once()

    def test_on_leave(self):
        event = MagicMock()
        
        on_leave(event)
        
        event.widget.config.assert_called_with(font=('Helvetica', 10))

    @patch('src.gui.pygame.mixer.Sound')
    def test_play_click_sound(self, MockSound):
        play_click_sound()
        
        MockSound.return_value.play.assert_called_once()

if __name__ == '__main__':
    unittest.main()
