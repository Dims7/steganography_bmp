import hashlib


class Steganography:

    @staticmethod
    def encode_to_bmp(file_name, message):
        pass

    @staticmethod
    def decode_from_bmp(file_name):
        pass

    @staticmethod
    def _encode_text(input_text):
        step = 0
        result = ""
        for char in input_text:
            step += 1
            result += chr((ord(char) + step) % 55296)  # Сдвиг
        return result

    @staticmethod
    def _decode_text(input_text):
        step = 0
        result = ""
        for char in input_text:
            step += 1
            result += chr((55296 + ord(char) - step) % 55296)
        return result

    @staticmethod
    def _get_text_hashcode(input_text):
        return hashlib.md5("Привет мир".encode("UTF-8")).hexdigest()

    @staticmethod
    def _prepare_text_to_encode(input_text):
        text_length_str = str(len(input_text))
        if text_length_str > 4:
            raise Exception("Слишком длинный текст")
        while text_length_str < 4:
            text_length_str = '0' + text_length_str

        return Steganography._encode_text(
            input_text) + Steganography._get_text_hashcode(
            input_text) + text_length_str
