"""SVG display of Treemap"""
import io
import sys

import svg_config

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# These are all set in the 'init' function
SVG_BUFFER: list[str] = []
SVG_OUT: io.BytesIO | None = None
WIDTH = 0
HEIGHT = 0
ELIDE_WIDE_LABELS = False  # This really belongs in a configuration file

SVG_HEAD = ""
SVG_PROLOG = """"
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
   </style>
   </defs>
"""

def init(width: int, height: int, svg_path: str = None):
    """We keep SVG commands in a buffer, to be written
    at the end of execution.
    """
    global SVG_BUFFER
    global SVG_OUT
    global WIDTH
    global HEIGHT
    WIDTH, HEIGHT = width, height
    if svg_path == None:
        svg_path = "treemap.svg"
    try:
        SVG_OUT = open(svg_path, "w")
        svg_header = f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" >
        """
        SVG_BUFFER = [svg_header, SVG_PROLOG]
        log.info(f"SVG figure will be written to {svg_path}")
    except FileNotFoundError:
        log.warning(f"Could not open {svg_path}")
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
    SVG_BUFFER.append(
        f"""<g><rect x="{llx + margin}" y="{lly + margin}" 
         width="{urx - llx - 2 * margin}"  height="{ury - lly - 2 * margin}"
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
        group_label = f"\n<title>{xml_escape(label)}</title>"
    else:
        group_label = ""
    SVG_BUFFER.append(
        f"""<g class="group">{group_label}
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
    SVG_BUFFER.append("</g>")


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

    if svg_config.SVG_HIDE_LONG_LABELS and width > (urx - llx):
        label = label.replace('\n', ' – ')
        SVG_BUFFER.append(f"""<title>{label}</title>""")

    else:
        label = label.replace('\n', f'</tspan><br /><tspan x="{center_x}" dy="1em">')
        SVG_BUFFER.append(
            f"""<text x="{center_x}"  y="{center_y}"
             class="tile_label_{properties["label_color"]}" ><tspan>{label}</tspan></text>
          """)

def close():
    log.info(f"Saving SVG representation as {SVG_OUT.name}")
    SVG_BUFFER.append("</svg>")
    SVG_OUT.write("".join(SVG_BUFFER))
    SVG_OUT.close()