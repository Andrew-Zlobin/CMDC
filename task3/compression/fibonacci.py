import bisect

class FibonacciCoder:
    def __init__(self):
        self._fib_numbers = self._generate_fibs_to_limit()
    def _generate_fibs_to_limit(self, limit=2**64):
        fibs = []
        a, b = 1, 2
        while a < limit:
            fibs.append(a)
            a, b = b, a + b
        return fibs

    def encode(self, numbers: list[int]) -> bytearray:
        numbers = [n+1 for n in numbers]
        if not all(n > 0 for n in numbers):
            raise ValueError("Fibonacci coding is defined for positive integers only.")
        all_bits = []
        for n in numbers:
            if n == 0: continue
            temp_n = n
            idx = bisect.bisect_right(self._fib_numbers, temp_n) - 1
            representation_bits = [0] * (idx + 1)
            while temp_n > 0:
                fib_idx = bisect.bisect_right(self._fib_numbers, temp_n) - 1
                representation_bits[fib_idx] = 1
                temp_n -= self._fib_numbers[fib_idx]
            all_bits.extend(map(str, representation_bits))
            all_bits.append('1')
        bit_string = "".join(all_bits)
        padded_len = (len(bit_string) + 7) & ~7
        padded_string = bit_string.ljust(padded_len, '0')
        return bytearray(int(padded_string[i:i+8], 2) for i in range(0, len(padded_string), 8))

    def decode(self, data: bytearray) -> list[int]:
        if not data:
            return []
        bit_string = ''.join(f'{byte:08b}' for byte in data)
        decoded_numbers = []
        current_pos = 0
        while True:
            separator_idx = bit_string.find('11', current_pos)
            if separator_idx == -1:
                break

            representation_str = bit_string[current_pos : separator_idx + 1]
            num = 0
            for i, bit in enumerate(representation_str):
                if bit == '1':
                    num += self._fib_numbers[i]
            decoded_numbers.append(num-1)
            current_pos = separator_idx + 2
        return decoded_numbers


if __name__ == '__main__':
    coder = FibonacciCoder()

    original_list_1 = [0, 1, 2, 3, 5, 8, 13, 17, 1024]
    print(f"Original List 1: {original_list_1}")

    encoded_data_1 = coder.encode(original_list_1)
    print(f"Encoded Data 1 (bytearray): {encoded_data_1}")
    decoded_list_1 = coder.decode(encoded_data_1)
    print(f"Decoded List 1: {decoded_list_1}")
    assert original_list_1 == decoded_list_1
    original_list_2 = [1000, 10000, 10000000, 1000000]
    print(f"Original List 2: {original_list_2}")
    encoded_data_2 = coder.encode(original_list_2)
    print(f"Encoded Data 2 (bytes): {len(encoded_data_2)}")
    decoded_list_2 = coder.decode(encoded_data_2)
    print(f"Decoded List 2: {decoded_list_2}")
    assert original_list_2 == decoded_list_2
