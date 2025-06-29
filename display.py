"""Graphical display for treemapper.  Can produce
SVG file in addition to Tk display.

Note we are using modules (display, tk_display, svg_display) as stateful objects,
which makes them "singletons".   To allow multiple instances of display would require
rewrite of all three modules to isolate state in objects managed by other code.
"""

import graphics.tk_display as tk
import graphics.svg_display as svg
import geometry
import color_contrast

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def init(width: int, height: int):
    tk.init(width, height)
    svg.init(width, height)

"""Tactics for drawing on Tk and SVG (and potentially others in future): 

Attributes that can be computed once and then interpreted for each medium
are kept in a property table, rather than passing a whole zoo of parameters
to each medium-specific drawing function.

For now, colors are randomly generated for each group or top-level individual tile.
"""

# ------
# Each color entry is fill color, label color.
# In SVG we should use CSS inheritance to manage inheritance of
# tile color from groups, but for Tk we have to keep our own stack
# of group colors.
#
COLOR_STACK: list[tuple[str, str]] = []  # Initially empty

def push_new_color():
    COLOR_STACK.append(color_contrast.next_color())

def pop_color():
    COLOR_STACK.pop()

def set_tile_color(properties: dict):
    """Adds tile color properties"""
    if len(COLOR_STACK) > 0:
        fill_color, label_color = COLOR_STACK[-1]
    else:
        fill_color, label_color = color_contrast.next_color()
    properties["fill_color"] = fill_color
    properties["stroke_color"] = "white"
    properties["label_color"] = label_color

# ------

def draw_tile(r: geometry.Rect,
              label: str | None = None,
              tags: list[str] | None = None):
    """Draw the tile (on both media).
     Displays on Tk (Python built-in graphics) and
     also writes corresponding graphics into buffer to
     produce corresponding SVG diagram which can be displayed
     in a web page, imported into a diagramming tool like
     Inkscape, OmniGraffle, Illustrator, etc.
     Tags can be used to indicate additional SVG classes for style sheets.
    """
    log.debug(f"Drawing {r}")
    properties = {"margin": 4, "class": "tile"}
    if label:
        properties["label"] = label
    if tags:
        properties["tags"] = " ".join(tags)
    # fill_color and label_color will be used in tk graphics,
    # and also in SVG graphics ONLY if the user hasn't provided a CSS stylesheet
    fill_color, label_color = color_contrast.next_color()
    set_tile_color(properties)
    tk.draw_rect(r.ll.x, r.ll.y, r.ur.x, r.ur.y, properties)
    svg.draw_tile(r.ll.x, r.ll.y, r.ur.x, r.ur.y, properties)
    llx, lly, urx, ury = r.ll.x, r.ll.y, r.ur.x, r.ur.y
    if label:
        tk.draw_label(label, llx, lly, urx, ury, properties)
        # svg label drawing is now within svg.draw_rect so that
        # a label can be a tool-tip if it doesn't fit in rectangle
        # svg.draw_label(label, llx, lly, urx, ury, properties)

def begin_group(r: geometry.Rect, label: str | None = None):
    """A group contains multiple rectangular regions.
    Rendering may differ between SVG and Tk versions,
    but in both cases we want to show hierarchy.
    The optional label appears as a tool-tip in the SVG version.
    """
    if not label:
        label = ""
    push_new_color()
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
    set_tile_color(properties)
    svg.begin_group(label, r.ll.x, r.ll.y, r.ur.x, r.ur.y, properties)

def end_group():
    """Must be matched with begin_group"""
    # Tk:  Nothing to do
    # SVG: Ends the SVG group
    pop_color()
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
