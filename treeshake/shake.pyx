import os
import glob
import ntpath


from treeshake.stylesheet import Stylesheet


cdef class Shaker:
    cdef list _stylesheets, _html_files
    cdef bint overwrite

    def __init__(self):
        self._stylesheets = []
        self._html_files = []

    cpdef void add_stylesheet(self, str path) except *:
        self._stylesheets.append(path)

    cpdef void add_html_file(self, str path) except *:
        self._html_files.append(path)

    cpdef void discover_add_stylesheets(self, str path, bint recursive=False) except *:
        for stylesheet in self.discover(path, '.css', recursive):
            self.add_stylesheet(stylesheet)

    cpdef void discover_add_html(self, str path, bint recursive = False) except *:
        for html_file in self.discover(path, '.html', recursive):
            self.add_html_file(html_file)

    cpdef void print_stylesheets(self) except *:
        print(self._stylesheets)
        print(self._html_files)

    cpdef list discover(self, str path, str extension, bint recursive=False):
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

    cpdef void _optimize_css_file(self, str file) except *:
        if file not in self._stylesheets:
            raise ValueError('The path to this file is not included or discovered yet.')

        print('Done optimizing, bye!')

