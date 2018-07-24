from crypter import Crypter
from converter import Converter
import os


class Steganography:
    # ToDo Добавить проверку на то, что что-то уже закодировано и если да, то удалить прошлое сообщение (параметр)

    @staticmethod
    def _find_pixels_array_start_pos(file_name):
        f = open(file_name, 'rb')
        f.seek(10)
        pixels_array_start = Converter.bytes_to_int(f.read(4))
        f.close()
        return pixels_array_start

    @staticmethod
    def _correct_pixels_array_start_pos(file_name, bytes_arr, is_insert):
        old_start_pos = Steganography._find_pixels_array_start_pos(file_name)
        if is_insert:
            new_start_pos = old_start_pos + len(bytes_arr)
        else:
            new_start_pos = old_start_pos - len(bytes_arr)
        Steganography._rewrite_pixels_array_start_pos(file_name, new_start_pos)

    @staticmethod
    def _rewrite_pixels_array_start_pos(file_name, new_start_pos):
        f = open(file_name, 'rb')
        file_data = bytearray(f.read())
        f.close()
        new_size_bytes = Converter.int_to_bytes(new_start_pos, 4)
        for i in range(4):
            file_data[10 + i] = new_size_bytes[i]
        f = open(file_name, 'wb')
        f.write(file_data)
        f.close()

    @staticmethod
    def _correct_file_size(file_name):
        f = open(file_name, 'rb')
        file_data = bytearray(f.read())
        f.close()

        file_size = Converter.int_to_bytes(os.path.getsize("palm.bmp"), 4)
        for i in range(4):
            file_data[i + 2] = file_size[i]

        f = open(file_name, 'wb')
        f.write(file_data)
        f.close()

    @staticmethod
    def encode_to_bmp(file_name, message):
        f = open(file_name, 'rb')
        file_data = bytearray(f.read())
        f.close()

        text_to_input = Steganography._convert_text_to_special_byte_arr_for_encode(
            message)
        pixels_arr_start = Steganography._find_pixels_array_start_pos(
            file_name)

        data_before_pixels_array = file_data[:pixels_arr_start]
        pixels_arr = file_data[pixels_arr_start:]

        f = open(file_name, 'wb')
        f.write(data_before_pixels_array)
        f.write(text_to_input)
        f.write(pixels_arr)
        f.close()

        Steganography._correct_file_size(file_name)
        Steganography._correct_pixels_array_start_pos(file_name, text_to_input,
                                                      True)

    # ToDo Добавить возможность стирать данные при раскодировке
    @staticmethod
    def decode_from_bmp(file_name):
        byte_arr = Steganography._get_special_byte_array_from_file(file_name)
        decoded_message = Steganography._convert_special_byte_arr_to_text(
            byte_arr)
        return decoded_message

    @staticmethod
    def delete_message_from_bmp(file_name):
        f = open(file_name, 'rb')
        file_data = bytearray(f.read())
        f.close()

        special_byte_arr = Steganography._get_special_byte_array_from_file(
            file_name)
        if Steganography._check_message_availability(special_byte_arr):
            end_pos = Steganography._find_pixels_array_start_pos(file_name)
            start_pos = end_pos - len(special_byte_arr)
            data_before_message = file_data[:start_pos]
            data_after_message = file_data[end_pos:]

            f = open(file_name, 'wb')
            f.write(data_before_message)
            f.write(data_after_message)
            f.close()
            Steganography._correct_pixels_array_start_pos(file_name,
                                                          special_byte_arr,
                                                          False)
        else:
            print("has not messange")

    @staticmethod
    def _convert_text_to_special_byte_arr_for_encode(input_text):

        encoded_text = Crypter.encode_text(input_text).encode("UTF-8")
        text_hashcode = Crypter.get_MD5_hash(input_text).encode(
            "UTF-8")
        result_arr_length = Converter.int_to_bytes(
            len(encoded_text) + len(text_hashcode) + 4, 4)
        return encoded_text + text_hashcode + result_arr_length

    # ToDo нужна проверка на то, что длина массива больше файла
    @staticmethod
    def _get_special_byte_array_from_file(file_name):
        f = open(file_name, 'rb')
        end_of_message = Steganography._find_pixels_array_start_pos(file_name)
        f.seek(end_of_message - 4)

        arr_size = Converter.bytes_to_int(f.read(4))
        f.seek(end_of_message - arr_size)
        resut_arr = bytearray(f.read(arr_size))
        f.close()
        return resut_arr

    @staticmethod
    def _check_message_availability(special_byte_arr):
        hash_from_byte_arr = special_byte_arr[-36:-4].decode("UTF-8")
        encoded_text = special_byte_arr[:-36].decode("UTF-8")
        decoded_text = Crypter.decode_text(encoded_text)
        hash_of_decoded_text = Crypter.get_MD5_hash(decoded_text)

        return hash_of_decoded_text == hash_from_byte_arr

    @staticmethod
    def _convert_special_byte_arr_to_text(special_byte_arr):
        if not Steganography._check_message_availability(special_byte_arr):
            raise Exception("Нарушена целостность данных")

        encoded_text = special_byte_arr[:-36].decode("UTF-8")
        decoded_text = Crypter.decode_text(encoded_text)
        return decoded_text
