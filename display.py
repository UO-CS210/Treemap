"""Graphical display for treemapper.  Can produce
SVG file in addition to Tk display.
"""

import graphics.tk_display as tk
import graphics.svg_display as svg
import geometry
import color_contrast
from typing import Optional
import io

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def init(width: int, height: int, svg_path: str = None):
    tk.init(width, height)
    svg.init(width, height)

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
    tk.draw_rect(r.ll.x, r.ll.y, r.ur.x, r.ur.y, properties)
    svg.draw_rect(r.ll.x, r.ll.y, r.ur.x, r.ur.y, properties)
    llx, lly, urx, ury = r.ll.x, r.ll.y, r.ur.x, r.ur.y
    if label:
        tk.draw_label(label, llx, lly, urx, ury, properties)
        svg.draw_label(label, llx, lly, urx, ury, properties)

def begin_group(label: str, r: geometry.Rect):
    """A group contains multiple rectangular regions.
    Rendering may differ between SVG and Tk versions,
    but in both cases we want to show hierarchy.
    """
    # Allocate color whether or not we use it, to
    # maintain consistency between Tk display and SVG
    fill_color, stroke_color = color_contrast.next_color()
    # Tk version - outline the group in red
    # Label is not visible
    properties = {"margin": 2, "class": "group_outline"}
    properties["fill_color"] = None
    properties["stroke_color"] = "red"
    tk.draw_rect(r.ll.x, r.ll.y, r.ur.x, r.ur.y, properties)
    # SVG version - create SVG group
    properties["fill_color"] = fill_color
    properties["stroke_color"] = stroke_color
    svg.begin_group(label, r.ll.x, r.ll.y, r.ur.x, r.ur.y, properties)

def end_group():
    """Must be matched with begin_group"""
    # Tk:  Nothing to do
    # SVG: Ends the SVG group
    svg.end_group()



def outline_group(r: geometry.Rect):
    log.debug(f"Outlining {r}")
    properties = {"margin": 2, "class": "group_outline"}
    properties["fill_color"] = None
    properties["stroke_color"] = "red"
    tk.draw_rect(r.ll.x, r.ll.y, r.ur.x, r.ur.y, properties)
    svg.draw_rect(r.ll.x, r.ll.y, r.ur.x, r.ur.y, properties)



def wait_close():
    """Hold display on screen until user indicates finish"""
    svg.close()
    tk.wait_close()
