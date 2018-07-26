# -*- coding: UTF-8 -*-

from steganography import Steganography
import sys
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', nargs='?', required=True)
    parser.add_argument('-e', '--encode')
    parser.add_argument('-d', '--decode', action='store_const', const=True,
                        default=False)
    parser.add_argument('-c', '--clear', action='store_const', const=True,
                        default=False)
    return parser


def run():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    if namespace.encode is not None and not namespace.decode:
        if namespace.clear:
            Steganography.delete_message_from_bmp(namespace.filename,
                                                  False)
        Steganography.encode_to_bmp(namespace.filename, namespace.encode)
        return "Encode complete."

    elif namespace.decode and namespace.encode is None:
        message = Steganography.decode_from_bmp(namespace.filename)
        if namespace.clear:
            Steganography.delete_message_from_bmp(namespace.filename,
                                                  False)
        return message

    elif (namespace.clear and namespace.encode is None and
          not namespace.decode):
        return Steganography.delete_message_from_bmp(namespace.filename, True)

    else:
        return "Wrong arguments."


if __name__ == "__main__":
    print(run())
