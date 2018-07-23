import hashlib

class Crypter:

    #ToDo Протестировать методы кодировки текста
    @staticmethod
    def encode_text(input_text):
        UTF8_CHARS_COUNT = 55296
        step = 0
        result = ""
        for char in input_text:
            step += 1
            result += chr((ord(char) + step) % UTF8_CHARS_COUNT)
        return result

    @staticmethod
    def decode_text(input_text):
        UTF8_CHARS_COUNT = 55296
        step = 0
        result = ""
        for char in input_text:
            step += 1
            result += chr(
                (UTF8_CHARS_COUNT + ord(char) - step) % UTF8_CHARS_COUNT)
        return result

    #ToDo Протестировать метод создания хэшкода
    @staticmethod
    def get_text_hashcode(input_text):
        return hashlib.md5(input_text.encode("UTF-8")).hexdigest()