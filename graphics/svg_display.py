"""SVG display of Treemap"""
import io
import sys
from idlelib.debugobj_r import remote_object_tree_item
from token import LBRACE

from graphics.tk_display import LINE_HEIGHT_APPROX
from treemap_options import options

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# We will assemble the output SVG file from
# these parts, in this order
#   - SVG header
#   - CSS prologue
#   - CSS entries buffer, which we build up incrementally as we build the structure
#   - CSS epilogue
#   - SVG entries buffer, which we build up incrementally with 1-1 correspondence to CSS entries
#   - SVG epilogue



SVG_HEAD = "uninitialized"  # Set in 'init' with height and width
CSS_PROLOGUE = """"
   <defs>
   <style>
    text {  text-anchor: middle;  
            font-family: Helvetica, Arial, sans-serif;
            font-size: 12pt;
            white-space: pre-wrap; 
    }
    tspan { white-space: pre-wrap; }
    .tile_label_white { fill: white;  white-space: pre-wrap; }
    .tile_label_black { fill: black;   white-space: pre-wrap; }
    .group_outline { stroke: red; fill: white; stroke-width: 1; }
    .group_outline:hover { fill: red; }
"""
CSS_BUFFER: list[str] = []
CSS_EPILOGUE   = """
   </style>
   </defs>
"""
SVG_BUFFER: list[str] = []
SVG_EPILOGUE = "\n</svg>"


SVG_OUT: io.BytesIO | None = None
WIDTH = 0
HEIGHT = 0
ELIDE_WIDE_LABELS = False  # This really belongs in a configuration file
IS_STYLED = False  # Is there a user-supplied CSS file, or do we need to randomly generate colors?


def init(width: int, height: int, svg_path: str = None):
    """We keep SVG commands in a buffer, to be written
    at the end of execution.
    """
    global SVG_HEAD
    global SVG_BUFFER
    global SVG_OUT
    global WIDTH
    global HEIGHT
    global IS_STYLED
    WIDTH, HEIGHT = width, height
    SVG_HEAD = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" >"""
    if not svg_path:
        svg_path = "treemap.svg"
    try:
        SVG_OUT = open(svg_path, "w")
        log.info(f"SVG figure will be written to {svg_path}")
    except FileNotFoundError:
        log.error(f"Could not open SVG file {svg_path}")
        sys.exit(1)

    css = options.get("css_file", False)
    if css:
        IS_STYLED = True
        try:
            css_file = open(css, "r")
            for line in css_file:
                CSS_BUFFER.append(line.strip())
        except FileNotFoundError:
            log.error(f"Could not open style file {css}")
            sys.exit(1)


def xml_escape(s: str) -> str:
    """"Escape XML special characters as XML entities"""
    return ((s.replace("&", "&amp;").
            replace("<", "&lt;")).
            replace(">", "&gt;").
            replace('"', '&quot;'))

LBRACE = "{"
RBRACE = "}"

def draw_rect(llx, lly, urx, ury, properties: dict):
    """Generate display directions for a tile in SVG rendering.
    Includes labeling the rectangle, in text or as a tool-tip.
    """
    margin = properties["margin"]
    if "label" in properties:
        css_class = gen_class_name(properties["label"])
    elif "class" in properties:
        css_class = gen_class_name(properties["class"])
    else:
        css_class = "tile"
    width = max(1, (urx - llx - 2 * margin))
    height = max(1, (ury - lly - 2 * margin))
    SVG_BUFFER.append(
        f"""\n<g class="{css_class}"><rect x="{llx + margin}" y="{lly + margin}" 
         width="{width}"  height="{height}"
         rx="10"  
         class="{css_class}" />
      """)
    if "label" in properties:
        # Label is associated with group that wraps rect, so that
        # it can be rendered as either <title> or <text> depending
        # on available space
        draw_label(properties["label"], llx, lly, urx, ury, properties)
    # If we haven't been given a custom CSS file, we'll fill in colors
    # that match the Tk rendering (which currently are randomly generated)
    if not IS_STYLED:
        CSS_BUFFER.append(f"""
            .{css_class}  {LBRACE} 
                fill: {properties["fill_color"]} ;
                color: {properties["label_color"]};
            {RBRACE}
        """)
    SVG_BUFFER.append("</g>")

