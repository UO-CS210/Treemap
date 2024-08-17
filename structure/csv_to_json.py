"""Extract the tree structure implied by a table (CSV format)
where some columns represent categories, subcategories, etc.,
and some columns (usually after the labels) are values (often numeric)
associated with leaf-level entries.
Output as nested dicts in JSON format.

Example input:
Program,Level,Course,SCH
CS,1xx,CS 102,376
CS,1xx,CS 110,976
CS,3xx,CS 330,320
CS,4xx,CS 407,40

Example output:
{ "CS": {
    "1xx": { "CS 102": 376,  "CS 110": 976 },
    "3xx": { "CS 330": 320 },
    "4xx": { "CS 407": 40 }}}

Transformation is guided by a configuration file in JSON format, e.g.
{
  "COMMENT" : "Configuration file for csv_to_json.py, gives schema of CSV file by listing column headers",
  "labels" : ["Program" ,"Level" , "Course"],
  "values" : ["SCH"]
}
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
    parser = argparse.ArgumentParser("Extract implied tree from CSV columns")
    parser.add_argument("schema", type=argparse.FileType(mode="r"),
                        help="JSON file specifying label and data columns")
    parser.add_argument("data", type=argparse.FileType(mode="r", encoding="utf-8-sig"),
                        nargs="?", default=sys.stdin,
                        help="Flat data file as CSV"
                        )
    parser.add_argument("output", type=argparse.FileType(mode="w"),
                        nargs="?", default=sys.stdout,
                        help="Json file representing restructured data")
    args = parser.parse_args()
    return args

columns = list[int] | list[str]

def load_schema(schema_file: io.IOBase) -> dict[str, columns]:
    """Configuration options we expect:
       "labels" -> non-empty list of column headers OR column numbers
       "values" -> non-empty list of column headers OR column numbers
       Each list must be homogenous ... do not mix column numbers and labels.
    """
    schema = json.load(schema_file)
    log.debug(f"Schema: \n{schema}")
    assert isinstance(schema, dict), f"Schema should be a dict with entries 'labels' and 'data'"
    return schema

nest = list[int] | dict[str, 'nest']

def insert(values: list[int], path: list[str], structure: dict):
    """Insert as value as structure[p1][p2][...][key] where pi are elements of path"""
    log.debug(f"Inserting {values} on path {path} in {structure}")
    if len(path) == 1:
        key = path[0]
        structure[key] = values
        return
    initial = path[0]
    suffix = path[1:]
    if initial not in structure:
        structure[initial] = {}
    insert(values, suffix, structure[initial])


def unflatten(flat: io.IOBase, schema: dict[str, columns]) -> dict:
    """Reshape flat CSV file into tree structure represented as nest of dictionaries.
    Rows that go in the tree are those with content in the data columns.
    Each label column is "sticky", i.e., when a column is empty, we assume it is a duplicate
    of the last non-empty value in that column, whether or not the previous row had
    data values.
    """
    reader = csv.DictReader(flat)
    labels = schema["labels"]
    values = schema["values"]

    #
    structure = {}
    row_labels = ["NA" for label in labels]

    for record in reader:
        for i,label in enumerate(labels):
            if record[label]:  # Retain "sticky" values when field is empty
                row_labels[i] = record[label]
            log.debug(f"Labels effectively {row_labels}")
        value_fields = [record[field] for field in values]
        if value_fields[0]:
            # This row has values to insert
            log.debug(f"Inserting {row_labels} -> {value_fields}")
            insert(value_fields, row_labels, structure)
    return structure



def main():
    args = cli()
    map = load_schema(args.schema)
    log.debug(f"Schema: {map}")
    structure = unflatten(args.data, map)
    # log.debug(f"Reshaped data: {json.dumps(structure, indent=3)}")
    print(json.dumps(structure, indent=3))

if __name__ == "__main__":
    main()
