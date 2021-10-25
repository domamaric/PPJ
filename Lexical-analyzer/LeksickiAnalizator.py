from sys import stdin


class DataTypes:
    OPERATORS = {
        "=": "OP_PRIDRUZI",
        "+": "OP_PLUS",
        "-": "OP_MINUS",
        "*": "OP_PUTA",
        "/": "OP_DIJELI",
        "(": "L_ZAGRADA",
        ")": "D_ZAGRADA"
    }
    KEYWORDS = {
        "za": "KR_ZA",
        "od": "KR_OD",
        "do": "KR_DO",
        "az": "KR_AZ"
    }
    NUMBER = "BROJ"
    IDENTIFIER = "IDN"


class Analyzer:
    def __init__(self, line_no=0, instruction=[], word_type=str()):
        self.line_no = line_no
        self.instruction = instruction
        self.word_type = word_type

    def analyze_lines(self, lines: list):
        # tpl -> tuple(int, str), pair of line number and instruction
        for tpl in lines:
            self.line_no = tpl[0]
            self.instruction = tpl[1].split()

            if not self.instruction:  # Line is empty, do nothing
                continue

            for word in self.instruction:
                if not word.isdigit():
                    # Dakle nije broj, chars je lista slova
                    chars = list(word)
                    print("{} {}".format(self.line_no, chars), end="")
                    print()

    @staticmethod
    def remove_comments(lines: list):
        commentless_prog = []
        for line in lines:
            if line.startswith('//'):
                # Remove comments from the begging of line
                commentless_prog.append('')
            elif '//' in line:
                # Remove comment in the middle of line
                index = line.index('//')
                line = line[:index]
                commentless_prog.append(line)
            else:
                # No comments in line, append line
                commentless_prog.append(line)

        return list(enumerate(commentless_prog, 1))


def main():
    data = [x.strip() for x in stdin.readlines()]

    lex = Analyzer()
    data = lex.remove_comments(data)  # data[0] vraca tuple
    lex.analyze_lines(data)


if __name__ == '__main__':
    main()
