# -*- coding: UTF-8 -*-

import base64
import hashlib


class Crypter:

    @staticmethod
    def encode_text(input_text):
        """Кодирует текст по модифицированному шифру цезаря
         + алгоритм base 64."""
        bytes_base64 = base64.b64encode(bytes(input_text, 'utf-8'))
        string_base64 = bytes_base64.decode('utf-8')

        UTF8_CHARS_COUNT = 55296
        step = 0
        result = ""
        for char in string_base64:
            step += 1
            result += chr((ord(char) + step) % UTF8_CHARS_COUNT)
        return result

    @staticmethod
    def decode_text(input_text):
        """Раскодирует текст, зашифрованный по модифицированному цезарю
         + base64."""
        UTF8_CHARS_COUNT = 55296
        step = 0
        result_cesar = ""
        for char in input_text:
            step += 1
            result_cesar += chr(
                (UTF8_CHARS_COUNT + ord(char) - step) % UTF8_CHARS_COUNT)

        result_bytes = base64.b64decode(result_cesar)
        return result_bytes.decode('utf-8')

    @staticmethod
    def get_MD5_hash(input_text):
        """Получает MD5 хэш."""
        return hashlib.md5(input_text.encode("UTF-8")).hexdigest()
