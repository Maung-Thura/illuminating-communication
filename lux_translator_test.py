import unittest
from lux_translator import lux_to_morse, morse_to_text

class TestLuxToText(unittest.TestCase):

    def test_sos(self):
        # Simulate lux values for S.O.S (Short - Short - Short / Long - Long - Long / Short - Short - Short)
        lux_values = [150, 150, 150, 50, 50, 50, 150, 150, 150]  # Morse equivalent: ... --- ...
        morse_code = lux_to_morse(lux_values)
        self.assertEqual(morse_code, "...---...")

        # Translate to English
        translated_text = morse_to_text(morse_code)
        self.assertEqual(translated_text, "SOS")

# ......-...--.
    def test_help(self):
        # Simulate lux values for HELP 
        lux_values = [150, 150, 150, 150, 150, 150, 50, 150, 150, 150, 50, 50, 150] 
        morse_code = lux_to_morse(lux_values)
        self.assertEqual(morse_code, "......-...--.")

        # Translate to English
        translated_text = morse_to_text(morse_code)
        self.assertEqual(translated_text, "HELP")

if __name__ == '__main__':
    unittest.main()