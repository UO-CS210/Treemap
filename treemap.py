"""Main "driver" program for treemap project.
(Command line interface.)

"""

import json    # Acquire data to be mapped in JSON exchange format  (see https://www.json.org)
import argparse
import mapper
from treemap_options import options

def cli() -> object:
    """Obtain input file and options from the command line.
    Returns an object with a field for each option.
    """
    parser = argparse.ArgumentParser("Depict a data set as a squarified treemap")
    parser.add_argument("input", help="Data input in json format",
                        type=argparse.FileType("r"))
    parser.add_argument("width", help="width of canvas in pixels",
                        type=int)
    parser.add_argument("height", help="height of canvas in pixels",
                        type=int)
    # User-provided CSS file to style the SVG output?  (Applies to SVG only)
    parser.add_argument("css", help="CSS file to use for SVG", nargs="?", default=None)
    # Suppress long labels? (Applies to SVG only for now)
    parser.add_argument("hide_long", help="Suppress display of overlong labels in SVG",
                        nargs="?", default=False)
    args = parser.parse_args()

    #  Options communicated through treemap_options
    if args.css:
        options["css_file"] = args.css_file
        # Implemented only by SVG output
    options["hide_long"] = args.hide_long

    return args


def main():
    """Display and produce an SVG treemap of the input data."""
    args = cli()
    values = json.load(args.input)
    mapper.treemap(values, args.width, args.height)


if __name__ == "__main__":
    main()