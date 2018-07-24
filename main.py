from steganography import Steganography

#ToDo добавить работу с аргументами
#ToDo Проверить работу на всех файлах в архиве
#ToDo добавить параметр удалить старое сообщение

if __name__ == "__main__":
    Steganography.encode_to_bmp('palm.bmp', "123")
    Steganography.decode_from_bmp('palm.bmp')
    Steganography.delete_message_from_bmp('palm.bmp', True)