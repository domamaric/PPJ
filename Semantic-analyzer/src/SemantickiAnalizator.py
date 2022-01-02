from sys import stdin
from collections import deque


class SemanticError(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return "err {} {}".format(self.token.ln_usage, self.token.value)


class Token:
    def __init__(self, ln_usage, ln_def, value):
        self.ln_usage = ln_usage
        self.ln_def = ln_def
        self.value = value

    def __str__(self):
        return "{} {} {}".format(self.ln_usage, self.ln_def, self.value)

    def __eq__(self, other):
        return isinstance(other, Token) and other.value == self.value


class Analyzer:
    def __init__(self, ast_str):
        self.tokens = []
        self.stack = deque()
        self.ast_str = ast_str
        self.cursor_index = 0
        self.cursor = ast_str[self.cursor_index]

    def analyse(self):
        while self.cursor is not None:
            if self.cursor == "<naredba_pridruzivanja>":
                self.operation_compound()
            elif self.cursor == "<za_petlja>":
                self.operation_loop()
            elif "IDN" in self.cursor:
                self.add_semantic_token()
            elif "az" in self.cursor:
                self.remove_from_stack()
            else:
                self.advance()

    def advance(self):
        if self.cursor_index + 1 < len(self.ast_str):
            self.cursor_index += 1
            self.cursor = self.ast_str[self.cursor_index]
        else:
            self.cursor_index = -1
            self.cursor = None

    def add_semantic_token(self):
        idn, ln_usage, idn_value = self.cursor.split()
        ln_def = self.find_def_on_stack(idn_value)

        if ln_def is not None and ln_def != ln_usage:
            self.tokens.append(Token(ln_usage, ln_def, idn_value))
        else:
            raise SemanticError(Token(ln_usage, ln_usage, idn_value))
        self.advance()

    def push_to_stack(self):
        const, ln_num, value = self.cursor.split()
        self.stack.append(Token(ln_num, ln_num, value))

    def pop_from_stack(self):
        return self.stack.pop()

    def remove_from_stack(self):
        while len(self.stack) > 0 and self.stack[-1].value != "za":
            self.pop_from_stack()

        self.pop_from_stack()
        self.advance()

    def find_def_on_stack(self, idn_value):
        for item in reversed(self.stack):
            if item.value == idn_value:
                return item.ln_def

        return None

    def operation_compound(self):
        self.advance()
        const, line_num, value = self.cursor.split()
        token = Token(line_num, line_num, value)
        token_present = False

        for item in reversed(self.stack):
            if item == token:
                token_present = True
                break

        if token_present:
            pass
        else:
            self.push_to_stack()
        self.advance()

    def operation_loop(self):
        self.advance()
        self.push_to_stack()
        self.advance()
        self.push_to_stack()
        self.advance()


def main():
    data = [x.strip() for x in stdin.readlines()]

    a = Analyzer(data)

    try:
        a.analyse()
        for token in a.tokens:
            print(token)
    except SemanticError as se:
        for token in a.tokens:
            print(token)
        print(se)
        return


if __name__ == "__main__":
    main()
