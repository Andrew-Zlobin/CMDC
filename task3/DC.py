# import traceback
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

class DC:
    @staticmethod
    def code(bwt_string : str, alphabet : str, char_spacing: list):
        x = alphabet + bwt_string
        n = len(x)
        is_known = [False] * n
        for i in range(len(alphabet)):
            is_known[i] = True

        encoded_output = []
        num_known_symbols = len(alphabet)

        i = 0
        while num_known_symbols < n:
            if not is_known[i]:
                i += 1
                continue

            if i + 1 < n and not is_known[i + 1]:
                is_known[i + 1] = True
                num_known_symbols += 1
            else:
                next_occurrence_spacing = char_spacing[i]
                unknown_count = next_occurrence_spacing - sum(is_known[i+1: i+next_occurrence_spacing+1])
                if next_occurrence_spacing != 0:
                    encoded_output.append(unknown_count)
                    if not is_known[i + next_occurrence_spacing]:
                        is_known[i + next_occurrence_spacing] = True
                        num_known_symbols += 1
                else:
                    encoded_output.append(0)

            i += 1
            if i >= n:
                i = 0

        return encoded_output
    @staticmethod
    def decode(encoded_stream, alphabet, bwt_length):
        alphabet_size = len(alphabet)
        total_length = alphabet_size + bwt_length
        UNKNOWN = None
        X = list(alphabet) + [UNKNOWN] * bwt_length
        stream_iter = iter(encoded_stream)
        for i in range(total_length):
            is_run_ahead = (i + 1 < total_length) and (X[i+1] is UNKNOWN)
            if is_run_ahead:
                X[i+1] = X[i]
            else:
                d = next(stream_iter, None)

                if d is None:
                    break

                if d > 0:
                    unknown_count = 0
                    for j in range(i + 1, total_length):
                        if X[j] is UNKNOWN:
                            unknown_count += 1
                            if unknown_count == d:
                                X[j] = X[i]
                                break
        bwt_part = X[alphabet_size:]
        if UNKNOWN in bwt_part:
            raise ValueError("Декодирование завершено, но остались неизвестные символы. Поток был неполным.")
        
        return "".join(bwt_part)


if __name__ == "__main__":
    test_cases = [(("а#ннБннБаааа", "#Бан"), [2, 4, 1, 1, 5, 0, 1, 2, 0, 0])]
    for test_case in test_cases:
        if test_case[1] != None:
            BWT.build_char_spacing(test_case[0][1] + test_case[0][0])
            # print(list(test_case[0][1] + test_case[0][0]))
            # print(BWT.get_char_spacing())
            print("code :", DC.code(test_case[0][0], test_case[0][1], BWT.get_char_spacing()) == test_case[1])
            # print(test_case[1], DC.code(test_case[0][0], test_case[0][1], BWT.get_char_spacing()))
            # print("decode :", DC.decode( DC.code(test_case[0][0], test_case[0][1]), test_case[0][1], len(test_case[0][0])) == test_case[0][0])
