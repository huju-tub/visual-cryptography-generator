class TextParser:
    def __init__(self, input_string="", input_text=""):
        self.input_string = input_string
        self.input_text = input_text

    def replace_symbols_with_space(self, symbols):
        if not self.input_string:
            print(self.input_text)
            while True:
                line = input()
                if line.strip() == '--':  # Sentinel value to stop input
                    break
                self.input_string += line + '\n'

        replaced_string = self.input_string
        for symbol in symbols:
            replaced_string = replaced_string.replace(symbol, ' ')
        return replaced_string
