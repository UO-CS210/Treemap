"""Graphical display for treemapper.  Can produce
SVG file in addition to Tk display.
"""

import graphics.graphics as graphics
import geometry
import color_contrast
from typing import Optional
import io

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

CANVAS: Optional[graphics.GraphWin] = None
SVG_BUFFER: Optional[list[str]] = None
SVG_OUT: Optional[io.BytesIO] = None

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
    .group_outline { stroke: red; fill: none; stroke-width: 4; }
   </style>
   </defs>
"""
def init(width: int, height: int, svg_path: str = None):
    global CANVAS
    global SVG_BUFFER
    global SVG_OUT
    CANVAS = graphics.GraphWin("Treemap", width, height)
    CANVAS.setCoords(0, 0, width, height)
    if svg_path == None:
        svg_path = "treemap.svg"
    try:
        SVG_OUT = open(svg_path, "w")
        svg_header = f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" >
        """
        SVG_BUFFER = [svg_header, SVG_PROLOG]
    except FileNotFoundError:
        log.warning(f"Could not open {svg_path}")

# For documentation, I want consistent color choice
# when describing an example step-by-step.
# Uncomment this line to produce the same colors on each
# run with the same input data.
# random.seed(43)


"""Tactics for drawing on Tk and SVG (and potentially others in future): 
Attributes that can be computed once and then interpreted for each medium
are kept in a property table, rather than passing a whole zoo of parameters
to each medium-specific drawing function. 
"""

def draw_tile(r: geometry.Rect, label: str = None):
    """Draw the tile (on both media).
     Displays on Tk (Python built-in graphics) and
     also writes corresponding graphics into buffer to
     produce corresponding SVG diagram which can be displayed
     in a web page, imported into a diagramming tool like
     Inkscape, OmniGraffle, Illustrator, etc.
    """
    log.debug(f"Drawing {r}")
    properties = {"margin": 4, "class": "tile"}
    fill_color, label_color = color_contrast.next_color()
    properties["fill_color"] = fill_color
    properties["stroke_color"] = "white"
    properties["label_color"] = label_color
    draw_rect_tk(r, properties)
    draw_rect_svg(r, properties)
    if label:
        draw_label_tk(label, r, properties)
        draw_label_svg(label, r, properties)

def outline_group(r: geometry.Rect):
    log.debug(f"Outlining {r}")
    properties = {"margin": 2, "class": "group_outline"}
    properties["fill_color"] = None
    properties["stroke_color"] = "red"
    draw_rect_tk(r, properties)
    draw_rect_svg(r, properties)

def draw_rect_tk(r: geometry.Rect, properties: dict):
    """Draw and label the rectangle on the Tk (Python built-in) display"""
    assert CANVAS, "Did you forget to initialize the window?"
    margin = properties["margin"]
    image = graphics.Rectangle(graphics.Point(r.ll.x+margin, r.ll.y+margin),
                              graphics.Point(r.ur.x-margin, r.ur.y-margin))
    fill = properties["fill_color"]
    if fill:
        image.setFill(fill)
    stroke = properties["stroke_color"]
    if stroke:
        image.setOutline(stroke)
    image.draw(CANVAS)


def draw_rect_svg(r: geometry.Rect, properties: dict):
    """Emit display directions for SVG rendering"""
    # Flip to orient y upward
    y_extent = CANVAS.height
    ll_y = y_extent - r.ur.y
    ur_y = y_extent - r.ll.y
    margin = properties["margin"]
    css_class = properties["class"]
    SVG_BUFFER.append(
    f"""<rect x="{r.ll.x+margin}" y="{ll_y+margin}" 
         width="{r.ur.x - r.ll.x - 2* margin}"  height="{r.ur.y - r.ll.y - 2 * margin}"
         rx="10"  fill="{properties["fill_color"]}" 
         class="{css_class}"/>
      """)
#    stroke="{properties["stroke_color"]}

def draw_label_tk(label: str, r: geometry.Rect, properties: dict):
    label = graphics.Text(graphics.Point((r.ll.x + r.ur.x)/2, (r.ll.y + r.ur.y)/2), label)
    label.setSize(12)
    label.setFace("helvetica")
    label.setTextColor(properties["label_color"])
    label.draw(CANVAS)


def draw_label_svg(label: str, r: geometry.Rect, properties: dict):
    # Flip to orient y upward
    y_extent = CANVAS.height
    ll_y = y_extent - r.ur.y
    ur_y = y_extent - r.ll.y
    center_x = (r.ur.x + r.ll.x) // 2
    center_y = (ll_y + ur_y) // 2
    SVG_BUFFER.append(
    f"""<text x="{center_x}"  y="{center_y}"
         class="tile_label_{properties["label_color"]}" > {label} </text>
      """)


def wait_close():
    """Hold display on screen until user presses enter"""
    if SVG_BUFFER:
        SVG_BUFFER.append("</svg>")
        SVG_OUT.write("".join(SVG_BUFFER))
        SVG_OUT.close()
    print("Click window to close it")
    CANVAS.getMouse()
    CANVAS.close()

