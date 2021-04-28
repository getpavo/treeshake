import cssutils
from bs4 import BeautifulSoup


cdef class Stylesheet:
    cdef str path

    def __init__(self, str path):
        self.path = path

    cpdef bint compare_with_html(self, str selector, str html_path) except *:
        with open(html_path, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')

        if len(soup.select(selector)) > 0:
            return True

        return False

    cpdef void optimize(self, list html_files, str output=None) except *:
        if output is None:
            output = self.path

        sheet = cssutils.parseFile(self.path)
        new_sheet = cssutils.css.CSSStyleSheet()
        cdef found = []

        for index, file in enumerate(html_files):
            for rule in sheet:
                if self.compare_with_html(rule.selectorText, file) and rule not in found:
                    new_sheet.add(rule)

        with open(output, 'w+b') as f:
            f.write(new_sheet.cssText)
