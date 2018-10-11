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
        message_list = Steganography._get_secret_list_from_message(message,
                                                                   len(files))
        for i in range(len(files)):
            Steganography.encode_to_bmp(files[i], message_list[i])

    @staticmethod
    def decode_from_many_bmp(files):
        """Декодирует сообщение из большого количества файлов"""
        message_list = []
        for file in files:
            message_list.append(Steganography.decode_from_bmp(file))
        return Steganography._get_message_from_secret_list(message_list)
