from tqdm import tqdm
from pydivsufsort import divsufsort

def get_suffix_array(text: str) -> list[int]:
    # indices = list(range(len(text)))
    # indices.sort(key=lambda i: text[i:])
    # return indices
    return divsufsort(text)

def bwt(text: str) -> str:
    EOF_CHAR = '\x01'
    if EOF_CHAR in text:
        raise ValueError("EOF ('\\x01') in text")

    text_with_eof = text + EOF_CHAR
    n = len(text_with_eof)

    suffix_array = get_suffix_array(text_with_eof)
    # print("built suffix array")
    bwt_chars = []
    for i in tqdm(range(n)):
        suffix_start_index = suffix_array[i]
        bwt_char = text_with_eof[suffix_start_index - 1]
        bwt_chars.append(bwt_char)
    # print(EOF_CHAR in bwt_chars)
    # print(EOF_CHAR in "".join(bwt_chars), bwt_chars.index(EOF_CHAR))
    return "".join(bwt_chars)

def ibwt(bwt_text: str) -> str:
    # print()
    EOF_CHAR = '\x01'
    n = len(bwt_text)
    if EOF_CHAR not in bwt_text:
        raise ValueError("EOF ('\\x01')not in text")

    l_col_indexed = [(bwt_text[i], i) for i in range(n)]

    f_col_indexed = sorted(l_col_indexed, key=lambda x: x[0])

    transformation_vector = [0] * n
    for i in range(n):
        transformation_vector[i] = f_col_indexed[i][1]

    current_index = bwt_text.find(EOF_CHAR)
    original_chars = []
    for _ in range(n):
        current_index = transformation_vector[current_index]
        original_chars.append(bwt_text[current_index])
    return "".join(original_chars).rstrip(EOF_CHAR)

class BWT:
    __char_spacing = None
    @staticmethod
    def build_char_spacing(text : str):
        spacing_counters = {symb : 0 for symb in set(text)}
        char_spacing = [0 for _ in range(len(text))]
        for i in range(len(text) - 1, -1, -1):
            if spacing_counters[text[i]] != 0:
                char_spacing[i] = spacing_counters[text[i]] - i
                spacing_counters[text[i]] = i
            else:
                spacing_counters[text[i]] = i
        BWT.__char_spacing = char_spacing
    @staticmethod
    def get_char_spacing():
        return BWT.__char_spacing

    @staticmethod
    def forward(line: str):
        BWT.build_char_spacing("".join(sorted(list(set(line)))) + line)
        # print("really start bwt")
        return bwt(line)

    @staticmethod
    def reverse(shuffled_line : str):
       return ibwt(shuffled_line)

if __name__ == "__main__":
    # test_cases = [("абракадабра", None),
    #               ("БанБананана", None)]
    test_cases = [("abracadabra", None)]
    for test_case in test_cases:
        shuffled = BWT.forward(test_case[0])
        res = BWT.reverse(shuffled)
        print(test_case[0], shuffled, res, test_case[0] == res)
