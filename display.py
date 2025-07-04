"""Graphical display for treemapper.  Can produce
SVG file in addition to Tk display.

Note we are using modules (display, tk_display, svg_display) as stateful objects,
which makes them "singletons".   To allow multiple instances of display would require
rewrite of all three modules to isolate state in objects managed by other code.
"""

import graphics.tk_display as tk
import graphics.svg_display as svg
import graphics.gr_display as gr
import geometry
from graphics import display_options as options
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
"""

# ------
# Tk display requires us to keep a stack of keys so that we can
# inherit graphical attributes from a parent.
#
INCLUSION_STACK: list[str] = []  # Initially empty

def lookup_colors(key: str) -> tuple[str, str]:
    """Finds nearest color for key or enclosing key on inclusion stack."""
    if key in options.color_scheme:
        return options.color_scheme[key]
    for enclosing in reversed(INCLUSION_STACK):
        if enclosing in options.color_scheme:
            return options.color_scheme[enclosing]
    # Not mapped in any enclosing object.  Generate a random color pair.
    # We memoize the assignment for two reasons:  So we can propagate it if
    # we are coloring a group, and so we will use the same color if we encounter
    # the same key again.   Exception:  None or "" don't get an assigned color,
    # and don't propagate to parts.
    fill, text = color_contrast.next_color()
    if key:
        options.color_scheme[key] = (fill, text)
    return fill, text


def pop_color():
    INCLUSION_STACK.pop()


# ------
#  V2, Summer 25
def draw_tile(r: geometry.Rect,
              key: str | None = None,
              value: str | None = None):
    """Draw the tile (on both media).
     Displays on Tk (Python built-in graphics) and
     also writes corresponding graphics into buffer to
     produce corresponding SVG diagram which can be displayed
     in a web page, imported into a diagramming tool like
     Inkscape, OmniGraffle, Illustrator, etc.
     `key`, if present, is normalized to become the class name
     for SVG CSS class and/or the Tk color assignment table.
    """
    log.debug(f"Drawing tile key {key} value {value} at {r}")
    # fill_color and label_color will be used in tk graphics,
    # and also in SVG graphics ONLY if the user hasn't provided a CSS stylesheet
    fill_color, label_color = lookup_colors(key)
    label = f"{key}\n{value}"
    tile = gr.Rectangular(key,
                          ((r.ll.x, r.ll.y), (r.ur.x, r.ur.y)),
                          label=label, fill_color=fill_color, label_color=label_color)

    tk.draw_tile(tile)
    svg.draw_tile(tile)


# V2, summer 25
def begin_group(r: geometry.Rect,
                key: str | None = None,
                value: str | None = None):
    """
    Begin a group of tiles. The `key` argument, if present,
    is normalized to become the class name for SVG CSS and/or
    the Tk color assignment table.  The (key, value) pair may not
    be directly visible, but if either `key` or `value` is present
    it will be displayed as a tooltip in SVG.
    """
    global INCLUSION_STACK
    INCLUSION_STACK.append(key)  # FIXME: Whoops, do we need the random color on the stack?
    fill_color, label_color = lookup_colors(key)
    if value:
        label = f"{key}: {value}"
    else:
        label = f"{key}"
    region = gr.Rectangular(key, ((r.ll.x, r.ll.y),(r.ur.x, r.ur.y)),
                            label=label, fill_color=fill_color, label_color=label_color)
    # SVG version - create SVG group
    # Note fill and label colors will be ignored if we have a CSS stylesheet
    svg.begin_group(region)

def end_group():
    """Must be matched with begin_group"""
    # Tk:  Nothing to do
    # SVG: Ends the SVG group
    INCLUSION_STACK.pop()
    svg.end_group()



def normalize_key(key: str) -> str:
    """Extract a suitable and predictable key from a category name.
    We extract as first line, replacing spaces by underscores, and
    removing any other non-alphanumeric characters.
    The result is usable as a dict key (for Tk color schemes)
     and CSS classes (to use in the SVG output).
    """
    basis = key.split()[0]
    if not basis[0].isalpha():
        basis = "C_" + basis
    chars = [ch for ch in basis if ch.isalnum()]
    return "".join(chars)


def wait_close():
    """Hold display on screen until user indicates finish"""
    svg.close()
    tk.wait_close()
