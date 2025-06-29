"""Manage color schemes.
A color scheme maps category names to background and text color pair.
A color scheme can be read from a CSV file.
A color scheme can be used for:
- Tk graphics:  get foreground and background color for a category
- SVG graphics: convert color scheme table into CSS stylesheet

"""
import sys
import csv
import io
import logging
import color_contrast

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Color scheme is represented as a dict, str -> tuple[str, str]
# e.g.  {"animals": ("#454532", "white"),
#        "vegetables": ("green", "black") }
#

def read_color_scheme(csv_file_name: str) -> dict[str, tuple[str, str]]:
    """Read a color scheme from a CSV file given the path as a string"""
    csv_file = open(csv_file_name, mode="r", encoding="utf-8")
    # May throw file-not-found error here;  sufficiently self-explanatory?
    return read_color_scheme_file(csv_file)

def read_color_scheme_file(csv_file: io.IOBase) -> dict[str, tuple[str, str]]:
    """Read a color scheme from an open CSV file."""
    assert isinstance(csv_file, io.IOBase), "Expecting an open file; try read_color_scheme to read from path"
    reader = csv.reader(csv_file, delimiter=",")
    result = {}
    for row in reader:
        # Comment lines may have just one cell or start with #
        if len(row) < 3 or not row[2] or row[0].startswith("#"):
            log.debug(r"Skipping record {row}")
            continue
        result[row[0]] = (row[1], row[2])
    return result

#  Can be run as a main program to produce a .css file from
#  a .csv file, so that we can have consistency between Tk and SVG
#  color schemes.
#
def to_css(table: dict[str, tuple[str, str]]) -> list[str]:
    """Convert a color scheme table into a CSS stylesheet,
    returned as if it had been read from file with readlines()
    """
    result: list[str] = []
    LB, RB = "{", "}"
    for key, (background, text) in table.items():
        # Note the "fill" attribute applies to text color as well as rectangle color in SVG,
        # so we need an extra entry to specify text color in text elements
        result.append(f".{key} {LB} fill: {background}; {RB}")
        result.append(f".{key} text {LB} fill: {text}; {RB}")
    return result

def main():
    """Can be run as a filter script that converts CSV on input to CSS on output."""
    log.info("Reading color scheme from standard input")
    table = read_color_scheme_file(sys.stdin)
    css = to_css(table)
    sys.stdout.write(css)
    print()  # Ending newline
    sys.stdout.flush()
    sys.stdout.close()

if __name__ == "__main__":
    main()
