import unittest
from src.utils import strip_ansi_codes

class TestUtils(unittest.TestCase):
    def test_strip_ansi_codes(self):
        # Teste com string contendo códigos ANSI
        self.assertEqual(strip_ansi_codes("\x1B[31mRed Text\x1B[0m"), "Red Text")
        
        # Teste com string sem códigos ANSI
        self.assertEqual(strip_ansi_codes("Plain Text"), "Plain Text")
        
        # Teste com string vazia
        self.assertEqual(strip_ansi_codes(""), "")
        
        # Teste com múltiplos códigos ANSI
        self.assertEqual(strip_ansi_codes("\x1B[31mRed\x1B[0m \x1B[32mGreen\x1B[0m"), "Red Green")

if __name__ == '__main__':
    unittest.main()
