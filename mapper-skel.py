""" Construct a treemap.
Author: _Your name here_
Credits: _Did you collaborate with other students or find useful materials online?
         _Did you use AI tools to create some starter code?

Instructions:  Copy this file to treemap.py and then edit it. REMOVE this part of the
docstring and complete the identifying information above.  Credits should start out
empty, but add classmates or outside sources (including web sources or AI helpers)
as appropriate.  Be certain you understand it well enough to recreate it without help.

Example use:  python3 mapper.py data/small_flat.json 500 500
"""

# Standard Python library modules
import json
import argparse
import logging

# Project modules, provided
import geometry
import display

# Project modules that you write
# import mapper_types  # We'll create this along with splitter.py
# import splitter      # Uncomment this when you have created splitter.py

# Enable logging with log.debug(msg), log.info(msg), etc.
logging.basicConfig()
log = logging.getLogger(__name__)  # Log messages will look like "DEBUG:mapper:msg"
log.setLevel(logging.DEBUG)   # Change to logging.INFO to suppress debugging messages

# Layout works with integers, floating point numbers, or a mix of the two.
Real = int | float    # Named type for use in type annotations

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
    parser.add_argument("svg", help="SVG output file",
                        nargs="?", default="output.svg")
    args = parser.parse_args()
    return args



def layout(items: list[Real], rect: geometry.Rect):
    """Lay elements of nest out in rectangle.
    Version 0 (skeleton code) just takes a slice off the canvas for
    each rectangle.  You will replace it with much better recursive
    layouts.
    """
    while len(items) > 0:
        log.debug(f"Laying out {items} in {rect}")
        proportion = items[0] / sum(items)
        left_rect, rect = rect.split(proportion)
        label = str(items[0])
        display.draw_tile(left_rect, label)
        items = items[1:]


def main():
    """Display and produce an SVG treemap of the input data."""
    args = cli()
    display.init(args.width, args.height, args.svg)
    values = json.load(args.input)
    area = geometry.Rect(geometry.Point(0, 0),
                         geometry.Point(args.width, args.height))
    layout(values, area)
    display.wait_close()

if __name__ == "__main__":
    main()



