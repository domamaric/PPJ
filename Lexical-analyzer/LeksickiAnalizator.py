from sys import stdin


class Automata:
    @staticmethod
    def simulate_automata(str_of_sth, line_no):
        curr_state = "S"
        if curr_state == "S":
            print(str_of_sth, line_no)
        elif curr_state == "IDN":
            pass
        elif curr_state == "KON":
            pass


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
    def __init__(self, line_no=0, pos=-1):
        self.line_no = line_no
        self.pos = pos

    def analyze_lines(self, lines: list):
        # tpl -> tuple(int, str), pair of line number and instruction
        for tpl in lines:
            self.line_no = tpl[0]
            str_of_sth = "".join(tpl[1].split()) # Remove all the whitespace

            if not str_of_sth:  # Line is empty, do nothing
                continue
            # print("{} {}".format(self.line_no, str_of_sth))
            # Moram razbit words u leksicke jedinke
            Automata.simulate_automata(str_of_sth, self.line_no)


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
    # Run program: LeksickiAnalizator.py < primjer.in
    data = [x.strip() for x in stdin.readlines()]

    lex = Analyzer()
    data = lex.remove_comments(data)
    lex.analyze_lines(data)


if __name__ == '__main__':
    main()
