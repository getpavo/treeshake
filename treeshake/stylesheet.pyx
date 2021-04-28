import cssutils
from bs4 import BeautifulSoup


cdef class Stylesheet:
    """Class that holds logic for a single Stylesheet.

    Attributes:
        path (str): The path to the file that the Stylesheet class belongs to.
    """
    cdef str path

    def __init__(self, str path):
        self.path = path

    cpdef bint compare_with_html(self, str selector, str html_path) except *:
        """Checks whether the given selector is used in a single html file.
        
        Arguments:
            selector (str): The css-selector to find in the html document.
            html_path (str): The path to the html file to use when comparing.
            
        Returns:
            bool: Whether or not the selector was found in the given html file.
        """
        with open(html_path, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')

        if len(soup.select(selector)) > 0:
            return True

        return False

    cpdef void optimize(self, list html_files, str output_path=None) except *:
        """Optimizes the stylesheet and outputs the content to a specified path.
        
        Parses the css and finds all selectors in the parsed document. Then, continues to iterate over all given 
        html files and checks whether or not the selector is used in these documents. If it used at least once,
        the css-rule will be added to the new stylesheet, which is outputted to the output_path.
        
        Arguments:
            html_files (list): List of paths to html files to compare.
            output_path (str): The path to the output directory. If none, defaults to original css folder.
        """
        if output_path is None:
            output_path = self.path

        sheet = cssutils.parseFile(self.path)
        new_sheet = cssutils.css.CSSStyleSheet()
        cdef list found = []

        for index, file in enumerate(html_files):
            for rule in sheet:
                if self.compare_with_html(rule.selectorText, file) and rule not in found:
                    new_sheet.add(rule)

        with open(output_path, 'w+b') as f:
            f.write(new_sheet.cssText)
