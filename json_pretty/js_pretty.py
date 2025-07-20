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


def main():
    diagnose("a")
    diagnose("string")
    diagnose(24)
    diagnose(TINY)
    diagnose(BITTY)
    diagnose(SHORT)
    diagnose(MED)


if __name__ == "__main__":
    main()
