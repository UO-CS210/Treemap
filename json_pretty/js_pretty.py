"""Pretty printer for json (first cut, incomplete)"""

# import json
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

TINY = {"a": 1}
BITTY = [1, "a"]
SHORT = { "a": 12, "b": [1, 2, 3]}
MED = { "a": 12, "b": [1, 2, 3, 4],
         "c": "sample",
         "d": [2, 4, 6, 8]}

LONG = { "a": 12, "b": [1, 2, 3, 4],  "c": "sample", "d": [2, 4, 6, 8], "e": [19, 32, 46, 84],
         "f": "getting a bit long", "g": "not going to fit on one line", "h": "Whoa, hold on",
         "i": ["Really needs to be broken", "into multiple lines"]}

type Nest = (str | int | float | bool |
                list[Nest] | tuple[Nest] | dict[str, Nest] )

def width(nest: Nest) -> int:
    """repr does the recursion for us."""
    return len(repr(nest))


def recwidth(nest: Nest) -> int:
    """Full length of printed version if on a single line"""
    # Base cases
    if isinstance(nest, (int | float | bool )):
        return len(str(nest))
    elif isinstance(nest, str):
        # Needs room for quote marks
        return len(nest) + 2

    # Recursive cases
    if isinstance(nest, (tuple, list)):
        # Sum of element lengths + ", " between elements and "[]"
        parts = sum(width(el) for el in nest)
        seps = 2*max(0, len(nest) - 1)
        brackets = 2
        return parts + seps + brackets
    if isinstance(nest, dict):
        # Almost the same, but each item is "k": v
        # So we add 2 for ": " and 2 for ", "
        parts = 0
        for key, value in nest.items():
            parts += width(key) + width(value) + 2  # 2 is for ": "
        seps = 2 * max(len(nest) - 1, 0)  # for ", " between items
        brackets = 2
        return parts + seps + brackets


def diagnose(nest: Nest):
    as_string = repr(nest)
    print(f"Predict {width(nest)}, actual {len(as_string)}")
    print(as_string)
    print()


def compact(nest: Nest, indent=4, width=72) -> str:
    """Produce a compact string representation of a nested structure
    in JSON-compatible format.
    """

    def layout(nest: Nest, level=0):
        """Recursively place portions of nest into lines buffer,
        breaking into indented regions as needed.
        """
        indentation = " " * level * indent
        if isinstance(nest, (int, float, bool, str)):  # Atomic types
            lines.append(indentation + repr(nest))
            return
        # Also anything that can fit in one line
        if len(repr(nest)) + len(indentation) <= width:
            lines.append(indentation + repr(nest))
            return

        assert(isinstance(nest, (list, tuple, dict))), f"Can't convert {type(nest)} to json format"

        # Lists and tuples are both represented in JSON as lists
        if isinstance(nest, (list, tuple)):
            # We already know the whole list or tuple is too long, so we'll break
            # it into lines.  Initial version puts brackets on separate lines. FIXME.
            lines.append(indentation + "[")
            for el in nest:
                layout(el, level + 1)
            lines.append(indentation + "]")
            return

        if isinstance(nest, dict):
            # Note breaking into tuples with ".items()" does NOT get what I want.
            # FIXME:  find tactic for formatting dictionary entries
            lines.append(indentation + "{")
            for el in nest.items():
                layout(el, level + 1)
            lines.append(indentation + "}")
            return

        assert False, "Can't get here, this should be unreachable"

    # Main body of compact
    lines = []
    layout(nest, level=0)
    return "\n".join(lines)










def main():
    diagnose("a")
    diagnose("string")
    diagnose(24)
    diagnose(TINY)
    diagnose(BITTY)
    diagnose(SHORT)
    diagnose(MED)

    print(compact(TINY))
    print(compact(BITTY))
    print(compact(SHORT))
    print(compact(MED))

    print("Default width and indent")
    print(compact(LONG))
    print("Short lines")
    print(compact(LONG, width=30))
    print("Short lines and long indents")
    print(compact(LONG, indent=8, width=30))

if __name__ == "__main__":
    main()
