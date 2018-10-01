# -*- coding: UTF-8 -*-

import os

import strings
from converter import Converter
from crypter import Crypter


# ToDO допилить методы для листинга
# ToDo добавить аргументы командной строки для листинга

class Steganography:

    @staticmethod
    def _get_pixels_array_start_pos(file_name):
        """Возвращает начало байтового массива .bmp файла."""
        with open(file_name, 'rb') as f:
            f.seek(10)
            pixels_array_start = Converter.bytes_to_int(f.read(4))
            return pixels_array_start

    @staticmethod
    def _correct_pixels_array_start_pos(file_name, bytes_arr, is_insert):
        """Корректирует позицию байтового массива .bmp файла после
        вставки или удаления сообщения."""
        old_start_pos = Steganography._get_pixels_array_start_pos(file_name)
        if is_insert:
            new_start_pos = old_start_pos + len(bytes_arr)
        else:
            new_start_pos = old_start_pos - len(bytes_arr)
        Steganography._rewrite_pixels_array_start_pos(file_name, new_start_pos)

    @staticmethod
    def _rewrite_pixels_array_start_pos(file_name, new_start_pos):
        """Заменияет позицию байтового массива в .bmp файле."""
        with open(file_name, 'rb') as f:
            file_data = bytearray(f.read())
        new_size_bytes = Converter.int_to_bytes(new_start_pos, 4)
        for i in range(4):
            file_data[10 + i] = new_size_bytes[i]
        with open(file_name, 'wb') as f:
            f.write(file_data)

    @staticmethod
    def _correct_file_size(file_name):
        """Корректирует поле в .bmp файле, отвечающее за размер файла."""
        with open(file_name, 'rb') as f:
            file_data = bytearray(f.read())

        file_size = Converter.int_to_bytes(os.path.getsize(file_name), 4)
        for i in range(4):
            file_data[i + 2] = file_size[i]

        with open(file_name, 'wb') as f:
            f.write(file_data)

    @staticmethod
    def _get_secret_list_from_message(message, elements_count):
        message_list = []
        if elements_count > 0:
            for i in range(elements_count):
                message_list.append("")
        else:
            message_list.append("")
        for i in range(len(message)):
            message_list[i % elements_count] += message[i]
        return message_list

    @staticmethod
    def _get_message_from_secret_list(secret_list):
        message = ""
        for k in range(len(secret_list[0])):
            for i in range(len(secret_list)):
                if len(secret_list[i]) > k:
                    message += secret_list[i][k]
        return message

    @staticmethod
    def encode_to_many_bmp(message, files):
        message_list = Steganography._get_secret_list_from_message(message,
                                                                   len(files))
        for i in range(len(files)):
            Steganography.encode_to_bmp(files[i], message_list[i])

    @staticmethod
    def decode_from_many_bmp(files):
        message_list = []
        for file in files:
            message_list.append(Steganography.decode_from_bmp(file))
        return Steganography._get_message_from_secret_list(message_list)

    @staticmethod
    def encode_to_bmp(file_name, message):
        """Кодирует сообщение в .bmp файл."""
        with open(file_name, 'rb') as f:
            file_data = bytearray(f.read())

        text_to_input = Steganography._convert_text_to_special_byte_arr(
            message)
        pixels_arr_start = Steganography._get_pixels_array_start_pos(
            file_name)

        data_before_pixels_array = file_data[:pixels_arr_start]
        pixels_arr = file_data[pixels_arr_start:]

        with open(file_name, 'wb') as f:
            f.write(data_before_pixels_array)
            f.write(text_to_input)
            f.write(pixels_arr)

        Steganography._correct_file_size(file_name)
        Steganography._correct_pixels_array_start_pos(file_name, text_to_input,
                                                      True)

    @staticmethod
    def decode_from_bmp(file_name):
        """Извлекает сообщение из .bmp файла."""
        byte_arr = Steganography._get_special_byte_array_from_file(file_name)
        decoded_message = Steganography._convert_special_byte_arr_to_text(
            byte_arr)
        return decoded_message

    @staticmethod
    def delete_message_from_bmp(file_name):
        """Удаляет шифрованное соообщение из .bmp файла при наличии."""
        with open(file_name, 'rb') as f:
            file_data = bytearray(f.read())

        special_byte_arr = Steganography._get_special_byte_array_from_file(
            file_name)
        if Steganography._check_message_availability(special_byte_arr):
            end_pos = Steganography._get_pixels_array_start_pos(file_name)
            start_pos = end_pos - len(special_byte_arr)
            data_before_message = file_data[:start_pos]
            data_after_message = file_data[end_pos:]

            with open(file_name, 'wb') as f:
                f.write(data_before_message)
                f.write(data_after_message)
            Steganography._correct_pixels_array_start_pos(file_name,
                                                          special_byte_arr,
                                                          False)

            return strings.MESSAGE_DELETED
        else:
            return strings.MESSAGE_NOT_FOUND

    @staticmethod
    def delete_message_from_many_bmp(files):
        """Удаляет шифрованное соообщение из списка .bmp файлов при наличии."""
        results = []
        for file in files:
            results.append(Steganography.delete_message_from_bmp(file))

        result_message = ""
        if strings.MESSAGE_NOT_FOUND in results:
            return strings.SOME_FILE_HAS_NOT_MESSAGE + "\n" + strings.MESSAGE_DELETED
        return strings.MESSAGE_DELETED

    @staticmethod
    def _convert_text_to_special_byte_arr(input_text):
        """Конвертирует текст в специальный байтовый массив,
        который впоследствии будет вставлен в .bmp файл."""
        encoded_text = Crypter.encode_text(input_text).encode("UTF-8")
        text_hashcode = Crypter.get_MD5_hash(input_text).encode(
            "UTF-8")
        result_arr_length = Converter.int_to_bytes(
            len(encoded_text) + len(text_hashcode) + 4, 4)
        return encoded_text + text_hashcode + result_arr_length

    @staticmethod
    def _get_special_byte_array_from_file(file_name):
        """Извлекает из файла специальный байтовый массив,
        который содержит метаданные и зашифрованное сообщение"""
        with open(file_name, 'rb') as f:
            end_of_message = Steganography._get_pixels_array_start_pos(
                file_name)
            f.seek(end_of_message - 4)

            arr_size = Converter.bytes_to_int(f.read(4))
            if end_of_message < arr_size:
                raise Exception(strings.DATA_CORRUPTED)
            f.seek(end_of_message - arr_size)
            resut_arr = bytearray(f.read(arr_size))
            return resut_arr

    @staticmethod
    def _check_message_availability(special_byte_arr):
        """Проверяет массив байт на наличие сообщения и метаданных."""
        try:
            hash_from_byte_arr = special_byte_arr[-36:-4].decode("UTF-8")
            encoded_text = special_byte_arr[:-36].decode("UTF-8")
            decoded_text = Crypter.decode_text(encoded_text)
            hash_of_decoded_text = Crypter.get_MD5_hash(decoded_text)
            return hash_of_decoded_text == hash_from_byte_arr
        except UnicodeDecodeError:
            raise Exception(strings.DATA_CORRUPTED)

    @staticmethod
    def _convert_special_byte_arr_to_text(special_byte_arr):
        """Конвертирует байтовый массив с сообщением обратно в сообщение."""
        if not Steganography._check_message_availability(special_byte_arr):
            raise Exception(strings.DATA_CORRUPTED)
        encoded_text = special_byte_arr[:-36].decode("UTF-8")
        decoded_text = Crypter.decode_text(encoded_text)
        return decoded_text
