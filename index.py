import sys

from SearchAndReplace import SearchAndReplace
from Grep import Grep
from InterfaceRenamer import LocalInterfaceRenamer, ExportedInterfaceRenamer, ExistingSymbolCache

directories = sys.argv
grep = Grep()
search_and_replace = SearchAndReplace(grep, directories)
existing_symbol_cache = ExistingSymbolCache(search_and_replace)
renamers = [
    LocalInterfaceRenamer(search_and_replace, existing_symbol_cache),
    ExportedInterfaceRenamer(search_and_replace, existing_symbol_cache),
]

existing_symbol_cache.warmup()

for renamer in renamers:
    renamer.refactor_all()
