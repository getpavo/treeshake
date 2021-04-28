import os
import glob
import ntpath

from treeshake.stylesheet import Stylesheet


cdef class Shaker:
    """
    Tree shaker class that holds all information needed for comparison.

    Attributes:
        _stylesheets (list): A list of paths to .css files that will be used in comparison.
        _html_files (list): A list of paths to .html files that will be used in comparison.
    """
    cdef list _stylesheets, _html_files

    def __init__(self):
        self._stylesheets = []
        self._html_files = []

    cpdef void add_stylesheet(self, str path) except *:
        """Adds a .css file to the list of stylesheets.
        
        Arguments:
            path (str): The path to the css file to add to the list.
        """
        self._stylesheets.append(path)

    cpdef void add_html_file(self, str path) except *:
        """Adds a .html file to the list of html files.
        
        Arguments:
            path (str): The path to the html file to add to the list.
        """
        self._html_files.append(path)

    cpdef void discover_add_stylesheets(self, str path, bint recursive=False) except *:
        """Finds all css files in a certain path and adds them to the list.
        
        Arguments:
            path (str): The path to the directory to use to discover.
            recursive (bool): Whether or not to go in-depth and find files recursively.
        """
        for stylesheet in self.discover(path, '.css', recursive):
            self.add_stylesheet(stylesheet)

    cpdef void discover_add_html(self, str path, bint recursive = False) except *:
        """Finds all html files in a certain path and adds them to the list.

        Arguments:
            path (str): The path to the directory to use to discover.
            recursive (bool): Whether or not to go in-depth and find files recursively.
        """
        for html_file in self.discover(path, '.html', recursive):
            self.add_html_file(html_file)

    cpdef void print_stylesheets(self) except *:
        print(self._stylesheets)
        print(self._html_files)

    cpdef list discover(self, str path, str extension, bint recursive=False):
        """Discovers files in a certain folder (recursively).
        
        Arguments:
            path (str): The path to the directory that is used as a starting point.
            extension (str): The extension to search for.
            recursive (bool): Whether or not to go in-depth and find files recursively.
        """
        cpdef list results = []
        if recursive:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(extension):
                        results.append(os.path.join(root, file))
        else:
            if path.endswith('/'):
                path = path[:-1]

            for file in glob.glob(f'{path}/*{extension}'):
                if file.endswith(extension):
                    results.append(file)

        return results

    cpdef void optimize(self, str output_directory):
        """Tree-shakes all css files in self._stylesheets.
        
        Compares all rules in the css-file to the html files and, if the rule is not used in any html file,
        deletes it from the output file. This leaves only used css-rules in the final product.
        
        Arguments:
            output_directory (str): The directory to output the files to.
        """
        if output_directory.endswith('/'):
            output_directory = output_directory[:-1]

        try:
            os.mkdir(output_directory)
        except OSError as e:
            if e.errno != 17:
                raise e

        for stylesheet in self._stylesheets:
            file_name = ntpath.basename(stylesheet)
            obj = Stylesheet(stylesheet)
            obj.optimize(self._html_files, f'{output_directory}/{file_name}')
