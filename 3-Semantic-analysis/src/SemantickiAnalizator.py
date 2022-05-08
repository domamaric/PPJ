from collections import deque
from sys import stdin


class SemanticError(Exception):
    """ Custom exception class for Semantic analysis error. """

    def __init__(self, token):
        """ Initialize token to be printed on as stderr.

        :param Token token: Token class instance.
        :returns None:
        """

        self.token = token

    def __str__(self):
        """ Represents Semantic analysis error in specific format:

        err <line_number> <value>
        """

        return "err {} {}".format(self.token.ln_usage, self.token.value)


class Token:
    """ Semantic token dataclass."""

    def __init__(self, ln_usage, ln_def, value):
        """ Initialize token.

        :param str ln_usage: Specifies line in which token is being used.
        :param str ln_def: Specifies line in which variable is being definied.
        :param str value: Token value.
        :returns None:
        """

        self.ln_usage = ln_usage
        self.ln_def = ln_def
        self.value = value

    def __str__(self):
        """ Represents token in specific format:

        <line_usage> <line_definition> <token_value>
        """

        return "{} {} {}".format(self.ln_usage, self.ln_def, self.value)

    def __eq__(self, other):
        """ Checks whether two tokens are equal.

        :param Token other: The token with which we compare.
        :returns bool:
        """

        return isinstance(other, Token) and other.value == self.value


class Analyzer:
    """ Semantic analyzer class for 'PJ' language. """

    def __init__(self, ast_str):
        """ Sets analyzer to inital state.

        :param list[str] ast_str: Nodes of Syntax tree represented by list.
        :returns None:
        """

        self.tokens = []
        self.stack = deque()
        self.ast_str = ast_str
        self.length = len(self.ast_str)
        self.cursor_index = 0
        self.cursor = ast_str[self.cursor_index]

    def analyse(self):
        """ Perform syntax analysis of program.

        Iterates over Syntax tree and calls appropriate funcions on each encounter.
        """

        while self.cursor is not None:
            if self.cursor == "<naredba_pridruzivanja>":
                self.compund_operation()
            elif self.cursor == "<za_petlja>":
                self.loop_operation()
            elif "IDN" in self.cursor:
                self.add_token()
            elif "az" in self.cursor:
                self.remove_from_stack()
            self.advance()

    def advance(self):
        """ Advance on other nodes of Syntax tree. """

        if self.cursor_index + 1 < self.length:
            self.cursor_index += 1
            self.cursor = self.ast_str[self.cursor_index]
        else:
            self.cursor_index = -1
            self.cursor = None

    def compund_operation(self):
        """ Saves variable definition on context stack.

        If variable is already defined in same scope, keep the original declaration.
        """

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

    def loop_operation(self):
        """ Save new scope to stack and following variable. """

        self.advance()
        self.push_to_stack()
        self.advance()
        self.push_to_stack()
        self.advance()

    def add_token(self):
        """ Record usage of existing identifier in semantic token set.

        Creates semantic Token from current cursor line.
        """

        idn, ln_usage, idn_value = self.cursor.split()
        ln_def = self.find_def_on_stack(idn_value)

        if ln_def is not None and ln_def != ln_usage:
            self.tokens.append(Token(ln_usage, ln_def, idn_value))
        else:
            raise SemanticError(Token(ln_usage, ln_usage, idn_value))
        self.advance()

    def remove_from_stack(self):
        """ Remove all variables defined in specific loop scope.

        Those are all variables saved on stack between KR_ZA and KR_AZ keywords.
        """

        while self.stack and self.stack[-1].value != "za":
            self.pop_from_stack()

        self.pop_from_stack()
        self.advance()

    def push_to_stack(self):
        """ Create new Token from current cursor line and push it to stack. """

        const, ln_num, value = self.cursor.split()
        self.stack.append(Token(ln_num, ln_num, value))

    def pop_from_stack(self):
        """ Remove the latest added Token from stack.

        :returns: Token from top of stack.
        """
        return self.stack.pop()

    def find_def_on_stack(self, idn_value):
        """ Check whether current variable being used is properly defined.

        Chek if variable is saved on context stack.

        :param str idn_value: Currently used variable value.
        :return: Line on which variable was defined. If variable doesn't exist returns None.
        """
        for item in reversed(self.stack):
            if item.value == idn_value:
                return item.ln_def

        return None


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
