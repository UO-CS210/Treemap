""" Construct a treemap.
Author: _Your name here_
Credits: _Did you collaborate with other students or find useful materials online?
         _Did you use AI tools to create some starter code?

Instructions:  Copy this file to treemap.md and then edit it. REMOVE this part of the
docstring and complete the identifying information above.  Credits should start out
empty, but add to them as you proceed.
"""

# Standard Python library modules
import json
import argparse

# Project modules, provided
import geometry
import display

# Project modules, you write
import splitter

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


def layout(li: list[int], rect: geometry.Rect):
    """Lay elements of li out in rectangle.
    Version 0 (skeleton code) just takes a slice off the canvas for
    each rectangle.  You will replace it with much better recursive
    layouts.
    """
    while len(li) > 0:
        proportion = li[0] / sum(li)
        left_rect, rect = rect.split(proportion)
        display.draw_tile(left_rect, li[0])
        li = li[1:]


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



