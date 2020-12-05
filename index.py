import sys

from SearchAndReplace import SearchAndReplace
from Grep import Grep
from InterfaceRenamer import LocalInterfaceRenamer, ExportedInterfaceRenamer

directories = sys.argv
grep = Grep()
search_and_replace = SearchAndReplace(grep, directories)
renamers = [
    LocalInterfaceRenamer(search_and_replace),
    ExportedInterfaceRenamer(search_and_replace),
]

for renamer in renamers:
    renamer.refactor_all()
