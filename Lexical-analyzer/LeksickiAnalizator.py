from sys import stdin


class Automata:
    """A finite state machine for text filters using regular expressions."""

    def __init__(self):
        """ Initialize automata start state and longest lexical token."""

        self.state = "S"
        self.curr_value = ""

    def simulate_automata(self, symbols, index, line_no):
        """Simulate the operation of finite state machine.

        FSM stops when confronts non alphanumeric symbol.

        :param str symbols: String of symbols
        :param int index: Position of 1st alphanumeric
        :param int line_no: Line number in program
        :returns : Position of first non alphanumeric
        """

        for c in symbols:
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
                    print("{} {} {}".format(DataTypes.IDENTIFIER, line_no,
                                            self.curr_value))
                    return index
            elif self.state == "KON":
                if c.isdigit():
                    self.curr_value += c
                else:
                    print("{} {} {}".format(DataTypes.NUMBER, line_no,
                                            self.curr_value))
                    return index
            index += 1
        if self.state == "IDN":
            print("{} {} {}".format(DataTypes.IDENTIFIER, line_no,
                                    self.curr_value))
        elif self.state == "KON":
            print("{} {} {}".format(DataTypes.NUMBER, line_no, self.curr_value))

        return index


class DataTypes:
    """Dataclass containing types of lexical tokens, operators, keywords, etc."""
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
    """Lexical analyzer or lexer scans the input and produces the matching tokens."""

    def __init__(self):
        self.line_no = -1

    def analyze_prog(self, lines):
        """Processes input program line by line.

        Furthermore, separates tuple on line number and line of code.

        :param list[tuple[int, str]] lines: List of line number and code
        :returns None:
        """

        for tpl in lines:
            self.line_no = tpl[0]
            line = tpl[1].split()

            if line:  # Line is empty, do nothing
                self.analyze_line(line)

    def analyze_line(self, line):
        """Processes input lines one token at time.

        If token is literal it's being procsesed by FSM.
        Otherwise, it's printed to stdin.

        :param list[str] line: List of lexical tokens
        :returns None:
        """

        for s in line:
            if s in DataTypes.KEYWORDS.keys():
                print("{} {} {}".format(DataTypes.KEYWORDS[s], self.line_no, s))
            else:
                i = 0
                while i < len(s):
                    if s[i] in DataTypes.OPERATORS.keys():
                        print("{} {} {}".format(DataTypes.OPERATORS[s[i]],
                                                self.line_no, s[i]))
                        i += 1
                    else:
                        temp = s[i:]
                        automata = Automata()
                        i = automata.simulate_automata(temp, i, self.line_no)

    @staticmethod
    def remove_comments(lines):
        """Removes comments from input program.

        :param list[str] lines: List of program file lines
        :returns: Pairs of program line index and code itself
        :rtype: list[tuple[int, str]]
        """

        commentless_prog = []
        for line in lines:
            try:
                ind_of_comm = line.index('//')  # Index of first comment symbol
                commentless_prog.append(line[:ind_of_comm])
            except ValueError:  # Line has no comments
                commentless_prog.append(line.rstrip())

        return list(enumerate(commentless_prog, 1))


def main():
    data = [x.strip() for x in stdin.readlines()]

    lex = Analyzer()
    comentless_data = lex.remove_comments(data)
    lex.analyze_prog(comentless_data)


if __name__ == '__main__':
    main()
