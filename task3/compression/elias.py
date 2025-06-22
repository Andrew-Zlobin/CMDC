import math

class Elias:
    def _gamma_encode(self, n: int) -> str:
        if n <= 0:
            raise ValueError("in func _gamma_encode n must be > 0")
        n_bin = bin(n)[2:]
        prefix = '0' * (len(n_bin) - 1)
        return prefix + n_bin

    def _delta_encode_positive(self, n: int) -> str:
        if n <= 1:
            raise ValueError("in func _delta_encode_positive > 1.")
        n_bin = bin(n)[2:]
        length_of_n_bin = len(n_bin)
        gamma_part = self._gamma_encode(length_of_n_bin)
        payload = n_bin[1:]
        return gamma_part + payload

    def _delta_decode_positive_from_stream(self, stream: str) -> tuple[int, int]:
        j = 0
        while stream[j] == '0':
            j += 1
        gamma_prefix_len = j
        gamma_len = 2 * gamma_prefix_len + 1
        gamma_code = stream[0:gamma_len]
        L = int(gamma_code[gamma_prefix_len:], 2)
        payload_len = L - 1
        payload_start = gamma_len
        payload_end = payload_start + payload_len
        payload = stream[payload_start:payload_end]
        positive_number_bin = '1' + payload
        positive_number = int(positive_number_bin, 2)
        consumed_len = payload_end
        return positive_number, consumed_len

    def encode(self, numbers: list[int]) -> bytearray:
        bit_stream_list = []
        for number in numbers:
            if number < 0:
                raise ValueError("n < 0, what do you expected?")
            if number == 0:
                bit_stream_list.append('11')
            elif number == 1:
                bit_stream_list.append('10')
            else:
                bit_stream_list.append(self._delta_encode_positive(number))
                # print(bit_stream_list) 
        bit_string = "".join(bit_stream_list)
        num_bits = len(bit_string)
        header = num_bits.to_bytes(8, 'big')
        padding_len = (8 - num_bits % 8) % 8
        padded_bit_string = bit_string + '0' * padding_len
        if len(padded_bit_string) == 0:
            data_bytes = b''
        else:
            int_array = [int(padded_bit_string[i:i+8], 2) for i in range(0, len(padded_bit_string), 8)]
            data_bytes = bytes(int_array)
        return bytearray(header + data_bytes)

    def decode(self, data: bytearray) -> list[int]:
        if len(data) < 8:
            return []
        header = data[:8]
        num_bits = int.from_bytes(header, 'big')
        data_bytes = data[8:]
        bit_string_list = [f'{byte:08b}' for byte in data_bytes]
        full_bit_string = "".join(bit_string_list)
        bit_string = full_bit_string[:num_bits]
        decoded_numbers = []
        current_pos = 0
        counter_poses = 0
        while current_pos < len(bit_string):
            if counter_poses < current_pos:
                counter_poses += 1000
                print(current_pos)
            if bit_string[current_pos:].startswith('11'):
                decoded_numbers.append(0)
                current_pos += 2
            elif bit_string[current_pos:].startswith('10'):
                decoded_numbers.append(1)
                current_pos += 2
            else:
                number, consumed = self._delta_decode_positive_from_stream(bit_string[current_pos:])
                decoded_numbers.append(number)
                current_pos += consumed
        return decoded_numbers

if __name__ == '__main__':
    coder = EliasDeltaNonNegativeCoder()

    data_to_encode = [1, 2, 3, 0, 15, 16, 99, 0, 1]
    print(f"data: {data_to_encode}")

    encoded_data = coder.encode(data_to_encode)
    print(f"coded: {encoded_data}")
    print(f"size: {len(encoded_data)} байт")


    decoded_data = coder.decode(encoded_data)
    print(f"decoded:  {decoded_data}")
    print(f"res: {data_to_encode == decoded_data}\n")

