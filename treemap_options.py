"""Options for treemap display.
We keep these in the form of a "property list", that is, a dict with properties as keys
and property values as settings.   Options can be set by main driver program and accessed
by other modules whose behavior they control.  Some options may apply to only some display media,
e.g., CSS stylesheets apply to SVG but not to Tk graphics.

Keeping these options as a dict rather than a set of individual variables makes it convenient to
check whether an option has been set at all.

Usage:
from treemap_options import options
...
if options.get(prop_name, False):
    # this code executed only if prop_name exists AND has a truthy value

"""

options = { # Non-default values set by treemap.py or other main program
}

