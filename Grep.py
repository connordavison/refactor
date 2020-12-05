import os
import re

class Grep:
    def __init__(self):
        pass

    def find_recursive(self, directory, pattern):
        for filepath in self.__walk(directory):
            if self.find(filepath, pattern):
                yield filepath

    def find(self, filepath, pattern):
        return any(self.match(filepath, pattern))

    def match_recursive(self, directory, pattern):
        for filepath in self.__walk(directory):
            for match in self.match(filepath, pattern):
                yield (filepath, match)

    def match(self, filepath, pattern):
        with open(filepath, 'r') as lines:
            for line in lines:
                for match in re.findall(pattern, line):
                    yield match

    def __walk(self, directory):
        for basename, _, filenames in os.walk(directory):
            for filename in filenames:
                yield os.path.join(basename, filename)
