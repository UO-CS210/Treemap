"""Align order of items in two nests (initially restricted to dicts)
Intended to be used in creating comparison treemaps, where we want layout to be compatible between the
two treemaps.  Reconciliation should take nests A and B and return A' and B' such that all the same
keys are present in both.
"""
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


# Non-recursive version, reconcile top-level dict keys only,
# inserting 0 values where there are missing keys.

def align(a: dict, b: dict) -> tuple[dict, dict]:
    """Returns pair a', b', the reconciled dicts, in an order
    that respects the order of each.
    """

    a_keys = list(a.keys())
    a_keys.reverse()   ## So popping is efficient
    b_keys = list(b.keys())
    b_keys.reverse()
    a_present = set(a_keys)
    b_present = set(b_keys)
    placed = set()

    a_aligned = {}
    b_aligned = {}

    def place(k: object):
        """Insert k into both dicts, defaulting to zero
        and recursively aligning their values if both are dicts.
        """
        a_val = a.get(k, 0)
        b_val = b.get(k, 0)
        if isinstance(a_val, dict) and isinstance(b_val, dict):
            a_val, b_val = align(a_val, b_val)
        a_aligned[k] = a_val
        b_aligned[k] = b_val
        placed.add(k)

    while a_keys and b_keys:
        log.debug(f"\n >{a_keys},\n  {b_keys}")
        # When one is exhausted, copy the
        # remainder of the other
        # Or one might already have been placed
        if a_keys[-1] in placed:
            # Can't happen?
            a_keys.pop()
        elif b_keys[-1] in placed:
            b_keys.pop()
        # They might be the same.
        elif a_keys[-1] == b_keys[-1]:
            place(a_keys.pop())
            b_keys.pop()
        # Or one or the other might not be shared
        elif a_keys[-1] not in b_present:
            place(a_keys.pop())
        elif b_keys[-1] not in a_present:
            place(b_keys.pop())
        # Both have keys that are present in both dicts,
        # but have not been placed yet.  Prioritize order of A.
        else:
            place(a_keys.pop())
    while a_keys:
        if a_keys[-1] not in placed:
            place(a_keys.pop())
        else:
            a_keys.pop()
    while b_keys:
        if b_keys[-1] not in placed:
            place(b_keys.pop())
        else:
            b_keys.pop()

    return a_aligned, b_aligned

d1 = {'a': {"ab": 2, "bc": 3}, 'b': 2, 'c': 4, 'd': 5}

d2 = {'y': 7, 'a': {"aa": 2, "ab": 3}, 'x': 6,   'd': 8, 'b': 4}

print(align(d1, d2))






