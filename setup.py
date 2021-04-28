from setuptools import setup, find_packages
from Cython.Build import cythonize

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='treeshake',
    version='0.1.5',
    packages=find_packages(),
    description='Remove unused css in Python projects with C-powered tree shaking.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities'
    ],
    url='https://github.com/jackmanapp/treeshake/',
    ext_modules=cythonize('treeshake/*.pyx', compiler_directives={'language_level': "3"}),
    install_requires=[
        'beautifulsoup4>=4.9.3',
        'cssutils>=2.2.0'
    ]
)