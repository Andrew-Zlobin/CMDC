from collections import Counter

class BWT:
    @staticmethod
    def forward(line: str):
        cyclical_shifts = ["" for _ in range(len(line))]
        for cycle_idx in range(len(line)):
            cyclical_shifts[cycle_idx] = line[cycle_idx:] + line[:cycle_idx]
        cyclical_shifts.sort()
        last_col = ''.join([shift[-1] for shift in cyclical_shifts])
        return last_col, cyclical_shifts.index(line)

    @staticmethod
    def reverse(shuffled_line : str, k : int):
        count = dict(Counter(shuffled_line)) # надо отсортировать по ключам
        cumsum = 0
        for i in sorted(count.keys()):
            cumsum = cumsum + count[i]
            count[i] = cumsum - count[i]
        reverse_transition = list(range(len(shuffled_line)))
        for i in range(len(shuffled_line)):
            reverse_transition[count[shuffled_line[i]]] = i
            count[shuffled_line[i]] += 1
        j = reverse_transition[k]
        res = ["" for _ in range(len(shuffled_line))]
        for i in range(len(shuffled_line)):
            res[i] = shuffled_line[j]
            j = reverse_transition[j]
        return ''.join(res)

if __name__ == "__main__":
    test_cases = [("абракадабра", None),
                  ("БанБананана", None)]
    for test_case in test_cases:
        shuffled, k = BWT.forward(test_case[0])
        res = BWT.reverse(shuffled, k)
        print(test_case[0], shuffled, res, test_case[0] == res)
