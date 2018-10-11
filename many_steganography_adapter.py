from random import randint

from steganography import Steganography
import strings


class ManySteganographyAdapter:
    @staticmethod
    def delete_message_from_many_bmp(files):
        """Удаляет шифрованное соообщение из списка .bmp файлов при наличии."""
        results = []
        for file in files:
            results.append(Steganography.delete_message_from_bmp(file))

        if strings.MESSAGE_NOT_FOUND in results:
            return strings.SOME_FILE_HAS_NOT_MESSAGE + "\n" + strings.MESSAGE_DELETED
        return strings.MESSAGE_DELETED

    @staticmethod
    def encode_to_many_bmp(message, files):
        """Кодирует сообщение в большое количество файлов"""

        for file in files:
            c = 0
            for i in range(len(files)):
                if files[i] == file:
                    c += 1
            if c > 1:
                raise AttributeError(strings.FILES_IN_PATH_REPEATED)


        message_list = ManySteganographyAdapter._get_secret_list_from_message(
            message, len(files))
        for i in range(len(files)):
            Steganography.encode_to_bmp(files[i], message_list[i])

    @staticmethod
    def decode_from_many_bmp(files):
        """Декодирует сообщение из большого количества файлов"""
        message_list = []
        for file in files:
            message_list.append(Steganography.decode_from_bmp(file))
        return ManySteganographyAdapter._get_message_from_secret_list(
            message_list)

    @staticmethod
    def _get_secret_list_from_message(message, elements_count):
        message_list = []
        salt = ManySteganographyAdapter._generate_salt(
            letters_count=elements_count)
        for i in range(elements_count):
            message_list.append(str(i) + salt)
        for i in range(len(message)):
            message_list[i % elements_count] += message[i]
        return message_list

    @staticmethod
    def _pop_and_check_salt(secret_arr):
        for i in range(len(secret_arr)):
            if secret_arr[i].find(str(i)) == 0:
                secret_arr[i] = secret_arr[i][len(str(i)):]
            else:
                raise AttributeError(strings.DATA_CORRUPTED)
        salt = secret_arr[0][:len(secret_arr)]

        for i in range(1, len(secret_arr)):
            if secret_arr[i].find(salt) != 0:
                raise AttributeError(strings.DATA_CORRUPTED)

        for i in range(len(secret_arr)):
            secret_arr[i] = secret_arr[i][len(salt):]


    @staticmethod
    def _get_message_from_secret_list(secret_list):
        ManySteganographyAdapter._pop_and_check_salt(
            secret_list)
        message = ""
        for k in range(len(secret_list[0])):
            for i in range(len(secret_list)):
                if len(secret_list[i]) > k:
                    message += secret_list[i][k]
        return message

    @staticmethod
    def _generate_salt(letters_count):
        chars = "qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM"
        salt = ""
        for _ in range(letters_count):
            salt += chars[randint(0, len(chars) - 1)]
        return salt
