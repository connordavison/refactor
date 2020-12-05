import re

class ExportedInterfaceRenamer:
    def __init__(self, search_and_replace):
        self.search_and_replace = search_and_replace

    def refactor_all(self):
        for (_, candidate) in self.search_and_replace.find(r'export interface (I[A-Z][a-zA-Z0-9]+)'):
            self.refactor(candidate)

    def refactor(self, symbol):
        substitute = symbol[1:]

        existing_symbols = self.search_and_replace.find(
            r'(?:class|enum|function|type) %s[^a-zA-Z0-9_]' % substitute
        )
    
        if any(existing_symbols):
            print('Skipping %s' % symbol)
            return

        print('Replacing %s with %s' % (symbol, substitute))

        print(
            str(self.search_and_replace.replace(symbol, substitute))
        )

class LocalInterfaceRenamer:
    def __init__(self, search_and_replace):
        self.search_and_replace = search_and_replace

    def refactor_all(self):
        matches = self.search_and_replace.find(r'(?<!export )interface (I[A-Z][a-zA-Z0-9]+)')

        for (filepath, candidate) in matches:
            self.refactor(candidate, filepath)

    def refactor(self, symbol, filepath):
        substitute = symbol[1:]

        existing_symbols = self.search_and_replace.find_in_file(
            r'(?:class|enum|function|type) %s[^a-zA-Z0-9_]' % substitute,
            filepath
        )
    
        if any(existing_symbols):
            print('Skipping %s in %s' % (symbol, filepath))
            return

        print('Replacing %s with %s in %s' % (symbol, substitute, filepath))

        print(
            str(
                self.search_and_replace.replace_symbol_in_file(
                    filepath,
                    symbol,
                    substitute
                )
            )
        )
