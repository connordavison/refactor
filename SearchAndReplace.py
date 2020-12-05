import os
import re

class FileReplaceCollection:
    def __init__(self, file_replaces):
        self.file_replaces = file_replaces

    def add(self, file_replace):
        self.file_replaces.append(file_replace)

    def __str__(self):
        string = ''

        for file_replace in self.file_replaces:
            string += str(file_replace)

        return string

class FileReplace:
    def __init__(self, file, line_replaces):
        self.file = file
        self.line_replaces = line_replaces

    def __str__(self):
        string = 'File: %s\n' % self.file

        for line_replace in self.line_replaces:
            string += str(line_replace)

        return string

class LineReplace:
    def __init__(self, original, new):
        self.original = original
        self.new = new

    def __str__(self):
        string = '\t+ %s\n' % self.original.rstrip()
        string += '\t- %s\n' % self.new.rstrip()

        return string

class SearchAndReplace:
    __SYMBOL_PATTERN = r'([^a-zA-Z0-9_])(%s)([^a-zA-Z0-9_])'
    __SYMBOL_REPLACEMENT = r'\1%s\3'

    def __init__(self, grep, directories):
        self.grep = grep
        self.directories = directories

    def replace_symbol(self, symbol, substitute):
        pattern = self.__SYMBOL_PATTERN % symbol
        replacement = self.__SYMBOL_REPLACEMENT % substitute

        return self.replace(pattern, replacement)

    def replace_symbol_in_files(self, filepaths, symbol, substitute):
        file_replaces = []

        for filepath in filepaths:
            file_replaces.append(
                self.replace_symbol_in_file(filepath, symbol, substitute)
            )

        return FileReplaceCollection(file_replaces)

    def replace_symbol_in_file(self, filepath, symbol, substitute):
        pattern = self.__SYMBOL_PATTERN % symbol
        replacement = self.__SYMBOL_REPLACEMENT % substitute

        return self.replace_in_file(filepath, pattern, replacement)

    def replace(self, pattern, replacement):
        file_replaces = []

        for directory in self.directories:
            for filepath in self.grep.find_recursive(directory, pattern):
                file_replaces.append(
                    self.replace_in_file(filepath, pattern, replacement)
                )

        return FileReplaceCollection(file_replaces)

    def replace_in_file(self, filepath, pattern, replacement):
        line_replaces = []

        with open(filepath, 'r') as lines:
            for line in lines:
                line_replace = LineReplace(
                    line,
                    re.sub(pattern, replacement, line)
                )

                line_replaces.append(line_replace)

        with open(filepath, 'w') as writer:
            for line_replace in line_replaces:
                writer.write(line_replace.new)

        return FileReplace(filepath, filter(
            lambda line_replace: line_replace.new != line_replace.original,
            line_replaces
        ))

    def find_all_symbols(self, symbol):
        return self.find(self.__SYMBOL_PATTERN % r'([A-Za-z_][a-zA-Z0-9]+)')

    def find_symbol(self, symbol):
        return self.find(self.__SYMBOL_PATTERN % symbol)

    def find(self, pattern):
        for directory in self.directories:
            yield from self.grep.match_recursive(directory, pattern)

    def find_in_file(self, pattern, filepath):
        return self.grep.match(filepath, pattern)
