import os
import sys

from Cython.Build import cythonize

extensions = cythonize('treeshake/*.pyx', compiler_directives={'language_level': "3"})


def build(setup_kwargs):
    setup_kwargs.update({
        'ext_modules': extensions,
    })
