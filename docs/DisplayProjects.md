# Beyond Treemaps: Project Ideas

There are many other ways to extend this project.  Here are a few.  
These are _much_ more challenging than completing the project.  They are 
not little "extra credit" extensions, but rather full-blown projects 
on their own.  If you 
want to tackle one of them, I suggest first trying to devise a plan 
of attack on your own, and then discussing it with your instructor 
before diving in. 

## User-defined color schemes

The `display` module of this project chooses colors randomly. Often 
they are ugly, and they never convey semantic information. You could 
make color choices based on a separate _style sheet_, which could be 
a dictionary with the same hierarchical structure as the data.  This 
would be particularly useful if you wanted to use a consistent color 
scheme for two treemaps to compare the distribution of values at one 
time with the distribution of values in the same categories at a 
different time.

## Comparable treemaps

If you want to compare treemaps of related data, you might also want 
to account for difference in total area and grouping.  Suppose, for 
example, we wanted to compare the distribution of student majors 
between different academic terms. Total enrollment between those 
terms might be different, so we might want to scale one of the 
overall dimensions (height or width of the treemap as a whole) 
accordingly.  We might also want to record the `bisect` decisions in 
one run and replay them in another, for consistent grouping. 

## Appropriate use of treemaps and other displays

Here is an open-ended mission for a student with a strong interest 
in data visualization and a willingness to study human perception. 

You can find many data analysis tools that offer treemap displays.  
If you read their documentation, you will find much of it devoted to 
warning against using treemaps inappropriately.  For example, 
a simple bar graph is much better than a treemap for making precise 
comparisons.  Consider how hard it is to see that vanilla and 
chocolate have the same area in the `tiny_categorical.json` data set: 

![Chocolate and vanilla are both 10](
img/tiny_categorical.svg)

On the other hand, treemaps can be useful for quickly grasping 
quantitative part/whole relationships, like seeing that the biomass 
of eukaryotes as a group are a very large fraction of the biomass of 
the oceans, or that students majoring in the natural sciences outnumber 
students majoring in the social sciences in a computing course, but 
are a smaller overall portion of the class than computing-related 
majors (CS, DSCI, MACS, and CIS).

Consider some specific _use_ for which a treemap could be 
used, and consider the perceptual and cognitive processing 
that task requires.  Critique the strengths and weaknesses of 
treemap visualization for _that specific use_.  Can you identify a 
way to ameliorate a weakness or enhance a strength?  Do not rely on 
introspection or speculation.  Also, don't accept advice found in 
documentation uncritically. There 
is a rich scientific literature 
on human perception and human computer interaction to draw on. 

## Alternative (accessible) media 

Here's a much bigger project that builds on the prior one, regarding 
appropriate use of treemaps.  This is more on the scale of an MS 
thesis than a class project, but if you are interested in user 
interface and especially in accessible computing, it is not too early 
to start thinking along these lines and building the knowledge you will 
need to build accessible interfaces as your software development 
skills grow.  

Considering the tasks that treemaps 
are used _appropriately_ for, what presentation could serve 
effectively for visually impaired (e.g., blind) users?   Consider 
at least tactile and audio displays.  Don't assume that it will be 
a simple translation of the treemap display to another medium. 

Start with the task, and make use of what you know or can learn 
about perception and cognition to devise displays that are suitable 
to _that task_ with available technology. For tactile displays, 
consider the capabilities and limitations of Braille printers 
(basically low resolution static bitmap displays), pin grid arrays
like [Graphiti](https://www.orbitresearch.com/product/graphiti-plus/)
(even lower resolution, and expensive, but dynamic), and tactile 
printing on [swell touch paper](
https://americanthermoform.com/product/swell-touch-paper/).

[Haptics](https://en.wikipedia.org/wiki/Haptic_technology)
(active touch) are distinct from tactile display, but 
might also be worth considering.  Currently haptics are used 
primarily for simple "simulated button" displays, e.g., simulating a 
button click on a trackpad that does not actually depress, or 
joystick "rumble". Several systems that integrate haptics into 
touchscreens are in development. 

The [International Conference on Audio Display](https://icad.org/)
is a rich source of ideas and experimental evidence regarding audio 
display.  

The [ACM SIGACCESS](https://www.sigaccess.org/)
[Conference on Computers and Accessibility](https://www.sigaccess.org/assets/)
is a source of recent research in accessible interfaces, including 
but not limited to accessibility for visually impaired users.  










