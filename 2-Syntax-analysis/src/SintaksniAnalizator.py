from collections import deque
from sys import stdin


class SA:
    """  A Syntax analyzer transforms a token stream (from the Lexical analyzer)
     into a Syntax tree, based on a grammar. """

    def __init__(self):
        """ Initialize analyzer grammar, syntax tree, etc."""

        self.gramatika = {
            '<program>': [(['<lista_naredbi>'], ['IDN', 'KR_ZA', 'endIn'])],
            '<lista_naredbi>': [
                (['<naredba>', '<lista_naredbi>'], ['IDN', 'KR_ZA']),
                (['$'], ['KR_AZ', 'endIn'])],
            '<naredba>': [(['<naredba_pridruzivanja>'], ['IDN']),
                          (['<za_petlja>'], ['KR_ZA'])],
            '<naredba_pridruzivanja>': [
                (['IDN', 'OP_PRIDRUZI', '<E>'], ['IDN'])],
            '<za_petlja>': [(['KR_ZA', 'IDN', 'KR_OD', '<E>', 'KR_DO', '<E>',
                              '<lista_naredbi>', 'KR_AZ'], ['KR_ZA'])],
            '<E>': [(['<T>', '<E_lista>'],
                     ['IDN', 'BROJ', 'OP_PLUS', 'OP_MINUS', 'L_ZAGRADA'])],
            '<E_lista>': [(['OP_PLUS', '<E>'], ['OP_PLUS']),
                          (['OP_MINUS', '<E>'], ['OP_MINUS']), (['$'],
                                                                ['IDN', 'KR_ZA',
                                                                 'KR_DO',
                                                                 'KR_AZ',
                                                                 'D_ZAGRADA',
                                                                 'endIn'])],
            '<T>': [(['<P>', '<T_lista>'],
                     ['IDN', 'BROJ', 'OP_PLUS', 'OP_MINUS', 'L_ZAGRADA'])],
            '<T_lista>': [(['OP_PUTA', '<T>'], ['OP_PUTA']),
                          (['OP_DIJELI', '<T>'], ['OP_DIJELI']), (['$'], ['IDN',
                                                                          'KR_ZA',
                                                                          'KR_DO',
                                                                          'KR_AZ',
                                                                          'OP_PLUS',
                                                                          'OP_MINUS',
                                                                          'D_ZAGRADA',
                                                                          'endIn'])],
            '<P>': [(['OP_PLUS', '<P>'], ['OP_PLUS']),
                    (['OP_MINUS', '<P>'], ['OP_MINUS']),
                    (['L_ZAGRADA', '<E>', 'D_ZAGRADA'], ['L_ZAGRADA']),
                    (['IDN'], ['IDN']), (['BROJ'], ['BROJ'])]
        }
        self.primjeni = {}
        self.tablica = {}
        self.stog = deque()
        self.stogLinija = deque()
        self.ulaz = []
        self.genStablo = []
        self.genStabloRazmak = []
        self.kraj = 0
        self.linija = 0
        self.ispis = ''
        self.lZagrada = []
        self.za = []
        self.od = []

    def zamijeni(self, lijevo, desno, primjeni):
        x = self.stog.pop()
        self.linija = self.stogLinija.pop()
        self.genStablo.append(x)
        self.genStabloRazmak.append(self.linija)
        for zn in reversed(desno):
            self.stog.append(zn)
            self.stogLinija.append(self.linija + 1)

    def pomakni(self, lijevo, desno, primjeni):
        simb = " ".join((self.ulaz[0][0], self.ulaz[0][1], self.ulaz[0][2]))
        if self.ulaz[0][0] == "L_ZAGRADA":
            self.lZagrada.append(self.linija)
        elif self.ulaz[0][0] == "KR_ZA":
            self.za.append(self.linija)
        elif self.ulaz[0][0] == "KR_OD":
            self.od.append(self.linija)
        elif self.ulaz[0][0] == "D_ZAGRADA":
            self.linija = self.lZagrada.pop()
        elif self.ulaz[0][0] == "KR_AZ":
            self.linija = self.za.pop()
        elif self.ulaz[0][0] == "KR_DO":
            self.linija = self.od.pop()
        self.genStablo.append(simb)
        self.genStabloRazmak.append(self.linija + 1)
        self.ulaz = self.ulaz[1:]

    def izvuci(self, lijevo, desno, primjeni):
        li = self.stogLinija.pop()
        x = self.stog.pop()
        if not x == self.ulaz[0][0]:
            self.linija = li
            self.genStablo.append(x)
            self.genStabloRazmak.append(self.linija)

    def izvuci_e(self, lijevo, desno, primjeni):
        """ Removes epsilon transition from stack. """
        x = self.stog.pop()
        self.linija = self.stogLinija.pop()
        self.genStablo.append(x)
        self.genStabloRazmak.append(self.linija)
        self.genStablo.append('$')
        self.genStabloRazmak.append(self.linija + 1)

    def zadrzi(self, lijevo, desno, primjeni):
        """ For now do nothing. """
        pass

    def prihvati(self, lijevo, desno, primjeni):
        """ Accepts final state of automata. """
        self.kraj = 1

    def obradi_epsilon(self, lijevo, desno, primjeni):
        for el in primjeni:
            self.tablica[(lijevo, el)] = (
                (self.izvuci_e, lijevo, desno, primjeni),
                (self.zadrzi, lijevo, desno, primjeni))

    def obradi_nezavrsni(self, lijevo, desno, primjeni):
        for el in primjeni:
            self.tablica[(lijevo, el)] = (
                (self.zamijeni, lijevo, desno, primjeni),
                (self.zadrzi, lijevo, desno, primjeni))

    def obradi_zavrsni(self, lijevo, desno, primjeni):
        """ Process final symbol.

        :param str lijevo: Left element of grammar.
        :param str desno: Rightmost element of grammar.
        :param function primjeni: Function to apply to elements.
        :returns None:
        """
        if len(desno) <= 1:
            self.tablica[(lijevo, desno[0])] = (
                (self.izvuci, lijevo, desno[1:], primjeni),
                (self.pomakni, lijevo, desno, primjeni))
        else:
            self.tablica[(lijevo, desno[0])] = (
                (self.zamijeni, lijevo, desno[1:], primjeni),
                (self.pomakni, lijevo, desno, primjeni))


