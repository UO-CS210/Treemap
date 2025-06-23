"""SVG display of Treemap"""
import io
import sys

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
                CSS_BUFFER.append(line)
        except FileNotFoundError:
            log.error(f"Could not open style file {css}")
            sys.exit(1)


def xml_escape(s: str) -> str:
    """"Escape XML special characters as XML entities"""
    return ((s.replace("&", "&amp;").
            replace("<", "&lt;")).
            replace(">", "&gt;").
            replace('"', '&quot;'))


def draw_rect(llx, lly, urx, ury, properties: dict):
    """Generate display directions for a tile in SVG rendering.
    Includes labeling the rectangle, in text or as a tool-tip.
    """
    margin = properties["margin"]
    css_class = properties["class"]
    width = max(1, (urx - llx - 2 * margin))
    height = max(1, (ury - lly - 2 * margin))
    SVG_BUFFER.append(
        f"""\n<g><rect x="{llx + margin}" y="{lly + margin}" 
         width="{width}"  height="{height}"
         rx="10"  fill="{properties["fill_color"]}" 
         class="{css_class}" />
      """)
    if "label" in properties:
        # Label is associated with group that wraps rect, so that
        # it can be rendered as either <title> or <text> depending
        # on available space
        draw_label(properties["label"], llx, lly, urx, ury, properties)
    SVG_BUFFER.append("</g>")


def begin_group(label: str | None,
                    llx: int, lly: int, urx: int, ury: int,
                    properties: dict):
    margin = properties["margin"]
    if label:
        group_label = f"<title>{xml_escape(label)}</title>"
    else:
        group_label = ""
    SVG_BUFFER.append(
        f"""\n<g class="group">{group_label}
        <rect x="{llx + margin}" y="{lly + margin}" 
        width="{urx - llx - 2 * margin}"  height="{ury - lly - 2 * margin}"
        rx="5"  
        class="group_outline" />
        """
    )

CHAR_WIDTH_APPROX = 17  # Rough approximation of average character width in pixels

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


def end_group():
    SVG_BUFFER.append("\n</g>")


def draw_label(label: str, llx: int, lly: int, urx: int, ury: int,
               properties: dict):
    """Generate display directions for a label in SVG rendering.
    May be rendered as <text> or <title> depending on available space, so
    make sure there is an element (e.g., a <g>...</g>) to attach the
    title to.
    """
    center_x = (urx + llx) // 2
    center_y = (lly + ury) // 2
    width = text_width_roughly(label)

    # If a label contains special HTML/XML characters, they must be escaped,
    # and newlines should break the text into parts
    label = xml_escape(label)

    if options["hide_long"] and width > (urx - llx):
        # Create a "title" element in place of textual label
        label = label.replace('\n', ' – ')
        SVG_BUFFER.append(f"""<title>{label}</title>""")
    else:
        label = label.replace('\n', f'</tspan><br /><tspan x="{center_x}" dy="1em">')
        SVG_BUFFER.append(
            f"""<text x="{center_x}"  y="{center_y}"
             class="tile_label_{properties["label_color"]}" ><tspan>{label}</tspan></text>
          """)

def close():
    # We will assemble the output SVG file from
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