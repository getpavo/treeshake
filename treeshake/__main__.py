from sys import argv
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

        if html_folder is None:
            html_folder = _ask('HTML directory path')

        if output_folder is None:
            output_folder = _ask('Output directory path')

        treeshaker = Shaker()
        treeshaker.discover_add_stylesheets(css_folder)
        treeshaker.discover_add_html(html_folder)
        start_time = now()

        files = treeshaker.optimize(output_folder)

        print(f'{Fore.GREEN}\nDone! Optimized {files} files in {round(now() - start_time, 5)} seconds!\n{Style.RESET_ALL}')
    except KeyboardInterrupt:
        print(f'{Fore.BLUE}\nDetected hard interrupt. Bye bye!\n{Style.RESET_ALL}')
        exit()


def _ask(msg):
    return input(f'{Fore.YELLOW}\n> {msg}: {Style.RESET_ALL}')


def _create_parser():
    parser = ArgumentParser(description='Tree shake stylesheets and improve performance from command line.')
    parser.add_argument('css', help='The path to the css folder', type=str)
    parser.add_argument('html', help='The path to the HTML folder', type=str)

    # Mutually exclusive group for output file information
    output_group = parser.add_mutually_exclusive_group(required=False)
    output_group.add_argument('--out', default='./out/', type=str)
    output_group.add_argument('--overwrite', default=False, action='store_true')

    return parser


if __name__ == '__main__':
    main(argv[1:])
