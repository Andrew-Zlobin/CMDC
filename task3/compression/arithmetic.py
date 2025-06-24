import io
#import arithmeticcoding
from . import arithmeticcoding
import struct

def encode(source_message: list, N=32) -> bytearray:
    alphabet = sorted(list(set(source_message)))
    symbol_map = {symbol: i for i, symbol in enumerate(alphabet)}
    source_message = [symbol_map[s] for s in source_message]
    max_symbol = max(source_message) if source_message else -1

    init_freqs = arithmeticcoding.FlatFrequencyTable(max_symbol + 1)    
    freqs = arithmeticcoding.SimpleFrequencyTable(init_freqs)

    buffer = io.BytesIO()
    bitout = arithmeticcoding.BitOutputStream(buffer)
    enc = arithmeticcoding.ArithmeticEncoder(N, bitout)

    for symbol in source_message:
        enc.write(freqs, symbol)
        freqs.increment(symbol)

    enc.finish()
    while bitout.numbitsfilled != 0:
        bitout.write(0)
    compressed_bytes = buffer.getvalue()
    buffer.close()
    buffer = bytearray()
    buffer += struct.pack('II', len(source_message), len(alphabet))
    for number in alphabet:
        buffer += struct.pack('Q', number)
    return buffer + bytearray(compressed_bytes)



def decode(encoded_sequence: bytearray, N = 32)-> list:
    offset = 0
    message_len, alphabet_size = struct.unpack_from('II', encoded_sequence, offset)
    offset += 8
    alphabet = []
    for _ in range(alphabet_size):
        number = struct.unpack_from('Q', encoded_sequence, offset)[0]
        alphabet.append(number)
        offset += 8
    encoded_sequence = encoded_sequence[offset:]
    compressed_bytes = bytes(encoded_sequence)
    init_freqs = arithmeticcoding.FlatFrequencyTable(alphabet_size)

    freqs = arithmeticcoding.SimpleFrequencyTable(init_freqs)

    decoded_message = []
    buffer = io.BytesIO(compressed_bytes)
    bitin = arithmeticcoding.BitInputStream(buffer)
    dec = arithmeticcoding.ArithmeticDecoder(N, bitin)

    for _ in range(message_len):
        symbol = dec.read(freqs)
        decoded_message.append(symbol)
        freqs.increment(symbol)

    bitin.close()
    decoded_message = [alphabet[i] for i in decoded_message]
    return decoded_message

if __name__ == "__main__":
    data = [1, 2, 3, 5, 983, 238, 27386876, 4589, 2, 0, 1] #[1,2,3,4,5]
    encoded = encode(data)
    decoded = decode(encoded)
    print(data == decoded)
