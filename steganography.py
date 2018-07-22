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

    @staticmethod
    def _convert_text_to_special_byte_arr_for_encode(input_text):
        text_length_str = Steganography._int_to_bytes(len(input_text), 4)
        encoded_text = Steganography._encode_text(input_text).encode("UTF-8")
        text_hashcode = Steganography._get_text_hashcode(input_text).encode(
            "UTF-8")
        return encoded_text + text_hashcode + text_length_str

    @staticmethod
    def _convert_special_byte_arr_to_text(byte_arr):
        text_len = Steganography._bytes_to_int(byte_arr[-4:])
        text_hash = byte_arr[-36:-4].decode("UTF-8")
        encoded_text = byte_arr[:-36].decode("UTF-8")
        text = Steganography._decode_text(encoded_text)

        hash_of_encoded_text = Steganography._get_text_hashcode(text)

        if (hash_of_encoded_text != text_hash):
            raise Exception("Нарушена целостность данных")

        return Steganography._decode_text(encoded_text)

    @staticmethod
    def _bytes_to_int(byte_arr):
        result_value = ''
        for byte_pos in range(len(byte_arr) - 1, -1, -1):
            result_value += bin(byte_arr[byte_pos])[2:].zfill(8)
        return int(result_value, 2)

    @staticmethod
    def _int_to_bytes(int_value, result_len):
        bin_value_str = str(bin(int_value))[2:]
        bin_value_str = bin_value_str.zfill(len(bin_value_str) // 8 * 8 + 8)
        result = bytearray()
        for byte_pos in range(len(bin_value_str) // 8 - 1, -1, -1):
            result.append(
                int(bin_value_str[byte_pos * 8:(byte_pos + 1) * 8], 2))
        while len(result) < result_len:
            result.append(0)
        return result
