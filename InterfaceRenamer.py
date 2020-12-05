import re

T_INTERFACE = 'interface'

class Symbol:
    def __init__(self, filepaths, type):
        self.filepaths = filepaths
        self.type = type

    def add_filepath(self, filepath):
        self.filepaths.add(filepath)

    def get_filepaths(self):
        return self.filepaths

    def get_type(self):
        return self.type

class ExistingSymbolCache:
    __cache = {}

    def __init__(self, search_and_replace):
        self.search_and_replace = search_and_replace
    
    def warmup(self):
        structural_symbol_matches = self.search_and_replace.find(
            r'(class|enum|function|type|interface) ([A-Z][a-zA-Z0-9]+)'
        )

        for (filepath, (symbol_type, symbol_name)) in structural_symbol_matches:
            if symbol_name not in self.__cache:
                self.__cache[symbol_name] = Symbol(set(), symbol_type)

        all_symbol_matches = self.search_and_replace.find(
            r'[^a-zA-Z0-9_]([A-Za-z_][a-zA-Z0-9_]+)'
        )

        for (filepath, symbol_name) in all_symbol_matches:
            if not symbol_name in self.__cache:
                continue

            self.__cache[symbol_name].add_filepath(filepath)

    def has(self, symbol_name):
        if symbol_name in self.__cache:
            return self.__cache[symbol_name]

        return False
    
    def get(self, symbol_name):
        return self.__cache[symbol_name]

class ExportedInterfaceRenamer:
    def __init__(self, search_and_replace, existing_symbol_cache):
        self.search_and_replace = search_and_replace
        self.existing_symbol_cache = existing_symbol_cache

    def refactor_all(self):
        for (_, candidate) in self.search_and_replace.find(r'export interface (I[A-Z][a-zA-Z0-9]+)'):
            self.refactor(candidate)

    def refactor(self, symbol):
        substitute = symbol[1:]
    
        if self.existing_symbol_cache.has(substitute):
            print('Skipping %s' % symbol)
            return

        print('Replacing %s with %s' % (symbol, substitute))

        if not self.existing_symbol_cache.has(symbol):
            raise ValueError('Missing interface in cache')

        filepaths = self.existing_symbol_cache.get(symbol).get_filepaths()

        print(
            str(self.search_and_replace.replace_symbol_in_files(filepaths, symbol, substitute))
        )


class LocalInterfaceRenamer:
    def __init__(self, search_and_replace, existing_symbol_cache):
        self.search_and_replace = search_and_replace
        self.existing_symbol_cache = existing_symbol_cache

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
