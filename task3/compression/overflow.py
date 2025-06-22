def overflow_encode_one(number):
    # print(number)
    if 0 <= number <= 254:
        return number.to_bytes(1, byteorder='big')
    elif 255 <= number <= 65789:
        encoded_value = (number - 255).to_bytes(2, byteorder='big')
        return b'\xff' + encoded_value
    elif number >= 65790:
        encoded_value = (number - 65790).to_bytes(4, byteorder='big')
        return b'\xff\xff\xff' + encoded_value
    else:
        raise ValueError("Number out of supported range for overflow coding (non-negative).")

def encode(number_list):
    encoded_data = bytearray()
    for num in number_list:
        encoded_data.extend(overflow_encode_one(num))
    return encoded_data

def decode(encoded_bytes):
    decoded_numbers = []
    i = 0
    while i < len(encoded_bytes):
        current_byte = encoded_bytes[i]

        if current_byte != 0xFF:
            decoded_numbers.append(current_byte)
            i += 1
        else:
            if i + 2 <= len(encoded_bytes):
                next_two_bytes_val = int.from_bytes(encoded_bytes[i+1:i+3], byteorder='big')
                if next_two_bytes_val + 255 == 65790:
                    if i + 4 <= len(encoded_bytes):
                        if encoded_bytes[i] == 0xFF and encoded_bytes[i+1] == 0xFF and encoded_bytes[i+2] == 0xFF:
                            value_part = int.from_bytes(encoded_bytes[i+3:i+7], byteorder='big')
                            decoded_numbers.append(65790 + value_part)
                            i += 7
                        else:
                            decoded_numbers.append(255 + next_two_bytes_val)
                            i += 3
                    else:
                        decoded_numbers.append(255 + next_two_bytes_val)
                        i += 3
                else:
                    decoded_numbers.append(255 + next_two_bytes_val)
                    i += 3
            else:
                raise ValueError("Incomplete encoded data.")
    return decoded_numbers
if __name__ == "__main__":
    numbers_to_encode = [100, 254, 255, 1000, 65789, 1234567890, 65790, 70000, 150]

    encoded_data = encode(numbers_to_encode)
    print(f"Original numbers: {numbers_to_encode}, size: {len(numbers_to_encode) * 4} bytes")
    print(f"Encoded data (hex): {encoded_data.hex()}, size : {len(encoded_data)} bytes")

    decoded_numbers = decode(encoded_data)
    print(f"Decoded numbers: {decoded_numbers}")
