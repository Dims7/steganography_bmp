# -*- coding: UTF-8 -*-

from steganography import Steganography
import sys

# ToDo добавить работу с аргументами
# ToDo Проверить работу на всех файлах в архиве
if __name__ == "__main__":
    flag_encode = False
    flag_decode = False
    flag_delete = False
    flag_message = False
    flag_path_file = False

    message = None
    file_path = None

    for arg in sys.argv[1:]:
        if flag_message and message is None:
            message = arg
        elif flag_path_file and file_path is None:
            file_path = arg
        elif arg == "-e":
            flag_encode = True
        elif arg == "-d":
            flag_decode = True
        elif arg == "-c":
            flag_delete = True
        elif arg == "-m":
            flag_message = True
        elif arg == "-f":
            flag_path_file = True

    flag_error = False

    if file_path is None:
        print("You must enter the path to the file with the -f argument")
        flag_error = True
    if flag_encode and message is None:
        print("You must enter a message with the -m argument")
        flag_error = True

    if not flag_error and flag_path_file:
        if (flag_encode and flag_message and not flag_decode and
                not flag_delete):
            Steganography.encode_to_bmp(file_path, message)
        elif flag_decode and not flag_message and not flag_encode:
            print(Steganography.decode_from_bmp(file_path))
            if flag_delete:
                Steganography.delete_message_from_bmp(file_path, False)
        elif (flag_delete and not flag_message and not flag_encode and
              not flag_message and not flag_decode):
            Steganography.delete_message_from_bmp(file_path, True)
        else:
            print("Wrong arguments.")
