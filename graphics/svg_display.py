"""SVG display of Treemap"""
import io
import sys

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# These are all set in the 'init' function
SVG_BUFFER: list[str] = []
SVG_OUT: io.BytesIO | None = None
WIDTH = 0
HEIGHT = 0

SVG_HEAD = ""
SVG_PROLOG = """"
   <defs>
   <style>
    text {  text-anchor: middle;  
            font-family: Helvetica, Arial, sans-serif;
            font-size: 12pt;
    }
    .tile_label_white { fill: white; }
    .tile_label_black { fill: black;  }
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



def draw_rect(llx, lly, urx, ury, properties: dict):
    """Generate display directions for a tile in SVG rendering"""
    margin = properties["margin"]
    css_class = properties["class"]
    SVG_BUFFER.append(
        f"""<rect x="{llx + margin}" y="{lly + margin}" 
         width="{urx - llx - 2 * margin}"  height="{ury - lly - 2 * margin}"
         rx="10"  fill="{properties["fill_color"]}" 
         class="{css_class}"/>
      """)

def begin_group(label: str | None,
                    llx: int, lly: int, urx: int, ury: int,
                    properties: dict):
    margin = properties["margin"]
    if label:
        group_label = f"\n<title>{label}</title>"
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

def end_group():
    SVG_BUFFER.append("</g>")
def draw_label(label: str, llx: int, lly: int, urx: int, ury: int,
               properties: dict):
    """Generate display directions for a label in SVG rendering"""
    center_x = (urx + llx) // 2
    center_y = (lly + ury) // 2
    SVG_BUFFER.append(
        f"""<text x="{center_x}"  y="{center_y}"
         class="tile_label_{properties["label_color"]}" > {label} </text>
      """)

def close():
    log.info("Writing SVG file")
    SVG_BUFFER.append("</svg>")
    SVG_OUT.write("".join(SVG_BUFFER))
    SVG_OUT.close()