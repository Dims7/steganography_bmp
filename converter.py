class Converter:

    @staticmethod
    def bytes_to_int(byte_arr):
        tmp_arr = []
        for byte_pos in range(len(byte_arr) - 1, -1, -1):
            tmp_arr.append(bin(byte_arr[byte_pos])[2:].zfill(8))
        return int(''.join(tmp_arr), 2)

    @staticmethod
    def int_to_bytes(int_value, result_len):
        if len(bin(int_value)) - 2 > result_len * 8:
            raise ValueError("Message to long")

        bin_value_str = str(bin(int_value))[2:]
        bin_value_str = bin_value_str.zfill(
            (len(bin_value_str) - 1) // 8 * 8 + 8)
        result = bytearray()
        for byte_pos in range(len(bin_value_str) // 8 - 1, -1, -1):
            result.append(
                int(bin_value_str[byte_pos * 8:(byte_pos + 1) * 8], 2))
        while len(result) < result_len:
            result.append(0)
        return result
