"""Main "driver" program for treemap project.  M Young, summer 2024
(Command line interface.)

2025-06 revisions:  Improved control of graphics (Tk and SVG)
- suppression of labels that overflow rectangles with the --messy flag
- user-provided CSS style sheet can be specified with --css  filename.css
  applies to SVG output only
- user-provided CSV color scheme can be specified with --csv  filename.csv,
  will also apply to SVG if css style sheet not specified
"""

import json    # Acquire data to be mapped in JSON exchange format  (see https://www.json.org)
import argparse

import color_scheme
import mapper
from treemap_options import options

def cli() -> object:
    """Obtain input file and options from the command line.
    Returns an object with a field for each option.
    """
    parser = argparse.ArgumentParser("Depict a data set as a squarified treemap")
    parser.add_argument("input", help="Data input in json format",
                        type=argparse.FileType("r"))
    # User-provided color scheme as CSV file (can apply to Tk and SVG)
    parser.add_argument("-c", "--colors", help="Color scheme as CSV file",
                        nargs="?", default=None, type=argparse.FileType("r"))
    # User-provided CSS file to style the SVG output?  (Applies to SVG only)
    parser.add_argument("--css", help="CSS file to use for SVG",
                        nargs="?", default=None, type=argparse.FileType("r"))
    # Suppress long labels? (Applies to SVG only for now)
    parser.add_argument("-m", "--messy", help="Include labels that are too big for their tiles",
                         action="store_true")
    parser.add_argument("width", help="width of canvas in pixels",
                        type=int)
    parser.add_argument("height", help="height of canvas in pixels",
                        type=int)

    args = parser.parse_args()

    #  Options communicated through treemap_options
    if args.css:
        options["css"] = args.css.readlines()
        # Implemented only by SVG output
    if args.colors:
        options["colors"] = color_scheme.read_color_scheme_file(args.colors)
        if not args.css:
            options["css"] = color_scheme.to_css(options["colors"])
    options["messy"] = args.messy

    return args


def main():
    """Display and produce an SVG treemap of the input data."""
    args = cli()
    values = json.load(args.input)
    mapper.treemap(values, args.width, args.height)


if __name__ == "__main__":
    main()