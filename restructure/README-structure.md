# Structuring flat data

Sometimes we have just a flat collection of data but we want to 
impose a hierarchical structure on it based on an external source of 
information.  For example, we might have just a list of university 
major codes and counts of students, even though we know that the 
majors are grouped into departments, schools, colleges, etc.  The 
hierarchical structure is known to us, but it is not reflected in 
the data set.   We want to reorganize that flat data set into a 
hierarchical (tree-structured) data set. 

It is not too hard to reorganize one flat data set manually, but it 
is both tedious and error-prone to repeat the same reorganization 
multiple times.  Therefore, we would rather automate the 
reorganization based on a _schema_ that can be reused.  That's what 
this sub-project attempts. 

## The Schema

We parse a schema as a json file. The schema is the grouping 
structure we want to impose on the data, represented as a list of
dictionaries. For example, if we wanted to group eggs and milk as 
proteins, grains and root vegetables as starches, and further 
identify various foods as grains and root vegetables, we might 
take the following json structure as a schema: 

```python
{"protein":  ["milk", "eggs"]}, 
  {"starch": { "grain":  ["wheat", "buckwheet", "rye"], 
              "roots":  ["potato", "carrot", "turnip"] }}
```
Then, if our data set (in CSV form) is 
```text
potato,12
cabbage,2
eggs,3
carrot,4
```
We would produce a structure like 
```python
  { "starch": {
      "roots": {  "potato": 12,  "carrot": 4  }
    },
    "cabbage": 2,
    "protein": { "eggs": 3 }
}
```
Note: 
- the structured data is always a dictionary, which is printed
  as a text file in json format
-  the order of the produced structure reflects the data set 
   rather than the schema
- schema elements that are not represented in the data set are omitted
  from the structure.
- data elements that do not appear in the schema become roots of the 
  structured data forest

## Approach

For each leaf element of the schema, we construct an association of 
that leaf element to an _ancestry path_ from root to leaf.  This 
ancestry path guides insertion into the resulting structure. 

## Sample data sets

In addition to the example above (`sample-data.csv` and 
`sample-structure.json`), I have included `sample-major-counts.csv` 
based on Fall 2023 enrollment in CS 210 at U. Oregon, and 
`sample-majors-schema.json` based on the grouping of major codes at
that time.  