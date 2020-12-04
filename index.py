import sys

from SearchAndReplace import SearchAndReplace
from Grep import Grep
from InterfaceRenamer import InterfaceRenamer

directories = sys.argv
grep = Grep()
searchAndReplacer = SearchAndReplace(Grep(), directories)
renamer = InterfaceRenamer(searchAndReplacer)

for directory in directories:
    for filepath in grep.find_files_recursive(directory, r'interface (I[A-Z][a-zA-Z0-9]+)'):
        with open(filepath, 'r') as lines:
            for line in lines:
                for candidate in renamer.find_candidates(line):
                    renamer.refactor(candidate)
