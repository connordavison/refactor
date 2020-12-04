import re

class InterfaceRenamer:
    def __init__(self, search_and_replace):
        self.search_and_replace = search_and_replace

    def find_candidates(self, text):
        return re.findall(r'interface (I[A-Z][a-zA-Z0-9]+)', text)

    def refactor(self, symbol):
        substitute = symbol[1:]
        symbol_already_exists = self.search_and_replace.find(
            re.compile('(?:class|enum|function) ' + substitute)
        )
    
        if symbol_already_exists:
            print('Skipping %s' % symbol)
            return

        print('Replacing %s with %s' % (symbol, substitute))
        print(
            str(self.search_and_replace.replace(symbol, substitute))
        )
