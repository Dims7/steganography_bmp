from steganography import Steganography

if __name__ == "__main__":
    Steganography.encode_to_bmp("palm.bmp", "Jorj")
    print(Steganography.decode_from_bmp("palm.bmp"))