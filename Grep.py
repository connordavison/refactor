import os
import re

class Grep:
    def __init__(self):
        pass

    def find_files_recursive(self, directory, pattern):
        for basename, _, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(basename, filename)

                if self.file_contains(filepath, pattern):
                    yield filepath

    def file_contains(self, filepath, pattern):
        with open(filepath, 'r') as lines:
            for line in lines:
                if re.search(pattern, line):
                    return True

        return False
