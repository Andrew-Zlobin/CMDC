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
        BWT.__char_spacing = spacing_counters
    @staticmethod
    def get_char_spacing():
        return BWT.__char_spacing

class DC:
    def code(text):
        

    def decode(text):
        pass
