"""
Tk (built-in Python graphics package) display of Treemap canvas.
"""

from . import graphics  # Zelle's Tk graphics package

from treemap_options import options

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

CANVAS: graphics.GraphWin | None = None

def init(width: int, height: int):
    global CANVAS
    CANVAS = graphics.GraphWin("Treemap", width, height)
    CANVAS.setCoords(0, 0, width, height)


def draw_rect(llx, lly, urx, ury, properties: dict):
    """Draw and label the rectangle on the Tk (Python built-in) display.
    Flips y axis (0 is at top).
    """
    assert CANVAS, "Did you forget to initialize the window?"
    margin = properties["margin"]
    lly_flipped = CANVAS.height - lly
    ury_flipped = CANVAS.height - ury
    image = graphics.Rectangle(graphics.Point(llx+margin, lly_flipped-margin),
                              graphics.Point(urx-margin,ury_flipped+margin))
    fill = properties["fill_color"]
    if fill:
        image.setFill(fill)
    stroke = properties["stroke_color"]
    if stroke:
        image.setOutline(stroke)
    image.draw(CANVAS)

# Text size estimates borrowed from svg_display.  Could be different
# in future depending on text sizes.  Can we actually measure the size
# of the text?
CHAR_WIDTH_APPROX = 12  # Rough approximation of average character width in pixels
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
    # Too wide?
    if text_width_roughly(label) > urx - llx:
        return False
    # Too tall?
    if len(label.split()) * LINE_HEIGHT_APPROX > ury - lly:
        return False
    return True


def draw_label(label: str, llx: int, lly: int, urx: int, ury: int, properties: dict):
    if not options["messy"] and not label_fits(label, llx, lly, urx, ury):
        return
    lly_flipped = CANVAS.height - lly
    ury_flipped = CANVAS.height - ury
    label = graphics.Text(graphics.Point((llx + urx)/2, (lly_flipped + ury_flipped)/2), label)
    label.setSize(12)
    label.setFace("helvetica")
    label.setTextColor(properties["label_color"])
    label.draw(CANVAS)


def wait_close():
    """Hold display on screen until user clicks"""
    print("Click window to close it")
    CANVAS.getMouse()
    CANVAS.close()


