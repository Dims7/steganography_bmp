# -*- coding: UTF-8 -*-

import base64
import hashlib


class Crypter:

    @staticmethod
    def encode_text(input_text):
        """Кодирует текст по модифицированному шифру цезаря."""
        resultBytes = base64.b64encode(bytes(input_text, 'utf-8'))
        return resultBytes.decode('utf-8')

    @staticmethod
    def decode_text(input_text):
        """Раскодирует текст, зашифрованный по модифицированному цезарю."""
        input_bytes = base64.b64decode(input_text)
        result = input_bytes.decode('utf-8')
        return result

    @staticmethod
    def get_MD5_hash(input_text):
        """Получает MD5 хэш."""
        return hashlib.md5(input_text.encode("UTF-8")).hexdigest()
