# -*- coding: UTF-8 -*-

import hashlib


class Crypter:

    @staticmethod
    def encode_text(input_text):
        """Кодирует текст по модифицированному шифру цезаря."""
        UTF8_CHARS_COUNT = 55296
        step = 0
        result = ""
        for char in input_text:
            step += 1
            result += chr((ord(char) + step) % UTF8_CHARS_COUNT)
        return result

    @staticmethod
    def decode_text(input_text):
        """Раскодирует текст, зашифрованный по модифицированному цезарю."""
        UTF8_CHARS_COUNT = 55296
        step = 0
        result = ""
        for char in input_text:
            step += 1
            result += chr(
                (UTF8_CHARS_COUNT + ord(char) - step) % UTF8_CHARS_COUNT)
        return result

    @staticmethod
    def get_MD5_hash(input_text):
        """Получает MD5 хэш."""
        return hashlib.md5(input_text.encode("UTF-8")).hexdigest()
