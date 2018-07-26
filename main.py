# -*- coding: UTF-8 -*-

from steganography import Steganography
import sys
import argparse
import strings


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', nargs='?', required=True,
                        help=strings.HELP_FILEPATH)
    parser.add_argument('-e', '--encode', help=strings.HELP_ENCODE)
    parser.add_argument('-d', '--decode', action='store_const', const=True,
                        default=False, help=strings.HELP_DECODE)
    parser.add_argument('-c', '--clear', action='store_const', const=True,
                        default=False, help=strings.HELP_CLEAR)
    return parser


def run():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    if namespace.encode is not None and not namespace.decode:
        if namespace.clear:
            Steganography.delete_message_from_bmp(namespace.filepath)
        Steganography.encode_to_bmp(namespace.filepath, namespace.encode)
        return strings.ENCODE_COMPLETE

    elif namespace.decode and namespace.encode is None:
        message = Steganography.decode_from_bmp(namespace.filepath)
        if namespace.clear:
            Steganography.delete_message_from_bmp(namespace.filepath)
        return message

    elif (namespace.clear and namespace.encode is None and
          not namespace.decode):
        return Steganography.delete_message_from_bmp(namespace.filepath)
    else:
        return strings.WRONG_ARGUMENTS


if __name__ == "__main__":
    print(run())
