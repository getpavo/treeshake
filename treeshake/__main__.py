from sys import argv
from os import path
from argparse import ArgumentParser
from colorama import init, Fore, Style
from time import time as now

from treeshake.shaker import Shaker


def main(args=None):
    try:
        init()
        parser = _create_parser()
        if args is None:
            args = argv[1:]

        args = parser.parse_args(args)

        css_folder = args.css
        html_folder = args.html
        output_folder = args.css if args.overwrite is True else args.out

        if css_folder is None:
            css_folder = _ask('CSS directory path')
            html_folder = _ask('HTML directory path')
            output_folder = _ask('Output directory path')

        if (args.safe is True) and (not path.exists(css_folder)) or (not path.exists(html_folder)) \
                or (not path.exists(output_folder)):
            raise KeyboardInterrupt(f'{Fore.RED}\nOne or more specified folders missing. '
                                    f'Exiting because of --safe flag\n{Style.RESET_ALL}')

        optimizer = Shaker()
        optimizer.discover_add_stylesheets(css_folder, args.recursive_css)
        optimizer.discover_add_html(html_folder, args.recursive_html)
        start_time = now()

        files = optimizer.optimize(output_folder)

        print(f'{Fore.GREEN}\nDone! Optimized {len(files)} files in {round(now() - start_time, 5)}s!\n{Style.RESET_ALL}')
    except KeyboardInterrupt as e:
        if str(e) != '':
            print(str(e))
        else:
            print(f'{Fore.BLUE}\n\nDetected hard interrupt. Bye bye!\n{Style.RESET_ALL}')
        exit()


def _ask(msg):
    return input(f'{Fore.YELLOW}\n> {msg}: {Style.RESET_ALL}')


def _create_parser():
    parser = ArgumentParser(description='Tree shake stylesheets and improve performance from command line.')

    # Required positional arguments
    parser.add_argument('css', help='The path to the css folder', type=str, nargs='?', default=None)
    parser.add_argument('html', help='The path to the HTML folder', type=str, nargs='?', default=None)

    # Optional arguments about directory management and discovery
    parser.add_argument('--recursive-css', help='Find stylesheets through all subfolders', action='store_true')
    parser.add_argument('--recursive-html', help='Find stylesheets through all subfolders', action='store_true')
    parser.add_argument('--safe', help='Throws an error if a directory does not exist', action='store_true', default=False)

    # Mutually exclusive group for output file information
    output_group = parser.add_mutually_exclusive_group(required=False)
    output_group.add_argument('--out', default='./out/', type=str)
    output_group.add_argument('--overwrite', default=False, action='store_true')

    return parser


if __name__ == '__main__':
    main(argv[1:])
