# Treeshake
![](https://img.shields.io/pypi/dm/treeshake?style=flat-square)
![](https://img.shields.io/pypi/status/treeshake?style=flat-square)
![](https://img.shields.io/github/repo-size/jackmanapp/treeshake?style=flat-square)

Ever used a CSS framework and cried about all the overhead it caused? Ever wrote so much CSS that you were no longer aware what parts of it were actually used? Fear no more. Just use `treeshake` before deployment and all of your troubles will melt away.

## Dead code elimination
Tree shaking is a concept mostly used in ECMAScript languages like Dart, JavaScript and Typescript that helps to eliminate unused code. Optimizing your code in a single bundle.

This project aims to bring the power of tree shaking for css to your Python projects. This small library is written in [Cython](https://cython.readthedocs.io/) and allows you to get the best performance out of your (potentially) bloated web applications.

## Quick example
The following piece of codes recursively adds all css files from `/styles/` and all html files from `/html` and compares the contents. Where possible, it will eliminate styling.

The new file is written to the `/out/` output directory.

```python
from treeshake import Shaker

treeshaker = Shaker()
treeshaker.discover_add_stylesheets('./styles/', True)
treeshaker.discover_add_html('./html/', True)
treeshaker.optimize('./out')
```

## Command line support
In the near future, we aim to provide a simple cli command to quickly start tree shaking directories. This feature is currently planned and expected to arrive in `v0.2.0`.

## Contributing
Any contribution to this project is very welcome. Please open an issue when you are dealing with a problem or want to discuss a feature. All contributions are handled by pull requests.

Please refer to [CONTRIBUTING.md](https://github.com/jackmanapp/treeshake/blob/main/CONTRIBUTING.md) for more information.