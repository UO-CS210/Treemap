# JSON pretty-printer

The JSON pretty-printer project is an alternative or add-on to the 
Treemap project.  It is intended to serve as an alternative for 
visually impaired students who rely on screen readers or other 
non-visual access to computer output.  It can also be used as an 
additional mini-project for students who have completed the Treemap 
project, reinforcing the key concept of traversing and summarizing 
recursive data structures (nested dicts, lists, and tuples in Python).

As in the Treemap project, we will recursively traverse a nested 
data structure obtained by reading a JSON file.  As in the Treemap 
project, we will make decisions based on summaries of structure.  
While the Treemap project summarizes quantities in nested 
categorical data, summaries in the JSON pretty-printer will 
represent the horizontal width required to print a portion of the 
data in JSON format.

The current (summer 2025, Python 3.12) version of json provides two 
options for the `dumps` method:  All on one line, or every item at 
every level on a line of its own.   `js_pretty` provides finer grain 
control, placing multiple items on a line _if they fit_. 

