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
        string = '\tFile: %s\n' % self.file

        for line_replace in self.line_replaces:
            string += str(line_replace)

        return string

class LineReplace:
    def __init__(self, original, new):
        self.original = original
        self.new = new

    def __str__(self):
        string = '\t+ %s\'\n' % self.original.rstrip()
        string += '\t- %s\'\n' % self.new.rstrip()

        return string

class SearchAndReplace:
    def __init__(self, grep, directories):
        self.grep = grep
        self.directories = directories

    def find(self, pattern):
        for directory in self.directories:
            if any(self.grep.find_files_recursive(directory, pattern)):
                return True

        return False

    def replace(self, pattern, replacement):
        file_replaces = []

        for directory in self.directories:
            for filepath in self.grep.find_files_recursive(directory, pattern):
                file_replaces.append(
                    self.replace_in_file(filepath, pattern, replacement)
                )

        return FileReplaceCollection(file_replaces)



    def replace_in_file(self, filepath, pattern, replacement):
        line_replaces = []

        with open(filepath, 'r') as lines:
            for line in lines:
                line_replaces.append(
                    LineReplace(
                        line,
                        re.sub(pattern, replacement, line)
                    )
                )

        with open(filepath, 'w') as writer:
            for line_replace in line_replaces:
                writer.write(line_replace.new)

        return FileReplace(filepath, filter(
            lambda line_replace: line_replace.new != line_replace.original,
            line_replaces
        ))
        
