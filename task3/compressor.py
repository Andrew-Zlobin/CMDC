import argparse
import os
import sys
from utils import file_management_on_decode, file_management_on_encode, BWT_DC_encode_pipeline, BWT_DC_decode_pipeline
from compression.elias import Elias
from compression import arithmetic
from compression import arithmeticcoding
from compression.fibonacci import FibonacciCoder
from compression import fibonacci
from compression import overflow
elias = Elias()
fibonacci = FibonacciCoder()

@file_management_on_encode
@BWT_DC_encode_pipeline
def encode_arithmetic(list_to_encode):
    return arithmetic.encode(list_to_encode)

@file_management_on_decode
@BWT_DC_decode_pipeline
def decode_arithmetic(text_to_decode):
    return arithmetic.decode(text_to_decode)

@file_management_on_encode
@BWT_DC_encode_pipeline
def encode_delta(list_to_encode):
    return elias.encode(list_to_encode)

@file_management_on_decode
@BWT_DC_decode_pipeline
def decode_delta(text_to_decode):
    return elias.decode(text_to_decode)

@file_management_on_encode
@BWT_DC_encode_pipeline
def overflow_encode(list_to_encode):
    return overflow.encode(list_to_encode)

@file_management_on_decode
@BWT_DC_decode_pipeline
def overflow_decode(text_to_decode):
    return overflow.decode(text_to_decode)

@file_management_on_encode
@BWT_DC_encode_pipeline
def fibonacci_encode(list_to_encode):
    return fibonacci.encode(list_to_encode)

@file_management_on_decode
@BWT_DC_decode_pipeline
def fibonacci_decode(text_to_decode):
    return fibonacci.decode(text_to_decode)


def parse_args():
    parser = argparse.ArgumentParser(
        description="CLI архиватор с поддержкой различных методов кодирования.",
        usage=(
            "архиватор.py [-h] [-f OUTPUT] (-g | -d | -o) input_file\n\n"
            "Форматы:\n"
            "  .txt -> кодирование\n"
            "  .compressed -> декодирование"
        )
    )

    parser.add_argument("input_file", help="Путь к входному файлу (.txt или .compressed)")
    parser.add_argument("-f", "--file", default="default.compressed", help="Выходной файл")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--arithmetic", action="store_true", help="Использовать арифметическое кодирование")
    group.add_argument("-d", "--delta", action="store_true", help="Использовать дельта-кодирование")
    group.add_argument("-o", "--overflow", action="store_true", help="Использовать overflow-кодирование")
    group.add_argument("-i", "--fibonacci", action="store_true", help="Использовать кодирование фибоначчи")

    return parser.parse_args()

def main():
    args = parse_args()

    input_path = args.input_file
    output_path = args.file
    ext = os.path.splitext(input_path)[1]

    is_encoding = ext == ".txt"
    is_decoding = ext == ".compressed"

    if not is_encoding and not is_decoding:
        print("Ошибка: допустимы только входные файлы с расширением .txt или .compressed")
        sys.exit(1)

    if args.arithmetic:
        if is_encoding:
            encode_arithmetic(input_path, output_path)
        else:
            decode_arithmetic(input_path, output_path)
    elif args.delta:
        if is_encoding:
            encode_delta(input_path, output_path)
        else:
            decode_delta(input_path, output_path)
    elif args.overflow:
        if is_encoding:
            overflow_encode(input_path, output_path)
        else:
            overflow_decode(input_path, output_path)
    elif args.fibonacci:
        if is_encoding:
            fibonacci_encode(input_path, output_path)
        else:
            fibonacci_decode(input_path, output_path)
    else:
        print("Ошибка: необходимо выбрать один из режимов (-a, -d, -o, -i)")
        sys.exit(1)

if __name__ == "__main__":
    main()

