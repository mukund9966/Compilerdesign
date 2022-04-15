import pandas as pd


class FF:

    def __init__(self, CFG: dict(), terminals: set(), nonTerminals: set(), startSymbol):

        self.CFG = CFG
        self.terminals = terminals
        self.nonTerminals = nonTerminals
        self.startSymbol = startSymbol
        self.table = dict()

    def calcFirst(self):
        calculated = set()
        first = dict()

        for nonTerminal in self.nonTerminals:
            self._first(nonTerminal, calculated, first)

        self.table["First"] = first

    def _first(self, nonTerminal, calculated, first):

        if nonTerminal in calculated:
            return
        else:
            calculated.add(nonTerminal)

        productions = self.CFG.get(nonTerminal, None)
        first[nonTerminal] = set()

        if productions is None:
            return
        else:
            for production in productions:
                f = set()
                curr = ""

                for char in production:
                    curr += char

                    if '@' in f:
                        f.remove('@')

                    if curr in self.nonTerminals:
                        if first.get(curr, None) is not None:
                            f.update(first.get(curr))
                        else:
                            self._first(curr, calculated, first)
                            f.update(first.get(curr))

                        curr = ""
                        if '@' in f:
                            continue
                        else:
                            break

                    elif curr in self.terminals:
                        f.add(curr)
                        curr = ""
                        break
                    elif char == '@':
                        f.add('@')

                first[nonTerminal].update(f)

    def calcFollow(self):
        calculated = set()
        follow = dict()

        for nonTerminal in self.nonTerminals:
            self._follow(nonTerminal, calculated, follow)

        self.table["Follow"] = follow

    def _follow(self, nonTerminal, calculated, follow):

        if nonTerminal in calculated:
            return
        else:
            calculated.add(nonTerminal)

        follow[nonTerminal] = set()
        if nonTerminal is self.startSymbol:
            follow[nonTerminal].add('$')

        for symbol in self.CFG:

            productions = self.CFG.get(symbol)

            for production in productions:
                curr = ""
                f = set()
                for index, char in enumerate(production):
                    curr += char

                    if curr == nonTerminal:
                        followString = production[index + 1:]

                        if followString == "":
                            if nonTerminal is symbol:
                                # A -> aA
                                # This condition will give Follow(A) = Follow(A)
                                # Ignore this case
                                pass
                            else:
                                if symbol not in calculated:
                                    self._follow(symbol, calculated, follow)
                                f.update(follow.get(symbol))
                        else:
                            currSymbol = ""
                            for c in followString:
                                currSymbol += c

                                if '@' in f:
                                    f.remove('@')

                                if currSymbol in self.nonTerminals:

                                    f.update(self.table["First"].get(currSymbol))
                                    currSymbol = ""
                                    if '@' in f:
                                        pass
                                    else:
                                        break

                                elif currSymbol in self.terminals:
                                    f.add(currSymbol)
                                    currSymbol = ""

                            if '@' in f:
                                f.remove('@')
                                if nonTerminal is symbol:
                                    # A -> aA
                                    # This condition will give Follow(A) = Follow(A)
                                    # Ignore this case
                                    pass
                                else:
                                    if symbol not in calculated:
                                        self._follow(symbol, calculated, follow)
                                    f.update(follow.get(symbol))
                    elif curr in self.nonTerminals or  curr in self.terminals:
                        curr = ""

                follow[nonTerminal].update(f)
