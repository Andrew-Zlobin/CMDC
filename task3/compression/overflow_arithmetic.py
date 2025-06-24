# import overflow
# import arithmetic
from . import arithmetic
from . import overflow

def encode(data_to_encode : list[int]) -> bytearray:
    data_after_overflow = overflow.encode(data_to_encode)
    return arithmetic.encode(list(data_after_overflow))

def decode(array : bytearray) -> list[int]:
    data_before_overflow = arithmetic.decode(array)
    return overflow.decode(bytearray(data_before_overflow))

if __name__ == "__main__":
    data = [1, 2, 3, 5, 983, 238, 27386876, 4589, 2, 0, 1] #[1,2,3,4,5]
    encoded = encode(data)
    decoded = decode(encoded)
    print(data == decoded)
