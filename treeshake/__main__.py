from sys import argv
from colorama import init, Fore, Style
from time import time as now

from treeshake.shaker import Shaker


def main(args=None):
    init()

    if args is None:
        args = argv[1:]

    css_folder = args[0] if len(args) > 0 else None
    html_folder = args[1] if len(args) > 1 else None
    output_folder = args[2] if len(args) > 2 else None

    if css_folder is None:
        css_folder = _ask('CSS directory path')

    if html_folder is None:
        html_folder = _ask('HTML directory path')

    if output_folder is None:
        output_folder = _ask('Output directory path')

    print('')

    treeshaker = Shaker()
    treeshaker.discover_add_stylesheets(css_folder)
    treeshaker.discover_add_html(html_folder)
    start_time = now()

    files = treeshaker.optimize(output_folder)

    print(f'{Fore.GREEN}Done! Optimized {files} files in {round(now() - start_time, 5)} seconds!{Style.RESET_ALL}')


def _ask(msg):
    return input(f'{Fore.YELLOW}\n> {msg}: {Style.RESET_ALL}')


if __name__ == '__main__':
    main(argv[1:])
