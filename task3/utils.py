from BWT import BWT
from DC import DC
import struct
def alphabet_to_number(alphabet):
    bitmask = [0] * 256
    for char in alphabet:
        bitmask[ord(char)] = 1
    # print("alphabet bitmask :", bitmask)
    # print("alphabet :", alphabet)
    # print("alphabet :", list(alphabet))
    bit_string = ''.join(str(b) for b in bitmask)
    return int(bit_string, 2)


def number_to_alphabet(number):
    bit_string = f"{number:0256b}"
    alphabet = [chr(i) for i, bit in enumerate(bit_string) if bit == '1']
    # print(bit_string)
    # print("alphabet:", ''.join(alphabet))
    # print("alphabet :", alphabet)
    # print('\x01' in alphabet)
    return alphabet


def file_management_on_encode(func):
    def handler(input_path, output_path):
        text = None
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()
        if not text:
            raise FileNotFoundError
        res = func(text)
        with open(output_path, "wb") as file:
            file.write(res)
    return handler

def file_management_on_decode(func):
    def handler(input_path, output_path):
        text = None
        with open(input_path, 'rb') as file:
            text = bytearray(file.read())
        if not text:
            raise FileNotFoundError
        res = func(text)
        with open(output_path, "w") as file:
            file.write(res)
    return handler

def BWT_DC_encode_pipeline(func):
    def handler(text):
        bwt_text = BWT.forward(text)
        alphabet = "".join(sorted(list(set(text))))
        int_alphabet = alphabet_to_number(alphabet)
        # print(int_alphabet)
        dc_text = DC.code(bwt_text, alphabet, BWT.get_char_spacing())
        text_len = len(bwt_text)
        array_to_encode = [text_len] + dc_text
        # num_bytes = struct.pack('>I', int_alphabet)
        num_bytes = int_alphabet.to_bytes(32, byteorder='big')
        return bytearray(num_bytes) + func(array_to_encode)
    return handler

def BWT_DC_decode_pipeline(func):
    def handler(coded_text):
        int_alphabet = int.from_bytes(coded_text[:32], byteorder='big')
        coded_text = coded_text[32:]
        array_to_encode = func(coded_text)
        # int_alphabet = array_to_encode[0]
        text_len = array_to_encode[0]
        dc_text = array_to_encode[1:]
        alphabet = number_to_alphabet(int_alphabet)
        dc_decoded = DC.decode(dc_text, alphabet, text_len)
        return dc_decoded[:len(dc_decoded) - 1]
    return handler
