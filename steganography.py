from crypter import Crypter


class Steganography:

    @staticmethod
    def encode_to_bmp(file_name, message):
        f = open(file_name, 'ab')
        text_to_input = Steganography._convert_text_to_special_byte_arr_for_encode(message)
        f.write(text_to_input)
        f.close()

    @staticmethod
    def decode_from_bmp(file_name):
        f = open(file_name, 'rb')
        file_size = len(f.read())
        f.seek(file_size - 4)

        arr_size = Steganography._bytes_to_int(f.read())
        f.seek(file_size - arr_size)
        resut_arr = f.read()
        f.close()
        return Steganography._convert_special_byte_arr_to_text(resut_arr)




    @staticmethod
    def _convert_text_to_special_byte_arr_for_encode(input_text):
        encoded_text = Crypter._encode_text(input_text).encode("UTF-8")
        text_hashcode = Crypter._get_text_hashcode(input_text).encode(
            "UTF-8")
        result_arr_length = Steganography._int_to_bytes(
            len(encoded_text) + len(text_hashcode) + 4, 4)
        return encoded_text + text_hashcode + result_arr_length

    @staticmethod
    def _convert_special_byte_arr_to_text(byte_arr):
        text_hash = byte_arr[-36:-4].decode("UTF-8")
        encoded_text = byte_arr[:-36].decode("UTF-8")
        text = Crypter._decode_text(encoded_text)
        hash_of_encoded_text = Crypter._get_text_hashcode(text)

        if (hash_of_encoded_text != text_hash):
            raise Exception("Нарушена целостность данных")

        return Crypter._decode_text(encoded_text)

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
