from steganography import Steganography

#ToDo добавить работу с аргументами
#ToDo Проверить работу на всех файлах в архиве
#ToDo Написать файл с инструкциями
if __name__ == "__main__":
    Steganography.encode_to_bmp("palm.bmp", "Jorj")
    print(Steganography.decode_from_bmp("palm.bmp"))