def gen_class_name(label: str) -> str:
    """Extract a suitable and predictable  CSS class name from a label.
    We keep first line, replacing spaces by underscores and removing
    other punctuation.
    """
    basis = label.split()[0]
    if not basis[0].isalpha():
        basis = "C_" + basis
    chars = [ch for ch in basis if ch.isalnum()]
    return "".join(chars)


def begin_group(label: str | None,
                    llx: int, lly: int, urx: int, ury: int,
                    properties: dict):
    margin = properties["margin"]
    if label:
        group_label = f"<title>{xml_escape(label)}</title>"
        group_class = gen_class_name(label)
    else:
        group_label = ""
    SVG_BUFFER.append(
        f"""
        <g class="group {group_class}">{group_label}
            <rect x="{llx + margin}" y="{lly + margin}" 
            width="{urx - llx - 2 * margin}"  height="{ury - lly - 2 * margin}"
            rx="5"  
            class="group_outline" />
        """
    )

def end_group():
    SVG_BUFFER.append("\n</g>")



CHAR_WIDTH_APPROX = 13  # Rough approximation of average character width in pixels
LINE_HEIGHT_APPROX = 17

def text_width_roughly(label: str) -> int:
    """Approximate width of a string in pixels, based on
    rendering in a 12pt font.  Very rough since real width
    depends on font, screen resolution, width of individual
    characters, etc.  Just a "better than nothing" guess.
    """
    lines = label.split()  # Guess at LONGEST line
    longest = 0
    for line in lines:
        longest = max(longest, len(line) * CHAR_WIDTH_APPROX)
    return longest

def label_fits(label: str, llx: int, lly: int, urx: int, ury: int) -> bool:
    """Does this label fit in the screen area (probably)?
    We can't measure it directly (e.g., we don't know the typeface and size),
    so we make a very rough guess based on typical character width and line height.
    """
    width = text_width_roughly(label)
    if width > (urx - llx):
        return False
    if len(label.split()) * LINE_HEIGHT_APPROX > ury - lly:
        return False
    return True


def draw_label(label: str, llx: int, lly: int, urx: int, ury: int,
               properties: dict):
    """Generate display directions for a label in SVG rendering.
    May be rendered as <text> or <title> depending on available space, so
    make sure there is an element (e.g., a <g>...</g>) to attach the
    title to.
    """
    center_x = (urx + llx) // 2
    center_y = (lly + ury) // 2


    # If a label contains special HTML/XML characters, they must be escaped,
    # and newlines should break the text into parts
    label = xml_escape(label)

    # Let's make a title element (tool tip) regardless
    # (even when it duplicates the label)

    # "Title" element works as a tool-tip
    title = label.replace('\n', ' – ')
    SVG_BUFFER.append(f"""<title>{title}</title>""")

    # Also a label in the rectangle if it fits
    if options["messy"] or label_fits(label, llx, lly, urx, ury):
        label = label.replace('\n', f'</tspan><tspan x="{center_x}" dy="1.2em">')
        SVG_BUFFER.append(
            f"""<text x="{center_x}"  y="{center_y}"
             class="tile_label_{properties["label_color"]}" ><tspan>{label}</tspan></text>
          """)

def close():
    # Assemble the output SVG file from
    # these parts, in this order
    #   - SVG header
    #   - CSS prologue
    #   - CSS entries buffer, which we build up incrementally as we build the structure
    #   - CSS epilogue
    #   - SVG entries buffer, which we build up incrementally with 1-1 correspondence to CSS entries
    #   - SVG epilogue
    log.info(f"Saving SVG representation as {SVG_OUT.name}")
    SVG_OUT.write(SVG_HEAD)
    SVG_OUT.write(CSS_PROLOGUE)
    SVG_OUT.write("\n".join(CSS_BUFFER))
    SVG_OUT.write(CSS_EPILOGUE)
    SVG_OUT.write("\n".join(SVG_BUFFER))
    SVG_OUT.write(SVG_EPILOGUE)
    SVG_OUT.close()