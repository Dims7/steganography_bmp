import unittest
from steganography import Steganography
import random
import string


class TestCodeText(unittest.TestCase):

    def make_test(self, text):
        text_for_code = text
        encoded_text = Steganography._encode_text(text_for_code)
        decoded_text = Steganography._decode_text(encoded_text)
        self.assertEqual(text_for_code, decoded_text)

    def test_empty_string(self):
        self.make_test("")

    def test_simple_strings(self):
        self.make_test("a")
        self.make_test("abc")
        self.make_test("lol")
        self.make_test("Hello")

    def test_symbols(self):
        self.make_test(".")
        self.make_test("\\")
        self.make_test("//")
        self.make_test("./,!@#$%^&*()!№;%:?*()")

    def test_random_words(self):
        for _ in range(100):
            string_for_test = "".join(random.SystemRandom().choices(
                string.ascii_letters + string.digits, k=random.randint(3, 25)))
            self.make_test(string_for_test)

class TestIntAndByteConverter(unittest.TestCase):

    def make_test(self):
        pass

if __name__ == "__main__":
    unittest.main()