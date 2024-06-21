"""Structure a flat data set (CSV format) as guided by a schema (json format).
See README-structure.md for detail.
M Young, 2024-06-19
"""
import json
import csv
import argparse
import io

import logging
import sys

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def cli() -> object:
    """Command line interface"""
    parser = argparse.ArgumentParser("Structure CSV data guided by json schema")
    parser.add_argument("schema", type=argparse.FileType(mode="r"),
                        help="Schema expressed as json; see README-structure.md for details")
    parser.add_argument("data", type=argparse.FileType(mode="r"),
                        nargs="?", default=sys.stdin,
                        help="Flat data file as CSV with each line being string, int for category, quantity"
                        )
    parser.add_argument("output", type=argparse.FileType(mode="w"),
                        nargs="?", default=sys.stdout,
                        help="Json file representing restructured data")
    args = parser.parse_args()
    return args

def parse_schema(schema_file: io.IOBase) -> dict[str, list[str]]:
    """Construct map from category to ancestry chain from elements of schema
    expressed as json.
    """
    map = { }
    schema = json.load(schema_file)
    log.debug(f"Schema: \n{schema}")
    assert isinstance(schema, list), f"Schema should be a list of dictionaries"

    def build_chains(prefix: list[str], element):
        """Build chains from this element downward through structure"""
        log.debug(f"Tracing ancestor chain {prefix} through {element}")
        if isinstance(element, str):
            map[element] = prefix.copy()
            log.debug(f"Added {element}: {prefix} to map")
        elif isinstance(element, list):
            for item in element:
                build_chains(prefix, item)
        elif isinstance(element, dict):
            for group, part in element.items():
                prefix.append(group)
                build_chains(prefix, part)
                prefix.pop()
        else:
            assert False, f"Trouble in schema, encountered {element}"

    for root in schema:
        build_chains([], root)
    return map

def insert(key: str, value: int, path: list[str], structure: dict):
    """Insert as value as structure[p1][p2][...][key] where pi are elements of path"""
    log.debug(f"Inserting {key}:{value} on path {path} in {structure}")
    if len(path) == 0:
        structure[key] = value
        return
    initial = path[0]
    suffix = path[1:]
    if initial not in structure:
        structure[initial] = {}
    insert(key, value, suffix, structure[initial])


def reshape(flat: io.IOBase, paths: dict[str, list[str]]) -> dict:
    """Reshape flat CSV file into tree structure represented as nest of dictionaries."""
    structure = {}
    reader = csv.reader(flat)
    for record in reader:
        log.debug(f"Interpreting CSV line as {record}")
        key, value = record[:2]
        if key in paths:
            path = paths[key]
        else:
            path = []
        insert(key, int(value), path, structure)
    return structure


def main():
    args = cli()
    map = parse_schema(args.schema)
    log.debug(f"Ancestry map: {map}")
    structure = reshape(args.data, map)
    # log.debug(f"Reshaped data: {json.dumps(structure, indent=3)}")
    print(json.dumps(structure, indent=3))

if __name__ == "__main__":
    main()
