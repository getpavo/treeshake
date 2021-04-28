import setuptools
from Cython.Build import cythonize

setuptools.setup(
    name='treeshake',
    ext_modules=cythonize('treeshake/*.pyx', compiler_directives={'language_level': "3"}),
)
