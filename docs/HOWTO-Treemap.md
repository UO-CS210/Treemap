# HOWTO build a treemap

A [_treemap_](https://en.wikipedia.org/wiki/Treemapping)
is a diagram that represents a collection of values by 
proportionally-sized tiles.  Tiles may also be grouped
to indicate hierarchical structure.  We will focus initially
on _tiling_ in part 1, then turn attention to _grouping_
in part 2 of this project. 

# Part 1: Tiling 

## Background

There are many variations on treemapping, but all are fundamentally 
built on recursively subdividing a collection of values while also 
subdividing the space to be tiled. For example, given the values
`[3, 9, 2, 4, 8]`, we might produce the diagram 

![Treemap of \[3, 9, 2, 4, 8\]](img/step-4.png)

The layout corresponds to a 
_tree_ of values. 

![Tree of values](img/tree.svg)

In the tree diagram, we can see the values to be tiled as leaves of 
the tree (represented as rectangles) with the individual values 3, 9,
2, 4, and 8.  Groups of nodes (which will be represented by groups 
of tiles) are represented by circles containing sums of tiles in 
each group.   Values 3 and 9 are grouped under a node 12 (3 + 9), 
2 and 4 grouped under 6, and 8 with the subgroup of 2 and 4 with
sum 14.  Finally, at the root of the tree, the value 26 represents 
subgroups with sums 12 and 14, which together include all the
values. The tile or group of tiles represented by each node is 
drawn in a size proportional to the value in the tree node 
representing that tile or group.  

![Tree nodes represent areas](img/tree-is-groups.png)

### Squarer is better

There are many ways we could divide a rectangle into tiles.  For 
example, we could simply slice it up either vertically or 
horizontally. 

![Tiling by slicing horizontally](img/slice-horizontally.png)

If we always slice the same way, we get long skinny tiles.  With a 
larger number of tiles, this becomes less and less useful. 

![Lots of tiles in one dimension](img/slice-lots-horizontally.png)

Slicing either horizontally or vertically can provide an aspect 
ratio (ratio of height to width) closer to 1.0, but is still not good. 

![Lots of tiles combining vertical and horizontal](img/slice-lots-alternating.png)

To do better, we need to divide the list of values into
better subgroups.  To "squarify" the tiles, we can repeatedly
subdivide the collection of values into groups that are as close as 
possible to equal in total. 

![Squarified treemap](img/squarify-lots.png)

### Balanced splits

We will provide better, more "squarified" treemaps by dividing each 
list of values at a point that minimizes the difference between the 
sum of the two parts.   This will not always be the middle of the 
list.  For example, suppose we want to divide the list
`[1, 1, 1, 1, 1, 5]` into two parts.  If we divided into `[1, 1, 1]`
and `[1, 1, 5]`, the sums would be 3 and 7.  Dividing into
`[1, 1, 1, 1, 1]` and `[5]` gives more balanced sums of 5 and 5.

### Example

Consider laying out a tiled diagram for `[3, 9, 2, 4, 8]` in a
square canvas, 750 by 750 units.  

The sum of values in `[3, 9, 2, 4, 8]` is 26, so we would like to 
divide it as close to possible to 13 + 13.  An exact split is not 
possible, but we can divide it into `[3, 9]` and
`[2, 4, 8]` (12 + 14).   We can make a corresponding division of the 
750 by 750 unit canvas into 346 by 750 (12/26 of the original 750 
unit width) and 
404 by 750 (14/26 of the original).  We will tile `[3, 9]` in the 
former and `[2, 4, 8]` in the latter. 

To lay out tiles for `[3, 9]` in the smaller of the two parts of the 
canvas, we again bisect it, in the only way possible as `[3]` and 
`[9]`.  The 346 by 750 region of the canvas is divided proportionally,
producing a 346 by 187 rectangle for `[3]`

![The first element is placed in a 346 by 187 rectangle](img/step-1-layout.png)

Similarly, `[9]` is placed in a 346 by 563 rectangle in the remaining 
part of the 346 by 750 region. 

![The second element is placed in a 346 by 563 rectangle](img/step-2-layout.png)

It remains to lay out `[2, 4, 8]` in the right side of the canvas.  
We bisect `[2, 4, 8]` into `[2, 4]` and `[8]`, (totals 6 and 8) and 
make a corresponding division of the canvas region.  `[2, 4]` is 
then bisected into `[2]` and `[4]`, again making corresponding 
divisions of the canvas region.  (Regions are split vertically if 
they are taller than they are wide, and horizontally otherwise.)

![The third and fourth elements are placed in their regions](img/step-3-layout.png)

This leaves just `[8]`, which is placed in the remaining portion of 
the canvas. 

![Final layout with 8 in the top right corner.](img/step-4-layout.png)

### Getting a start

First make sure you really understand the concept of dividing a 
list of values while making corresponding subdivisions of
a rectangular area.  Re-read the section above, more than once if 
you need to.  This is a general rule of program design:  You 
absolutely _must_ have a clear conceptual design before you start 
writing code.  That doesn't mean that you have worked out every 
detail of the design.  In most cases you will revise the design of 
your code multiple times as the consequences of your design 
decisions become apparent.  But you must have a clear concept of 
your solution strategy before you begin. Otherwise, your
muddy concept will  
mire your code so badly that you must abandon it and start over.

In what follows, I have provided some code that manipulates 
rectangles and their display on screen. It will be up to you to 
decompose a list of values and direct the corresponding 
decomposition of a rectangular canvas.  

### Geometry

I have provided a module `geometry.py` with `Point` and `Rect` 
(rectangle) classes.  A rectangle is defined by its lower left and 
upper right corners, in integer coordinates.  `Rect` provides a 
method `split` that returns two sub-rectangles in some proportion.  
For example, suppose we have decomposed `li = [2, 4, 3, 3]` into
`left = [2, 4]` and `right = [3, 3]`. To divide a 
rectangular region into subregions proportional to the parts of
the list, we could write

```python
    proportion = sum(left) / sum(li)
    left_rect, right_rect = rect.split(proportion)
```

Suppose the original `rect` has area 10.  This code would divide it 
into a rectangle `left_rect` with area 6, corresponding to the sum
the list `left`, and a rectangle `right_rect`, corresponding to the 
sum of list `right` (the remainder of the original list `li`). 

### Create the list splitting module

You will need to write a bisection function that 
takes a list of two or more positive integers and returns two sublists which together 
comprise the original list.  We will put it in its own source file. 

Start with a skeleton that enables logging and the `doctest` module 
for including test cases in function docstrings.  Save this in a 
file `splitter.py`:

```python
"""Split a list li of at least two positive integers into two balanced parts,
prefix and suffix, such that prefix+suffix == li and
abs(sum(prefix) - sum(suffix)) is minimized.

# Your instructor may ask you to identify yourself here
"""

import doctest

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

#  Your bisection function will go here. 

if __name__ == "__main__":
    doctest.testmod()
```

Importing `doctest` allows you to write test cases as part of
your function docstring.  The bit at the end
(`if __name__ == "__main__"`) runs the test cases when you
execute your `splitter.py` directly, but not when you import it
for use in another Python module like the `mapper.py` that we will
build shortly. 

The part from `import logging` through `log.setLevel(logging.DEBUG)` 
lets you write "log" messages in your code to help with debugging.  
Log messages are similar to print statements, but they have two 
important advantages.   First, you can suppress their output by 
changing the log "level".  Initially we have configured the logging 
package to print anything in a `log.debug("your message here")` 
statement.   Later, when you have successfully debugged this module, 
you don't have to remove or "comment out" those statements.  You can 
just change the level with `log.setLevel(logging.INFO)` to suppress
output from calls to`log.debug()`.  The second advantage of logging
is that the printed output comes with some extra identifying 
information.  For example, here is some log output from my 
implementation: 

```text
DEBUG:splitter:[1]|[2, 1]
DEBUG:splitter:(Exclude item at split)
```

Initially this may not seem like much of an advantage.  Why would 
you need to know that the log message came from `splitter.py`?  As 
you progress farther in programming, building programs composed of 
many source code files working together, the identifying information 
becomes essential. 

Now you should add the header of the `bisect` function, including 
test cases, with a dummy body. 

```python
def bisect(li: list[int]) -> tuple[list[int], list[int]]:
    """Returns (prefix, suffix) such that prefix+suffix == li
    and abs(sum(prefix) - sum(suffix)) is minimal.
    Breaks tie in favor of earlier split, e.g., bisect([1,5,1]) == ([1], [5, 1]).
    Requires len(li) >= 2, and all elements of li positive.

    >>> bisect([1, 1, 2])  # Perfect balance
    ([1, 1], [2])
    >>> bisect([2, 1, 1])  # Perfect balance
    ([2], [1, 1])
    >>> bisect([1, 2, 1])  # Equally bad either way; split before pivot
    ([1], [2, 1])
    >>> bisect([6, 5, 4, 3, 2, 1])  # Must include element at split
    ([6, 5], [4, 3, 2, 1])
    >>> bisect([1, 2, 3, 4, 5])
    ([1, 2, 3], [4, 5])
    """
    assert len(li) >= 2, f"Cannot bisect {li}; length must be at least 2"
    log.debug(f"Bisecting {li}")
    return ([], [])  # FIXME:  Replace this with implementation
```

There are several things to notice about this function header: 
- It specifies that `bisect` takes one argument, which should be
  a list of integers.  The Python interpreter will not check this,
  unfortunately, but you may be using other tools such as 
  an interactive development environment (IDE)
  like VS Code or PyCharm that provides type annotation checking.
- It specifies that `bisect` will return _two_ integer values in a
  tuple.  This is a handy feature of Python ... we can write
  `return a, b` to return the values of `a` and `b` together in a 
  tuple. 
- The type annotations do not specify that the input list must
  have at least two elements, and that all of them must be
  _positive_ integers, or that the result should be two parts of the
  original list in the same order, with balanced sums.  Type 
  annotations are not powerful enough to specify these _semantic_ 
  properties, so they are instead stated succinctly in the docstring 
  comment.  "_Succinctly_" is not incidental here:  The docstring 
  should serve as quick reference documentation for another 
  programmer who wants to reuse your code.
- Following the main docstring, we have included a set of 
  _doctest_ test cases to check our implementation.  Passing
  these test cases will not guarantee that your implementation
  is correct; no finite set of test cases can do that.  They will,
  however, catch many simple and common bugs.
- The first statement in the body of the function is an
  `assert` statement that checks to be sure `bisect` has been
  called with a list of at least two elements.  It does not
  check all the required properties of `li`, which would require
  more elaborate code, but it is a little bit of _defensive 
  programming_ to make debugging easier. 
- We initially write a dummy body (always returning `([], []))` 
  regardless of the input argument) so that we can start testing
  even _before_ we have written the real function body. 

### Checkpoint

At this point you should check to your work.  We don't expect our 
test cases to succeed.  In fact they should all fail. We just want 
to ascertain that we haven't made any fatal typos or syntax errors. 
You should run `splitter.py`, and expect to see output that looks 
like this: 

```doctest
DEBUG:__main__:Bisecting [1, 1, 2]
**********************************************************************
File "/Users/michal/Dropbox/23F-210/projects/Treemap/splitter.py", line 20, in __main__.bisect
Failed example:
    bisect([1, 1, 2])  # Perfect balance
Expected:
    ([1, 1], [2])
Got:
    ([], [])
... lots more like that 
**********************************************************************
1 items had failures:
   5 of   5 in __main__.bisect
***Test Failed*** 5 failures.
```

That's fine! It's what we expected!  

On the other hand, if your output looks like this:
```doctest
  File "/Users/michal/Dropbox/23F-210/projects/Treemap/splitter.py", line 14
    def bisect(li: list[int]) -> tuple[list[int, list[int]]:
                                      ^
SyntaxError: '[' was never closed
```
or like this: 
```doctest
Error
**********************************************************************
File "/Your/file/path/here", line 20, in splitter.bisect
Failed example:
    bisect([1, 1, 2])  # Perfect balance
Exception raised:
    Traceback (most recent call last):
      ... more stuff here
      File "/Your/file/path/here", line 34, in bisect
        retrun ([], [])  # FIXME:  Replace this with implementation
    NameError: name 'retrun' is not defined
```
 
then you have an error that is best to repair now, before you start 
work writing your bisection code. 

When you have only test _failures_ and no more test _errors_, we can 
move on to the next step. 

### Finding our balance

How can we divide a list of positive integers in a balanced way, 
considering the _sums_ of the two parts rather than their _length_?
We can find the smallest index _i_ such that `sum(li[:i+1])` is 
greater than half the sum of the whole list `li`.  

Consider if `li` is  `[1, 2, 3, 4, 5, 6]`, which has sum 21. 
The _i_ we seek would be 4, because `li[:4]` is `[1, 2, 3, 4]`, with 
sum 10, a little less than half of 21, and `li[:5]`, which is
`[1, 2, 3, 4, 5]`, sums to 15.   

Can we be sure that such an _i_ will always exist?
Provided all the 
elements of `li` are positive and `len(li) > 1`, we can be sure 
that `sum(li) > sum(li)/2`.  Since `li[:len(li)+1]` is the same as 
`li`, we know that there is some _i_ in `range(len(i))` such that `sum(li[:i+1])` is 
greater than half the sum of the whole list.  We just need to find
the _smallest_ such _i_, which we can do by looping through the 
indexes of `li`. 

Our first cut at the bisection algorithm might apply this property 
directly: 

```python
    for i in range(len(li)):
        if sum(li[:i+1]) > sum(li) / 2:
            break
    return li[:i], li[i:]
```

This solution uses notation like `li[:i]` to denote the _slice_ of 
the list from `li[0]` up to but not including `li[i]`, and `li[i:]` 
to denote  the slice starting at `li[i]` and including the rest of 
the list.  If you are not familiar with slices, try a few examples 
in the Python console: 

```pycon
PyDev console: starting.
>>> my_list = [1, 2, 3]
>>> my_list[1:]
[2, 3]
>>> my_list[:1]
[1]
>>> my_list[3:]
[]
>>> my_list[1:3]
[2, 3]
```

When we execute our program, some of our doctests will succeed, but 
one will fail: 

```pycon
Failed example:
    bisect([6, 5, 4, 3, 2, 1])  # Must include element at split
Expected:
    ([6, 5], [4, 3, 2, 1])
Got:
    ([6], [5, 4, 3, 2, 1])
```

In this example, splitting into a part that sums to 11 and 
another that sums to 10 is better than splitting into 6 and 15.  It 
appears that we must add a check in our function to determine 
whether `li[i]` should be included or excluded from the first part.

We can make the needed adjustment with a few lines of code.  There 
are two possibilities.  We could split `li` into `li[:i]` and 
`li[i:]` (excluding `li[i]` from the first part and including it in 
the second), or we could split into `li[:i+1]` and `li[i+1:]`, 
placing item `i` in the first part.  We want the first part to come 
as close to half the sum of `li` as possible, which we can determine
by subtracting each sum from `sum(li)/2` and comparing the absolute 
value of the differences.   I leave that to you. 

### Too slow! 

There is another problem with our first solution: Although `sum` is a 
built-in Python function, internally it is a 
loop that works as if you had written 

```python
def sum(li: list[int]) -> int: 
    total = 0
    for i in range(len(li)):
        total = total + li[i]
    return total
```

Consider that this `sum` function is called each time through the 
loop in our `bisect` function.  How many times is the statement 
`total = total + li[i]` executed?

Suppose the `li` is `[1, 1, 1, 1, 10]`, which is the worst case in 
which our loop sums each slice up to the last.  To simplify our 
reasoning, we'll consider only the call to `sum(li)`, which sums the 
whole list each time.  Since our loop will execute 5 times (once for 
each item in the list), and we will loop through the whole list to 
sum it each time, this will be 25 additions.  That doesn't sound bad,
but now imagine our list has 100 elements. 100 times 100 is 10,000.  
A list of 1000 elements will perform 1,000,000 additions, and so on: 
The number of operations is growing proportionally to the _square_ 
of the length of the list.  This is called a _quadratic_ growth 
pattern, which is something we'd like to avoid if we can. 

We do not have a doctest to determine whether our implementation of 
`bisect` is fast enough, but I have included such a test case in a 
separate testing script, `test_splitter.py`.  The speed test times 
bisection of a list of 50,001 integers.  It checks to be sure the 
function executes in less than a second.  Try it: 

```commandline
python3 test_splitter.py
```

On my vintage 2020 M1 
Macbook Pro, our first implementation fails the speed test with 
messages that look something like this: 

```pycon
DEBUG:test_splitter:Splitting 50001 items in 20.64364004135132 seconds
Ran 9 tests in 20.648s
FAILED (failures=1)

Failure
Traceback (most recent call last):
  File "/your/path/test_splitter.py", line 78, in test_fast_enough
    self.assertLess(elapsed, 1.0)
AssertionError: 20.64364004135132 not less than 1.0
```

### Faster! 

We can do much better by calculating a list of _partial sums_.
Consider the list `[1, 2, 3, 4, 5]`; the corresponding list of 
partial sums is `[1, 3, 6, 10, 15]`, i.e., `partials[i]` is equal to 
`sum(li[:i+1])`.  The trick is that we don't need to call the `sum` 
function for each element `i`.  Instead, we can keep a running total.
For example, the partial sum at index 3 is the partial sum at index 
2 plus the item at index 3. 

|  list    | i=0 | i=1 | i=2| i=3| i=4 |
|----------|-----|-----|----|----|-----|
| li:      |   1 |  2  |  3 |  4 |  5  |
|partials: |   1 |  3  |  6 | 10 | 15  |

We can create this list in one "pass", looping through `li` while 
keeping a running total and appending the running total to a new 
list `partials`.   

After we have created the list `partials`, we can make one more loop 
(after the first loop, not inside it) to find the element `i` at 
at the balance point 
where `partials[i]` is first greater than `sum(li) // 2`.  Don't 
call `sum(li) // 2` each time through the loop! Compute it just once, 
store it in a variable, and use it over and over in the loop.  You 
already have `sum(li)` as the last of the partial sums you 
calculated above, so you can reuse that.  

When you have replaced the _quadratic time_ algorithm that
called `sum(li)` each time through the loop
each time through the loop with a _linear time_ algorithm that
just checks the precomputed partial sum at each position, your 
code will run much faster on long lists.  The timing test case in
`test_splitter.py` should now bisect a list of 50,001 items in
a fraction of a second: 

```pycon
Launching unittests with arguments python -m unittest /your_path/test_splitter.py  
DEBUG:test_splitter:Splitting 50001 items in 0.009398937225341797 seconds
Ran 9 tests in 0.011s
OK
```

### Checkpoint: Summary of your work so far

So far you have created a function `bisect` in a new file
`splitter.py`.  This function takes a list of at least two
positive integers.  It returns _two_ results as a tuple.
The first result and the second result together comprise the input 
list, and their sum is as close as possible to equal. 
You have created a 
linear time algorithm that first
creates a list of partial sums, then in a separate loop finds the 
index of the first element of the partial sum that is greater than 
the sum of all the elements of the list being bisected.  Finally it 
chooses to include that element in the first part or not.  

All the doctests in `splitter.py` should now pass when you execute 
`splitter.py` by itself.  The test cases in `test_splitter.py` 
include those and a few more, including a speed test.  All the test 
cases in `test_splitter.py` should also pass. 

### Laying tile

Now that we can split a list of positive integers into two balanced 
parts, let's use it over and over to tile a rectangular area.  Start 
by making a copy of `mapper-skel.py` in a new file `mapper.py`.  
This program should "work" in the sense that it can produce a (very 
bad) treemap by simply slicing off one rectangle for each data 
element in a list.  Try it: 
```commandline
> python3 mapper.py data/medium_flat.json 500 500
```
You should see a tiling that is dominated by skinny rectangles: 
![Output of skeleton program](img/skel_output.svg)

This diagram is drawn as the program runs and also saved in SVG 
format as `output.svg`.   Colors may vary as they are generated 
randomly.  If you run the same program again, you will see a 
different selection of colors. Click the program display to close it. 

While the `geometry` module always splits a rectangle in the 
narrower dimension, we nonetheless get a very poor layout because of 
the way the `layout` function loops through the list of values, 
simply drawing one rectangle after another. 

```python
def layout(li: list[int], rect: geometry.Rect):
    """Lay elements of li out in rectangle. Version 0.
    """
    while len(li) > 0:
        proportion = li[0] / sum(li)
        left_rect, rect = rect.split(proportion)
        display.draw_tile(left_rect, li[0])
        li = li[1:]
```

Splitting the list into balanced parts, using the `bisect` function 
you just completed, can provide a much better layout.  We'll want to 
divide the rectangular area into two parts proportional to the sums 
of the lists returned by `bisect`, similar to the proportional 
splitting in the skeleton code.  Then we'll need to lay out each of 
the two lists. Since we may need to split each of those lists again, 
a simple loop will not suffice.   The problem is inherently 
_recursive_. 

In any recursive algorithm, we must identify one or more base cases 
and one or more recursive cases.  The base case for recursive tiling 
of a list of integer values is simple:  If the list contains a 
single value, it takes the whole rectangle:
```python
    display.draw(rect, li[0])
```

The recursive case uses the `bisect` function: 
```python
  left, right = splitter.bisect(li)
```

Here I am calling the parts "left" and "right", but they might be 
layed out either horizontally or vertically, depending on the choice 
made by `rect.split`.  

In the recursive case we will _two_ recursive calls:  One to tile 
the sub-list `left` in one part of the provided rectangle, and one 
more to tile the sub-list `right`. 

That is enough information to write a recursive version of `layout`. 
Do that now, and the same command above should produce a much nicer
treemap: 

![Result of tiling `data/medium_flat.json`](img/part1-result.svg)

### Checkpoint

This concludes part 1 of the project.  You should now have a 
function `bisect` in `splitter.py` and a function `layout` in 
`mapper.py` that together produce treemaps like the illustration 
above from lists of integers in JSON files like
`data/medium_flat.json`.   This might be a good time for a 
little rest, a cup of tea or coffee, a refreshing walk, or
tackling some reading for another class. 

Part 2 will consider richer data sources with hierarchical structure 
that we wish to preserve in the treemap. 






