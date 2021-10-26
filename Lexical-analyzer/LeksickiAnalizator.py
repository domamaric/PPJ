from sys import stdin


class Automata:
    def __init__(self):
        self.state = "S"
        self.curr_value = ""

    def simulate_automata(self, str_of_sth, index, line_no):
        for c in str_of_sth:
            if self.state == "S":
                if c.isdigit():
                    self.state = "KON"
                else:
                    self.state = "IDN"
                self.curr_value += c
            elif self.state == "IDN":
                if c.isalnum():
                    self.curr_value += c
                else:
                    print("{} {} {}".format(DataTypes.IDENTIFIER, line_no, self.curr_value))
                    return index
            elif self.state == "KON":
                if c.isdigit():
                    self.curr_value += c
                else:
                    print("{} {} {}".format(DataTypes.NUMBER, line_no, self.curr_value))
                    return index
            index += 1
        if self.state == "IDN":
            print("{} {} {}".format(DataTypes.IDENTIFIER, line_no, self.curr_value))
        elif self.state == "KON":
            print("{} {} {}".format(DataTypes.NUMBER, line_no, self.curr_value))

        return index


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
    def __init__(self):
        self.line_no = -1

    def analyze_prog(self, lines: list):
        # tpl -> tuple(int, str), pair of line number and instruction
        for tpl in lines:
            self.line_no = tpl[0]
            line = tpl[1].split()

            if line:  # Line is empty, do nothing
                self.analyze_line(line)

    def analyze_line(self, line):
        for s in line:
            if s in DataTypes.KEYWORDS.keys():
                print("{} {} {}".format(DataTypes.KEYWORDS[s], self.line_no, s))
            else:
                i = 0
                while i < len(s):
                    if s[i] in DataTypes.OPERATORS.keys():
                        print("{} {} {}".format(DataTypes.OPERATORS[s[i]], self.line_no, s[i]))
                        i += 1
                    else:
                        temp = s[i:]
                        # print(temp)
                        automata = Automata()
                        i = automata.simulate_automata(temp,i, self.line_no)

    @staticmethod
    def remove_comments(lines: list):
        commentless_prog = []
        for line in lines:
            try:
                ind_of_comm = line.index('//') # Ako postoji ostat će ovde
                commentless_prog.append(line[:ind_of_comm])
            except ValueError: # Dakle nema comentara u liniji
                commentless_prog.append(line.rstrip())

        return list(enumerate(commentless_prog, 1))


def main():
    # Run program: LeksickiAnalizator.py < primjer.in
    data = [x.strip() for x in stdin.readlines()]

    lex = Analyzer()
    data = lex.remove_comments(data)
    lex.analyze_prog(data)


if __name__ == '__main__':
    main()