class Parser(SA):
    """ A 'PJ' langugae parser implementation. """
    def __init__(self):
        super().__init__()

    def parsiraj(self):
        """ Prints abstract syntax tree to stdin.

        :returns None:
        """
        while self.kraj == 0:
            if self.stog:
                stanje = self.stog[-1]
            else:
                stanje = "empty"
            if self.ulaz:
                ulazniniz = self.ulaz[0]
                znak = ulazniniz[0]
            else:
                znak = "endIn"
            if (stanje, znak) in self.tablica:
                funkcije = self.tablica[(stanje, znak)]
                for par in funkcije:
                    par[0](par[1], par[2], par[3])
            else:
                if znak == "endIn":
                    self.ispis = "err kraj\n"
                else:
                    s = " ".join(
                        (self.ulaz[0][0], self.ulaz[0][1], self.ulaz[0][2]))
                    self.ispis = "err " + s + "\n"
                self.kraj = 2
                break


def main():
    s = Parser()

    data = [x.strip() for x in stdin.readlines()]
    for d in data:
        s.ulaz.append(d.split())

    for lijevo in s.gramatika:
        for produkcija in s.gramatika[lijevo]:
            desno = produkcija[0]
            primjeni = produkcija[1]

            b = desno[0]
            if b == '$':
                s.obradi_epsilon(lijevo, desno, primjeni)
            elif b[0] == '<':
                s.obradi_nezavrsni(lijevo, desno, primjeni)
            else:
                s.obradi_zavrsni(lijevo, desno, primjeni)

    znakovistoga = ["KR_OD", "KR_DO", "KR_AZ", "D_ZAGRADA", "OP_PRIDRUZI",
                    "IDN"]
    for znak in znakovistoga:
        s.tablica[(znak, znak)] = (
            (s.izvuci, lijevo, desno, primjeni),
            (s.pomakni, lijevo, desno, primjeni))

    s.tablica[("empty", "endIn")] = (
        (s.prihvati, lijevo, desno, primjeni),
        (s.prihvati, lijevo, desno, primjeni)
    )

    s.stog.append("<program>")
    s.stogLinija.append(s.linija)
    s.parsiraj()

    if not s.kraj == 2:
        for i in range(0, len(s.genStablo)):
            pr = ""
            for j in range(0, s.genStabloRazmak[i]):
                pr += " "
            pr += s.genStablo[i]
            s.ispis += pr + "\n"

    s.ispis = s.ispis[:-1]
    print(s.ispis)


if __name__ == "__main__":
    main()
