import hashlib

class Crypter:

    @staticmethod
    def _encode_text(input_text):
        UTF8_SYMBOLS_COUNT = 55296
        step = 0
        result = ""
        for char in input_text:
            step += 1
            result += chr((ord(char) + step) % UTF8_SYMBOLS_COUNT)  # Сдвиг
        return result

    @staticmethod
    def _decode_text(input_text):
        UTF8_SYMBOLS_COUNT = 55296
        step = 0
        result = ""
        for char in input_text:
            step += 1
            result += chr(
                (UTF8_SYMBOLS_COUNT + ord(char) - step) % UTF8_SYMBOLS_COUNT)
        return result

    @staticmethod
    def _get_text_hashcode(input_text):
        return hashlib.md5(input_text.encode("UTF-8")).hexdigest()