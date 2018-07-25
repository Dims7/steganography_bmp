# -*- coding: UTF-8 -*-

import unittest
from steganography import Steganography
import random
import string
from crypter import Crypter
from converter import Converter
import shutil


# ToDo написать тесты
# ToDo прогнать на PEP 8 валидаторе
class TestConverter(unittest.TestCase):

    def test_backward_compatibility(self):
        for _ in range(1000):
            value = random.randint(0, 1000000)
            self.assertEqual(value, Converter.bytes_to_int(
                Converter.int_to_bytes(value, 4)))

    def test_any_values(self):
        self.assertEqual(bytearray(b'\xff'), Converter.int_to_bytes(255, 1))
        self.assertEqual(bytearray(b'\xff\x00'),
                         Converter.int_to_bytes(255, 2))
        self.assertEqual(bytearray(b'\x00'), Converter.int_to_bytes(0, 1))
        self.assertEqual(bytearray(b'\x75'), Converter.int_to_bytes(117, 1))

    def check_exception_long_message(self, value, count):
        with self.assertRaises(ValueError) as cm:
            Converter.int_to_bytes(value, count)
        exception = cm.exception
        self.assertEqual("Message to long", exception.args[0])

    def test_so_big_int_value(self):
        self.check_exception_long_message(256, 1)
        self.check_exception_long_message(65536, 2)
        self.check_exception_long_message(65536, 1)


class TestCrypter(unittest.TestCase):

    def test_hash_code(self):
        self.assertEqual("3e25960a79dbc69b674cd4ec67a72c62",
                         Crypter.get_MD5_hash("Hello world"))
        self.assertEqual("d41d8cd98f00b204e9800998ecf8427e",
                         Crypter.get_MD5_hash(""))
        self.assertEqual("aaccedee5cc97822658304e92121bd3f",
                         Crypter.get_MD5_hash("уекрекыонекуцкнелеунл"))

    def make_test_backward_compatibility(self, text):
        text_for_code = text
        encoded_text = Crypter.encode_text(text_for_code)
        decoded_text = Crypter.decode_text(encoded_text)
        self.assertEqual(text_for_code, decoded_text)

    def test_empty_string(self):
        self.make_test_backward_compatibility("")

    def test_simple_strings(self):
        self.make_test_backward_compatibility("a")
        self.make_test_backward_compatibility("abc")
        self.make_test_backward_compatibility("lol")
        self.make_test_backward_compatibility("Hello")

    def test_symbols(self):
        self.make_test_backward_compatibility(".")
        self.make_test_backward_compatibility("\\")
        self.make_test_backward_compatibility("//")
        self.make_test_backward_compatibility("./,!@#$%^&*()!№;%:?*()")

    def test_random_words(self):
        for _ in range(100):
            string_for_test = "".join(random.SystemRandom().choices(
                string.ascii_letters + string.digits, k=random.randint(3, 25)))
            self.make_test_backward_compatibility(string_for_test)


class TestSpecialByteArrFromSteganography(unittest.TestCase):
    def make_test_backward(self, message):
        converted_value = Steganography._convert_text_to_special_byte_arr(
            message)
        result_message = Steganography._convert_special_byte_arr_to_text(
            converted_value)
        self.assertEqual(message, result_message)

    def test_backward_compatibility(self):
        self.make_test_backward("")
        self.make_test_backward("1")
        self.make_test_backward("erlpiagjreawg'lkijeraq';hj")
        self.make_test_backward("щшоуцкфпжоукфпжщшоуфщшоуфкпщшок")


class TestCodeAllTypeOfBmpFiles(unittest.TestCase):

    def check_file(self, file_path):
        Steganography.encode_to_bmp(file_path, "Code")
        result = Steganography.decode_from_bmp((file_path))
        self.assertEqual("Code", result)

    def test_code_decode_all_type_of_bmp_files(self):
        folder_name = self.create_folder_with_tmp_bmp_files(
            "bmp_files_for_test")
        prefix = folder_name + "/"
        suffix = ".bmp"
        for i in range(1, 16):
            file_name = prefix + str(i) + suffix
            self.check_file(file_name)
        self.delete_folder_with_bmp_files(folder_name)

    def create_folder_with_tmp_bmp_files(self, path_to_bmp):
        shutil.copytree(path_to_bmp, "tmp_test_dir")
        return "tmp_test_dir"

    def delete_folder_with_bmp_files(self, path_to_bmp):
        shutil.rmtree(path_to_bmp)


if __name__ == "__main__":
    unittest.main()
